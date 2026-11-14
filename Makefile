# LADE — development Makefile
#
# One place for the operations this repository needs while it is being developed:
# provisioning the nine role profiles, verifying them, running one, inspecting it,
# and resetting them to test a fresh setup end to end.
#
#   make help                 # every target, one line each
#   make check                # ./setup.sh --check (drift between repo and runtime)
#   make verify               # per-role health + "can this profile attach?" (the regression test)
#
# Conventions
#   ROLE=<role>  picks a single profile for the targets that act on one.
#   CONFIRM=1    is required by every target that deletes something.
#   DRY=1        prints what a destructive target would remove, and removes nothing.
#
# The repository path may contain spaces; nothing here splits on whitespace.

SHELL := /bin/bash
.SHELLFLAGS := -eu -o pipefail -c
.ONESHELL:
.SUFFIXES:
.DEFAULT_GOAL := help

# `make` must be invoked from the repository root (directly or with `make -C <repo>`).
# Do NOT derive this with $(dir ...) or $(patsubst ...): those split on whitespace and
# mangle a repository path that contains spaces or non-ASCII bytes ("Área de trabalho").
ROOT := $(CURDIR)
HERMES ?= hermes
HERMES_HOME ?= $(HOME)/.hermes
PROFILES_DIR := $(HERMES_HOME)/profiles
HERMES_AGENT := $(HERMES_HOME)/hermes-agent
VENV_PY := $(shell if [ -x "$(HERMES_AGENT)/venv/bin/python3" ]; then printf '%s' "$(HERMES_AGENT)/venv/bin/python3"; else printf 'python3'; fi)
DEV := scripts/lade_dev.py
REPAIR := scripts/repair_profile_homes.sh
# The provisioned repository layout that setup.sh owns; everything else under
# profiles/<role>/ is runtime state Hermes should be writing in the HOME instead.
KEEP_IN_REPO := -name AGENTS.md -o -name SOUL.md -o -name profile.yaml -o -name config.yaml -o -name .env -o -name skills
VERIFY_TIMEOUT ?= 5
SMOKE_TIMEOUT ?= 180

# ────────────────────────────────────────────────────────────────────────────────
##@ Meta

.PHONY: help
help: ## Show this help
	@awk 'BEGIN {FS = ":.*## "; printf "\nLADE development targets\n"} \
	     /^##@/ {printf "\n%s\n", substr($$0, 5)} \
	     /^[a-zA-Z0-9_.-]+:.*## / {printf "  \033[36m%-24s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@printf '\nVariables: ROLE=<role>  CONFIRM=1 (destructive)  DRY=1 (preview)  HERMES_HOME=%s\n\n' "$(HERMES_HOME)"

.PHONY: env print-venv-python
env: ## Print the environment this Makefile will use
	@printf 'repository      %s\n' "$(ROOT)"
	@printf 'hermes binary   %s -> %s\n' "$(HERMES)" "$$(command -v "$(HERMES)" || echo MISSING)"
	@printf 'hermes version  %s\n' "$$("$(HERMES)" --version 2>/dev/null | head -1 || echo MISSING)"
	@printf 'hermes home     %s\n' "$(HERMES_HOME)"
	@printf 'runtime python  %s\n' "$(VENV_PY)"
	@printf 'roles           %s\n' "$$(ls -1 "$(ROOT)/profiles" 2>/dev/null | tr '\n' ' ')"

print-venv-python: ## Print the runtime python path (for scripts/lade_dev.py)
	@printf '%s\n' "$(VENV_PY)"

# ────────────────────────────────────────────────────────────────────────────────
##@ Provisioning

.PHONY: setup
setup: ## Provision/repair links and skills (./setup.sh)
	cd "$(ROOT)" && ./setup.sh

.PHONY: check
check: ## Report drift between the repository and the runtime (writes nothing)
	cd "$(ROOT)" && ./setup.sh --check

.PHONY: drift
drift: check ## Alias of check

.PHONY: repair-homes repair-homes-check
repair-homes: ## Make every profile home a real directory that resolves inside $HERMES_HOME
	bash "$(ROOT)/$(REPAIR)" --apply

repair-homes-check: ## Report profile-home layout drift only (writes nothing)
	bash "$(ROOT)/$(REPAIR)" --check

# ────────────────────────────────────────────────────────────────────────────────
##@ Verify

.PHONY: verify
verify: ## Health of every profile + will the CLI attach? (exit 1 on any FAIL)
	cd "$(ROOT)" && "$(VENV_PY)" "$(DEV)" --timeout "$(VERIFY_TIMEOUT)" verify

.PHONY: verify-canonical
verify-canonical: ## The three facts that decide attach vs "another tenant's gateway"
	cd "$(ROOT)" && "$(VENV_PY)" "$(DEV)" --timeout "$(VERIFY_TIMEOUT)" canonical

.PHONY: roster
roster: ## Which profiles the host gateway serves, and every parked one with its reason
	cd "$(ROOT)" && "$(VENV_PY)" "$(DEV)" --timeout "$(VERIFY_TIMEOUT)" roster

.PHONY: links
links: ## Check every symlink in the repo and in the profile homes resolves
	@cd "$(ROOT)"
	broken=0
	while IFS= read -r -d '' link; do
	  if [ ! -e "$$link" ]; then
	    printf '  broken  %s -> %s\n' "$$link" "$$(readlink "$$link")"
	    broken=1
	  fi
	done < <(find "$(ROOT)/profiles" "$(PROFILES_DIR)" -type l -print0 2>/dev/null)
	if [ "$$broken" -eq 0 ]; then printf 'RESULT: every symlink resolves.\n'; else printf 'RESULT: broken symlinks above (run: make setup).\n'; exit 1; fi

.PHONY: lint
lint: ## Syntax-check shell and Python, parse every YAML file
	@cd "$(ROOT)"
	for f in setup.sh scripts/*.sh; do [ -f "$$f" ] || continue; bash -n "$$f" && printf '  ok  bash -n %s\n' "$$f"; done
	for f in scripts/*.py; do [ -f "$$f" ] || continue; "$(VENV_PY)" -m py_compile "$$f" && printf '  ok  py_compile %s\n' "$$f"; done
	for f in profiles/*/config.yaml profiles/*/profile.yaml; do
	  [ -f "$$f" ] || continue
	  "$(VENV_PY)" -c 'import sys, ruamel.yaml as y; y.YAML(typ="safe").load(open(sys.argv[1], encoding="utf-8"))' "$$f" \
	    && printf '  ok  yaml %s\n' "$$f"
	done
	if command -v shellcheck >/dev/null 2>&1; then
	  shellcheck setup.sh scripts/*.sh && printf '  ok  shellcheck\n'
	else
	  printf '  skip  shellcheck not installed\n'
	fi
	printf 'RESULT: lint clean.\n'

.PHONY: doctor
doctor: ## Hermes self-check (config, providers, dependencies)
	"$(HERMES)" doctor

# ────────────────────────────────────────────────────────────────────────────────
##@ Profiles: run and inspect

.PHONY: profiles
profiles: ## List every profile with model and gateway state
	"$(HERMES)" profile list

.PHONY: require-role
require-role:
	@if [ -z "$(ROLE)" ]; then printf 'usage: make <target> ROLE=<role>\navailable: %s\n' "$$(ls -1 "$(ROOT)/profiles" | tr '\n' ' ')"; exit 2; fi

.PHONY: run
run: require-role ## Start an interactive session as one role: make run ROLE=orchestrator
	cd "$(ROOT)" && exec "$(HERMES)" -p "$(ROLE)"

.PHONY: smoke
smoke: require-role ## One-shot turn as one role (proves end to end: make smoke ROLE=architect)
	cd "$(ROOT)" && timeout "$(SMOKE_TIMEOUT)" "$(HERMES)" -p "$(ROLE)" chat -q "Reply with the single word OK."

.PHONY: status
status: require-role ## Gateway status for one role
	"$(HERMES)" -p "$(ROLE)" gateway status

.PHONY: tools
tools: require-role ## Effective toolset of one role
	"$(HERMES)" -p "$(ROLE)" tools list

.PHONY: skills
skills: require-role ## Skills visible to one role
	"$(HERMES)" -p "$(ROLE)" skills list

.PHONY: logs
logs: require-role ## Tail the agent and error logs of one role
	@tail -n 40 "$(PROFILES_DIR)/$(ROLE)/logs/agent.log" 2>/dev/null || printf 'no agent.log yet\n'
	printf '\n--- errors ---\n'
	tail -n 40 "$(PROFILES_DIR)/$(ROLE)/logs/errors.log" 2>/dev/null || printf 'no errors.log yet\n'

.PHONY: session
session: require-role ## Show the last sessions recorded for one role
	"$(HERMES)" -p "$(ROLE)" sessions --limit 10 2>/dev/null || printf 'run `hermes -p %s --help` for the session command of this version\n' "$(ROLE)"

# ────────────────────────────────────────────────────────────────────────────────
##@ Gateway

.PHONY: gateway-status
gateway-status: ## Host gateway status across every profile
	"$(HERMES)" gateway status

.PHONY: gateway-restart
gateway-restart: ## Restart the host gateway (run this from a shell OUTSIDE the gateway)
	@printf 'note: a gateway restart kills anything running inside the gateway (this shell included).\n'
	"$(HERMES)" gateway restart

.PHONY: rescan
rescan: ## Ask the host gateway to reconcile profiles/ right now
	cd "$(ROOT)" && "$(VENV_PY)" "$(DEV)" --timeout 30 rescan

.PHONY: serve
serve: require-role ## Explicitly serve one parked profile on the host gateway
	cd "$(ROOT)" && "$(VENV_PY)" "$(DEV)" --timeout 40 serve "$(ROLE)"

# ────────────────────────────────────────────────────────────────────────────────
##@ Reset (destructive — require CONFIRM=1)

.PHONY: prune-runtime
prune-runtime: ## Remove runtime state that leaked into the repository (keeps the provisioned layout)
	@cd "$(ROOT)"
	for dir in profiles/*/; do
	  while IFS= read -r -d '' entry; do
	    if [ "$(DRY)" = "1" ]; then printf '  would remove  %s\n' "$$entry"; else rm -rf "$$entry" && printf '  removed       %s\n' "$$entry"; fi
	  done < <(find "$$dir" -mindepth 1 -maxdepth 1 \( $(KEEP_IN_REPO) \) -prune -o -print0)
	done
	if [ "$(DRY)" = "1" ]; then printf 'note: dry run only.\n'; else printf 'kept in %s: AGENTS.md SOUL.md profile.yaml config.yaml .env skills\n' "profiles/<role>"; fi

.PHONY: reset-homes
reset-homes: ## Delete every LADE profile home, then re-provision them (CONFIRM=1)
	@if [ "$(CONFIRM)" != "1" ]; then printf 'Refusing: this deletes %s/profiles/<role> for every role.\nRe-run with CONFIRM=1 (and DRY=1 to preview).\n' "$(HERMES_HOME)"; exit 2; fi
	cd "$(ROOT)"
	for dir in profiles/*/; do
	  role="$$(basename "$$dir")"
	  home="$(PROFILES_DIR)/$$role"
	  if [ "$(DRY)" = "1" ]; then printf '  would delete  %s\n' "$$home"; continue; fi
	  rm -rf "$$home" && printf '  deleted       %s\n' "$$home"
	done
	if [ "$(DRY)" != "1" ]; then ./setup.sh; fi

.PHONY: reset-profiles
reset-profiles: ## Full reset: homes + runtime state + skills, then re-provision (CONFIRM=1)
	@if [ "$(CONFIRM)" != "1" ]; then printf 'Refusing: this deletes every LADE profile home AND the runtime state in the repository.\nRe-run with CONFIRM=1 (and DRY=1 to preview).\n'; exit 2; fi
	$(MAKE) --no-print-directory reset-homes CONFIRM=1 DRY=$(DRY)
	$(MAKE) --no-print-directory prune-runtime DRY=$(DRY)
	if [ "$(DRY)" = "1" ]; then
	  printf 'note: dry run only — nothing re-provisioned.\n'
	else
	  ./setup.sh
	  printf '\nnext: `make gateway-restart`, then `make verify`\n'
	fi

.PHONY: backup
backup: ## Archive profile content and homes into .lade-backups/ (keeps runtime state)
	@cd "$(ROOT)"
	stamp="$$(date +%Y%m%dT%H%M%S)"
	mkdir -p .lade-backups
	tar -czf ".lade-backups/profiles-$$stamp.tar.gz" profiles
	printf '  wrote .lade-backups/profiles-%s.tar.gz\n' "$$stamp"

.PHONY: restore
restore: ## Restore the newest backup archive over profiles/ (CONFIRM=1)
	@if [ "$(CONFIRM)" != "1" ]; then printf 'Refusing: this overwrites profiles/.\nRe-run with CONFIRM=1.\n'; exit 2; fi
	cd "$(ROOT)"
	archive="$$(ls -1t .lade-backups/profiles-*.tar.gz 2>/dev/null | head -1 || true)"
	if [ -z "$$archive" ]; then printf 'no backup in .lade-backups/ (run: make backup)\n'; exit 1; fi
	printf '  restoring %s\n' "$$archive"
	tar -xzf "$$archive"
	printf '  done. run ./setup.sh, then make verify.\n'

# ────────────────────────────────────────────────────────────────────────────────
##@ Housekeeping

.PHONY: clean
clean: ## Remove caches this Makefile created (backups are kept)
	@cd "$(ROOT)"
	rm -rf .lade-backups
	find . -name __pycache__ -type d -prune -exec rm -rf {} + 2>/dev/null || true
	printf 'cleaned.\n'

.PHONY: report
report: ## Show the path of the defect report for this repository
	@ls -1 docs/reports/*.md 2>/dev/null || printf 'no report found\n'