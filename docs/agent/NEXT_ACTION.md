# RentEase Next Action

## Immediate Next Phase

```text
Phase 14C-3B2 - Additive Billing and Meter Schema
```

Status: waiting for explicit user approval. This phase adds new tables only; it must not switch current invoice calculation, reads, writes, reports, or UI.

## Goal

Add the approved ServiceDefinition, Meter, MeterReading, and InvoiceLine foundations while keeping `PriceConfig`, `InvoiceDetail`, current totals, payments, and all existing workflows authoritative.

## Required Context

- `AGENTS.md`
- `docs/agent/RENTEASE_CURRENT_STATE.md`
- `docs/architecture/DATA_MODEL_ALIGNMENT.md`
- `docs/architecture/TARGET_DATA_MODEL.md`
- `docs/agent/RENTEASE_SECURITY_RULES.md`
- `.agents/skills/rentease/references/backend-safety.md`
- current billing models/migration/tests, Property/Room constraints, account model, and admin inspected directly

## Approval Decisions Required Before Editing

- approve four additive models and one reviewed migration
- approve the exact fields, relationships, choices, and uniqueness constraints recorded in `TARGET_DATA_MODEL.md`
- keep old billing tables and every current calculation/read/write path authoritative
- create no backfill, demo records, meters, readings, invoice lines, UI, or PostgreSQL data in this phase

## Expected Scope After Approval

- add ServiceDefinition, Meter, MeterReading, and InvoiceLine models and admin registration
- add database constraints for owner/property scope, period uniqueness, non-negative numeric values, and stable invoice line codes where expressible
- add model validation for cross-Property service/meter consistency and reading monotonicity
- add forward/backward migration tests and model/constraint tests
- keep `PriceConfig`, `Invoice`, `InvoiceDetail`, `PaymentHistory`, billing services, portal, reports, templates, settings, auth, legacy apps, protected SQLite, and real data unchanged

## Required Checks

- `manage.py check`
- `manage.py makemigrations --check --dry-run`
- targeted billing model/migration tests and full test suite
- clean forward/backward migration on disposable databases
- existing billing compatibility, payment, role-isolation, and Property tests
- `git diff --check`
- clean final worktree after the requested local commit

## Stop Conditions

- explicit Phase 14C-3B2 approval has not been given
- existing billing behavior or old model fields must change
- a backfill or current read/write switch becomes necessary
- protected local SQLite, real data, settings, authentication, permissions, templates, reports, or legacy runtime would change
- an irreversible migration is required
- the starting worktree or Django checks are not clean

Phase 14C-3B3 backfill/reconciliation/read-write switch, billing UI completion, maintenance/data governance, production legacy exclusion, PostgreSQL provisioning, and real-data onboarding remain separately approval-gated.
