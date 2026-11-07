# review-principles.md

> **Version:** 0.1.0 · Agent-specific principles. Central knowledge lives in `references/`; do not duplicate it here.

## 1. Review order (stop early on a blocker)
1. **Contract:** `task.md` complete? Each `acceptance_criteria` item mapped to evidence.
2. **Traceability and gates:** header present and valid (`AGENTS.md` §10); gate results recorded; no gate failed.
3. **Definition of Done:** `lattinus-code.md` §6.1 + the matching §6.2 / §8 / §9 checklist by deliverable type.
4. **Correctness and risk:** logic, edge cases, error handling, data/CRS validity, security, reversibility.
5. **Evidence:** tests, lint, type check, data-quality or eval results exist and are credible.
6. **Documentation and changelog:** accurate against the artifact; `policies/documentation.md` satisfied.
7. **Scope:** nothing outside `expected_outputs` or inside `out_of_scope`.

## 2. Depth by risk
| Risk | Examples | Depth |
|------|----------|-------|
| High | ADRs, data contracts, security, public APIs, breaking changes | Full pass, all steps, skills loaded |
| Medium | New modules, pipelines, geospatial processing | Steps 1–6 |
| Low | Docs, internal refactor with tests | Steps 1–3 + spot check |

## 3. Severity
| Level | Definition | Effect |
|-------|-----------|--------|
| `blocker` | Violates a policy, acceptance criterion or DoD item; unsafe or irreversible | `REWORK` |
| `major` | Likely defect or missing required evidence | `REWORK` |
| `minor` | Quality issue with no contract violation | Recorded, non-blocking |
| `nit` | Style or preference | Recorded only if useful |

## 4. Finding format
`[severity] <location> — <violated criterion> — <evidence> — <what resolves it>`

## 5. Verdict rules
- `PASS`: no open blocker/major; DoD met; unverified items declared.
- `REWORK(agent, reason)`: name the responsible agent and a reason checkable by re-review. Include cycle number (1 or 2).
- `ESCALATE`: third failure, unresolved conflict, missing information, or a policy block outside agent scope. Use the format in `AGENTS.md` §13.

## 6. Lessons
Write when: recurring pattern, non-obvious cause, or triggered a REWORK. Format: `task_id · context · what failed · rule to prevent it`. Skip trivial or one-off issues.

## 7. Anti-patterns
- Rubber-stamping (PASS without checking evidence).
- Rewriting the artifact instead of returning it.
- Blocking on style or taste.
- Raising out-of-scope issues as REWORK reasons.
- Reviewing without the acceptance criteria.
- Moving the goalposts between REWORK cycles (new blockers must be tied to changes made, or a previously missed criterion, stated as such).