# RentEase Next Action

## Current State

RentEase is on branch:

```text
complete-product
```

Current status:

- Local demo ready.
- Not production-ready yet.
- Backend/frontend/docs monorepo structure is in place.
- Official local virtual environment is `backend/venv/`.
- Root `venv/` was removed safely.
- README has been updated for the current project structure.
- Final demo checklist exists at `docs/demo/FINAL_DEMO_CHECKLIST.md`.
- Route smoke test passed for public, protected anonymous, admin, owner, and tenant routes.
- Legacy dependency audit is complete.
- Helper files were archived.

## Immediate Priority

1. Manual browser walkthrough.
2. UI polish only if the browser walkthrough finds visible issues.
3. Realistic demo data polish.
4. Final submission docs and diagrams.

## Recommended Next Phase

```text
Realistic Demo Data Polish
```

Goal:

- Make local demo data feel like a real Vietnamese rental-room scenario.
- Keep fake/safe values only.
- Avoid real citizen identity data.
- Keep seed data idempotent.
- Do not create migrations or schema changes unless explicitly approved.

## Manual Browser Walkthrough Checklist

Review these pages in the browser:

- `/`
- `/rooms/`
- `/login/`
- `/owner/dashboard/`
- `/owner/rooms/`
- `/owner/tenants/`
- `/owner/contracts/`
- `/owner/invoices/`
- `/tenant/dashboard/`
- `/tenant/invoices/`
- `/tenant/payments/`
- `/admin/`
- `/reports/`
- `/legacy/login/`

Check:

- Page loads correctly.
- Layout is readable at desktop width.
- No raw Django template tags appear.
- No private data appears on public pages.
- Tenant identity-sensitive fields are not exposed in list/search surfaces.
- Demo data looks understandable for presentation.

## Do Not Do Yet

- Do not delete legacy apps.
- Do not delete legacy templates/static.
- Do not move Django apps into `backend/apps/`.
- Do not rename `backend/hostello_backend/`.
- Do not harden production settings without a separate plan.
- Do not use real personal data in demo records.

