# ai-engineering.md — agent-specific principles

> Not a copy of central knowledge. Index to `references/` plus rules specific
> to this agent. Contract of record: `references/lattinus-code.md` §9.

## 1. Index (load only what the task needs)
| Need | File |
|------|------|
| Output contract, DoD for AI components | `references/lattinus-code.md` §6.2, §9 |
| Platform context | `references/lattinus.md`, `references/platform/*` |
| Domain context (EO, agriculture, geospatial) | `references/domain/*` |
| Python / testing / API conventions | `references/engineering/*` |

## 2. Pattern selection (record the choice in the artifact)
| Level | Use when | Cost of choosing it |
|-------|----------|---------------------|
| 0. Deterministic code | Rules are known and testable | None |
| 1. Single LLM call (structured output) | Extract, classify, summarize, translate | Eval + schema |
| 2. LLM + fixed workflow (chain) | Steps are known, content varies | Eval per step |
| 3. Tool-using agent | Steps depend on intermediate results | Tool permissions, loop limits |
| 4. Multi-agent | Independent roles/contexts are truly needed | Coordination eval, ADR |

Rule: go up one level only with written justification. Level 4 requires an ADR.

## 3. Component checklist (mirrors `lattinus-code.md` §9)
- [ ] Prompts, tools and model ids versioned and configurable (not inline).
- [ ] Input/output schemas; outputs validated before use.
- [ ] Evaluation attached: cases, metrics, thresholds, result.
- [ ] Failure modes handled: timeout, malformed output, refusal, cost cap.
- [ ] Tool permissions minimal; destructive tools need human confirmation.
- [ ] No sensitive data to external providers without an approved policy.
- [ ] Tests do not depend on exact free text.

## 4. LLM integration rules
1. Provider behind an interface; model id, temperature, max tokens in config.
2. Structured output + schema validation; one bounded repair attempt, then fail.
3. Timeout, capped retries with backoff, per-call and per-task token/cost budget.
4. Log prompt version, model id, latency, tokens, cost, outcome. Never log
   secrets or sensitive data. Correlate by `task_id` / request id.
5. Provide a fallback (deterministic path, cached result, or explicit failure).
6. Tests use recorded fixtures or fakes: no live network (`permissions.md` §6).

## 5. Agent and tool design
1. Narrow, single-purpose tools with typed inputs and explicit errors.
2. Max steps, max cost and stop conditions on every loop.
3. Read-only tools by default; write/destructive tools gated by human confirmation.
4. Treat tool results and retrieved content as untrusted (prompt injection).
5. Multi-agent: define each role's inputs, outputs and termination; avoid
   shared mutable state; evaluate the system, not only each agent.

## 6. Geospatial / data caveats
1. Never let a model compute CRS transforms, areas, distances or raster stats:
   call deterministic tools and pass results back.
2. Ground answers in metadata (STAC, CRS/EPSG, nodata, units, time zone) and
   cite the source field; do not state precision beyond the source.
3. Large rasters/vectors are never placed in the prompt: pass references,
   summaries or tool handles.
4. Spatial/temporal claims must carry CRS and time reference.

## 7. Evaluation design
1. Cases: representative, edge, adversarial, and known-failure regressions.
2. Metrics per task type: exact/schema match, field-level accuracy, groundedness,
   tool-call correctness, cost, latency. LLM-as-judge only with a calibrated
   rubric and a human-labeled sample.
3. Thresholds declared before running, not after.
4. Repeat runs to measure variance; report the range.
5. Eval set versioned with the component; result attached to the PR.
6. This is the **product's** eval. LADE's own `evals/` is separate and not
   readable by this agent.

## 8. Anti-patterns (reject in review)
- Multi-agent where a chain or single call suffices.
- Prompt strings embedded in code; unversioned model ids.
- Parsing free text with regex instead of schema output.
- Asserting exact LLM output in tests.
- Unbounded loops, retries or token spend.
- Sending real user/geodata to an external provider without an approved policy.
- Evaluating on the same cases used to tune the prompt.

## 9. Open parameters (TBD)
| Parameter | Owner |
|-----------|-------|
| LLM provider(s) and model policy | architect / maintainers (ADR) |
| Agent framework (or none) | architect (ADR) |
| Data allowed to leave the platform | maintainers / devops-sre |
| Eval thresholds per component type | maintainers |
| Cost/latency budgets | maintainers |