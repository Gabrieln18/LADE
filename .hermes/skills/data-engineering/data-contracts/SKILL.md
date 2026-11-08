---
name: data-contracts
description: Define, review or version a data contract (schema, semantics, owner, SLA, compatibility rules) for any dataset, table, file or payload exchanged between components. Use whenever a task creates or changes a dataset interface, adds/renames/removes a field, changes units, CRS or nodata, or when ingestion, pipelines or data-quality need a contract to build against, even if the task never says "contract".
owner: data-engineer
version: 0.1.0
---

# data-contracts

## 1. When to use / When NOT to use
Use: new dataset interface, schema change, unit/CRS/nodata change, ownership or SLA definition, compatibility review.
Do NOT use: for runtime checks (`data-quality`), data movement (`ingestion`, `pipelines`) or engine tuning (`processing/*`).

## 2. Required inputs (task.md)
- Dataset name, producer, known consumers.
- Sample data or source schema.
- Existing contract (if changing one) and the reason for the change.
- Output language for the human-readable summary (default PT-BR).

## 3. Procedure
1. Check whether a contract already exists. If yes, start from it and classify the change (step 6).
2. Fill the contract template (section 4). Every field needs type, nullability and description. Missing facts become declared assumptions, never silent guesses.
3. For spatial data, declare CRS (EPSG), geometry type and validity rule. For rasters: resolution, extent, nodata, dtype, units, scale/offset, band semantics, resampling.
4. For temporal data, declare time zone (UTC by default), acquisition vs processing time, temporal resolution.
5. Declare SLA (freshness, completeness) and the `data-quality` rules that verify it. Reference rules by id; do not define checks here.
6. Classify the change and bump the version (section 5).
7. Define validation points: on input and on output of every producer.
8. If the contract standard is not yet decided (ODCS or other, see lattinus-code §14), keep the template ODCS-aligned and flag the open decision.

## 4. Contract template (minimum)
```yaml
id: <dataset-id>
version: <semver>
owner: <team-or-person>
description: <what it represents>
source: {origin: <...>, license: <...>, attribution: <...>}
schema:
  - {name: <field>, type: <type>, nullable: <bool>, unit: <unit|none>, description: <...>, constraints: <...>}
keys: {primary: [<field>], partition: [<field>]}
spatial: {crs: <EPSG:xxxx|n/a>, geometry: <type|n/a>, validity: <rule>}
raster: {resolution: <...>, nodata: <...>, dtype: <...>, units: <...>, resampling: <...>}   # if applicable
temporal: {timezone: UTC, resolution: <...>, time_field: <acquisition|processing>}
sla: {freshness: <...>, completeness: <...>}
quality_rules: [<data-quality rule ids>]
compatibility: <backward|forward|full|none>
changelog: [{version: <...>, change: <...>, breaking: <bool>}]
```

## 5. Versioning (SemVer)
| Change | Class | Bump |
|--------|-------|------|
| Add optional field; add doc; widen a type | Compatible | minor/patch |
| Remove or rename field; narrow type; make nullable field required | Breaking | major |
| Change unit, CRS, nodata, key or semantics of a field | Breaking | major |
| Add enum value | Compatible for producers, check consumers | minor |

Breaking changes require an ADR (human approval before implementation), a migration path and a deprecation window.

## 6. Standards
- `lattinus-code.md` §3 (ODCS or declared equivalent, EPSG, STAC) and §8 (geospatial metadata).
- Field names: lowercase `snake_case`. Units explicit, preferably SI.
- No secrets or personal data in examples.

## 7. Outputs
Contract file, change classification, migration notes (if breaking), traceability header (`AGENTS.md` §10).

## 8. Gates triggered
- Documentation: always (contract is documentation).
- Dependencies: if a contract tool or validator library is proposed.
- Git: before commit.

## 9. Done checklist
- [ ] All template fields present or explicitly `n/a` with reason.
- [ ] Owner and consumers named.
- [ ] CRS/units/nodata/time zone declared where applicable.
- [ ] Change classified and version bumped.
- [ ] Quality rules referenced by id.
- [ ] ADR requested if breaking.

## 10. Escalate when
- Source schema is unknown and no sample exists.
- A breaking change affects consumers outside the task.
- Ownership is unclear.

## 11. Anti-patterns
Schema inferred from one sample only; implicit units; "TBD" without owner; breaking change shipped as minor; duplicating quality rules inside the contract.

## 12. References (pointers only)
`references/engineering/data.md`, `references/domain/geospatial.md`, `references/lattinus-code.md`.
If a file is missing, record the gap in `memory/open-questions.md`; do not invent content.