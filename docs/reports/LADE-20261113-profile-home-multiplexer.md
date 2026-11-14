# Defect report — `hermes -p <role>` blocks on a blank screen

> **Date:** 2026-11-13 · **Revised:** 2026-11-14 (runtime layout repaired; see §7)
> **Component:** profile provisioning (`setup.sh`, `profiles/<role>/`) + Hermes gateway attach
> **Severity:** high — every LADE role profile was unusable; no work could start
> **Status:** fixed. Root cause confirmed; the `setup.sh` fix is committed (`b0f2f8d`);
> the runtime layout was repaired on 2026-11-14 (`make repair-homes`). One
> `hermes gateway restart` — a human action — remains before the profiles attach.
> **Found by:** development session on Hermes Agent v0.23.1 (2026.9.24), Linux, user systemd unit `hermes-gateway.service`
> **Re-verified on 2026-11-14 against:** Hermes Agent v0.23.1+842.gdcfbaf0 (2026.9.24), same machine

---

## 1. Summary

`hermes -p <role>` prints nothing and never returns. The process is not waiting for
stdin: it blocks inside the gateway attach path before the welcome banner is drawn.

Cause: a LADE profile home **resolves outside the Hermes root**. `setup.sh` used to
symlink `~/.hermes/profiles/<role>` at `<repo>/profiles/<role>`, so the profile's
canonical path lived in this repository. The runtime derives the Hermes root from that
path, concludes the repository is a **second Hermes root ("tenant")**, and therefore
reads the live host gateway — the very process that already serves these profiles — as
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

Reproduced as a bounded run on 2026-11-14, which is also the cheapest way to test it
from a script or a session that must not hang:

```console
$ timeout 60 hermes -p orchestrator -z "responda apenas OK"
$ echo $?
124                   # nothing printed; killed by the timeout
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
multiplexer_root_for()      None                       <-- CLIENT LOOKS ELSEWHERE
launched_by_other_tenant()  True                       <-- HOST READ AS ANOTHER TENANT
verdict                     START (never attachable)
```

On 2026-11-13 the same command printed `/home/<user>/<repo>` for
`multiplexer_root_for()`. The value differs because the bogus root has no recorded
gateway at all on this build: the third line is the load-bearing one, and it is stable.

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
(`::_serve_profile_runtime`, line 417, `async def`). A profile whose home changes under
a running multiplexer is served only after the binding is rebuilt; otherwise it is
parked with `gateway/run_runtime.py` line 51 — *"session authority database does not
belong to the reserved profile"* — because a session DB carries the identity of the
home that created it. In place, `rescan-profiles` re-added exactly the one profile
whose home had been torn down and rebuilt; the other eight stayed parked, and
`serve-profile` recorded them in `served_profiles` while the actual serve failed.
**A gateway restart is required after the layout changes.** Until it happens the
multiplexer keeps ticking the homes it reserved at boot, so `cron/`, `logs/`,
`plugins/` and `plugin-update-checks/` reappear inside `profiles/<role>/` in the
repository even after they are cleaned — visible as `runtime_state_in_repo` in
`make verify`. This was observed again on 2026-11-14: after `make prune-runtime`
removed every stray, the still-running gateway recreated `state.db` in all nine
repository directories within seconds (§5.3).

---

## 5. Evidence

### 5.1 The failure, side by side (2026-11-13)

Same machine, same gateway (`make verify-canonical`):

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

### 5.2 The same roster, before the restart (2026-11-14)

```
Host gateway pid 2296 (multiplex: None)
served_profiles:
  /home/<user>/.hermes
  /home/<user>/<repo>/profiles/ai-engineer
  ... (the nine repository paths)
parked_profiles: none
```

The roster is keyed by the paths reserved at boot, so after the repair it still names
the nine repository paths. `hermes gateway list` shows all nine profiles plus `default`
on pid 2296 — a green list that says nothing about whether the client can attach.

### 5.3 After the repair, before the gateway restart (2026-11-14)

| Check | Result |
|---|---|
| `make verify-canonical` | `ATTACH` for all nine roles; root, multiplexer root and tenant verdict all correct |
| `make repair-homes-check` | exit 2 via `make` (the script itself exits 1) — home layout clean; the only drift is `repository profiles/<role>/state.db exists` ×9, recreated by the running gateway |
| `./setup.sh --check` | exit 0 — `Result: structure consistent.` |
| `make links` | exit 0 — `every symlink resolves` |
| `make lint` | exit 0 — `lint clean` (shellcheck not installed) |
| `make verify` | exit 2 via `make` — 9 × `[ FAIL ] served: absent: this profile cannot attach` and 9 × `[ WARN ] runtime_state_in_repo state.db` |
| `git status` | clean (the repository root stays clean: no `state.db`, no `gateway.sock`, no `config.yaml`) |

The nine `served` failures and the nine warnings are the same single fact — the host
gateway still holds its boot bindings — and both are cleared by the restart. They are
the expected pre-restart state, not a new defect.

Per-role canonical output after the repair:

```
get_default_hermes_root()   /home/<user>/.hermes
multiplexer_root_for()      /home/<user>/.hermes
launched_by_other_tenant()  False
verdict                     ATTACH
```

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

Applied on 2026-11-14 in this order: `make backup` (archive at
`.lade-backups/profiles-20261114T094941.tar.gz`), `make repair-homes` (the nine
whole-directory symlinks were moved to `~/.hermes/.lade-home-backup/`), then
`make prune-runtime` to clear the runtime state the old layout had left in the
repository. The per-profile `memories/` and `sessions/` were empty at that point, so
nothing of value was discarded; the archive is the fallback.

### 6.2 `setup.sh` — done

Absorbed into `setup.sh` (section 2) in commit `b0f2f8d` *"feat: updated setup.sh"*.
The script now creates the real directory, links `AGENTS.md SOUL.md config.yaml
profile.yaml skills/` and `.env`, and reports a whole-directory symlink as drift in
`--check`.

The patch that was attached to this report is kept as development history at
`docs/reports/attachments/archive/setup-multihome.patch`. **Do not apply it**: it no
longer applies (`git apply --check` fails at `setup.sh:178`) because the change is
already in the file. It is archived for the record only.

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

| # | Criterion | State on 2026-11-14 |
|---|---|---|
| 1 | `hermes -p <role>` paints the welcome banner and accepts a prompt, for all nine roles, from a clean shell | pending the gateway restart (§5.3) |
| 2 | `make verify` exits 0: every home a real directory inside `$HERMES_HOME`, every content symlink resolves, every profile served, no runtime state in the repository | layout and symlinks pass; `served` ×9 and `runtime_state_in_repo` ×9 pending the restart |
| 3 | `make verify-canonical` reports `ATTACH` for all nine roles | **met** — 9/9 `ATTACH` |
| 4 | `bash scripts/repair_profile_homes.sh --check` exits 0 | pending the restart (only the gateway-recreated `state.db` remains) |
| 5 | `./setup.sh --check` exits 0 | **met** — exit 0, `structure consistent` |
| 6 | `git status` in the repository stays clean after the six checks | **met** — clean; nothing at the repository root |

Criterion 1 is the one that defines "done": the other five are its preconditions.
Until it is re-run after the restart, this report claims a repaired layout and a
correct attach decision, not a working `hermes -p <role>`.

## 8. Regression harness

`make verify` is the guard: it fails on exactly the four facts of §4
(`home_is_symlink`, `home_outside_root`, `multiplexer_root`, `served`). Run it after
any change to `setup.sh`, to `profiles/<role>/`, or after adding a role.

## 9. Code references

Re-anchored on 2026-11-14 against Hermes Agent v0.23.1+842.gdcfbaf0 — every line below
was re-checked in the installed tree, and all of them still hold.

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
| `_serve_profile_runtime` | `gateway/run_profile_reconcile.py:417` (`async def`) |
| session-authority refusal | `gateway/run_runtime.py:51` |
| `GatewayConnection.start` | `hermes_cli/gateway_connection.py:212` (the blocking `self._ready.wait(...)` is line 237) |
| `_is_gateway_runtime_lock_active_strict` | `gateway/status.py:1042` |

## 10. Revision history

| Date | Change |
|---|---|
| 2026-11-13 | Report written: root cause, reproduction, evidence, fix, acceptance criteria. `setup.sh` fix generated as a patch. |
| 2026-11-14 | `setup.sh` fix confirmed committed (`b0f2f8d`); patch archived (§6.2). Runtime layout repaired with `make repair-homes` and `make prune-runtime` (§6.1). §2 bounded reproduction added; §5 re-measured, §7 turned into a results table, §9 re-anchored. Remaining: one gateway restart, then re-run §7. |
