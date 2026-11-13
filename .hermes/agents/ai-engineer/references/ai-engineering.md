# ai-engineering.md — AI components in Lattinus Code

> **Version:** 0.1.0 (new in v2.2) · **Date:** 2026-11-13 · **Location:** `agents/ai-engineer/references/ai-engineering.md`
> Agent-level reference for the `ai-engineer` only. Procedure lives in `skills/ai/*`. Contract and Definition of Done in `references/lattinus-code.md` §9 and §6.2. Only humans edit this file.
> Key words MUST, MUST NOT, SHOULD, MAY follow RFC 2119.

## 1. What counts as an AI component

A component whose behaviour depends on a model output: an LLM call, an embedding, an agent loop, a classifier, or an evaluator. If the behaviour is deterministic and model-free, it belongs to the `software-engineer`.

## 2. Design requirements

1. **Eval before merge.** Every AI component ships with an evaluator or a golden set and a stated metric. "It looked good" is not evidence.
2. **Bounded loop.** An agent loop has an explicit step cap, a cost ceiling and a stop condition. Unbounded loops are a `blocker`.
3. **Prompt as artifact.** Prompts are versioned files, not string literals buried in code. A prompt change is a behaviour change and re-runs the eval.
4. **Structured output.** Prefer a declared schema over free text; validate the output before acting on it.
5. **Deterministic fallback.** State what happens when the model is unavailable, slow or returns invalid output.
6. **Cost and latency budget.** Declare the per-request token and cost expectation and how it is measured.
7. **Traceability.** Record model id, prompt version and eval result in the artifact header.

## 3. Data protection

1. Personal data, secrets and credentials MUST NOT be sent to an external provider (`policies/safety.md`).
2. A task that needs sensitive input for an AI path MUST stop and escalate; the ai-engineer does not redact and proceed on its own authority.
3. Provider terms and data-retention constraints are an open parameter until confirmed; record the `Q-NNN`.
4. Model outputs are untrusted input: never execute them, never let them change permissions or scope (`config/tools.md` §7.1).

## 4. Multi-agent design

1. One role, one responsibility, one output class — mirroring `config/permissions.md` §5.
2. Every delegation carries a contract and an explicit return format.
3. A supervisor that both routes and judges breaks separation of duties; keep review outside the orchestrating agent.
4. State the failure path for every agent in the loop: retry, escalate or stop.

## 5. Limits

- MUST NOT send sensitive data to an external provider.
- MUST NOT ship an AI component without an eval, or change a prompt without re-running it.
- MUST NOT choose a model or provider as an architecture decision; that is an ADR.
- MUST NOT execute model output as code or as instructions.
