---
name: evaluation
description: Design, implement and report evaluations for AI components - golden cases, metrics, pass thresholds, regression checks across prompt/model versions, adversarial cases and careful use of LLM-as-judge. Use whenever a task delivers or changes an agent, prompt, model or LLM integration, or asks to "test", "benchmark" or "measure" AI behavior, since an AI component is not done without an evaluation result. Do not use to write LADE's own golden tasks in evals/golden-tasks/ (human-only) or for ordinary unit tests of deterministic code (testing).
version: 0.1.0
---

# evaluation

Owner: `ai-engineer` · Normative source: `references/lattinus-code.md` §9 · Gates: `safety`, `dependencies`

## Purpose
Produce evidence that an AI component meets its acceptance criteria and does not regress, accepting that outputs are non-deterministic.

## Use when
- Delivering or changing an agent, prompt, model or LLM integration.
- Comparing prompt or model versions.
- Defining or reporting pass thresholds for an AI component.

## Do not use when
- Writing or editing `evals/golden-tasks/` (humans only; propose cases as text).
- Testing deterministic code -> `skills/software-engineering/testing`.

## Required inputs (from `task.md`)
- Behavior to be evaluated and acceptance criteria.
- Access to representative or synthetic data (no sensitive data without approval).
- Versions under test (prompt ID, model ID, config).
- Risk level, which sets how strict the thresholds are.

## Procedure
1. **Define what "good" means.** Translate acceptance criteria into measurable properties: correctness, schema validity, groundedness, safety, refusal behavior, latency, cost.
2. **Build the case set.** Cover: typical cases, edge cases, adversarial cases (prompt injection, malformed input, out-of-scope requests) and known past failures. Label expected outcomes. Keep cases versioned and free of secrets or personal data.
3. **Prefer objective checks.** Schema validation, exact or structured matches, tool-call assertions, rule-based checks. Use them before any model-based grading.
4. **Use LLM-as-judge carefully.** Only for properties that cannot be checked objectively. Use a rubric with explicit criteria, a judge model different from the one under test when possible, and calibrate on a human-labeled sample. Record judge model and prompt version. Never use a judge as the sole gate for high-risk behavior.
5. **Handle non-determinism.** Fix configuration and seeds where supported; run multiple trials for stochastic behavior; report rate and spread, not a single run.
6. **Set thresholds before running.** Declare pass thresholds per metric, and which failures are blocking (for example any safety failure). Do not tune thresholds to the result.
7. **Run regression.** Compare against the previous version on the same cases. A change in prompt, model or tools triggers a re-run.
8. **Evaluate failure behavior.** Timeouts, malformed output, refusals, cost limit hits.
9. **Report.** Versions, case counts, metrics, thresholds, failures with examples, known limits and unverified areas. Attach to the PR as evidence.
10. **Keep the harness offline-capable** where possible, with recorded outputs for CI. Network-dependent runs are marked and isolated.

## Output
- Case set, harness/script, results report (metrics vs thresholds, failures, limits).
- Proposed additions to LADE golden tasks, as text, when relevant.
- Traceability header per `AGENTS.md` §10.

## Checklist
- [ ] Criteria are translated into metrics with thresholds set before the run.
- [ ] Cases include typical, edge, adversarial and past-failure cases.
- [ ] Objective checks come first; judge use is justified and calibrated.
- [ ] Multiple trials or fixed config; spread reported.
- [ ] Regression compared against the previous version.
- [ ] Failure-mode behavior evaluated.
- [ ] Versions (prompt, model, judge) recorded in the report.
- [ ] No secrets or personal data in cases or reports; limits stated honestly.

## Failure modes
- Evaluating on the same examples used to craft the prompt (overfitting).
- A single run presented as a result for a stochastic system.
- Judge model grading its own outputs with no calibration.
- Thresholds adjusted after seeing results.
- Only happy-path cases; no adversarial or out-of-scope cases.
- Reporting an aggregate score that hides a blocking failure.

## Escalate when
- Thresholds cannot be met and the acceptance criteria need a human decision.
- Representative data is unavailable and synthetic data would be misleading.
- A safety-relevant failure is found.

## Related
- Skills: `skills/ai/agent-design`, `skills/ai/multi-agent`, `skills/ai/llm-integration`, `skills/software-engineering/testing`
- References: `references/lattinus-code.md` §6.2, §9; `evals/README.md` (LADE's own golden-task conventions, read-only)