---
name: multi-agent
description: Design coordination between multiple AI agents - topology (supervisor, pipeline, parallel), handoff contracts, shared state, loop and cost limits, partial-failure handling and separation of duties. Use whenever a task involves two or more agents, an orchestrator, delegation, agent-to-agent messages or a review loop, even if the task only says "split this across agents". Do not use for the internal design of one agent (agent-design), the model call (llm-integration) or metrics (evaluation).
version: 0.1.0
---

# multi-agent

Owner: `ai-engineer` · Normative source: `references/lattinus-code.md` §9 · Gates: `safety`, `dependencies`

## Purpose
Define how agents cooperate so that responsibility, state and cost stay explicit and bounded.

## Use when
- A task needs more than one agent or role.
- Defining delegation, routing, handoff or review loops.
- Debugging coordination failures (loops, lost context, conflicting outputs).

## Do not use when
- Designing one agent's role, tools or prompt -> `agent-design`.
- Designing provider calls -> `llm-integration`.
- Measuring quality -> `evaluation`.

## Required inputs (from `task.md`)
- The end-to-end goal and its acceptance criteria.
- Candidate agents or roles and their permissions.
- Latency, cost and risk constraints.
- Where humans must approve.

## Procedure
1. **Justify the split.** State why one agent is not enough (distinct permissions, separation of duties, parallelism, context size). If there is no reason, recommend a single agent.
2. **Choose the topology** and record the trade-off:
   - *Pipeline*: fixed order, simple, easy to audit.
   - *Supervisor/orchestrator*: dynamic routing, one accountable coordinator.
   - *Parallel fan-out/fan-in*: independent subtasks, needs a merge rule.
   Prefer the simplest that meets the goal. Avoid free-form agent-to-agent chatter.
3. **Define handoff contracts.** Every handoff has a typed message: task id, objective, inputs, expected output schema, acceptance criteria, constraints, out of scope. Sub-agents start with zero context, so the message must be self-sufficient.
4. **Define shared state.** Single owner per piece of state, explicit write rules, no hidden shared memory. State carries `task_id` and version.
5. **Enforce separation of duties.** An agent never approves its own output; reviewers do not modify what they review; permissions are not widened by delegation.
6. **Bound the system.** Max delegation depth, max total steps, max review cycles, global cost and time budget, and cycle detection. On limit reached: stop and escalate to a human.
7. **Handle partial failure.** Define behavior for timeout, invalid output, missing agent and conflicting results: retry limit, fallback, or escalate. Never continue silently with partial results.
8. **Define the merge rule** for parallel outputs (who decides on conflict, what is discarded, what is escalated).
9. **Make it observable.** Trace each handoff (from, to, task id, outcome, cost) for audit and replay.
10. **Hand over to evaluation.** Define end-to-end golden cases plus failure-injection cases.

## Output
- Coordination spec: topology diagram, handoff schemas, state ownership table, limits, failure matrix.
- Implementation and tests if in scope.
- Traceability header per `AGENTS.md` §10.

## Checklist
- [ ] Split is justified; simpler alternative considered.
- [ ] Topology chosen and trade-off recorded.
- [ ] Handoff schemas exist and are self-sufficient.
- [ ] Every state item has one owner and write rules.
- [ ] Separation of duties holds; no self-approval.
- [ ] Depth, step, review-cycle, cost and time limits are set.
- [ ] Partial-failure and conflict behavior is defined.
- [ ] Handoffs are traced; end-to-end evaluation needs are listed.

## Failure modes
- More agents than the problem needs, multiplying cost and error.
- Handoffs with implicit context that the receiver does not have.
- Unbounded review or delegation loops.
- Agents rewriting each other's artifacts without an owner.
- Errors compounding silently across hops.
- One failing sub-agent causing a confident but wrong final result.

## Escalate when
- Limits are reached, or agents produce conflicting outputs the merge rule cannot resolve.
- The design requires an agent to exceed its permissions or remove a separation of duties (needs an ADR).
- Accountability for an irreversible action is unclear.

## Related
- Skills: `skills/ai/agent-design`, `skills/ai/evaluation`, `skills/architecture/adr`
- References: `references/lattinus-code.md` §9; `AGENTS.md` §6, §8.2 (LADE's own handoff and review-loop model as a worked example)