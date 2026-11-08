<!--
templates/runbook.md · v0.1.0 · Used by: skills/documentation/repository-docs
Contract: references/lattinus-code.md §6.2 (Data pipeline, Infrastructure) and §11 (Observability and Operability).
- A runbook documents how to operate a service, job or pipeline. It does not define architecture (ARQ) or contracts (IF/EVT).
- Every command must be verified in the repository or labeled `unverified`.
- NEVER write secret values, tokens or internal credentials. Reference the secret mechanism by name.
- Remove this comment and add the traceability header (AGENTS.md §10) as an HTML comment.
-->

# Runbook — {{COMPONENT_NAME}}

| Field | Value |
|-------|-------|
| ID | {{DOCUMENT_ID_OR_NONE}} |
| Status | {{Draft \| Proposed \| Accepted}} |
| Owner | {{OWNER}} |
| Last review | {{DATE}} |
| Version | {{VERSION}} |
| Related | {{ARQ_IF_STK_IDS}} |

## 1. Purpose and scope

{{WHAT_THIS_COMPONENT_DOES_AND_WHEN_THIS_RUNBOOK_APPLIES}}

**Out of scope:** {{OUT_OF_SCOPE}}

## 2. Prerequisites

| Item | Detail |
|------|--------|
| Access | {{ROLES_OR_PERMISSIONS_NEEDED}} |
| Secrets | {{SECRET_MECHANISM_NAME_ONLY}} |
| Tools | {{TOOLS_AND_VERSIONS}} |
| Inputs | {{DATA_OR_CONFIG_REQUIRED}} |

## 3. Run

```bash
{{RUN_COMMAND}}
```

- Expected result: {{SUCCESS_CONDITION}}
- Idempotency: {{SAFE_TO_RERUN_YES_OR_NO_AND_WHY}}

## 4. Monitor

| Signal | Where | Healthy | Alert when |
|--------|-------|---------|------------|
| {{METRIC_OR_LOG}} | {{LOCATION}} | {{NORMAL_RANGE}} | {{THRESHOLD_OR_TBD}} |

For pipelines include: success and failure counts, data volume, freshness, data-quality check results.

## 5. Retry

| Failure | Retry safe? | Procedure |
|---------|-------------|-----------|
| {{FAILURE}} | {{YES_OR_NO}} | {{STEPS}} |

Behavior on partial failure: {{WHAT_IS_COMMITTED_WHAT_IS_NOT}}

## 6. Backfill <!-- required for pipelines; otherwise remove -->

1. {{DETERMINE_RANGE_AND_PARAMETERS}}
2. {{RUN_BACKFILL_COMMAND}}
3. {{VALIDATE_OUTPUT_QUALITY_CHECKS}}

Constraints: {{LIMITS_RATE_COST_OVERWRITE_BEHAVIOR}}

## 7. Rollback

1. {{DECIDE_ROLLBACK_CRITERIA}}
2. {{ROLLBACK_STEPS}}
3. {{VERIFY_SYSTEM_CONSISTENT}}

Point of no return: {{IRREVERSIBLE_STEPS_OR_NONE}}

## 8. Known failure modes

| Symptom | Likely cause | Action |
|---------|--------------|--------|
| {{SYMPTOM}} | {{CAUSE}} | {{ACTION}} |

## 9. Escalation

| Condition | Contact or channel |
|-----------|--------------------|
| {{CONDITION}} | {{OWNER_OR_CHANNEL}} |

## 10. Change record

| Date | Version | Change | Approval |
|------|---------|--------|----------|
| {{DATE}} | {{VERSION}} | {{CHANGE}} | {{APPROVAL_REFERENCE}} |