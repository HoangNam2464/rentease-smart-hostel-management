# RentEase Next Action

## Immediate Next Phase

```text
Phase 14C-3B3A - Disposable Invoice-Line Backfill and Exact Reconciliation
```

Status: waiting for explicit user approval. This phase proves compatibility on disposable test data only; it must not switch current invoice calculation, reads, writes, reports, or UI.

## Goal

Add a reversible data migration that maps every existing `InvoiceDetail` into four deterministic compatibility `InvoiceLine` rows and proves exact financial and relationship parity. `PriceConfig`, `InvoiceDetail`, current totals, payments, and all existing workflows remain authoritative.

## Required Context

- `AGENTS.md`
- `docs/agent/RENTEASE_CURRENT_STATE.md`
- `docs/architecture/DATA_MODEL_ALIGNMENT.md`
- `docs/architecture/TARGET_DATA_MODEL.md`
- `docs/agent/RENTEASE_SECURITY_RULES.md`
- `.agents/skills/rentease/references/backend-safety.md`
- current billing models, services, migrations, and tests inspected directly

## Approval Decisions Required Before Editing

- approve one reversible compatibility data migration and its exact reconciliation rules
- create four lines per existing detail using stable codes: `legacy-rent`, `legacy-electricity`, `legacy-water`, and `legacy-service`
- keep old billing tables and every current calculation/read/write path authoritative
- create no ServiceDefinition, Meter, or MeterReading records from legacy invoice-only values
- use disposable test databases only; do not migrate protected SQLite or real data in this phase

## Expected Scope After Approval

- add one reversible data migration that creates exactly four zero-preserving compatibility lines per existing `InvoiceDetail`
- use snapshot amounts already stored on each detail; do not recalculate from current `PriceConfig`
- require signed line sum, `InvoiceDetail.total_line_amount`, and `Invoice.total_amount` to match with exact `Decimal('0.00')` variance
- preserve invoice/payment counts, paid amount, remaining amount, status, owner/tenant relationships, and all legacy billing rows
- make reversal delete only lines created by this migration and stop on stable-code collisions rather than overwrite data
- add forward/backward migration tests for zero usage, paid/partial/unpaid invoices, row counts, relationships, and exact totals
- keep billing services, portal, reports, templates, settings, auth, legacy apps, protected SQLite, and real data unchanged

## Required Checks

- `manage.py check`
- `manage.py makemigrations --check --dry-run`
- targeted billing compatibility/backfill migration tests and full test suite
- clean forward/backward migration on disposable databases with exact row-count and financial reconciliation
- existing billing compatibility, payment, role-isolation, and Property tests
- `git diff --check`
- clean final worktree after the requested local commit

## Stop Conditions

- explicit Phase 14C-3B3A approval has not been given
- existing billing behavior, schema, or old model fields must change
- a current read/write switch becomes necessary
- any source invoice/detail totals differ before or after compatibility-line creation
- a stable compatibility line code already exists for a source invoice
- protected local SQLite, real data, settings, authentication, permissions, templates, reports, or legacy runtime would change
- an irreversible migration is required
- the starting worktree or Django checks are not clean

Phase 14C-3B3B read/write switch, billing UI completion, maintenance/data governance, production legacy exclusion, PostgreSQL provisioning, and real-data onboarding remain separately approval-gated.
