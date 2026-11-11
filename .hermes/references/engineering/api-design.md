---
name: api-design
description: Design, specify and review HTTP and async APIs contract-first with OpenAPI 3.x or AsyncAPI, standard error model (RFC 9457), pagination, idempotency, versioning and breaking-change control. Use whenever a task creates, changes, consumes or reviews an API, endpoint, schema, webhook or event interface, even if the user only says "add an endpoint" or "expose this data".
---

# Skill: api-design

> **Version:** 0.1.0 (draft) · **Date:** 2026-11-06 · **Location:** `skills/software-engineering/api-design/SKILL.md`
> Defines *how to design API contracts*. Acceptance rules live in `references/lattinus-code.md` (§3, §6.2 API row). Do not restate them here.

## When to use / not use

**Use:** new or changed endpoints, schemas, events; contract review; compatibility analysis.
**Do not use:** for internal function signatures (use `python` / `golang`), or for data-at-rest contracts (use `data-engineering/data-contracts`).

## Inputs

- `task.md`: `acceptance_criteria`, `constraints`, `out_of_scope`, consumers of the API.
- Existing specification (OpenAPI/AsyncAPI) and current version, if any.
- `references/engineering/api.md`, only if listed in the manifest and needed.

## Procedure

1. **Identify consumers and use cases.** Who calls it, how often, with what data volume.
2. **Contract first.** Write or update the spec (OpenAPI 3.x for HTTP, AsyncAPI for async) *before* implementation. Implementation follows the spec.
3. **Model resources and operations** (see Standards). Reuse existing schemas and conventions in the repository.
4. **Classify the change:** additive (compatible) or breaking. Declare it in the PR.
5. **If breaking:** stop and propose an ADR (`architect` writes it, a human approves) before implementing. Include a deprecation window and migration path (`lattinus-code.md` §4.1, §7.6).
6. **Validate the spec** with the repository's OpenAPI/AsyncAPI validator. If none exists, propose one via the `dependencies` gate.
7. **Hand off** the validated spec to `software-engineer` through `task.md`, with examples and error cases.

## Standards

- **Spec:** every operation has `operationId`, summary, request and response schemas, and at least one example. Schemas are reused via `$ref`, not duplicated.
- **Resources:** nouns, plural, lowercase kebab-case paths. Methods follow semantics: `GET` safe, `PUT`/`DELETE` idempotent, `POST` creates or triggers.
- **Status codes:** use the narrowest correct code (200, 201, 202, 204, 400, 401, 403, 404, 409, 422, 429, 5xx). Document every code an operation can return.
- **Errors:** RFC 9457 Problem Details (`application/problem+json`): `type`, `title`, `status`, `detail`, `instance`, plus extensions. Stable, documented `type` values. No stack traces or sensitive data.
- **Pagination:** required for collections. Prefer cursor-based for large or changing data; state the default and maximum page size.
- **Idempotency:** unsafe operations that clients may retry (`POST`) support an idempotency key, or document why not.
- **Long-running work:** return `202 Accepted` with a status resource; do not hold connections open.
- **Versioning:** SemVer for the spec. Major version visible in the path or media type, per repository convention. Additive changes only within a major version.
- **Compatible changes:** new optional fields, new endpoints, new enum values only if documented as open. **Breaking:** removing or renaming fields, changing types or semantics, tightening validation, making optional required.
- **Spatial data:** state CRS (EPSG) explicitly in request and response (`lattinus-code.md` §8). Prefer GeoJSON or the standard in the repository; declare coordinate order and precision. Catalog interfaces follow STAC where applicable.
- **Time:** ISO 8601 / RFC 3339, UTC by default.
- **Security:** authentication and authorization declared in the spec; validate and sanitize all input; no secrets in URLs or logs; rate limits documented.
- **Async (AsyncAPI):** declare channels, message schemas, delivery semantics (at-least-once assumed unless stated) and consumer idempotency.

## Checklist

- [ ] Spec updated and valid; examples included.
- [ ] Every operation documents success and error responses (RFC 9457).
- [ ] Collections paginated; retry-safe operations idempotent or justified.
- [ ] Change classified compatible or breaking; breaking has an approved ADR and migration path.
- [ ] Auth, CRS and time conventions declared.
- [ ] Backward compatibility and versioning impact stated in the PR.

## Gates

- `dependencies`: spec validators, code generators, new libraries.
- `safety`: designs that expose destructive or external-facing operations.
- `documentation`: any change to the public contract.

## Anti-patterns

- Implementing first and writing the spec afterwards to match.
- Verbs in paths (`/getUser`), inconsistent naming, mixed casing.
- Returning `200` with an error body; leaking internals in error messages.
- Unbounded collection responses; offset pagination over fast-changing data without justification.
- Silent breaking changes (renaming a field "because it is cleaner").
- Ambiguous geometry: no CRS, unspecified axis order.
- Exposing storage schema directly as the API schema.

## Escalate when

- The change is breaking and no ADR is approved.
- Consumers are unknown and compatibility cannot be assessed.
- Security or authorization requirements are unspecified.
- The task requires an interface convention not defined in the repository or `references/`.