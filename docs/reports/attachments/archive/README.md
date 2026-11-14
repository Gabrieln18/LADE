# Attachments — archive

Historical development attachments. **Nothing here is meant to be applied.**

| File | Origin | Why it is archived |
|---|---|---|
| `setup-multihome.patch` | `docs/reports/LADE-20261113-profile-home-multiplexer.md` §6.2, 2026-11-13 | The change it carries was absorbed into `setup.sh` section 2 in commit `b0f2f8d` ("feat: updated setup.sh"). It no longer applies — `git apply --check` fails at `setup.sh:178` — and applying it would revert the current provisioning. Kept as the record of how the fix was first generated. |

The live source of truth for the profile-home layout is `setup.sh` plus
`scripts/repair_profile_homes.sh`; the test is `./setup.sh --check` and
`bash scripts/repair_profile_homes.sh --check`.
