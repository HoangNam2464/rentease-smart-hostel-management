# RentEase Master Tasks

## Current Product Status

RentEase is local-demo ready and role-based:

- public room browsing
- viewing registration
- owner portal
- tenant portal
- Django Admin / Jazzmin
- staff reports
- local fake demo data seed command

RentEase is not production-ready.

## Main Remaining Work

1. Safe repo hygiene cleanup.
2. Browser visual review and final UI fixes.
3. Production settings split.
4. Owner-facing billing detail / utility entry.
5. Account lifecycle and onboarding.
6. Deployment readiness.
7. Automated tests and CI.
8. Long-term legacy cleanup after dependency audit.

## Non-Goals For Small Phases

- Do not delete legacy apps.
- Do not change schema unless explicitly approved.
- Do not commit database or environment files.
- Do not expose tenant citizen ID data.
