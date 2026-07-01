# RentEase Next Action

## Immediate Next Phase

```text
Phase 14C-3B3B1 - Atomic Compatibility-Line Dual-Write
```

Status: waiting for explicit user approval. This phase changes billing write behavior and must keep InvoiceDetail and current invoice calculations/read paths authoritative.

## Goal

Atomically synchronize the four deterministic compatibility `InvoiceLine` rows whenever an InvoiceDetail is created or updated, while preserving every current total, payment, status, read path, report, and UI behavior.

## Required Context

- `AGENTS.md`
- `docs/agent/RENTEASE_CURRENT_STATE.md`
- `docs/architecture/DATA_MODEL_ALIGNMENT.md`
- `docs/architecture/TARGET_DATA_MODEL.md`
- `docs/agent/RENTEASE_SECURITY_RULES.md`
- `.agents/skills/rentease/references/backend-safety.md`
- current billing models, services, migrations, admin behavior, and tests inspected directly

## Approval Decisions Required Before Editing

- approve runtime dual-write for `legacy-rent`, `legacy-electricity`, `legacy-water`, and `legacy-service`
- keep InvoiceDetail authoritative for snapshots, calculations, invoice totals, reads, reports, and UI
- require InvoiceDetail save, compatibility-line synchronization, and invoice recalculation to succeed or roll back together
- update only lines linked to the saved detail; reject reserved-code ownership conflicts
- create no ServiceDefinition, Meter, or MeterReading records from InvoiceDetail values
- do not switch read authority, apply migrations to protected SQLite, or operate on real data in this phase

## Expected Scope After Approval

- add one focused synchronization service that derives quantities, unit prices, and amounts only from the saved InvoiceDetail snapshot
- invoke synchronization atomically from supported InvoiceDetail create/update paths without changing snapshot semantics
- preserve zero-usage electricity/water lines and exact line/detail/header total parity
- reject a reserved compatibility code when its existing line is not linked to the same InvoiceDetail
- prove repeated saves update rather than duplicate the four lines
- prove a synchronization error rolls back the detail snapshot, invoice totals, and compatibility lines together
- keep portal, reports, templates, settings, auth, schema, migrations, legacy apps, protected SQLite, and real data unchanged

## Required Checks

- `manage.py check`
- `manage.py makemigrations --check --dry-run`
- targeted dual-write, billing compatibility, payment, and migration tests plus the full suite
- exact line/detail/header parity after create, update, repeated save, zero usage, and forced rollback
- existing billing compatibility, payment, role-isolation, and Property tests
- `git diff --check`
- clean final worktree after the requested local commit

## Stop Conditions

- explicit Phase 14C-3B3B1 approval has not been given
- InvoiceDetail can no longer remain authoritative
- a schema migration, read-authority switch, UI/report change, or meter/service invention becomes necessary
- exact line/detail/header parity cannot be maintained atomically
- a reserved compatibility line belongs to another source
- protected local SQLite, real data, settings, authentication, permissions, templates, reports, or legacy runtime would change
- the starting worktree or Django checks are not clean

Phase 14C-3B3B2 read-authority switch, billing UI completion, maintenance/data governance, production legacy exclusion, PostgreSQL provisioning, and real-data onboarding remain separately approval-gated.
