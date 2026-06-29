# RentEase Next Action

## Immediate Next Phase

```text
Phase 14C-2 - Schema Safety Baseline and Legacy Audit
```

This phase may add tests and update current architecture references. It must not change models, migrations, settings, database schema/data, authentication, billing calculations, URLs, or legacy code.

## Goal

Protect current RentEase behavior with a focused automated baseline and determine exactly which legacy HOSTELLO dependencies and tables a fresh PostgreSQL database would create before any target-schema implementation begins.

## Required Context

- `AGENTS.md`
- `docs/agent/RENTEASE_CURRENT_STATE.md`
- `docs/architecture/PROJECT_STRUCTURE_MAP.md`
- `docs/architecture/LEGACY_BOUNDARIES.md`
- `docs/architecture/DATA_MODEL_ALIGNMENT.md`
- `docs/architecture/TARGET_DATA_MODEL.md`
- `docs/agent/RENTEASE_SECURITY_RULES.md`
- `.agents/skills/rentease/references/backend-safety.md`
- current models, migrations, settings, URLs, admin registrations, and existing tests inspected directly

## Required Output

- test inventory and missing critical coverage
- new tests for owner/tenant isolation and migration-sensitive core behavior where absent
- current legacy dependency map across installed apps, imports, URLs, admin, content types, models, and migrations
- recommendation: temporarily retain legacy tables in PostgreSQL or schedule a separate safe removal phase
- expected active/legacy table inventory for a clean migration
- exact files and approval gates for Phase 14C-3A Property Foundation
- updated current documentation without a phase log

## Required Checks

- `manage.py check`
- `manage.py makemigrations --check --dry-run`
- targeted tests and full test suite
- `git diff --check`
- clean final worktree after the requested local commit

## Stop Conditions

- any proposed test requires production or real personal data
- existing owner/tenant isolation cannot be demonstrated
- active models or migrations have an unexpected legacy dependency
- the audit unexpectedly requires settings, URL, legacy-code, model, or migration changes
- the starting worktree or Django checks are not clean

Phase 14C-3 model and migration work requires separate explicit approval after this audit is reviewed.
