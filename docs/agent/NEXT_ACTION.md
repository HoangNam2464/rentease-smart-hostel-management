# RentEase Next Action

## Immediate Next Phase

```text
Phase 14C - PostgreSQL Migration Planning
```

This is a planning-only phase. Do not change database configuration, schema, migrations, or data without a separate approved implementation plan.

## Goal

Produce a safe, reviewable plan for creating a fresh PostgreSQL production database from Django migrations, preserving an explicit local SQLite fallback, and onboarding owner-approved real data without copying demo or regression records.

## Required Context

- `AGENTS.md`
- `docs/agent/RENTEASE_CURRENT_STATE.md`
- `docs/architecture/PROJECT_STRUCTURE_MAP.md`
- `docs/architecture/DATA_MODEL_ALIGNMENT.md`
- `.agents/skills/rentease/references/backend-safety.md`
- Current database/settings configuration inspected directly from source

## Planning Output

The plan should cover:

- current SQLite and `DATABASE_URL` behavior
- PostgreSQL environment assumptions
- dependency and credential requirements
- schema creation and Django migration sequence
- SQLite backup and rollback
- a clean-database recommendation that does not transfer demo, regression, or test rows
- approved sources and ownership for real rooms, tenants, contracts, invoices, payments, and media
- administrator bootstrap and real-data import/onboarding sequence
- validation of row counts, relationships, uniqueness, users, money totals, media references, and critical workflows
- explicit handling for any legitimate non-demo SQLite records, without assuming they should be copied
- local-development fallback
- deployment order and downtime considerations
- explicit implementation files and commands
- stop conditions and risks

## Forbidden In This Phase

- No settings changes
- No database writes or exports containing sensitive data
- No schema/model/migration changes
- No dependency installation
- No PostgreSQL service provisioning
- No push or tag

Implementation requires explicit approval after the plan is reviewed.
