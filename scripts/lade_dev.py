#!/usr/bin/env python3
"""LADE development helper: canonical-path verification and gateway control.

Read-only by default. Every check here exists because of one defect that made
`hermes -p <role>` paint a blank screen: a profile home that resolves OUTSIDE
$HERMES_HOME (a whole-directory symlink into this repository). The runtime finds
the multiplexing gateway at `home.parent.parent`, so such a home points the client
at the repository instead of the Hermes root, and startup blocks before the banner.

Run it through the Hermes venv, which is where the runtime dependencies live:

    PY=$(make -s print-venv-python)      # or: ~/.hermes/hermes-agent/venv/bin/python3
    $PY scripts/lade_dev.py verify

Subcommands
    verify      per-role health: home layout, content links, served verdict (read-only)
    canonical   the three facts that decide attach vs. "another tenant" (read-only)
    roster      who serves what, and every parked profile with its reason (read-only)
    rescan      ask the host gateway to reconcile profiles/ (side effect: may serve)
    serve NAME  explicitly serve one profile on the host gateway (side effect)

Exit codes: 0 all good, 1 at least one FAIL, 2 bad usage.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

ROLES_FALLBACK = (
    "orchestrator", "architect", "software-engineer", "data-engineer",
    "geospatial-engineer", "ai-engineer", "devops-sre", "technical-writer", "reviewer",
)

# Content that lives in the repository and is mirrored into the profile home.
CONTENT_ENTRIES = ("config.yaml", "profile.yaml", "AGENTS.md", "SOUL.md")
# The whole provisioned repository layout. Anything else under profiles/<role>/ is
# runtime state that belongs in the profile home instead (setup.sh owns this list).
ALLOWED_IN_REPO = frozenset({*CONTENT_ENTRIES, ".env", "skills"})
# Runtime control files worth naming explicitly when they show up in the repository.
RUNTIME_NAMES = frozenset({
    "state.db", "state.db-shm", "state.db-wal",
    "gateway.lock", "gateway.pid", "gateway.sock", "gateway.sock.path",
    "gateway_state.json", "gateway-starts.log", "gateway.parked",
})

FAIL, WARN, OK, SKIP = "FAIL", "WARN", "ok", "skip"


class Report:
    """A flat list of findings with a stable, greppable shape."""

    def __init__(self, verbose: bool = False) -> None:
        self.rows: list[tuple[str, str, str, str]] = []  # role, level, code, detail
        self.verbose = verbose

    def add(self, role: str, level: str, code: str, detail: str = "") -> None:
        self.rows.append((role, level, code, detail))

    def failures(self) -> list[tuple[str, str, str, str]]:
        return [r for r in self.rows if r[1] in (FAIL, WARN)]

    def render(self) -> None:
        width = max((len(r[2]) for r in self.rows), default=0)
        current = None
        for role, level, code, detail in self.rows:
            if role != current:
                print(f"\n{role}")
                current = role
            if level == OK and not self.verbose:
                continue
            mark = {"ok": "  ok  ", "skip": " skip ", "WARN": " WARN ", "FAIL": " FAIL "}[level]
            print(f"  [{mark}] {code:<{width}}  {detail}")


def hermes_home() -> Path:
    env = os.environ.get("HERMES_HOME", "").strip()
    return Path(env).expanduser() if env else Path.home() / ".hermes"


def hermes_root() -> Path:
    """The Hermes DATA root (the directory that holds profiles/ and gateway.sock)."""
    home = hermes_home().resolve()
    return home.parent.parent if home.parent.name == "profiles" else home


def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def bootstrap_hermes() -> None:
    """Make the installed Hermes importable (what every diagnostic here needs)."""
    for candidate in (hermes_home() / "hermes-agent", hermes_root() / "hermes-agent"):
        if (candidate / "hermes_constants.py").is_file():
            sys.path.insert(0, str(candidate))
            return
    raise SystemExit(
        "error: Hermes is not importable. Set HERMES_HOME to the Hermes root, or run with\n"
        "       ~/.hermes/hermes-agent/venv/bin/python3 (the runtime venv, not the toolchain python)."
    )


def discover_roles() -> list[str]:
    """Roles from this repository (the source of truth), falling back to the known list."""
    found = sorted(p.parent.name for p in (repo_root() / "profiles").glob("*/config.yaml"))
    return found or list(ROLES_FALLBACK)


# ── checks ────────────────────────────────────────────────────────────────────────────────────────

def check_home_layout(role: str, report: Report) -> Path | None:
    """Is the profile home a REAL directory that resolves inside the Hermes root?"""
    from hermes_constants import get_default_hermes_root
    from hermes_cli.gateway_runtime_multiplex import multiplexer_root_for

    home = hermes_home() / "profiles" / role
    if not home.exists():
        report.add(role, FAIL, "home_missing", f"{home} does not exist (run: make setup)")
        return None
    if home.is_symlink():
        report.add(role, FAIL, "home_is_symlink",
                   f"{home} -> {os.readlink(home)} (must be a real directory; run: make repair-homes)")
        return None

    resolved = home.resolve()
    if resolved != home:
        report.add(role, WARN, "home_not_canonical", f"{home} resolves to {resolved}")
    report.add(role, OK, "home", str(home))

    root = get_default_hermes_root(home=resolved)
    if root != hermes_root():
        report.add(role, FAIL, "home_outside_root",
                   f"derived Hermes root is {root}, expected {hermes_root()}")
    else:
        report.add(role, OK, "root", str(root))

    mux = multiplexer_root_for(resolved)
    if mux is None or mux != hermes_root():
        report.add(role, FAIL, "multiplexer_root",
                   f"client looks for the gateway at {mux}, the host gateway lives at {hermes_root()}")
    else:
        report.add(role, OK, "multiplexer_root", str(mux))
    return resolved


def check_content_links(role: str, home: Path, report: Report) -> None:
    """Do the content symlinks point into THIS repository's profiles/<role>?"""
    source = repo_root() / "profiles" / role
    for entry in CONTENT_ENTRIES:
        src, dst = source / entry, home / entry
        if not src.exists():
            report.add(role, FAIL, f"source_missing:{entry}", f"{src} does not exist")
            continue
        if dst.is_symlink():
            if dst.resolve() != src.resolve():
                report.add(role, FAIL, f"link_wrong:{entry}", f"{dst} -> {os.readlink(dst)}")
            else:
                report.add(role, OK, f"link:{entry}", "-> repository")
        elif dst.exists():
            report.add(role, WARN, f"link_shadowed:{entry}",
                       f"{dst} is a real file, not a symlink into the repository")
        else:
            report.add(role, FAIL, f"link_missing:{entry}", f"{dst} missing (run: make repair-homes)")

    dst, src = home / ".env", hermes_root() / ".env"
    if not src.exists():
        report.add(role, WARN, "env_missing", f"{src} does not exist; this role has no credentials")
    elif not dst.exists():
        report.add(role, FAIL, "link_missing:.env", f"{dst} missing (run: make repair-homes)")
    elif dst.resolve() != src.resolve():
        report.add(role, WARN, "link_wrong:.env", f"{dst} -> {os.readlink(dst) if dst.is_symlink() else 'real file'}")
    else:
        report.add(role, OK, "link:.env", "-> " + str(src))


def check_repo_runtime_pollution(role: str, report: Report) -> None:
    """Runtime state must live in the HOME; anything else here means the old layout is back.

    A whole-directory symlink makes the runtime treat this repository as a Hermes root,
    so Hermes writes state.db, gateway.sock, cron/, logs/, plugins/, ... beside the
    source files. Naming the control files first, then everything unexpected.
    """
    source = repo_root() / "profiles" / role
    if not source.is_dir():
        return
    strays = sorted(p.name for p in source.iterdir() if p.name not in ALLOWED_IN_REPO)
    if strays:
        control = [name for name in strays if name in RUNTIME_NAMES]
        detail = ", ".join(strays)
        if control:
            detail = f"{', '.join(control)} (and {len(strays) - len(control)} more)"
        report.add(role, WARN, "runtime_state_in_repo",
                   f"{detail} in the repository (run: make prune-runtime)")
    else:
        report.add(role, OK, "no_runtime_state", "repository holds the provisioned layout only")


def check_served(role: str, home: Path, report: Report, timeout: float) -> None:
    """Is the live host gateway serving this profile, per read-only discovery?"""
    from hermes_cli.gateway_runtime import discover_gateway_endpoint
    from gateway.host_attach import host_gateway

    try:
        gateway = host_gateway()
    except Exception as exc:  # health: allow BLE001 -- a broken probe must not hide the layout result
        report.add(role, WARN, "gateway_probe_failed", f"{type(exc).__name__}: {exc}")
        return
    if gateway is None:
        report.add(role, SKIP, "served", "no host gateway is running; start it to check attach")
        return

    previous = os.environ.get("HERMES_HOME")
    os.environ["HERMES_HOME"] = str(home)
    try:
        verdict = discover_gateway_endpoint(home, timeout=timeout)
    finally:
        if previous is None:
            os.environ.pop("HERMES_HOME", None)
        else:
            os.environ["HERMES_HOME"] = previous

    detail = verdict.state + (f" ({verdict.reason_code})" if verdict.reason_code else "")
    if verdict.state == "ready":
        report.add(role, OK, "served", detail)
        return
    if verdict.reason_code == "profile_parked":
        report.add(role, FAIL, "served", f"{detail}: {(verdict.detail or '')[:120]}")
    else:
        report.add(role, FAIL, "served", f"{detail}: this profile cannot attach (see: make roster)")


# ── subcommands ───────────────────────────────────────────────────────────────────────────────────

def cmd_verify(args: argparse.Namespace) -> int:
    bootstrap_hermes()
    roles = args.roles or discover_roles()
    report = Report(verbose=args.verbose)
    print(f"LADE verify | repository: {repo_root()}")
    print(f"            | hermes root: {hermes_root()}")
    for role in roles:
        home = check_home_layout(role, report)
        if home is None:
            continue
        check_content_links(role, home, report)
        check_repo_runtime_pollution(role, report)
        check_served(role, home, report, args.timeout)
    report.render()
    bad = report.failures()
    print()
    if bad:
        print(f"RESULT: {len(bad)} finding(s) — {sum(1 for r in bad if r[1] == FAIL)} failure(s), "
              f"{sum(1 for r in bad if r[1] == WARN)} warning(s)")
        return 1
    print(f"RESULT: {len(roles)} profile(s) consistent.")
    return 0


def cmd_canonical(args: argparse.Namespace) -> int:
    """The three facts that decide attach vs. 'another tenant's gateway'."""
    bootstrap_hermes()
    from hermes_constants import get_default_hermes_root
    from hermes_cli.gateway_runtime_multiplex import multiplexer_root_for
    from gateway.host_attach import launched_by_other_tenant

    root = hermes_root()
    roles = args.roles or discover_roles()
    print(f"hermes root: {root}")
    bad = 0
    for role in roles:
        home = (hermes_home() / "profiles" / role)
        resolved = home.resolve()
        derived = get_default_hermes_root(home=resolved)
        mux = multiplexer_root_for(resolved)
        other = launched_by_other_tenant(root, resolved)
        ok = derived == root and mux == root and not other
        bad += 0 if ok else 1
        print(f"\n{role}")
        print(f"  home                        {home}")
        print(f"  realpath                    {resolved}")
        print(f"  get_default_hermes_root()   {derived}" + ("" if derived == root else "   <-- WRONG ROOT"))
        print(f"  multiplexer_root_for()      {mux}" + ("" if mux == root else "   <-- CLIENT LOOKS ELSEWHERE"))
        print(f"  launched_by_other_tenant()  {other}" + ("" if not other else "   <-- HOST READ AS ANOTHER TENANT"))
        print(f"  verdict                     {'ATTACH' if ok else 'START (never attachable)'}")
    return 1 if bad else 0


def cmd_roster(args: argparse.Namespace) -> int:
    bootstrap_hermes()
    from gateway.control_socket import query_gateway_control

    root = hermes_root()
    identity = query_gateway_control(root, "identify", timeout=args.timeout)
    if not identity:
        print(f"No host gateway answers at {root} (socket: {root / 'gateway.sock'}).")
        return 0
    print(f"Host gateway pid {identity.get('pid')} (multiplex: {identity.get('multiplex')})")
    print("served_profiles:")
    for entry in identity.get("served_profiles") or []:
        print(f"  {entry.get('home') if isinstance(entry, dict) else entry}")
    state_file = root / "gateway_state.json"
    try:
        parked = (json.loads(state_file.read_text(encoding="utf-8")) or {}).get("parked_profiles") or {}
    except (OSError, ValueError):
        parked = {}
    print(f"parked_profiles: {len(parked)}" if parked else "parked_profiles: none")
    for name, reason in sorted(parked.items()):
        print(f"  {name}: {reason}")
    return 0


def cmd_rescan(args: argparse.Namespace) -> int:
    bootstrap_hermes()
    from gateway.control_socket import rescan_gateway_profiles

    answer = rescan_gateway_profiles(hermes_root(), timeout=args.timeout)
    if not answer:
        print("No answer from the host gateway.")
        return 1
    print(json.dumps(answer, indent=2, default=str))
    return 0


def cmd_serve(args: argparse.Namespace) -> int:
    bootstrap_hermes()
    from gateway.control_socket import query_gateway_control

    answer = query_gateway_control(hermes_root(), "serve-profile",
                                   params={"name": args.name}, timeout=args.timeout)
    print(json.dumps(answer or {"error": "no answer"}, indent=2, default=str))
    return 0 if answer and not answer.get("error") else 1


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="LADE development helper")
    parser.add_argument("--roles", nargs="*", help="roles to act on (default: every role in the repo)")
    parser.add_argument("-v", "--verbose", action="store_true", help="also print passing checks")
    parser.add_argument("--timeout", type=float, default=5.0, help="per-gateway-call timeout (s)")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("verify", help="per-role health and served verdict (read-only)")
    sub.add_parser("canonical", help="the three facts behind attach vs. other-tenant (read-only)")
    sub.add_parser("roster", help="served and parked profiles (read-only)")
    sub.add_parser("rescan", help="ask the host gateway to reconcile profiles/")
    serve = sub.add_parser("serve", help="explicitly serve one profile on the host gateway")
    serve.add_argument("name")
    args = parser.parse_args(argv)

    handlers = {"verify": cmd_verify, "canonical": cmd_canonical, "roster": cmd_roster,
                "rescan": cmd_rescan, "serve": cmd_serve}
    return handlers[args.command](args)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))