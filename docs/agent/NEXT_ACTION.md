# RentEase Next Action

## Immediate Next Phase

```text
Phase 14C - PostgreSQL Migration Planning
```

This is a planning-only phase. Do not change database configuration, schema, migrations, or data without a separate approved implementation plan.

## Goal

Produce a safe, reviewable plan for moving the production target from local SQLite to PostgreSQL while preserving the local demo workflow.

## Required Context

- `AGENTS.md`
- `docs/agent/RENTEASE_CURRENT_STATE.md`
- `docs/architecture/PROJECT_STRUCTURE_MAP.md`
- `.agents/skills/rentease/references/backend-safety.md`
- Current database/settings configuration inspected directly from source

## Planning Output

The plan should cover:

- current SQLite and `DATABASE_URL` behavior
- PostgreSQL environment assumptions
- dependency and credential requirements
- schema creation and Django migration sequence
- SQLite backup and rollback
- data transfer options and recommendation
- validation of row counts, relationships, users, media references, and critical workflows
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
