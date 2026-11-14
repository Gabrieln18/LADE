#!/usr/bin/env bash
# repair_profile_homes.sh — make every LADE profile home resolve INSIDE $HERMES_HOME.
#
# Why this exists
#   `hermes -p <role>` sets HERMES_HOME=$HERMES_HOME/profiles/<role>, and the runtime
#   derives the Hermes ROOT from that path by stripping `profiles/<name>`. If the
#   profile directory is itself a symlink into this repository, the path resolves to
#   <repo>/profiles/<role>, so:
#       * get_default_hermes_root() answers the REPOSITORY (a second "tenant" root);
#       * gateway_runtime_multiplex.multiplexer_root_for() sends the client looking for
#         the multiplexing gateway at <repo> instead of $HERMES_HOME;
#       * gateway.host_attach.launched_by_other_tenant() then reads the live host
#         gateway as another tenant's, and decide() answers START instead of ATTACH.
#   The client starts a gateway on the bogus root that can never become attachable, so
#   `hermes -p <role>` blocks before painting the banner: a blank screen.
#
# What this does (idempotent)
#   Replaces <root>/profiles/<role> with a REAL directory (mode 700) whose entries are
#   symlinks back into this repository — the documented overlay-home shape, read the
#   other way round. Content stays in git, exactly once; runtime state (state.db,
#   sessions, memories, logs, locks) is then created by Hermes inside the home and
#   stops landing in the repository.
#
#   Runtime control files are NEVER created here: a stale gateway.lock still flocked
#   by the host gateway parks the profile ("home owned by another gateway"), and a
#   legacy state.db parks it ("session authority database does not belong to the
#   reserved profile") because a DB carries the identity of the home that made it.
#   Let the gateway create both.
#
# Usage
#   scripts/repair_profile_homes.sh --check     # report drift, write nothing, exit 1 on drift
#   scripts/repair_profile_homes.sh --apply     # repair in place
#   scripts/repair_profile_homes.sh --apply --role orchestrator
#
# After --apply the running host gateway must re-bind (it holds each profile's session
# authority from its own boot): `hermes gateway restart` from a shell OUTSIDE the
# gateway, or `make gateway-restart`. `make verify` tells you when it took effect.

set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
HERMES_HOME="${HERMES_HOME:-$HOME/.hermes}"
PROFILES_DIR="$HERMES_HOME/profiles"
BACKUP_DIR="$HERMES_HOME/.lade-home-backup"
CONTENT_ENTRIES=(AGENTS.md SOUL.md config.yaml profile.yaml)

mode=""
only_role=""
for arg in "$@"; do
  case "$arg" in
    --check) mode=check ;;
    --apply) mode=apply ;;
    --role) shift; only_role="${1:-}" ;;
    --role=*) only_role="${arg#*=}" ;;
    -h|--help) sed -n '2,40p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) printf 'unknown option: %s\n' "$arg" >&2; exit 2 ;;
  esac
done
if [ -z "$mode" ]; then
  printf 'usage: %s --check | --apply [--role <role>]\n' "$0" >&2
  exit 2
fi

fail=0
ok()   { printf '  ok     %s\n' "$*"; }
drift(){ printf '  DRIFT  %s\n' "$*"; fail=1; }
note() { printf '  note   %s\n' "$*"; }

[ -d "$PROFILES_DIR" ] || { printf 'error: %s does not exist (run ./setup.sh first)\n' "$PROFILES_DIR" >&2; exit 2; }

link_entry() {  # link_entry <role> <home> <repo-dir> <entry>
  local role="$1" home="$2" src="$3" entry="$4"
  local dst="$home/$entry"
  [ -e "$src/$entry" ] || return 0
  if [ -L "$dst" ]; then
    # Compare RESOLVED targets: a link straight at the repository file and one that
    # reaches it through the repo-side .env chain are both correct.
    [ "$(readlink -f "$dst")" = "$(readlink -f "$src/$entry")" ] && ok "$role/$entry -> repository" \
      || drift "$role/$entry resolves to '$(readlink -f "$dst")'"
  elif [ -e "$dst" ]; then
    drift "$role/$entry is a real entry in the home; it must be a symlink into the repository"
  elif [ "$mode" = check ]; then
    drift "$role/$entry not linked (run --apply)"
  else
    ln -s "$src/$entry" "$dst" && ok "$role/$entry -> $src/$entry"
  fi
}

printf 'LADE profile homes | repository: %s\n' "$ROOT"
printf '                   | hermes home: %s\n' "$HERMES_HOME"
[ "$mode" = check ] && printf '                   | mode: --check (writes nothing)\n'

for config in "$ROOT"/profiles/*/config.yaml; do
  [ -f "$config" ] || continue
  role="$(basename "$(dirname "$config")")"
  [ -n "$only_role" ] && [ "$role" != "$only_role" ] && continue

  src="$ROOT/profiles/$role"
  home="$PROFILES_DIR/$role"
  printf '\n%s\n' "$role"

  if [ -L "$home" ]; then
    if [ "$mode" = check ]; then
      drift "$home is a whole-directory symlink -> $(readlink "$home") (run --apply)"
      continue
    fi
    mkdir -p "$BACKUP_DIR"
    mv "$home" "$BACKUP_DIR/$role.symlink-$(date +%Y%m%dT%H%M%S)"
    ok "moved the whole-directory symlink to ${BACKUP_DIR/#$HOME/~}"
    mkdir -p "$home" && chmod 700 "$home"
    ok "created a real home directory"
  elif [ -d "$home" ]; then
    chmod 700 "$home" 2>/dev/null || true
    ok "home is a real directory"
  elif [ "$mode" = check ]; then
    drift "$home is missing (run --apply)"
    continue
  else
    mkdir -p "$home" && chmod 700 "$home"
    ok "created home directory"
  fi

  for entry in "${CONTENT_ENTRIES[@]}"; do
    link_entry "$role" "$home" "$src" "$entry"
  done

  # The skill tree generated by setup.sh, mirrored as one symlink.
  if [ -d "$src/skills" ]; then
    if [ -L "$home/skills" ]; then
      [ "$(readlink -f "$home/skills")" = "$(readlink -f "$src/skills")" ] && ok "$role/skills -> repository" \
        || drift "$role/skills resolves to '$(readlink -f "$home/skills")'"
    elif [ -e "$home/skills" ]; then
      drift "$role/skills is a real directory in the home; it must be a symlink into the repository"
    elif [ "$mode" = check ]; then
      drift "$role/skills not linked (run --apply)"
    else
      ln -s "$src/skills" "$home/skills" && ok "$role/skills -> $src/skills"
    fi
  else
    note "$role/skills is missing in the repository (run ./setup.sh to generate it)"
  fi

  # Credentials are never committed: the home points straight at the shared .env.
  if [ -f "$HERMES_HOME/.env" ]; then
    if [ -L "$home/.env" ]; then
      [ "$(readlink -f "$home/.env")" = "$(readlink -f "$HERMES_HOME/.env")" ] && ok "$role/.env -> hermes home" \
        || drift "$role/.env resolves to '$(readlink -f "$home/.env")'"
    elif [ -e "$home/.env" ]; then
      drift "$role/.env is a real file in the home; it must be a symlink"
    elif [ "$mode" = check ]; then
      drift "$role/.env not linked (run --apply)"
    else
      ln -s "$HERMES_HOME/.env" "$home/.env" && ok "$role/.env -> $HERMES_HOME/.env"
    fi
  else
    note "$role: no $HERMES_HOME/.env to link; provide credentials per profile"
  fi

  # Runtime state is the home's, never the repository's.
  for stray in state.db state.db-shm state.db-wal gateway.lock gateway.pid gateway_state.json; do
    [ -e "$src/$stray" ] && drift "repository profiles/$role/$stray exists — runtime state belongs in the home (make prune-runtime)"
  done
done

printf '\n'
if [ "$fail" -eq 0 ]; then
  printf 'RESULT: every profile home resolves inside %s\n' "$HERMES_HOME"
  exit 0
fi
if [ "$mode" = check ]; then
  printf 'RESULT: drift detected — run --apply, then `hermes gateway restart` and `make verify`\n' >&2
else
  printf 'RESULT: drift remains — re-run --check for details\n' >&2
fi
exit 1