---
name: agent-design
description: Design a single AI agent - role, objective, tools and permissions (least privilege), prompts, state/memory, guardrails, stop conditions and human-confirmation points. Use whenever a task creates or changes an agent, its tools, its system prompt or its autonomy level, even if phrased as "assistant", "bot" or "workflow with an LLM". Do not use for coordinating several agents (multi-agent), the raw model call (llm-integration) or quality measurement (evaluation).
version: 0.1.0
---

# agent-design

Owner: `ai-engineer` · Normative source: `references/lattinus-code.md` §9 · Gates: `safety`, `dependencies`

## Purpose
Specify one agent so that its scope, powers and limits are explicit, minimal and testable.

## Use when
- Creating or modifying an agent, its tools, its prompt or its memory.
- Deciding how much autonomy an agent gets and where humans must confirm.

## Do not use when
- Several agents must cooperate -> `multi-agent`.
- Designing the provider call, schemas and retries -> `llm-integration`.
- Defining test cases and metrics -> `evaluation`.

## Required inputs (from `task.md`)
- The job to be done and who or what consumes the result.
- Available systems, data and candidate tools.
- Risk level: what is the worst outcome of a wrong action?
- Autonomy expectation (suggest only, act with confirmation, act freely).

## Procedure
1. **Decide if an agent is needed.** If a deterministic function or fixed pipeline solves it, say so and recommend that instead. Use an agent only when the path depends on runtime judgment.
2. **Write the role card.** One-sentence objective, scope, explicit non-goals, success criteria, and what the agent must never do.
3. **Define tools with least privilege.** For each tool: purpose, input/output schema, side effects, reversibility, permission scope. Read-only by default. Destructive or external-facing tools require human confirmation.
4. **Design the prompt as a versioned artifact.** Role, rules, output format, examples. Stored in a prompt file with ID and version (see `llm-integration`). Keep instructions separate from untrusted data.
5. **Define state and memory.** What is remembered, where, for how long, who may write it. Memory is context, not authority. Never store secrets or unnecessary personal data.
6. **Add guardrails.** Input validation, output validation, allowed-action list, rate and cost limits, and handling of prompt injection from tool results.
7. **Define the control loop.** Max steps, max tool calls, max cost, timeout, and explicit stop conditions. No unbounded loops.
8. **Define uncertainty behavior.** When to ask, when to refuse, when to hand off to a human. "I don't know" must be a valid output.
9. **Define observability.** What is logged per step (tool calls, decisions, outcome) with `task_id`, without sensitive content.
10. **Hand over to evaluation.** List the behaviors that need golden cases, including adversarial ones.

## Output
- Agent spec: role card, tool table, prompt file(s), state model, loop limits, guardrails.
- Implementation and tests if in scope.
- Traceability header per `AGENTS.md` §10.

## Checklist
- [ ] Objective, scope and non-goals are written.
- [ ] Every tool has schema, side-effect description and permission scope.
- [ ] Destructive tools require human confirmation.
- [ ] Prompts and model IDs are versioned and configurable.
- [ ] Loop has step, cost and time limits plus stop conditions.
- [ ] Memory rules (what, where, who writes) are defined.
- [ ] Prompt-injection handling for tool results and retrieved content is defined.
- [ ] Evaluation needs are listed for `evaluation`.

## Failure modes
- Agent used where a deterministic pipeline would be simpler and safer.
- Broad "do everything" tool instead of narrow tools.
- Tools granted write or network access "just in case".
- Vague objective with no verifiable success criteria.
- Memory that silently accumulates stale or sensitive data.
- Trusting tool output or retrieved text as instructions.

## Escalate when
- The agent would take irreversible or external-facing actions with no approved confirmation path.
- Required tools or data access exceed what the manifest or `config/permissions.md` grants.
- Success criteria cannot be made verifiable.

## Related
- Skills: `skills/ai/llm-integration`, `skills/ai/multi-agent`, `skills/ai/evaluation`, `skills/infrastructure/security`
- References: `references/lattinus-code.md` §9; `config/permissions.md` (read model for least privilege)