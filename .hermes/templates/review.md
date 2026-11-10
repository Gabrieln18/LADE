<!--
TEMPLATE: review.md · v0.1.0 (bootstrap) · Location: templates/review.md
Purpose:   Review record: checklist + verdict (AGENTS.md §8).
Filled by: reviewer (standard level) or the human reviewer (human-only, use §8 variant).
Used when: after policy gates, before delivery.
Consumed by: orchestrator (routes verdict), requester/maintainer (approves PR).
Rules: the reviewer MUST NOT modify the artifact under review. Corrections return via REWORK.
Instantiate: copy, fill, delete all <!-- --> comments. Write content in `output_language`.
-->
---
task_id: LADE-YYYYMMDD-NNN
produced_by: reviewer
review_level: standard   # human-only | standard
references: [references/lattinus-code.md]
adr: none
gates: {safety: na, dependencies: na, git: na, documentation: na}
status: IN_REVIEW
assumptions: []
artifact_reviewed: <path or PR>
artifact_author: <agent>
rework_cycle: 0/2        # a third failure becomes ESCALATE
verdict: PASS            # PASS | REWORK(<agent>, <reason>) | ESCALATE
---

# Review: <task_id> · <artifact name>

## 1. Verdict
**`PASS`** | **`REWORK(<agent>, <verifiable reason>)`** | **`ESCALATE`**
<!-- Keep exactly one. REWORK MUST name the responsible agent and a verifiable reason. -->

Justification (2-4 lines): <result first, then why>

## 2. Acceptance criteria (from task.md)
| AC | Met | Evidence |
|----|-----|----------|
| AC1 | yes / no / partial | <test, output, link> |

## 3. Definition of Done
<!-- Source of truth: references/lattinus-code.md §6. Do not copy items; mark them. -->

### 3.1 Universal (§6.1)
- [ ] Acceptance criteria met with evidence
- [ ] Traceability header present
- [ ] Policy gates passed and recorded
- [ ] No secrets, personal data or absolute local paths
- [ ] Lint, format, type check, tests pass (local and CI, CI is `TBD`)
- [ ] No unapproved dependency
- [ ] Assumptions and limitations declared
- [ ] Documentation updated where needed
- [ ] Changelog entry (if user-visible or interface change)

### 3.2 By deliverable type (§6.2)
<!-- Keep only applicable rows; detail in §8 (geospatial) and §9 (AI) of lattinus-code.md. -->
- Type: <code | api | data-pipeline | geospatial | ai | infrastructure | architecture | documentation>
- [ ] <criterion from §6.2 for this type>

## 4. Policy gates
| Gate | Result | Note |
|------|--------|------|
| safety | pass / na / fail | |
| dependencies | pass / na / fail | |
| git | pass / na / fail | |
| documentation | pass / na / fail | |

## 5. Findings
<!-- Severity: blocker (forces REWORK) | major | minor | note. Every blocker needs a verifiable fix. -->
| # | Severity | Location | Agent | Finding | Verifiable fix |
|---|----------|----------|-------|---------|----------------|
| 1 | | | | | |

## 6. Unverified items
<!-- What the reviewer could not check, and why. -->
- <item>

## 7. Lesson candidate (standard only)
<!-- One entry for memory/lessons.md, if a lesson exists. Otherwise write "none". -->
- Task: <task_id>
- Lesson: <what to do or avoid next time>
- Applies to: <agent / skill / workflow>

## 8. Variant: human-only sign-off
<!-- Use instead of §1-§3 when review_level = human-only. Gates still apply (§4). -->
- Reviewer: <name>
- Date: YYYY-MM-DD
- Decision: approved / changes requested
- Notes: <text>