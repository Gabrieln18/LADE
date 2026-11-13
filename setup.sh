#!/usr/bin/env bash
# setup.sh — provision LADE roles as Hermes profiles.
#
# Idempotent. Creates nothing outside this repository except symlinks in
# ~/.hermes/profiles/ and the skills trust entry. Never installs packages,
# never writes credentials, never configures an MCP server.
#
# Usage:
#   ./setup.sh            provision (safe to re-run)
#   ./setup.sh --check    report drift and exit non-zero; writes nothing
#   ./setup.sh --no-trust skip `hermes skills trust`
#
# Source of truth: .hermes/config/profiles.md §2 (roles, toolsets) and
# .hermes/agents/<role>/AGENTS.md (declared skills). See README.md.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HERMES_HOME="${HERMES_HOME:-$HOME/.hermes}"
PROFILES_DIR="$HERMES_HOME/profiles"

CHECK=0
TRUST=1
for arg in "$@"; do
  case "$arg" in
    --check)    CHECK=1 ;;
    --no-trust) TRUST=0 ;;
    -h|--help)  sed -n '2,16p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) echo "unknown option: $arg" >&2; exit 2 ;;
  esac
done

ROLES=(
  orchestrator
  architect
  software-engineer
  data-engineer
  geospatial-engineer
  ai-engineer
  devops-sre
  technical-writer
  reviewer
)

fail=0
note() { printf '  %s\n' "$*"; }
warn() { printf '  DRIFT  %s\n' "$*"; fail=1; }
ok()   { printf '  ok     %s\n' "$*"; }

# Skills declared in a role manifest's `skills:` block, one per line.
declared_skills() {
  python3 - "$1" <<'PY'
import re, sys
path = sys.argv[1]
text = open(path, encoding="utf-8").read()
# Take the first fenced yaml block, else the whole file.
m = re.search(r"```yaml\n(.*?)```", text, re.S)
body = m.group(1) if m else text
out, inside = [], False
for raw in body.splitlines():
    line = raw.rstrip()
    if not line or line.lstrip().startswith("#"):
        continue
    if re.match(r"^skills:\s*(#.*)?$", line):
        inside = True
        continue
    if inside:
        item = re.match(r"^\s+-\s+(.+?)\s*$", line)
        if item:
            value = item.group(1).split("#")[0].strip().strip('"').strip("'")
            if value:
                out.append(value)
            continue
        # any non-list line ends the block
        if not line.startswith((" ", "\t")):
            break
        if re.match(r"^\s+[A-Za-z_][\w.-]*:", line):
            break
print("\n".join(out))
PY
}

echo "LADE setup — $ROOT"
[ "$CHECK" -eq 1 ] && echo "mode: --check (no writes)"

# 1. Role directories and required files
echo
echo "1. Role directories"
for role in "${ROLES[@]}"; do
  dir="$ROOT/profiles/$role"
  manifest="$ROOT/.hermes/agents/$role/AGENTS.md"
  soul="$ROOT/.hermes/agents/$role/SOUL.md"

  [ -f "$manifest" ] || { warn "missing manifest .hermes/agents/$role/AGENTS.md"; continue; }
  [ -f "$soul" ]     || { warn "missing role identity .hermes/agents/$role/SOUL.md"; continue; }

  if [ "$CHECK" -eq 1 ]; then
    [ -d "$dir" ] || { warn "missing profiles/$role"; continue; }
  else
    mkdir -p "$dir"
  fi

  for f in profile.yaml config.yaml AGENTS.md; do
    [ -f "$dir/$f" ] || warn "profiles/$role/$f missing"
  done

  # SOUL.md is a symlink to the core role identity: one file, two paths.
  if [ -L "$dir/SOUL.md" ] || [ -f "$dir/SOUL.md" ]; then
    target="$(readlink "$dir/SOUL.md" 2>/dev/null || echo "regular-file")"
    if [ "$target" = "regular-file" ]; then
      warn "profiles/$role/SOUL.md is a regular file; it must symlink to .hermes/agents/$role/SOUL.md"
    elif [ "$target" != "../../.hermes/agents/$role/SOUL.md" ]; then
      warn "profiles/$role/SOUL.md points to '$target'"
    else
      ok "profiles/$role/SOUL.md -> $target"
    fi
  elif [ "$CHECK" -eq 1 ]; then
    warn "profiles/$role/SOUL.md missing"
  else
    ln -s "../../.hermes/agents/$role/SOUL.md" "$dir/SOUL.md"
    ok "created profiles/$role/SOUL.md"
  fi

  # Skills: symlinks into the single pool, derived from the manifest.
  skills_dir="$dir/skills"
  if [ "$CHECK" -eq 1 ]; then
    [ -d "$skills_dir" ] || warn "profiles/$role/skills/ missing"
  else
    mkdir -p "$skills_dir"
  fi

  while IFS= read -r skill; do
    [ -n "$skill" ] || continue
    name="$(basename "$skill")"
    source_path="$ROOT/.hermes/$skill"
    link="$skills_dir/$name"
    if [ ! -d "$source_path" ]; then
      warn "manifest declares $skill but .hermes/$skill does not exist"
      continue
    fi
    if [ -L "$link" ]; then
      current="$(readlink "$link")"
      expected="../../../.hermes/$skill"
      [ "$current" = "$expected" ] && ok "skills/$name" || warn "skills/$name points to '$current'"
    elif [ -e "$link" ]; then
      warn "skills/$name exists and is not a symlink"
    elif [ "$CHECK" -eq 1 ]; then
      warn "skills/$name missing"
    else
      ln -s "../../../.hermes/$skill" "$link"
      ok "skills/$name -> ../../../.hermes/$skill"
    fi
  done < <(declared_skills "$manifest")

  # Stale symlinks: a skill no longer declared in the manifest.
  if [ -d "$skills_dir" ]; then
    declared_names="$(declared_skills "$manifest" | while IFS= read -r s; do [ -n "$s" ] && basename "$s"; done)"
    while IFS= read -r link; do
      [ -n "$link" ] || continue
      name="$(basename "$link")"
      if ! printf '%s\n' "$declared_names" | grep -qx "$name"; then
        if [ "$CHECK" -eq 1 ]; then
          warn "stale skills/$name"
        else
          rm -f "$link"; ok "removed stale skills/$name"
        fi
      fi
    done < <(find "$skills_dir" -maxdepth 1 -type l 2>/dev/null)
  fi
done

# 2. Profile homes
echo
echo "2. Profile homes in $PROFILES_DIR"
if [ "$CHECK" -eq 1 ]; then
  [ -d "$PROFILES_DIR" ] || warn "$PROFILES_DIR does not exist"
else
  mkdir -p "$PROFILES_DIR"
fi

for role in "${ROLES[@]}"; do
  link="$PROFILES_DIR/$role"
  target="$ROOT/profiles/$role"
  [ -d "$target" ] || { warn "profiles/$role missing; cannot link"; continue; }
  if [ -L "$link" ]; then
    current="$(readlink "$link")"
    [ "$current" = "$target" ] && ok "$role -> $target" || warn "$link points to '$current'"
  elif [ -e "$link" ]; then
    warn "$link exists and is not a symlink; remove it by hand"
  elif [ "$CHECK" -eq 1 ]; then
    warn "$role not linked"
  else
    ln -s "$target" "$link"
    ok "linked $role"
  fi

  # Credentials are never committed. The profile reads the maintainer's shared
  # .env through a symlink, so a role runs without copying secrets into git.
  if [ -f "$HERMES_HOME/.env" ]; then
    if [ -e "$target/.env" ] || [ -L "$target/.env" ]; then
      ok "$role .env present"
    elif [ "$CHECK" -eq 1 ]; then
      warn "$role .env missing (run ./setup.sh)"
    else
      ln -s "$HERMES_HOME/.env" "$target/.env"
      ok "$role .env -> $HERMES_HOME/.env"
    fi
  else
    note "$role: no $HERMES_HOME/.env to link; provide credentials per profile"
  fi
done

# 3. Skill scoping per profile
#
# The real binding is each profile's own skills/ directory. The repository skill
# tree is also trusted so a maintenance session started at the repo root sees the
# same SKILL.md files, but trust is best-effort: `.hermes/` doubles as a Hermes
# project-state directory name and discovery there is not guaranteed. The profile
# check below is the authoritative one.
echo
echo "3. Skill scoping per profile"
if [ "$TRUST" -eq 1 ] && command -v hermes >/dev/null 2>&1; then
  if hermes skills trust "$ROOT" >/dev/null 2>&1; then
    ok "repository skill tree trusted (best-effort)"
  else
    note "hermes skills trust did not confirm; profile skills are unaffected"
  fi
elif [ "$TRUST" -eq 0 ]; then
  note "repository trust skipped (--no-trust)"
else
  note "hermes not on PATH; skipping runtime checks"
fi

if command -v hermes >/dev/null 2>&1; then
  for role in "${ROLES[@]}"; do
    manifest="$ROOT/.hermes/agents/$role/AGENTS.md"
    [ -f "$manifest" ] || continue
    expected="$(declared_skills "$manifest" | while IFS= read -r s; do [ -n "$s" ] && basename "$s"; done | sort)"
    count_expected="$(printf '%s\n' "$expected" | grep -c . || true)"
    count_actual="$(hermes skills list -p "$role" 2>/dev/null | grep -c '│ local ' || true)"
    if [ "$count_expected" = "$count_actual" ]; then
      ok "$role: $count_actual skill(s) visible"
    else
      warn "$role: expected $count_expected skill(s), visible $count_actual"
    fi
  done
fi

# 4. Summary
echo
if [ "$fail" -eq 0 ]; then
  echo "Result: structure consistent."
  [ "$CHECK" -eq 0 ] && echo "Next: hermes profile list  ·  hermes -p orchestrator"
  exit 0
fi
echo "Result: drift detected." >&2
[ "$CHECK" -eq 1 ] && echo "Run ./setup.sh to repair." >&2
exit 1
