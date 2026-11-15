#!/usr/bin/env python3
"""Render the per-profile AI model from .hermes/config/models.yaml.

LADE's single source of truth for which model a role runs on is
``.hermes/config/models.yaml``. This helper materializes it into each
``profiles/<role>/config.yaml`` and verifies that the two agree.

Subcommands
    list     role -> class -> model, the effective mapping (read-only)
    check    report drift between models.yaml and the rendered config.yaml (read-only)
    render   write the managed regions into every config.yaml (idempotent)
    set      record a role's model in models.yaml, preserving comments

Each ``config.yaml`` carries three marker-delimited regions -- ``lade:model``,
``lade:fallback`` and ``lade:reasoning`` -- and only what lies between a pair of
markers is rewritten. The rest of the file (the toolset allowlist, approvals,
skill scoping) is never touched. When the markers are absent the regions are
inserted next to their natural anchor, so this also upgrades a pre-v2.3.0 file.

Run through any Python that has PyYAML or ruamel.yaml (the Hermes runtime venv has
both). ``set`` needs ruamel.yaml to keep the catalog's comments.

Exit codes: 0 ok, 1 drift/failure, 2 bad usage.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROLES_FALLBACK = (
    "orchestrator", "architect", "software-engineer", "data-engineer",
    "geospatial-engineer", "ai-engineer", "devops-sre", "technical-writer", "reviewer",
)
CATALOG_REL = Path(".hermes") / "config" / "models.yaml"
NOTE = "generated from .hermes/config/models.yaml by setup.sh -- do not edit"


# ── catalog ──────────────────────────────────────────────────────────────────────────────────────

def load_catalog(path: Path) -> dict:
    """Read models.yaml. PyYAML first, then ruamel; either is fine for a read."""
    text = path.read_text(encoding="utf-8")
    try:
        import yaml
        return yaml.safe_load(text) or {}
    except ImportError:
        pass
    from ruamel.yaml import YAML
    return YAML(typ="safe").load(text) or {}


def _first(entries, key):
    """First truthy ``key`` across the precedence-ordered mappings."""
    for entry in entries:
        if isinstance(entry, dict) and entry.get(key) not in (None, "", [], {}):
            return entry[key]
    return None


def resolve(catalog: dict, role: str) -> dict:
    """Effective model settings for *role*: role keys > class preset > defaults."""
    defaults = catalog.get("defaults") or {}
    classes = catalog.get("classes") or {}
    roles = catalog.get("roles") or {}
    role_entry = roles.get(role) or {}
    cls_entry = classes.get(role_entry.get("class")) or {}
    chain = (role_entry, cls_entry)

    def pick(key):
        value = _first(chain, key)
        return value if value is not None else defaults.get(key)

    return {
        "role": role,
        "class": role_entry.get("class", ""),
        "model": pick("model") or "",
        "provider": pick("provider") or "",
        "base_url": pick("base_url") or "",
        "reasoning_effort": _first(chain, "reasoning_effort") or "",
        "fallback": _first(chain, "fallback") or [],
    }


def role_class(catalog: dict, role: str) -> str:
    return (catalog.get("roles") or {}).get(role, {}).get("class", "")


# ── region rendering ─────────────────────────────────────────────────────────────────────────────

def begin_line(tag: str, indent: str = "") -> str:
    return f"{indent}# >>> {tag} ({NOTE}) >>>"


def end_line(tag: str, indent: str = "") -> str:
    return f"{indent}# <<< {tag} <<<"


def model_body(r: dict) -> list[str]:
    return [
        "model:",
        f"  default: {r['model']}",
        f"  provider: {r['provider']}",
        f"  base_url: {r['base_url']}",
    ]


def fallback_body(r: dict) -> list[str]:
    fallback = r.get("fallback") or []
    if not fallback:
        return ["fallback_providers: []"]
    out = ["fallback_providers:"]
    for entry in fallback:
        items = list(entry.items())
        if not items:
            continue
        out.append(f"  - {items[0][0]}: {items[0][1]}")
        out.extend(f"    {k}: {v}" for k, v in items[1:])
    return out


def reasoning_body(r: dict, indent: str = "  ") -> list[str]:
    effort = r.get("reasoning_effort") or ""
    return [f"{indent}reasoning_effort: {effort}"] if effort else []


def _find_line(lines: list[str], token: str) -> int | None:
    return next((i for i, line in enumerate(lines) if token in line), None)


def _span(lines: list[str], tag: str) -> tuple[int, int] | None:
    bi = _find_line(lines, f">>> {tag}")
    ei = _find_line(lines, f"<<< {tag}")
    if bi is not None and ei is not None and ei >= bi:
        return bi, ei
    return None


def _replace_region(lines: list[str], tag: str, body: list[str], indent: str = "") -> list[str]:
    span = _span(lines, tag)
    if span is None:
        return lines  # caller inserts when absent
    bi, ei = span
    block = [begin_line(tag, indent), *body, end_line(tag, indent)]
    return lines[:bi] + block + lines[ei + 1:]


def _insert_plain_model(lines: list[str], r: dict) -> list[str]:
    """Upgrade a pre-v2.3.0 file: wrap its plain top-level ``model:`` block in markers."""
    anchor = next((i for i, line in enumerate(lines) if line.rstrip() == "model:"), None)
    if anchor is None:
        # No model block at all: insert before the first top-level ``agent:``.
        agent = next((i for i, line in enumerate(lines) if line.rstrip() == "agent:"), None)
        anchor = agent if agent is not None else len(lines)
        block = [begin_line("lade:model"), *model_body(r), end_line("lade:model"), ""]
        return lines[:anchor] + block + lines[anchor:]
    end = anchor + 1
    while end < len(lines) and (lines[end] == "" or lines[end][:1] in (" ", "\t")):
        end += 1
    block = [begin_line("lade:model"), *model_body(r), end_line("lade:model")]
    return lines[:anchor] + block + lines[end:]


def _insert_after(lines: list[str], index: int, block: list[str]) -> list[str]:
    return lines[:index + 1] + block + lines[index + 1:]


def render_text(text: str, r: dict) -> str:
    """Return *text* with its three managed regions in sync with *r* (idempotent)."""
    lines = text.split("\n")

    if _span(lines, "lade:model") is None:
        lines = _insert_plain_model(lines, r)
    else:
        lines = _replace_region(lines, "lade:model", model_body(r))

    if _span(lines, "lade:fallback") is None:
        mi = _find_line(lines, "<<< lade:model")
        block = [begin_line("lade:fallback"), *fallback_body(r), end_line("lade:fallback"), ""]
        lines = _insert_after(lines, mi, block) if mi is not None else lines + block
    else:
        lines = _replace_region(lines, "lade:fallback", fallback_body(r))

    if _span(lines, "lade:reasoning") is None:
        ai = next((i for i, line in enumerate(lines) if line.rstrip() == "agent:"), None)
        body = reasoning_body(r)
        block = [begin_line("lade:reasoning", "  "), *body, end_line("lade:reasoning", "  ")]
        lines = _insert_after(lines, ai, block) if ai is not None else lines
    else:
        lines = _replace_region(lines, "lade:reasoning", reasoning_body(r), indent="  ")

    return "\n".join(lines)


# ── subcommands ──────────────────────────────────────────────────────────────────────────────────

def _roles(catalog: dict, root: Path) -> list[str]:
    found = sorted(p.parent.name for p in (root / "profiles").glob("*/config.yaml"))
    return found or list(ROLES_FALLBACK)


def cmd_list(args) -> int:
    catalog = load_catalog(args.root / CATALOG_REL)
    roles = _roles(catalog, args.root)
    width = max(len(r) for r in roles)
    print(f"model per role | source: {CATALOG_REL} | provider: {catalog.get('defaults', {}).get('provider', '')}")
    print()
    for role in roles:
        r = resolve(catalog, role)
        label = r["class"] or "individual"
        extra = f"  effort={r['reasoning_effort']}" if r["reasoning_effort"] else ""
        print(f"  {role:<{width}}  [{label}]  {r['model']}{extra}")
    return 0


def cmd_check(args) -> int:
    catalog = load_catalog(args.root / CATALOG_REL)
    roles = args.roles or _roles(catalog, args.root)
    drifted = 0
    for role in roles:
        path = args.root / "profiles" / role / "config.yaml"
        current = path.read_text(encoding="utf-8")
        expected = render_text(current, resolve(catalog, role))
        if current != expected:
            drifted += 1
            print(f"  DRIFT  profiles/{role}/config.yaml does not match models.yaml")
    if drifted:
        print(f"\nResult: model drift in {drifted} profile(s). Run ./setup.sh to repair.")
        return 1
    print(f"  ok     model: {len(roles)} profile(s) match models.yaml")
    return 0


def cmd_render(args) -> int:
    catalog = load_catalog(args.root / CATALOG_REL)
    roles = args.roles or _roles(catalog, args.root)
    written = 0
    for role in roles:
        path = args.root / "profiles" / role / "config.yaml"
        if not path.is_file():
            print(f"  skip   profiles/{role}/config.yaml missing")
            continue
        current = path.read_text(encoding="utf-8")
        expected = render_text(current, resolve(catalog, role))
        if expected != current:
            path.write_text(expected, encoding="utf-8")
            written += 1
            print(f"  ok     rendered model for {role}")
        else:
            print(f"  ok     up to date: {role}")
    print(f"\nResult: {written} file(s) updated.")
    return 0


def cmd_set(args) -> int:
    path = args.root / CATALOG_REL
    try:
        from ruamel.yaml import YAML
    except ImportError:
        print("error: ruamel.yaml is required to update models.yaml (it preserves comments)", file=sys.stderr)
        return 1
    yaml = YAML()
    yaml.preserve_quotes = True
    with path.open(encoding="utf-8") as handle:
        data = yaml.load(handle) or {}
    roles = data.setdefault("roles", {})
    entry = roles.setdefault(args.role, {})
    entry["model"] = args.model
    if args.provider:
        entry["provider"] = args.provider
    if args.effort:
        entry["reasoning_effort"] = args.effort
    with path.open("w", encoding="utf-8") as handle:
        yaml.dump(data, handle)
    print(f"  ok     roles.{args.role}.model = {args.model}")
    return 0


def main(argv: list[str]) -> int:
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent,
                        help="repository root (default: parent of scripts/)")
    common.add_argument("--roles", nargs="*", help="roles to act on (default: every role in the repo)")
    parser = argparse.ArgumentParser(description="Render per-profile models from .hermes/config/models.yaml")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("list", parents=[common], help="effective model per role (read-only)")
    sub.add_parser("check", parents=[common], help="report drift between models.yaml and config.yaml (read-only)")
    sub.add_parser("render", parents=[common], help="write the managed regions into every config.yaml")
    setp = sub.add_parser("set", parents=[common], help="record a per-role override in models.yaml")
    setp.add_argument("role")
    setp.add_argument("model")
    setp.add_argument("--provider")
    setp.add_argument("--effort")
    args = parser.parse_args(argv)
    handlers = {"list": cmd_list, "check": cmd_check, "render": cmd_render, "set": cmd_set}
    return handlers[args.command](args)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
