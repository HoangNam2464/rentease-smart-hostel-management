# RentEase Production Roadmap

## Current Classification

RentEase is usable locally but not production-ready.

Final classification from production audit:

```text
C. Usable locally, but not production-ready.
```

## Next Action

Recommended next action:

```text
Phase 14B-2: Production Settings Split Planning
```

Do not implement before producing a plan and receiving approval.

## Phase 14B-2: Production Settings Split

Goal: make settings production-aware while preserving local development.

Must address:

- `DEBUG`
- `SECRET_KEY`
- `ALLOWED_HOSTS`
- `CSRF_TRUSTED_ORIGINS`
- HTTPS/security headers
- secure cookies
- database configuration
- static/media configuration
- email settings
- logging
- `.env` support
- requirements
- `.gitignore`

No schema change expected.

## Phase 14C: Owner Billing Detail / Utility Entry

Goal: make billing truly usable for real hostel operation.

Current state:

- Owner can create invoice headers.
- Owner can record payments.
- Payment recalculates `paid_amount`, `remaining_amount`, and `status`.

Gap:

- Owner cannot create invoice detail/utility/service line items from portal.
- Meaningful invoice totals may require admin/model setup.

Needed:

- owner-facing invoice details
- utility readings
- service charges
- rent/deposit/fee breakdown
- clear tenant invoice detail display

## Phase 14D: Account Lifecycle

Goal: make account management real-world usable.

Needed:

- password reset
- owner/tenant onboarding
- tenant account creation/invitation
- profile update rules
- email verification if needed

## Phase 14E: Deployment Readiness

Goal: prepare real deployment.

Needed:

- PostgreSQL/MySQL
- production `.env`
- `collectstatic`
- static/media hosting
- HTTPS
- WSGI/ASGI server
- logging
- backups
- error pages
- deployment documentation
- CI/test strategy

## Later Cleanup

Optional later:

- remove or fully isolate legacy HOSTELLO apps
- clean HOSTELLO branding from legacy/static/settings
- add report exports
- add online payment integration
- add advanced analytics

## Keep This Roadmap Updated

After each completed and locked phase, update this roadmap if priorities or production gaps change.
