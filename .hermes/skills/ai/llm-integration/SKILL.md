---
name: llm-integration
description: Design and implement the boundary between Lattinus code and an LLM provider - model configuration, prompt versioning, input/output schemas with validation, retries, timeouts, cost limits, refusal and malformed-output handling, and data privacy. Use whenever a task adds or changes a model call, a prompt, a structured-output parser or a provider client, even if the task does not say "LLM integration". Do not use for agent behavior (agent-design), agent coordination (multi-agent) or measuring quality (evaluation).
version: 0.1.0
---

# llm-integration

Owner: `ai-engineer` · Normative source: `references/lattinus-code.md` §9 · Gates: `safety`, `dependencies`

## Purpose
Make every model call explicit, configurable, validated and bounded, so the rest of the system treats the LLM as an untrusted, non-deterministic component.

## Use when
- Adding or changing a model call, prompt, parser or provider client.
- Choosing or changing a model ID, temperature or token limits.
- Defining what data may be sent to an external provider.

## Do not use when
- Defining an agent's role, tools or stop rules -> `agent-design`.
- Coordinating several agents -> `multi-agent`.
- Defining quality metrics or golden cases -> `evaluation`.

## Required inputs (from `task.md`)
- Purpose of the call and the consumer of its output.
- Provider/runtime constraints (if the runtime is `TBD`, stay provider-agnostic and declare it as an assumption).
- Data classification of what goes into the prompt.
- Latency, cost and availability expectations.

## Procedure
1. **Define the contract.** Write input and output schemas (typed models or JSON Schema). Free text is allowed only when the consumer is a human.
2. **Isolate the client.** One thin adapter per provider behind an internal interface. Business code MUST NOT import a provider SDK directly.
3. **Externalize configuration.** Model ID, version, temperature, max tokens, timeout and retry policy live in configuration, never inline. Prompts live in versioned files with an ID and version, not in code strings.
4. **Compose prompts safely.** Separate instructions from data. Treat retrieved or user-supplied content as untrusted (prompt injection). Never concatenate secrets.
5. **Validate every output.** Parse, then validate against the schema before use. On failure: bounded retry with the validation error as feedback, then a defined fallback or explicit error. Never pass unvalidated output downstream.
6. **Bound execution.** Set timeouts, max retries with backoff and jitter, max tokens, and a per-task and per-run cost ceiling. Retry only on transient errors (timeouts, rate limits, 5xx), never on refusals or schema failures beyond the declared limit.
7. **Handle refusals and empties.** Detect refusal, truncation (stop reason) and empty output as distinct, logged outcomes.
8. **Protect data.** Send the minimum data needed. Redact personal data and secrets. Sending sensitive data to an external provider requires an approved policy (`safety` gate + human).
9. **Log without leaking.** Structured logs with `task_id`/request id, model ID, prompt version, token counts, latency, outcome. No prompt or response bodies containing sensitive data.
10. **Test without the network.** Unit tests use a fake adapter with recorded or synthetic responses. Do not assert on exact free-text output.
11. **Run the gates.** `dependencies` for any new SDK or library; `safety` for external calls.

## Output
- Adapter, schemas, prompt files and configuration, plus tests.
- Short design note: contract, failure behavior, cost/latency assumptions.
- Traceability header per `AGENTS.md` §10.

## Checklist
- [ ] Model ID, prompt and parameters are versioned and configurable.
- [ ] Input and output schemas exist; outputs validated before use.
- [ ] Timeouts, retry limits and cost ceilings set.
- [ ] Timeout, malformed output, refusal and truncation have defined behavior.
- [ ] No sensitive data sent externally without approved policy.
- [ ] No secrets in code, prompts, logs or fixtures.
- [ ] Tests run offline and do not depend on exact wording.
- [ ] New dependencies passed the `dependencies` gate and human approval.

## Failure modes
- Prompts or model IDs hard-coded in business logic.
- Parsing with regex on free text instead of schema validation.
- Unbounded retries or loops that multiply cost.
- Logging full prompts that contain user or personal data.
- Treating model output as trusted input to tools, SQL, shell or file paths.
- Assuming one provider's features (tool calling, JSON mode) exist everywhere without an adapter.

## Escalate when
- The call needs sensitive data sent to an external provider and no policy exists.
- Cost or latency requirements cannot be met within the declared limits.
- The needed provider, SDK or runtime is not decided (`TBD`) and no safe assumption exists.

## Related
- Skills: `skills/ai/agent-design`, `skills/ai/evaluation`, `skills/software-engineering/api-design`, `skills/infrastructure/security`
- References: `references/lattinus-code.md` §9, §10; `agents/ai-engineer/references/ai-engineering.md` (record in `memory/open-questions.md` if missing)