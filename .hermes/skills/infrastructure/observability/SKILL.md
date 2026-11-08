---
name: observability
description: Define telemetry conventions and operational artifacts for Lattinus modules using OpenTelemetry. Covers structured logging, metrics, traces, health/readiness, pipeline metrics (success, failure, volume, freshness), OTel Collector configuration, SLI/SLO definitions, alert rules as code, and runbooks. Use this skill whenever a task adds or changes a service, pipeline, job or edge deployment, or mentions logs, metrics, tracing, monitoring, alerting, SLOs, runbooks or "how will we know it works in production", even if observability is not named.
---

# observability

> **Version:** 0.1.0 (bootstrap) · **Date:** 2026-11-08 · **Owner agent:** `devops-sre` · **Category:** `skills/infrastructure/`
> Key words MUST, MUST NOT, SHOULD, MAY follow RFC 2119.

## 1. Scope

**Covers:** telemetry conventions, Collector configuration, backend-facing definitions, health signals, SLI/SLO, alerts as code, runbooks, edge profile.

**Does not cover:** choosing the backend (ADR via `architect`), writing instrumentation inside business logic (`software-engineer` / `data-engineer`, delegated through `task.md`), dataset lineage (owned by the data-domain layers; telemetry only provides correlation identifiers).

## 2. Provisional Lattinus baseline

Source: Notion Lattinus, Platform Observability 2.0, OBS-STK-001 (**Draft**, 2026-09-14). Cite as `unverified` until promoted to `references/`.

- OpenTelemetry is the instrumentation and transport standard (OTLP gRPC/HTTP). The OTel Collector is the preferred vendor-neutral gateway.
- Backend candidates (initial, **not commitments**): Prometheus or Mimir (metrics), Loki (logs), Tempo (traces), Grafana (visualization).
- The backend is replaceable and MUST NOT become a mandatory dependency for domain execution.
- Application code uses the Lattinus observability abstraction where available. Backend-specific clients live only at the infrastructure boundary.
- OTel configuration is injected via environment or config, never hard-coded in domain modules.
- Edge profile: collector plus selected local backends, with configurable sampling and retention.

## 3. Inputs (from `task.md`)

Component and workload type, runtime profile (cloud or edge), signals required, existing SLOs if any, consumers of the alerts.

## 4. Procedure

1. **Choose signals per workload.** Services: logs, RED metrics (rate, errors, duration), traces. Pipelines and jobs: logs, run metrics, traces per stage.
2. **Logs.** Structured (JSON), UTC timestamp, level, service name, `trace_id`, `span_id`, and `task_id` or request id for correlation. No secrets, personal data, raw parcel geometries or producer identifiers.
3. **Metrics.** Naming follows OpenTelemetry semantic conventions. Labels are low-cardinality: never parcel ids, user ids or free text. Pipeline minimum set: runs by status, run duration, records/bytes processed, assets produced, data freshness (age of newest output), quality-check failures.
4. **Traces.** One span per pipeline stage or request hop. Propagate context across HTTP and queues. Record dataset or asset identifiers as span attributes only if they are not sensitive.
5. **Fail-open telemetry.** Exporter or collector failure MUST NOT fail the workload. Buffers are bounded; drops are counted.
6. **Health.** Services: liveness and readiness signals (readiness reflects dependencies the service truly needs, not the telemetry backend). Jobs: success/failure signal plus last-success timestamp.
7. **Collector definition.** Receivers (OTLP), processors (memory limiter, batch, attribute redaction), exporters per signal. Backends are parameters, not constants. A backend decision goes to an ADR.
8. **SLI/SLO.** For each user-facing service or critical pipeline propose: SLI definition, measurement window, target, error-budget policy. Targets are proposals for human approval.
9. **Alerts as code.** Symptom-based (user or data impact), each with severity, owner, and a runbook link. No alert without an action. Avoid per-cause alerts that duplicate a symptom alert.
10. **Edge profile.** Document footprint, sampling, retention and behavior when the uplink is down (local buffering limits).
11. **Runbook** (`lattinus-code.md` §11): how to run, monitor, retry, backfill and roll back; behavior on partial failure and on retries (idempotency).
12. **Validate statically.** Collector config validation and alert-rule lint using the project's chosen tools (declare them). Add or confirm a test showing the workload runs with telemetry disabled.

## 5. Delegations (do not perform; request via Orchestrator)

- Instrumentation code in services or pipelines: `software-engineer`, `data-engineer`, `geospatial-engineer`.
- Backend selection or any change of the telemetry contract: `architect` (ADR).
- New telemetry packages: `dependencies` gate plus human approval.

## 6. Deliverable checklist (`lattinus-code.md` §6.2, §11)

- [ ] Logs, metrics and traces conventions stated and consistent with OpenTelemetry.
- [ ] Health/readiness defined for services; success/failure/volume metrics for pipelines.
- [ ] Collector and alert definitions reproducible from code.
- [ ] Fail-open behavior stated and tested or marked unverified.
- [ ] SLI/SLO proposals marked as pending approval.
- [ ] Runbook covers run, monitor, retry, backfill, rollback, partial failure.
- [ ] No sensitive data in any telemetry field.
- [ ] Backend choice either referenced to an approved ADR or declared as an assumption.

## 7. Guardrails

- MUST NOT write to or reconfigure live observability backends. Produce definitions only.
- MUST NOT hard-code endpoints, tokens or tenant ids.
- MUST NOT make telemetry a hard dependency of domain execution.
- MUST NOT use observability data as lineage of record.
- Network use only on hosts allowlisted in `config/tools.md`.

## 8. Escalate when

- A backend must be fixed to proceed (needs ADR).
- Cardinality or volume would exceed what the declared backend or edge device can hold.
- Required instrumentation is missing in code and cannot be delegated within the task.
- A telemetry field would carry personal or producer data with no approved policy.

## 9. References

- `references/lattinus-code.md` §3 (OpenTelemetry), §7.4, §11
- Notion Lattinus: Platform Observability 2.0 (OBS-OVW-001, OBS-ARQ-001, OBS-STK-001). Status Draft. Promote to `references/` (human action).