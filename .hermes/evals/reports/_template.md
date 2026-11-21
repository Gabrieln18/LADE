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

## 7. Multi-agent mechanism (when the run exercised delegation)
| Question | Answer | Evidence |
|----------|--------|----------|
| Did the run delegate at all (`delegate_task` calls)? | | trace `output.stream.jsonl` |
| Which profile/model served the child? | | delegation log path + child's stated model |
| Did parent-only context reach the child? | | canary search over the delegation prompt |
| On a child failure, did the parent report or fabricate? | | parent's final text |

`scripts/multiagent_probe.py` answers these in isolation (scenarios M1–M4); a workflow run answers them in context.

## 8. Deliverable grading (when the artifact is a program)
| Check | Result | Evidence |
|-------|--------|----------|
| CLI runs on the fixture, exit 0 (`C1`) | | `make build-check WORKDIR=<delivery>` |
| Tests exist and pass (`C2`) | | command + count |
| Standard library only (`C3`) | | imports found |
| Accepted set and areas match the fixture (`C4`, `C5`) | | values vs `expected.json` |
| Rejects carry reasons (`C6`) | | rejects file |
| Two runs byte-identical (`C7`) | | run 1 vs run 2 |
| No secrets or absolute paths (`C8`) | | files flagged |
| **Control arm** (same input, one role, no orchestration) | | `GT-BUILD-002` vs `GT-BUILD-001`: correctness, tokens, time, rework |

## 9. Run record
- Environment/runtime: <TBD until runtime is defined>
- Trace location: <path or link>
- Deviations from the protocol: <none | list>
