# api.md — API Engineering Reference

> **Version:** 0.2.0 (draft) · **Date:** 2026-11-12 · **Location:** `references/engineering/api.md`
> Replaces `api-design.md` (a verbatim copy of the `api-design` skill, and the wrong filename: every manifest points to `api.md`). **Delete `references/engineering/api-design.md`.**
> Procedure lives in `skills/software-engineering/api-design/SKILL.md`. Only humans edit this file.

## 1. Standards `ACCEPTED` (`lattinus-code.md` §3)

| Area | Standard |
|------|----------|
| HTTP | OpenAPI 3.x |
| Async | AsyncAPI |
| Errors | RFC 9457 Problem Details (`application/problem+json`) |
| Time | ISO 8601 / RFC 3339, UTC default |
| Spatial | EPSG explicit in request and response; STAC for catalog interfaces |
| Versioning | SemVer 2.0.0 |

## 2. Lattinus context

- Serving API (module 2.1) is the unified front door: REST, GraphQL, AI, streaming (`architecture.md` §2). Its spec is `OPEN` (`OQ-REF-014`).
- Interface contracts between modules use IF/EVT documents (`references/engineering/documentation.md` §1). IF-001 and EVT-001 (Ingestion ↔ Storage) are not read: do not infer their payloads.
- Public SDK surfaces expose no engine names (`platform/transformation.md` §3, `OQ-REF-010`).

## 3. Open parameters (`TBD`)

| Parameter | Owner |
|-----------|-------|
| Major version location (path vs media type) | Maintainers / architect (ADR) |
| Spec validator and CI integration | Maintainers / devops-sre |
| Deprecation window | Maintainers |
| Authentication scheme | architect (ADR) |
