# RentEase Next Action

## Immediate Next Phase

```text
Phase 14C-3B1 - Billing and Meter Compatibility Baseline
```

Status: waiting for explicit user approval. This phase must freeze and document current financial behavior before any service, meter, reading, or invoice-line schema is added.

## Goal

Create an evidence-backed compatibility and reconciliation baseline for current rent, electricity, water, service-fee, invoice-total, payment, remaining-balance, and overpayment behavior; finalize the smallest additive Phase 14C-3B2 schema without changing production behavior.

## Required Context

- `AGENTS.md`
- `docs/agent/RENTEASE_CURRENT_STATE.md`
- `docs/architecture/DATA_MODEL_ALIGNMENT.md`
- `docs/architecture/TARGET_DATA_MODEL.md`
- `docs/agent/RENTEASE_SECURITY_RULES.md`
- `.agents/skills/rentease/references/backend-safety.md`
- current `PriceConfig`, `Invoice`, `InvoiceDetail`, and `PaymentHistory` models, migrations, signals/services, owner forms/views, tenant reads, reports, admin, seed command, and tests inspected directly

## Approval Decisions Required Before Editing

- approve a no-schema billing compatibility audit and regression-test phase
- keep every current calculation, invoice status transition, payment rule, and overpayment rejection unchanged
- use only disposable test data; do not inspect or mutate protected local SQLite or real data
- defer new models and migrations to separately approved Phase 14C-3B2

## Expected Scope After Approval

- map the current billing write/read paths and calculation triggers from source
- add missing regression tests for rent, electricity, water, service, zero usage, price snapshots, recalculation, partial/full payment, remaining balance, and overpayment
- define reconciliation inputs/outputs and acceptance tolerances for the later additive migration
- finalize proposed fields, uniqueness, ordering, ownership, and compatibility links for ServiceDefinition, Meter, MeterReading, and InvoiceLine
- keep models, migrations, settings, authentication, permissions, templates, legacy apps, PostgreSQL provisioning, and real data unchanged

## Required Checks

- `manage.py check`
- `manage.py makemigrations --check --dry-run`
- targeted billing tests and full test suite
- current owner/tenant isolation and payment-overflow tests
- `git diff --check`
- clean final worktree after the requested local commit

## Stop Conditions

- explicit Phase 14C-3B1 approval has not been given
- any current financial total or status behavior must change
- a model, migration, setting, authentication, permission, template, legacy runtime, PostgreSQL, or real-data change becomes necessary
- protected local SQLite would need inspection or mutation
- the starting worktree or Django checks are not clean

Phase 14C-3B2 additive schema, 14C-3B3 reconciliation/read-write switch, maintenance/data-governance work, production legacy exclusion, PostgreSQL provisioning, and real-data onboarding remain separately approval-gated.
