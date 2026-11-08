---
name: data-quality
description: Design, implement or review data quality checks that verify a data contract at runtime: completeness, validity, uniqueness, consistency, freshness and geospatial checks, each with a threshold and a failure action. Use whenever a task adds a pipeline stage or dataset, mentions validation, anomalies, bad records, nodata, cloud masks, invalid geometries or quality reports, or needs quality evidence for a PR.
owner: data-engineer
version: 0.1.0
---

# data-quality

## 1. When to use / When NOT to use
Use: defining or running checks, deciding failure behavior, producing quality evidence.
Do NOT use: to define the schema or SLA (`data-contracts`), or to move or transform data (`ingestion`, `pipelines`).

## 2. Required inputs (task.md)
- The data contract (id and version). Without one, ask for it or declare the assumed schema.
- Thresholds from the contract/task. If absent, propose values and mark them as assumptions.
- Sample data for local runs.

## 3. Procedure
1. Read the contract. Derive checks from it; do not invent rules the contract does not imply without declaring them.
2. Pick the dimensions (section 4) relevant to each field or dataset.
3. Define each check with: `id`, `dimension`, `target`, `rule`, `threshold`, `severity`, `action`.
4. Place checks at boundaries: input (after ingestion), after major transforms, output (before publish).
5. Choose the failure action per check (section 5). Never drop records silently.
6. Implement checks as code, deterministic, runnable locally on sample data.
7. Produce the quality report (section 6) and attach it as PR evidence.
8. Define behavior when the check itself cannot run (treat as failure for `block` checks).

## 4. Dimensions and geospatial checks
| Dimension | Examples |
|-----------|----------|
| Completeness | null rate per field, expected partitions/dates present |
| Validity | type, range, enum, regex, units plausible |
| Uniqueness | duplicates on declared key |
| Consistency | cross-field and cross-dataset rules, referential integrity |
| Freshness | latest timestamp within SLA |
| Spatial | valid, non-empty, expected geometry type; CRS matches contract; extent within expected bounds; spatial coverage |
| Raster | nodata share, value range vs dtype/units, cloud/mask coverage, band count |
| Temporal | gaps in series, time zone and ordering, acquisition vs processing time |
| Outliers | statistical or domain limits, with the method declared |

## 5. Failure actions
| Action | Use when |
|--------|----------|
| `block` | The output would violate the contract; stop publish, task `BLOCKED` |
| `quarantine` | Few bad records; move to a quarantine location with reason, continue |
| `warn` | Informative; record in report, do not stop |

Quarantined records are kept with `check_id`, reason and run id. Rates above the threshold escalate to `block`.

## 6. Quality report (evidence)
```yaml
run_id: <id>
dataset: <contract id@version>
checks:
  - {id: <...>, status: pass|fail|error, observed: <value>, threshold: <value>, action: <block|quarantine|warn>, affected: <count>}
summary: {passed: <n>, failed: <n>, quarantined: <n>, blocked: <bool>}
```

## 7. Standards
`lattinus-code.md` §6.2 (data pipeline), §8 (quality checks, accuracy and uncertainty). Do not report derived precision beyond what sources support.

## 8. Outputs
Check definitions and code, sample-run report, traceability header (`AGENTS.md` §10).

## 9. Gates triggered
Dependencies (if a validation library is proposed), Documentation, Git.

## 10. Done checklist
- [ ] Every check has threshold and action.
- [ ] Checks trace back to contract fields or declared assumptions.
- [ ] Report generated from a real run on sample data.
- [ ] No silent record loss.
- [ ] Behavior when a check errors is defined.

## 11. Escalate when
- No contract and no safe assumption on schema.
- Thresholds are domain decisions the agent cannot justify.
- Quarantine volume suggests a source or contract problem.

## 12. Anti-patterns
Thresholds without justification; warn-only for contract violations; checks that pass on empty data; dropping bad rows to "make it pass"; coverage metrics replacing meaningful assertions.

## 13. References (pointers only)
`references/engineering/data.md`, `references/domain/geospatial.md`, `references/domain/earth-observation.md`.
Record missing files in `memory/open-questions.md`.