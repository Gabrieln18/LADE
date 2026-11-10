<!--
TEMPLATE: research.md · v0.1.0 (bootstrap) · Location: templates/research.md
Purpose:   Structured investigation that supports a decision (technology comparison, feasibility, bug root-cause, domain question).
Filled by: any agent, within its manifest.
Used when: a decision depends on information not yet in references/.
Consumed by: requester, architect (design/ADR input), orchestrator.
Rule: separate FACTS (sourced), ASSUMPTIONS (declared) and RECOMMENDATIONS (reasoned) (SOUL §3). Never fabricate APIs, versions or results.
Instantiate: copy, fill, delete all <!-- --> comments. Write content in `output_language`.
-->
---
task_id: LADE-YYYYMMDD-NNN
produced_by: <agent>
review_level: standard   # human-only | standard
references: []
adr: none
gates: {safety: na, dependencies: na, git: na, documentation: na}
status: IN_PROGRESS
assumptions: []
research_date: YYYY-MM-DD
---

# Research: <question as a title>

## 1. Question and decision supported
- Question: <one sentence>
- Decision this informs: <e.g. choose library X, ADR-NNNN, design option>

## 2. Scope
- In scope: <...>
- Out of scope: <...>

## 3. Method and sources
<!-- How the research was done. Every source: link or path, date, and reliability note. -->
| # | Source | Type (reference / official doc / code / experiment) | Date | Reliability |
|---|--------|------------------------------------------------------|------|-------------|
| 1 | | | | |

## 4. Findings
<!-- Cite sources by number. Keep the three classes apart. -->

### 4.1 Facts (sourced)
- F1: <statement> [source #]

### 4.2 Assumptions (declared)
- A1: <statement> · how to verify: <...>

### 4.3 Recommendations (reasoned)
- R1: <recommendation> · based on: F#, A#

## 5. Comparison (if applicable)
| Criterion | Option A | Option B |
|-----------|----------|----------|
| | | |

## 6. Conclusion
- Answer: <direct answer to §1>
- Confidence: <high | medium | low> · why: <...>

## 7. Unverified items
<!-- What was not checked, and why. -->
- <item>

## 8. Follow-ups
<!-- Append each to memory/open-questions.md with task_id and owner. -->
- <question or action, owner>