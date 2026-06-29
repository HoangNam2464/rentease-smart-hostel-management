# RentEase Planned Features

This directory reserves product areas that are expected after the current RentEase foundation. It prevents future work from being hidden inside unrelated apps while avoiding premature Django apps, models, migrations, URLs, or settings.

Nothing under `planned/` is active code. A folder name means only `PLANNED`; it does not mean approved, implemented, installed, or safe to migrate.

| Placeholder | Intended scope | Likely implementation boundary |
|---|---|---|
| `property-portfolio` | Properties/buildings, addresses, room amenities, image galleries | New architecture decision before extending `properties` and `listings` |
| `billing-utilities` | Meter readings, service catalog, invoice generation, deposits | Extend `billing` only after calculation and migration design |
| `account-lifecycle` | Owner/tenant onboarding, invitations, recovery, verification | Extend `accounts` and `tenants` after auth/security review |
| `maintenance-operations` | Schedules, vendors, work orders, completion evidence | Extend `maintenance` after workflow and media-security design |
| `payments-notifications` | Reconciliation, receipts, gateways, delivery channels | Separate integration plan with idempotency and privacy controls |
| `data-governance` | PostgreSQL import, audit trail, provenance, retention, backups | Cross-cutting production plan; never store real data in Git |

Before activating any placeholder:

1. Confirm the user workflow and role permissions.
2. Compare it with `docs/architecture/DATA_MODEL_ALIGNMENT.md` and current source.
3. Produce an approved model, migration, rollback, privacy, and test plan.
4. Create or extend a Django app only after the ownership boundary is clear.
5. Replace the placeholder with task-specific implementation documentation; do not leave parallel plans.

The immediate database task remains PostgreSQL planning in `docs/agent/NEXT_ACTION.md`.
