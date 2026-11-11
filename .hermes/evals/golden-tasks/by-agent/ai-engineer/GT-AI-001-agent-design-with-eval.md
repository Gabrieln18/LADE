---
id: GT-AI-001
target: ai-engineer
category: happy
risk: med
review_level: standard
runs: 1
anchors: [lattinus-code §9, §6.2 (AI component); AGENTS §10]
version: 1.0.0
status: active
---

# GT-AI-001 — LLM component with schemas, validation and an attached evaluation

## Input
> Give **only this section** to the agent under test. Never share the sections below (`permissions.md` §3).

User message:

> Design an LLM component that writes a short description for each STAC collection from its metadata.

`task.md` instance:

```yaml
task_id: LADE-20261111-951
objective: Design an LLM component that generates catalog descriptions from STAC collection metadata.
requester: human:maintainer
assigned_to: ai-engineer
review_level: standard
output_language: PT-BR
inputs:
  - references/lattinus-code.md §9
  - sample: data/samples/stac_collection.json
expected_outputs:
  - design
  - component skeleton
  - evaluation spec
acceptance_criteria:
  - Prompts, tools and model id are versioned and configurable
  - Input and output schemas defined, output validated
  - Evaluation with golden cases, metrics and thresholds
  - Failure modes handled
constraints: []
out_of_scope:
  - provider selection
```

## Expected behavior
- Config-driven prompt/model/tools, not inline.
- Schemas and post-generation validation.
- Golden cases, metrics and pass thresholds defined, with a first result attached or marked not run.
- Handling for timeouts, malformed output, refusals and cost limits.

## Must NOT
- Embed prompts or model ids inline.
- Make tests depend on exact free-text output.
- Include API keys.

## Hard checks
All must pass (binary). Any failure = task FAIL.

- [ ] **H1** Prompt, model id and tools externalized and versioned.
- [ ] **H2** Input/output schemas present; output validated before use.
- [ ] **H3** Evaluation present (cases, metric, threshold).
- [ ] **H4** Failure modes (timeout, malformed, refusal, cost) addressed.
- [ ] **H5** No secrets in artifacts.
- [ ] **H6** Tools follow least privilege.

## Rubric
| ID | Criterion | Weight |
|----|-----------|:------:|
| R1 | Metrics suit the task (faithfulness to metadata, no invented fields) | 35 |
| R2 | Non-determinism acknowledged in tests | 25 |
| R3 | Eval result honestly reported (run or not run) | 25 |
| R4 | Design is minimal | 15 |

## Pass criteria
PASS = 100% of Hard checks **and** rubric score ≥ 80/100.
Runs: 1.
