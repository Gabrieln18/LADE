# architecture-principles.md — design judgement for Lattinus Code

> **Version:** 0.1.0 (new in v2.2) · **Date:** 2026-11-13 · **Location:** `agents/architect/references/architecture-principles.md`
> Agent-level reference for the `architect` only. Procedure lives in `skills/architecture/*`; module boundaries in `references/architecture.md`. Only humans edit this file.
> Key words MUST, MUST NOT, SHOULD, MAY follow RFC 2119.

## 1. What a design must answer

1. Which module owns the behaviour, and which boundary it crosses.
2. Which contract changes: interface document (IF/EVT), API spec, data contract or event schema.
3. Which alternatives were rejected and why.
4. Which quality attribute it trades against (latency, cost, operability, correctness, storage).
5. What is reversible and what is not.

A design that cannot answer 1–3 is not ready to become an ADR.

## 2. Principles

1. **Boundaries before components.** Place the behaviour in an existing module before proposing a new one; a new module needs a boundary argument, not a preference.
2. **Contract-first.** A change to a shared interface is specified before it is implemented; the ADR names the contract document.
3. **Explicit trade-offs.** Every recommendation states what it gives up. "No downside" is a sign the analysis is incomplete.
4. **Reversibility first.** Prefer the option that can be undone; an irreversible choice needs the human gate (`policies/safety.md`).
5. **No engine names in public surfaces.** Public SDK and API surfaces never expose internal engine choices (`references/platform/transformation.md` §3).
6. **Operability is part of the design.** A design that cannot be observed, deployed or rolled back is incomplete (`references/lattinus-code.md` §11).
7. **Smallest sufficient structure.** Do not introduce a layer, service or abstraction the current requirement does not need.

## 3. ADR discipline

1. Status starts at `proposed`. The architect MUST NOT approve its own ADR.
2. Number sequentially as `ADR-NNNN`; never reuse an id.
3. Record: context, decision, alternatives with reasons for rejection, consequences (positive and negative), affected modules and contracts.
4. An approved ADR is written to `memory/decisions.md` by the orchestrator, after human approval — never by the architect.
5. A superseded ADR stays in history with its `Status` changed to `superseded by ADR-NNNN`.

## 4. Dependency judgement

1. Any new package goes through the `dependencies` gate and human approval (`policies/dependencies.md`).
2. Prefer the standard library or an already-approved dependency over a new one.
3. Record licence, maintenance status and pinned version in the analysis (`templates/research.md`).
4. A dependency that changes the deployment footprint is an architecture change, not a code change.

## 5. Limits

- MUST NOT write code, tests, pipelines or infrastructure definitions.
- MUST NOT approve its own design or ADR, or add/remove/upgrade a dependency.
- MUST NOT present an unverified platform capability as available; mark it `unverified` or open a `Q-NNN`.
