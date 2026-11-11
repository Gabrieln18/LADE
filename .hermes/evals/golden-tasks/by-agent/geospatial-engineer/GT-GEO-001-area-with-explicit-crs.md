---
id: GT-GEO-001
target: geospatial-engineer
category: happy
risk: med
review_level: standard
runs: 1
anchors: [lattinus-code §8 (CRS, Geometry validity, Accuracy), §6.2; SOUL §3]
version: 1.0.0
status: active
---

# GT-GEO-001 — Area computation with explicit CRS and justified reprojection

## Input
> Give **only this section** to the agent under test. Never share the sections below (`permissions.md` §3).

User message:

> Compute the area in hectares of these parcels. They are in lon/lat.

`task.md` instance:

```yaml
task_id: LADE-20261111-941
objective: Compute parcel areas (ha) for parcels located in the São Francisco Valley, Brazil.
requester: human:maintainer
assigned_to: geospatial-engineer
review_level: standard
output_language: PT-BR
inputs:
  - data/samples/parcels.geojson (declared CRS: EPSG:4326)
expected_outputs:
  - code
  - tests
  - short method note
acceptance_criteria:
  - Area in hectares per parcel
  - CRS handling explicit and justified
  - Invalid geometries handled by declared behavior
constraints: []
out_of_scope: []
```

## Expected behavior
- Reprojects to a suitable projected CRS (e.g. SIRGAS 2000 UTM 24S, EPSG:31984) or uses a geodesic method, and logs the choice.
- Validates geometries and declares repair/reject/quarantine.
- States accuracy limits and units.

## Must NOT
- Compute area in degrees or silently on EPSG:4326.
- Hide the reprojection.

## Hard checks
All must pass (binary). Any failure = task FAIL.

- [ ] **H1** Input CRS stated as an EPSG code.
- [ ] **H2** Area computed in a projected CRS or geodesically; choice justified.
- [ ] **H3** Reprojection explicit and logged.
- [ ] **H4** Geometry validity checked with declared behavior for invalid input.
- [ ] **H5** Output states units (ha) and rounding/precision limits.
- [ ] **H6** Test with a known-area parcel.

## Rubric
| ID | Criterion | Weight |
|----|-----------|:------:|
| R1 | CRS choice fits region and purpose (accepts any suitable CRS or geodesic) | 30 |
| R2 | Uncertainty/precision stated honestly | 25 |
| R3 | Tests include an invalid geometry | 25 |
| R4 | Method note is brief and clear | 20 |

## Pass criteria
PASS = 100% of Hard checks **and** rubric score ≥ 80/100.
Runs: 1.
