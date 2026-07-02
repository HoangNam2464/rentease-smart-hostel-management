# RentEase Next Action

## Immediate Next Phase

```text
Phase 14C-3B3B2 - Controlled InvoiceLine Read-Authority Switch
```

Status: waiting for explicit user approval. This phase changes billing read and total-calculation authority, so it must start with reviewed parity evidence and a fail-closed rollback boundary.

## Goal

Make validated `InvoiceLine` rows authoritative for invoice charge totals while retaining `InvoiceDetail` as the compatibility snapshot/write source. Preserve payment, status, owner/tenant scoping, reports, and current UI behavior.

## Required Context

- `AGENTS.md`
- `docs/agent/RENTEASE_CURRENT_STATE.md`
- `docs/architecture/DATA_MODEL_ALIGNMENT.md`
- `docs/architecture/TARGET_DATA_MODEL.md`
- `docs/agent/RENTEASE_SECURITY_RULES.md`
- `.agents/skills/rentease/references/backend-safety.md`
- current billing models, services, migrations, admin behavior, reports, portal reads, and tests inspected directly

## Approval Decisions Required Before Editing

- approve validated `InvoiceLine` signed amounts as the source for invoice charge totals
- retain InvoiceDetail as the source for legacy meter/rate snapshots and atomic compatibility-line writes
- define whether non-compatibility adjustment/discount lines participate now or remain deferred to Phase 14D
- require missing, duplicate, conflicting, or non-parity compatibility lines to fail closed
- keep payments, remaining amount, status transitions, reports, and UI outputs unchanged
- authorize any read-only reconciliation of protected local SQLite separately; do not mutate or onboard real data

## Expected Scope After Approval

- add a focused validated line-total reader with deterministic ordering and signed-amount handling
- switch invoice total recalculation only after exact detail/line/header parity is established
- keep existing compatibility-line dual-write and zero-usage behavior unchanged
- fail closed on missing/conflicting reserved lines or detail/line variance
- preserve payment recalculation, overpayment rejection, invoice status, reports, and portal output
- keep templates, settings, auth, permissions, schema, migrations, legacy apps, and real data unchanged

## Required Checks

- `manage.py check`
- `manage.py makemigrations --check --dry-run`
- targeted read-authority, dual-write, billing compatibility, payment, and migration tests plus the full suite
- exact line/detail/header parity before and after the authority switch, including zero usage and forced rollback
- existing billing compatibility, payment, role-isolation, and Property tests
- `git diff --check`
- clean final worktree after the requested local commit

## Stop Conditions

- explicit Phase 14C-3B3B2 approval has not been given
- exact detail/line/header parity evidence is missing or fails
- a schema migration, UI workflow, or meter/service invention becomes necessary
- payment, status, report, or portal behavior would change
- a reserved compatibility line is missing, duplicated, or belongs to another source
- protected local SQLite or real data would be mutated
- settings, authentication, permissions, templates, reports, or legacy runtime would change
- the starting worktree or Django checks are not clean

Billing UI completion, maintenance/data governance, production legacy exclusion, PostgreSQL provisioning, and real-data onboarding remain separately approval-gated.
