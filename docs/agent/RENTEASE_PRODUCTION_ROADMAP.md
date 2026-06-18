# RentEase Production Roadmap

## Current Classification

RentEase is usable locally but not production-ready.

Final classification from production audit:

```text
C. Usable locally, but not production-ready.
```

## Next Action

There are now two recommended roadmap tracks. Choose the next track based on the current project goal.

`docs/agent/NEXT_ACTION.md` controls the immediate next step. If this roadmap and `NEXT_ACTION.md` differ, read both and follow `NEXT_ACTION.md` for the immediate phase unless the user explicitly changes priority.

If the immediate goal is Python course demo, prioritize Track A first.

If the goal is real deployment, prioritize Track B first.

Both tracks must follow the SPQM workflow and Definition of Done.

## Track A: Demo/Product Polish Track

Purpose: make the current Python/Django project look and feel more like a real usable product for demo and presentation.

Recommended order:

1. UI/UX audit and redesign planning
2. Public UI polish
3. Owner dashboard/sidebar/layout polish
4. Owner CRUD page polish
5. Tenant portal polish
6. README/demo package
7. screenshots/video demo support

## Track B: Real Production Readiness Track

Purpose: make the project safer for real deployment later.

Recommended order:

1. Production Settings Split
2. Owner Billing Detail / Utility Entry
3. Account Lifecycle
4. Deployment Readiness
5. CI/test coverage
6. optional legacy cleanup

Recommended next production-hardening action:

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
