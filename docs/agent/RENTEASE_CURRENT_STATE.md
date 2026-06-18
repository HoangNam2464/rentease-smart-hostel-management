# RentEase Current State

## Branch

```text
complete-product
```

## Latest Known Commit

```text
6c6023a Remove legacy API and fees root routes
```

## Release Tags

Final local demo release tag:

```text
release-rentease-complete-product-v1
```

Latest production-hardening tag:

```text
phase14b1-remove-legacy-root-api-fees
```

Latest agent guidance docs commit:

```text
7da10ec Add RentEase agent guidance docs
```

SPQM documentation baseline:

```text
docs/spqm/
```

The SPQM documentation baseline has been created to support process, quality, backlog, metrics, release readiness, and continuous improvement.

Autonomous execution docs:

```text
docs/agent/AUTONOMOUS_EXECUTION_PLAN.md
docs/agent/NEXT_ACTION.md
```

These files allow future agent sessions to start from a short prompt, read the current next action, and continue safely through approved documentation, UI, and planning work.

## Runtime State

- Local runtime works.
- Django check passes.
- Migration dry-run says `No changes detected`.
- RentEase is ready for local demo and controlled testing.
- RentEase is not production-ready yet.

## Documentation Layers

RentEase now has two documentation layers:

- `docs/agent/` for coding-agent project memory, safety rules, current state, security rules, roadmap, and workflow.
- `docs/spqm/` for process model, quality gates, backlog, metrics, release checklist, and continuous improvement.

These documents support future work, but they do not make RentEase production-ready by themselves.

`docs/agent/NEXT_ACTION.md` controls the immediate next recommended phase. Agents must read it before choosing new work.

## Completed Locked Phases

Phase 8B-2 Owner Room Create/Update

Tag: `phase8b2-owner-room-create-update`

Phase 8C-1 Owner Tenant Update

Tag: `phase8c1-owner-tenant-update`

Phase 8D-1 Owner Contract Create/Update

Tag: `phase8d1-owner-contract-create-update`

Phase 8E-1 Owner Invoice Create/Update

Tag: `phase8e1-owner-invoice-create-update`

Phase 8F-1 Owner Payment Recording

Tag: `phase8f1-owner-payment-recording`

Phase 8G-1 Owner Dashboard / Reports Polish

Tag: `phase8g1-owner-dashboard-polish`

Phase 12A-1 Legacy Root URL Cleanup

Tag: `phase12a1-legacy-root-url-cleanup`

Phase 12A-2 Shared Tenant Edit Hardening

Tag: `phase12a2-shared-tenant-readonly`

Phase 12B-1 Public Root Landing Route Fix

Tag: `phase12b1-public-root-landing`

Phase 12B Full Regression Clean

Tag: `phase12b-full-regression-clean`

Phase 12C Home Landing Polish

Tag: `phase12c-home-landing-polish`

Phase 14B-1 Remove Legacy Root API / Fees Routes

Tag: `phase14b1-remove-legacy-root-api-fees`

## Working Now

- Public landing page
- Public rooms
- Public room detail
- Viewing registration
- Login/logout
- Role-based routing
- Owner dashboard
- Owner rooms
- Owner listings
- Owner linked tenants
- Shared tenant readonly protection
- Owner contracts
- Owner invoices
- Owner payment recording
- Owner repairs
- Owner viewing registrations
- Tenant dashboard
- Tenant profile
- Tenant contracts
- Tenant invoices
- Tenant payments
- Tenant repairs
- Tenant notifications
- Admin site
- Staff-only reports
- Legacy available only under `/legacy/` and `/legacy/login/`

## Important Production Gaps

- Production settings not hardened
- SQLite/local setup still active
- Owner-facing invoice detail/utility billing incomplete
- Account lifecycle incomplete
- Owner cannot create brand-new independent tenant yet
- Deployment/static/media/email/logging not production-ready

## Next Action

Current recommended next action:

```text
Phase 14B-2: Production Settings Split Planning
```

Goal: make settings production-aware while preserving local development.

Do not implement before planning and approval.

## Do Not Assume

Future agents must verify this state locally. Do not trust this file alone if git history has moved.
