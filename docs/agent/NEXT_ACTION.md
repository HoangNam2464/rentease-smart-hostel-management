# RentEase Next Action

## Immediate Next Phase

```text
Phase 14C-3C1 - Maintenance Lifecycle Correction
```

Status: waiting for explicit user approval. This phase changes the `MaintenanceRecord` schema and lifecycle rules, so it must begin with a reviewed field, migration, compatibility, and rollback plan.

## Goal

Replace the ambiguous required `performed_date` with lifecycle-safe scheduling and execution timestamps while preserving room/repair relationships, owner and staff workflows, reports, existing records, and privacy boundaries.

## Current Problem

- `MaintenanceRecord.performed_date` is required even for scheduled or cancelled work.
- Scheduled, in-progress, completed, and cancelled states do not have distinct date semantics.
- The model cannot represent a scheduled date, optional start time, and optional completion time without overloading one field.
- Reports currently order and summarize completed work through `performed_date`, so migration and compatibility behavior must be explicit.

## Approval Decisions Required Before Editing

- add `scheduled_for`, nullable `started_at`, and nullable `completed_at`
- define whether `scheduled_for` is a date or timezone-aware datetime
- backfill existing `performed_date` conservatively without inventing start/completion times
- require completed records to have `completed_at` and prevent completion before start
- define cancelled-record date behavior and whether a cancellation timestamp is deferred
- preserve or transition `performed_date` only through a reversible migration plan
- keep vendor, performed-by, cost, owner/tenant scoping, reports, templates, settings, auth, and legacy apps unchanged unless separately approved

## Expected First Step After Approval

- inspect all `MaintenanceRecord` model, admin, report, seed, template, and test consumers
- write the exact additive migration/backfill/constraint plan before changing the schema
- add lifecycle validation and disposable forward/backward migration tests
- update reports only where required to preserve current completed-maintenance output
- avoid protected media or data-governance work; that remains Phase 14C-3C2

## Required Checks

- `manage.py check`
- `manage.py makemigrations --check --dry-run`
- maintenance model and migration forward/backward tests
- report/admin compatibility tests
- owner/tenant relationship and privacy regression tests
- full test suite
- `git diff --check`

## Stop Conditions

- explicit Phase 14C-3C1 approval has not been given
- existing dates cannot be mapped without guessing
- an irreversible migration or destructive field removal is proposed without a verified compatibility period
- owner/tenant scoping, repair-request relationships, or report behavior would change unexpectedly
- protected media, audit logging, billing, PostgreSQL, settings, auth, permissions, or legacy work becomes necessary
- protected local SQLite or real data would be mutated
- the starting worktree or Django checks are not clean

Owner billing UI completion, protected-document/audit foundations, production legacy exclusion, PostgreSQL provisioning, and real-data onboarding remain separately approval-gated.
