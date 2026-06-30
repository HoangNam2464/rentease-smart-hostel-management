# RentEase Next Action

## Immediate Next Phase

```text
Phase 14C-3A4 - Required Property Relationship and Room-Code Constraint
```

Status: waiting for explicit user approval. This is a schema-and-migration phase and must remain separate from billing, PostgreSQL provisioning, and legacy exclusion.

## Goal

Complete the transitional Property foundation by requiring every Room to belong to an owner-matched Property and scoping room-code uniqueness to that Property while retaining `Room.owner` as the current authorization boundary.

## Required Context

- `AGENTS.md`
- `docs/agent/RENTEASE_CURRENT_STATE.md`
- `docs/architecture/DATA_MODEL_ALIGNMENT.md`
- `docs/architecture/TARGET_DATA_MODEL.md`
- `docs/architecture/LEGACY_BOUNDARIES.md`
- `docs/agent/RENTEASE_SECURITY_RULES.md`
- `.agents/skills/rentease/references/backend-safety.md`
- current Property/Room models, migrations, admin/forms/querysets, migration tests, and protected-data boundaries inspected directly

## Approval Decisions Required Before Editing

- approve changing `Room.property` from nullable to required
- approve replacing owner-plus-room-code uniqueness with Property-plus-room-code uniqueness
- keep `Room.owner` and all current authorization querysets during this phase
- approve a precondition migration that stops on null Property, owner mismatch, or duplicate `(property, room_code)` data instead of guessing
- keep protected local SQLite and all real data untouched; exercise migrations only in disposable test databases unless separately authorized

## Expected Scope After Approval

- add a reviewed migration precondition for zero null, zero owner mismatch, and zero duplicate Property room codes
- make `Room.property` required
- replace `unique_room_code_per_owner` with a Property-scoped unique constraint
- preserve owner/property consistency in forms and Django Admin
- update model and migration tests for forward/reverse behavior and constraint enforcement
- keep authentication, permissions, billing, settings, reports, legacy apps, PostgreSQL provisioning, and real-data onboarding unchanged

## Required Checks

- `manage.py check`
- `manage.py makemigrations --check --dry-run`
- targeted model/admin/form/migration tests and full test suite
- migration forward and backward on disposable databases
- zero-null, owner-match, and duplicate-precondition tests
- existing role, public privacy, staff report, billing, and seed tests
- `git diff --check`
- clean final worktree after the requested local commit

## Stop Conditions

- explicit Phase 14C-3A4 approval has not been given
- current disposable migration-state data contains null Property, owner mismatch, or duplicate `(property, room_code)` rows that are not deliberately covered by the precondition tests
- authorization would need to switch away from `Room.owner`
- protected local SQLite or real data would need mutation
- billing, authentication, settings, legacy runtime, PostgreSQL provisioning, or another model area must change
- the starting worktree or Django checks are not clean

Billing/meter work, maintenance/data-governance work, production legacy exclusion, PostgreSQL provisioning, and real-data onboarding remain separately approval-gated.
