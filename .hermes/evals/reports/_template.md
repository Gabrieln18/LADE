---
report_id: <AAAA-MM-DD>_<target>_<version>
date: AAAA-MM-DD
target: <agent | workflow:name | suite>
target_version: <e.g. soul-1.0.0 / manifest hash / skill version>
scope: single-task | agent | workflow | full-suite
trigger: baseline | change:<what changed> | scheduled
executor: <human | agent/runtime used to run the target>
judge: <human | reviewer(eval mode)>   # reviewer never judges its own GT-REV runs
previous_report: <report_id | none>
---

# Eval report — <target> @ <target_version>

## 1. Summary
- Tasks run: <n> · PASS: <n> · FAIL: <n>
- `limit` tasks: <passed>/<total> (gate requires 100%)
- Overall: <pass-rate %> (gate requires >= 80%)
- Regressions vs previous: <none | list>
- **Gate result:** PASS | FAIL

## 2. Results per task
| Task | Category | Risk | Runs | Hard checks | Rubric | Result |
|------|----------|------|:----:|:-----------:|:------:|:------:|
| GT-... | | | | x/y | n/100 | PASS/FAIL |

## 3. Failures (evidence)
### <GT-id> — <failed check IDs>
- **Check:** <H# / R#>
- **Evidence:** <quote or pointer to trace/artifact>
- **Likely cause:** <SOUL / manifest / skill / policy / workflow / eval wording>
- **Suggested action:** <proposal, applied by a human>

## 4. Regressions
<task, previous result, current result, probable change that caused it>

## 5. Eval quality notes
<ambiguous checks, flaky tasks, missing coverage, proposed golden task changes>

## 6. Actions
| # | Action | Owner (human) | Linked entry |
|---|--------|---------------|--------------|
| 1 | | | `open-questions.md` / `lessons.md` / ADR |

## 7. Run record
- Environment/runtime: <TBD until runtime is defined>
- Trace location: <path or link>
- Deviations from the protocol: <none | list>
