# testing.md — Testing Reference

> **Version:** 0.2.0 (draft) · **Date:** 2026-11-12 · **Location:** `references/engineering/testing.md`
> Replaces the 0.1.0 file (a verbatim copy of the `testing` skill). Procedure lives in `skills/software-engineering/testing/SKILL.md`.
> Only humans edit this file.

## 1. Runners `ACCEPTED`

| Language | Command |
|----------|---------|
| Python | `uv run pytest` (`uv run pytest -x -q` while iterating) |
| Go | `go test ./...` (`-race` for concurrency) |

## 2. Project rules (from `lattinus-code.md` §7.2, §9; not restated beyond pointers)

- Pyramid and determinism: `lattinus-code.md` §7.2.
- AI components: never assert exact free text (`lattinus-code.md` §9).
- Spatial fixtures declare CRS (EPSG), nodata and dtype (`lattinus-code.md` §8).
- Data quality inside pipelines is not unit testing: `skills/data-engineering/data-quality`.

## 3. Open parameters (`TBD`)

| Parameter | Owner |
|-----------|-------|
| Coverage threshold (Q-006) | Maintainers |
| Test layout and markers in Lattinus Code | Maintainers |
| Shared sample data location for product tests | Maintainers |
| CI required checks (Q-003) | Maintainers / devops-sre |
