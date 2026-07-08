# RentEase Planned Features

This directory reserves product areas that are expected after the current RentEase foundation. It prevents future work from being hidden inside unrelated apps while avoiding premature Django apps, models, migrations, URLs, or settings.

Nothing under `planned/` is active code. A folder name means only `PLANNED`; it does not mean approved, implemented, installed, or safe to migrate.

| Placeholder | Priority | Intended scope | Likely implementation boundary |
|---|---|---|---|
| `property-portfolio` | Pre-PostgreSQL foundation | Properties/buildings, addresses, room amenities, image galleries | Property relationship first; gallery/amenities may follow later |
| `billing-utilities` | Pre-PostgreSQL foundation | Meter readings, service catalog, invoice generation, deposits | Additive compatibility migration before retiring fixed detail fields |
| `account-lifecycle` | After PostgreSQL foundation | Owner/tenant onboarding, invitations, recovery, verification | Extend `accounts` and `tenants` after auth/security review |
| `maintenance-operations` | Pre-PostgreSQL foundation | Schedules, vendors, work orders, completion evidence | Correct date/status semantics first; richer operations may follow |
| `payments-notifications` | Later integration | Reconciliation, receipts, gateways, delivery channels | Separate integration plan with idempotency and privacy controls |
| `data-governance` | Required before real data | PostgreSQL import, audit trail, provenance, retention, backups | Cross-cutting production plan; never store real data in Git |

Before activating any placeholder:

1. Confirm the user workflow and role permissions.
2. Compare it with `docs/DATA.md`, `docs/TARGET.md`, and current source.
3. Produce an approved model, migration, rollback, privacy, and test plan.
4. Create or extend a Django app only after the ownership boundary is clear.
5. Replace the placeholder with task-specific implementation documentation; do not leave parallel plans.

The single immediate iteration lives in `docs/NEXT.md`.
