# RentEase Next Action

## Immediate Next Phase

```text
Phase 14C-3A - Property Foundation
```

Status: waiting for explicit user approval. Do not edit models or create migrations merely because this file names the next phase.

## Goal

Add the property/building layer between owner and room through a reversible transitional migration while preserving every current owner, tenant, listing, billing, repair, and report scope.

## Required Context

- `AGENTS.md`
- `docs/agent/RENTEASE_CURRENT_STATE.md`
- `docs/architecture/PROJECT_STRUCTURE_MAP.md`
- `docs/architecture/LEGACY_BOUNDARIES.md`
- `docs/architecture/DATA_MODEL_ALIGNMENT.md`
- `docs/architecture/TARGET_DATA_MODEL.md`
- `docs/agent/RENTEASE_SECURITY_RULES.md`
- `.agents/skills/rentease/references/backend-safety.md`
- current `properties`, `portal`, `listings`, `reports`, admin, seed command, templates, migrations, and tests inspected directly

## Approval Decisions Required Before Editing

- approve Phase 14C-3A model and migration changes
- confirm the minimum Property identifier, name, address, contact, status, and timezone fields
- confirm one default Property per existing owner for the disposable-data backfill
- confirm `Room.owner` remains temporarily as a compatibility field
- confirm room-code uniqueness moves to Property plus room code only after backfill and scope updates
- approve the forward/backward disposable-database migration rehearsal

## Expected Scope After Approval

- add `Property` and a nullable transitional `Room.property`
- create and review the data backfill migration
- update owner-scoped querysets, forms, admin, public listings, reports, seed data, and tests
- make the property relationship required only after isolation and backfill checks pass
- keep authentication, billing calculations, legacy apps, production settings, and real data unchanged

## Required Checks

- `manage.py check`
- `manage.py makemigrations --check --dry-run`
- targeted tests and full test suite
- `git diff --check`
- migration forward/backward rehearsal on a disposable database copy
- row-count, null-property, owner/property mismatch, and cross-owner isolation checks
- clean final worktree after the requested local commit

## Stop Conditions

- explicit Phase 14C-3A approval has not been given
- the backfill cannot map every room to exactly one owner-owned Property
- owner/tenant/listing/report isolation differs during the transition
- the migration is not reversible on disposable data
- billing, authentication, settings, legacy runtime, or real personal data would need to change
- the starting worktree or Django checks are not clean

Phase 14C-3B billing/meter work and Phase 14C-3D production legacy exclusion remain separately approval-gated.
