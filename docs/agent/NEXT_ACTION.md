# RentEase Next Action

## Immediate Next Phase

```text
Phase 14C-3A2 - Default Property Backfill
```

Status: waiting for explicit user approval. Do not create the data migration merely because this file names the next phase.

## Goal

Populate the additive Property schema without inventing addresses or changing current owner-scoped behavior.

## Required Context

- `AGENTS.md`
- `docs/agent/RENTEASE_CURRENT_STATE.md`
- `docs/architecture/PROJECT_STRUCTURE_MAP.md`
- `docs/architecture/LEGACY_BOUNDARIES.md`
- `docs/architecture/DATA_MODEL_ALIGNMENT.md`
- `docs/architecture/TARGET_DATA_MODEL.md`
- `docs/agent/RENTEASE_SECURITY_RULES.md`
- `.agents/skills/rentease/references/backend-safety.md`
- current `accounts.UserProfile`, `properties.Property`, `properties.Room`, migrations, disposable seed data, and tests inspected directly

## Approval Decisions Required Before Editing

- approve the Phase 14C-3A2 reversible data migration
- confirm one default Property is created for every existing owner profile, including owners without rooms
- confirm deterministic codes may use the owner primary key and names may use the existing owner display name
- confirm `rental_address` is copied when present while unknown ward/province/location fields remain blank
- confirm every current Room is linked to its owner's default Property

## Expected Scope After Approval

- add one reversible `RunPython` migration after `properties.0002`
- preserve all owner-profile, room, contract, listing, invoice, repair, and payment rows
- keep `Room.owner` authoritative and `Room.property` nullable at schema level
- add migration tests for deterministic creation, room linking, no invented address, and reverse preservation
- keep portal/admin/forms/reports/templates/seed data, authentication, billing, settings, legacy apps, and real data unchanged

## Required Checks

- `manage.py check`
- `manage.py makemigrations --check --dry-run`
- targeted tests and full test suite
- `git diff --check`
- migration forward/backward rehearsal in the disposable test database
- owner/property counts, room counts, zero unlinked existing rooms after forward migration, zero owner/property mismatches, and reverse preservation
- clean final worktree after the requested local commit

## Stop Conditions

- explicit Phase 14C-3A2 approval has not been given
- deterministic codes would collide or a room cannot map to exactly one owner-owned Property
- owner/tenant/listing/report isolation differs during the transition
- the migration is not reversible on disposable data
- invented personal/location data, billing, authentication, settings, legacy runtime, or real production data would be required
- the starting worktree or Django checks are not clean

Phase 14C-3A3 product integration, Phase 14C-3B billing/meter work, and Phase 14C-3D production legacy exclusion remain separately approval-gated.
