# review-principles.md — how the reviewer judges

> **Version:** 0.1.0 (new in v2.2) · **Date:** 2026-11-13 · **Location:** `agents/reviewer/references/review-principles.md`
> Agent-level reference for the `reviewer` only. It defines criteria and severity; the report format is `templates/review.md`. Only humans edit this file.
> Key words MUST, MUST NOT, SHOULD, MAY follow RFC 2119.

## 1. Basis of judgement

Judge the artifact against, in this order:

1. the `acceptance_criteria` in its `task.md`;
2. the Definition of Done in `references/lattinus-code.md` §6 and §12;
3. `policies/*` (always prevailing);
4. the domain reference the artifact cites;
5. the relevant skill, used as a criterion — never as a style preference.

Taste is not a criterion. When a finding rests on a convention not written in 1–5, it is a `note`, not a `major`.

## 2. Evidence rule

1. A criterion is met only when evidence exists: test output, command output, header, diff, cited reference.
2. Absence of evidence is a finding, not a pass.
3. A check that could not be run is reported as `not verified`, with the reason. It MUST NOT be scored as a pass.
4. The reviewer reads the artifact, not the author's description of it.

## 3. Severity

| Severity | Meaning | Effect on verdict |
|----------|---------|-------------------|
| `blocker` | Unsafe, irreversible, contract-breaking or violates a policy | forces `REWORK` |
| `major` | Acceptance criterion unmet, or Definition of Done broken | forces `REWORK` |
| `minor` | Real defect with bounded impact; the criterion is still met | `PASS` allowed, listed as follow-up |
| `note` | Improvement or convention outside 1–5 | `PASS`, no action required |

Rules:
1. Every finding cites location, the violated criterion and what would resolve it.
2. A finding without a resolution is an opinion; drop it or convert it to a `Q-NNN`.
3. Out-of-scope issues are reported as `open-questions`, never as `REWORK` reasons.

## 4. Separation of duties

1. The reviewer MUST NOT modify the artifact under review. Corrections return as `REWORK(agent, reason)`.
2. The reviewer MUST NOT review an artifact it authored. Its authored outputs are review reports and lessons only.
3. Documentation is reviewed like any other artifact, using the documentation skills as criteria.
4. At most 2 `REWORK` cycles per task; the next failure is `ESCALATE`.

## 5. Proportional depth

Scale scrutiny to risk:

| Risk | Depth |
|------|-------|
| Architecture, data contracts, security, public APIs | Full pass over every criterion plus the domain reference |
| Behaviour change in an existing module | Criteria plus tests and regression coverage |
| Documentation only | Criteria, command verification, placeholder and link check |
| Trivial fix | Criteria plus the diff |

## 6. Lessons

Write to `memory/lessons.md` only when the failure is recurring, non-obvious or caused a `REWORK`. One entry per lesson, with `task_id` and `Affects`. Post-merge defects reported by humans are recorded the same way (`references/lattinus-code.md` §13.4).

## 7. Limits

- MUST NOT issue `PASS` with an open `blocker` or `major`.
- MUST NOT lower a criterion to reach `PASS`, or raise one to justify `REWORK`.
- MUST NOT exceed the rework limit, or review its own `GT-REV-*` eval runs (`evals/README.md` §4).
