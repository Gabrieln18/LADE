# Defect report — `hermes -p <role>` blocks on a blank screen

> **Date:** 2026-11-13 · **Component:** profile provisioning (`setup.sh`, `profiles/<role>/`) + Hermes gateway attach
> **Severity:** high — every LADE role profile is unusable; no work can start
> **Status:** root-caused, reproduced, fix verified on one role, repo-side fix not yet merged
> **Found by:** development session on Hermes Agent v0.23.1 (2026.9.24), Linux, user systemd unit `hermes-gateway.service`

---

## 1. Summary

`hermes -p <role>` prints nothing and never returns. The process is not waiting for
stdin: it blocks inside the gateway attach path before the welcome banner is drawn.

Cause: a LADE profile home **resolves outside the Hermes root**. `setup.sh` symlinks
`~/.hermes/profiles/<role>` at `<repo>/profiles/<role>`, so the profile's canonical
path lives in this repository. The runtime derives the Hermes root from that path,
concludes the repository is a **second Hermes root ("tenant")**, and therefore reads
the live host gateway — the very process that already serves these profiles — as
*another tenant's*. The client refuses to attach and starts its own gateway on the
bogus root, which can never become attachable. Startup blocks forever.

The same mechanism makes the repository grow a complete Hermes home of its own
(`state.db`, `gateway.sock`, `gateway.lock`, `kanban.db`, `config.yaml`, `memories/`,
`logs/`, …) at its root, because that is where the doomed gateway runs.

---

## 2. Symptom

```console
$ hermes -p orchestrator
                      # blank screen, indefinitely; Ctrl+C restores the prompt
```

Interrupting the process produces this stack, which is the fingerprint to look for:

```
File "hermes_cli/gateway_connection.py", line 413, in _send
    self.start()
File "hermes_cli/gateway_connection.py", line 237, in start
    if not self._ready.wait(max(deadline - time.monotonic(), 0)):
```

For comparison, a profile whose home is inside the Hermes root (`doctor-copilot-docs`)
paints the full banner in the same terminal.

Two misleading observations during triage:

* `hermes -p orchestrator gateway status` answers `✓ Gateway is running via the
  default-profile multiplexer` — a *different* code path (`host_attach.decide`) that
  gets the right answer, while the interactive client does not.
* Deleting the stale per-profile `gateway.lock` changes the verdict from
  `starting` to `absent` and still leaves the blank screen.

---

## 3. Minimal reproduction

```bash
# 1. reproduce the layout
ln -s "$PWD/profiles/orchestrator" ~/.hermes/profiles/orchestrator
# 2. observe
hermes -p orchestrator            # blank screen; Ctrl+C for the stack above
# 3. read the three facts that decide it (read-only)
make verify-canonical
```

`make verify-canonical` on a broken layout prints, per role:

```
get_default_hermes_root()   /home/<user>/<repo>        <-- WRONG ROOT
multiplexer_root_for()      /home/<user>/<repo>        <-- CLIENT LOOKS ELSEWHERE
launched_by_other_tenant()  True                       <-- HOST READ AS ANOTHER TENANT
verdict                     START (never attachable)
```

---

## 4. Root cause

Four facts compose into the failure. All are in Hermes, not in LADE; LADE's
provisioning is what triggers them.

**4.1 The launcher points `HERMES_HOME` at the profile directory.**
`hermes_cli/main.py::_apply_profile_override` (line 508) resolves `-p <role>` through
`hermes_cli/profiles.py::resolve_profile_env` (line 2335) and sets
`HERMES_HOME=<root>/profiles/<role>` — the *symlink* path, which is correct here.

**4.2 The runtime canonicalizes it, and the root derivation follows the realpath.**
`hermes_constants.py::get_default_hermes_root` (line 302) strips a trailing
`profiles/<name>` to find the root. Applied to a canonicalized home, it answers
`<repo>`, not `$HERMES_HOME`. `gateway_runtime_multiplex.py::multiplexer_root_for`
(line 18) makes the same assumption more directly: the multiplexing gateway for a
profile home is `home.parent.parent`. For a home in the repository that is the
repository.

**4.3 The host gateway is then judged to belong to another tenant.**
`gateway/host_attach.py::launched_by_other_tenant` (line 118) compares
`get_default_hermes_root(owner_home)` with `get_default_hermes_root(our_home)`. The
owner is `/home/<user>/.hermes`; our derived root is the repository; they differ, so
the live multiplexer — which genuinely serves all nine LADE profiles — is classified
as foreign.

**4.4 `decide()` therefore starts a second gateway that cannot serve.**
`gateway/host_attach.py::decide` (line 363) short-circuits on that same predicate and
returns `START` instead of `ATTACH`. `hermes_cli/gateway_runtime.py` then runs
`ensure_gateway_runtime` (line 414) against the bogus root; discovery
(`discover_gateway_endpoint`, line 318) finds no owner there, and every attempt ends
as `state="starting"`/`reason_code="deadline"` or `inaccessible`/`runtime_exited` —
never `ready`. The client waits in `GatewayConnection.start()` before the banner is
painted. Nothing is ever shown.

**Secondary damage.** While trying, the gateway writes a real Hermes home into the
repository root. Table stakes for the fix: `state.db`, `gateway.sock`, `gateway.lock`,
`kanban.db`, `config.yaml`, `SOUL.md`, `memories/`, `logs/`, `skills/`, `plugins/`,
`platforms/`, `pending_messages/`, `cron/`, `cache/`, `install_id`, `installs/`,
`state/`, `.hermes-update-in-progress.lock`, `.install_id.lock`, `.clean_shutdown`.

**Why the multiplexer rescues only some profiles.** `gateway/run_profile_reconcile.py`
holds each profile's session-authority binding for the process lifetime
(`::_serve_profile_runtime`, line 417). A profile whose home changes under a running
multiplexer is served only after the binding is rebuilt; otherwise it is parked with
`gateway/run_runtime.py` line 51 — *"session authority database does not belong to the
reserved profile"* — because a session DB carries the identity of the home that
created it. In place, `rescan-profiles` re-added exactly the one profile whose home
had been torn down and rebuilt; the other eight stayed parked, and `serve-profile`
recorded them in `served_profiles` while the actual serve failed. **A gateway restart
is required after the layout changes.** Until it happens the multiplexer keeps ticking
the homes it reserved at boot, so `cron/`, `logs/`, `plugins/` and
`plugin-update-checks/` reappear inside `profiles/<role>/` in the repository even after
they are cleaned — visible as `runtime_state_in_repo` in `make verify`.

---

## 5. Evidence

Same machine, same gateway, side by side (`make verify-canonical`):

| | LADE role (broken) | `doctor-copilot-docs` (correct) |
|---|---|---|
| canonical home | `<repo>/profiles/orchestrator` | `~/.hermes/profiles/doctor-copilot-docs` |
| `get_default_hermes_root()` | `<repo>` | `~/.hermes` |
| `multiplexer_root_for()` | `<repo>` | `~/.hermes` |
| `launched_by_other_tenant()` | `True` | `False` |
| `decide()` | `start` (never attachable) | `attach` |
| `ensure_gateway_runtime()` | `starting` / `deadline` | `ready`, attachable |

The multiplexer's own roster proves it *is* serving these profiles — the client simply
cannot reach that conclusion (`make roster`):

```json
{"pid": 2612, "multiplex": true,
 "served_profiles": [{"home": "/home/<user>/.hermes"},
                     {"home": "/home/<user>/<repo>/profiles/orchestrator"}, ...]}
```

Note the roster keys profiles by **home path**, which is why a roster entry and a
client lookup can disagree.

---

## 6. Fix

### 6.1 Runtime layout (the actual fix)

Make every profile home a **real directory that resolves inside `$HERMES_HOME`**,
with the repository's content files symlinked into it:

```
~/.hermes/profiles/orchestrator/      real directory, mode 0700
  config.yaml   -> <repo>/profiles/orchestrator/config.yaml
  profile.yaml  -> <repo>/profiles/orchestrator/profile.yaml
  AGENTS.md     -> <repo>/profiles/orchestrator/AGENTS.md
  SOUL.md       -> <repo>/profiles/orchestrator/SOUL.md
  .env          -> ~/.hermes/.env
  skills        -> <repo>/profiles/orchestrator/skills
  state.db, cron/, logs/, memories/, cache/, sessions/, ...   created HERE by Hermes
```

This keeps content in git exactly once and moves runtime state out of the repository.
It is the overlay-home shape the runtime documents, read the other way round.

Rules that must be respected when building it:

* **Never symlink runtime control files into the home** — no `gateway.lock`,
  `gateway.pid`, `gateway_state.json`, `state.db`. A `gateway.lock` still flocked by
  the host gateway parks the profile (*"home owned by another gateway"*); a legacy
  `state.db` parks it (*"session authority database does not belong to the reserved
  profile"*). Let the gateway create both.
* The home directory must be **mode 0700** (discovery validates private ownership).
* A bind mount of `<repo>/profiles/<role>` onto `~/.hermes/profiles/<role>` achieves
  the same canonical path while keeping every byte in the repository. It needs root,
  so this repository standardises on the real-directory-plus-symlinks shape.

Tooling in this repository:

```bash
bash scripts/repair_profile_homes.sh --check    # report drift, writes nothing
bash scripts/repair_profile_homes.sh --apply    # repair in place (idempotent)
make repair-homes && make gateway-restart && make verify
```

### 6.2 `setup.sh` must stop creating the whole-directory symlink

Section 2 of `setup.sh` currently does `ln -s "$target" "$link"`. A ready patch is
attached to this report at `docs/reports/attachments/setup-multihome.patch`
(generated with `diff -u --label a/setup.sh --label b/setup.sh`; applies cleanly with
`git apply` from the repository root — verified with `git apply --check`).
It creates the real directory, links `AGENTS.md SOUL.md config.yaml profile.yaml
skills/` and `.env`, and reports a whole-directory symlink as drift in `--check`.

### 6.3 Upstream candidates (Hermes)

Any of these would have prevented the whole class:

1. `get_default_hermes_root` should not treat an arbitrary `<X>/profiles/<name>` as a
   Hermes root without corroborating evidence (a `config.yaml`, a `state.db`, a
   `gateway.sock`, or the process's own `HERMES_HOME` ancestry).
2. `multiplexer_root_for` should consider the recorded host gateway
   (`~/.local/state/hermes/gateway-locks/host-gateway.json`) instead of assuming
   `home.parent.parent`.
3. `launched_by_other_tenant` should consult the host record's `served_profiles`
   roster — it already contains the profile — before declaring a foreign tenant.
4. `host_attach.decide` returning `START` for a home the host gateway demonstrably
   serves is the last chance to fail loudly instead of hanging.

---

## 7. Acceptance criteria

1. `hermes -p <role>` paints the welcome banner and accepts a prompt, for all nine
   roles, from a clean shell.
2. `make verify` exits 0: every home is a real directory inside `$HERMES_HOME`, every
   content symlink resolves, every profile is served (`state="ready"`), and no runtime
   state sits in the repository.
3. `make verify-canonical` reports `ATTACH` for all nine roles.
4. `bash scripts/repair_profile_homes.sh --check` exits 0.
5. `./setup.sh --check` (with the fix in 6.2) exits 0.
6. `git status` in the repository stays clean after the six checks above — no
   `state.db`, no `gateway.sock`, no `config.yaml` at the repository root.

## 8. Regression harness

`make verify` is the guard: it fails on exactly the four facts of §4
(`home_is_symlink`, `home_outside_root`, `multiplexer_root`, `served`). Run it after
any change to `setup.sh`, to `profiles/<role>/`, or after adding a role.

## 9. Code references

| Symbol | Location |
|---|---|
| `_apply_profile_override` | `hermes_cli/main.py:508` |
| `resolve_profile_env` | `hermes_cli/profiles.py:2335` |
| `get_default_hermes_root` | `hermes_constants.py:302` |
| `named_profile_home` | `hermes_constants.py:345` |
| `multiplexer_root_for` | `hermes_cli/gateway_runtime_multiplex.py:18` |
| `ensure_gateway_runtime` | `hermes_cli/gateway_runtime.py:414` |
| `discover_gateway_endpoint` | `hermes_cli/gateway_runtime.py:318` |
| `_served_by_multiplexer` | `hermes_cli/gateway_runtime.py:225` |
| `missing_owner_state` | `hermes_cli/gateway_runtime_discovery.py:233` |
| `launched_by_other_tenant` | `gateway/host_attach.py:118` |
| `decide` | `gateway/host_attach.py:363` |
| `_serve_profile_runtime` | `gateway/run_profile_reconcile.py:417` |
| session-authority refusal | `gateway/run_runtime.py:51` |
| `GatewayConnection.start` | `hermes_cli/gateway_connection.py:237` |
| `_is_gateway_runtime_lock_active_strict` | `gateway/status.py:1042` |
