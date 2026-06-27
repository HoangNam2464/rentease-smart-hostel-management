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
- UI through Phase 20N is complete.
- Admin privacy hardened: citizen_id removed from TenantAdmin/CoTenantAdmin list and search, ContractAdmin/InvoiceAdmin search replaced with safe fields.

## Last Completed Phase

```text
Phase 20N: Admin Search Privacy Hardening
```

Tag: `phase20n-admin-search-privacy-hardening`

## Immediate Priority

```text
Phase 20O: Admin Sensitive Detail Permission Planning
```

Goal:

- Plan whether `citizen_id`, `citizen_id_front`, `citizen_id_back` in Tenant/CoTenant admin detail forms should:
  - remain editable for all staff (current state)
  - become read-only for non-superuser staff
  - become superuser-only
- This is a planning-only phase unless approved for implementation.
- Do not implement before producing a plan and receiving explicit user approval.

## Recommended Next Phase After 20O

```text
Phase 14B-2: Production Settings Split Planning
```

Goal: Make settings production-aware while preserving local development.

Must address:
- `DEBUG`
- `SECRET_KEY`
- `ALLOWED_HOSTS`
- HTTPS/security headers
- secure cookies
- database configuration
- static/media configuration
- email settings
- logging
- `.env` support

Do not implement before producing a plan and receiving explicit approval.

## Manual Browser Walkthrough Checklist

Review these pages in the browser before any submission or release:

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
- Do not push to GitHub without explicit approval.
