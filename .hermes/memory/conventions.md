# conventions.md

> **Writer:** orchestrator, after human approval. **Mode:** append. If this file already exists in the repository, **append only the C-001 entry**.
> Each entry MUST cite how the human approved (`memory/README.md` §3.9, Q-014).

## Entries

### C-001 · Python toolchain: uv + ruff + pytest
- **Date:** 2026-11-12
- **Task:** none (v2.1 review session)
- **Decision:** Python projects use `uv` (environment, `uv.lock`), `ruff` (lint and format) and `pytest`. `poetry` is not used.
- **Source:** `references/engineering/python.md` §1.
- **Approval evidence:** maintainer answer in the v2.1 review session, 2026-11-12 (formal evidence format pending Q-014).
- **Open:** type checker (Q-018), Python version (Q-019).
