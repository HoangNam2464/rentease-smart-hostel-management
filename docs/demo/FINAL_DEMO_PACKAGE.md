# RentEase Final Demo Package

## Status

RentEase is ready for a local course demo.

Current demo package status:

- public UI polished
- owner portal polished
- tenant portal polished
- demo seed command implemented
- final demo walkthrough verified
- README updated for local setup and presentation
- final polished local demo release verified
- final visual QA checklist prepared
- screenshot and video preparation guide prepared
- product-grade UI redesign completed

Final local demo release tag:

```text
release-rentease-polished-local-demo-v2
```

RentEase is not production-ready yet.

## Required Commands

From the repository root:

```powershell
cd hostello_backend
```

Run checks:

```powershell
.\venv\Scripts\python.exe manage.py check
.\venv\Scripts\python.exe manage.py makemigrations --check --dry-run
```

Seed demo data:

```powershell
.\venv\Scripts\python.exe manage.py seed_rentease_demo_data --dry-run --owner-username owner_test --tenant-username tenant_test
.\venv\Scripts\python.exe manage.py seed_rentease_demo_data --owner-username owner_test --tenant-username tenant_test
```

Start local server:

```powershell
.\venv\Scripts\python.exe manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

## Demo Accounts

Local demo accounts only:

| Role | Username | Password |
| --- | --- | --- |
| Admin | `admin_test` | `Test@12345` |
| Owner | `owner_test` | `Test@12345` |
| Tenant | `tenant_test` | `Test@12345` |

Do not show passwords in screenshots, slides, or recorded video.

## Demo Route List

### Public

```text
/
/rooms/
/rooms/<published_id>/
/rooms/<published_id>/register/
/rooms/<published_id>/register/success/
/login/
```

### Owner

```text
/owner/dashboard/
/owner/rooms/
/owner/rooms/new/
/owner/listings/
/owner/tenants/
/owner/contracts/
/owner/contracts/new/
/owner/invoices/
/owner/invoices/new/
/owner/repairs/
/owner/viewing-registrations/
```

Recommended owner detail pages:

```text
/owner/rooms/<id>/
/owner/listings/<id>/
/owner/contracts/<id>/
/owner/invoices/<id>/
/owner/invoices/<id>/payments/new/
/owner/repairs/<id>/
/owner/viewing-registrations/<id>/
```

### Tenant

```text
/tenant/dashboard/
/tenant/profile/
/tenant/contracts/
/tenant/invoices/
/tenant/payments/
/tenant/repairs/
/tenant/repairs/new/
/tenant/notifications/
```

Recommended tenant detail pages:

```text
/tenant/contracts/<id>/
/tenant/invoices/<id>/
/tenant/repairs/<id>/
```

### Admin And Reports

```text
/admin/
/reports/
/reports/billing/
```

Reports are staff-only.

### Legacy Safety

```text
/legacy/
/legacy/login/
```

These root legacy routes should remain unavailable:

```text
/api/requests/
/api/admin/requests/
/fees/
```

## Screenshot Checklist Summary

Capture these for presentation:

- landing page
- public room list
- public room detail
- viewing registration form
- portal login
- owner dashboard
- owner rooms
- owner invoices
- owner payment recording form
- owner repairs
- owner viewing registrations
- tenant dashboard
- tenant contract or invoice detail
- tenant payments
- tenant repairs
- staff reports if needed
- custom 404 page if using `DEBUG=False`
- legacy route isolation if security scope is discussed

Full checklist:

```text
docs/demo/SCREENSHOT_CHECKLIST.md
docs/ui/PHASE_17C_FINAL_VISUAL_QA.md
docs/demo/PHASE_18A_SCREENSHOT_VIDEO_PREP.md
docs/ui/PHASE_19A_PRODUCT_GRADE_UI_REDESIGN.md
```

## Video Demo Outline

Target length: 3 to 5 minutes.

1. Start at `/` and introduce the product.
2. Browse rooms publicly.
3. Open a public room detail page.
4. Show viewing registration.
5. Log in as owner.
6. Show owner dashboard metrics.
7. Show rooms, invoices, payment recording, repairs, and viewing registrations.
8. Log in as tenant.
9. Show tenant dashboard, contract, invoices, payments, repairs, and notifications.
10. End with admin/reports protection and remaining production limitations.

## Verification Summary

Latest verified walkthrough:

- Phase: Phase 15F Final Demo Walkthrough Verification
- Django check: passed
- Migration dry-run: `No changes detected`
- Route smoke tests: 53 routes passed
- Privacy scan: 28 public/owner/tenant pages passed
- Sensitive data leaks: none detected on tested product pages
- Raw template tags: none detected

Final release verification:

- Phase: Phase 16B Final Local Demo Release Tag
- Django check: passed
- Migration dry-run: `No changes detected`
- Demo seed command: passed and remained idempotent
- Route smoke tests: 42 routes passed
- Privacy scan: 32 public/owner/tenant product pages passed
- Sensitive data leaks: none detected on tested product pages
- Raw template tags: none detected
- Root legacy `/api/requests/` and `/fees/` remained unavailable

Final visual QA planning:

- Phase: Phase 17C Final Visual QA and Screenshot Checklist
- Browser page list: documented
- Desktop/mobile viewport checklist: documented
- Screenshot checklist: updated
- Video demo checklist: updated
- Security/privacy visual checklist: documented

Screenshot and video preparation:

- Phase: Phase 18A Screenshot Capture and Demo Video Preparation
- Pre-recording setup: documented
- Screenshot capture order: documented
- 3 to 5 minute video outline: documented
- Vietnamese narration script: documented
- Manual visual QA checklist: documented

Product-grade UI redesign:

- Phase: Phase 19A Product-Grade UI Redesign
- Landing page: redesigned
- Public room pages: redesigned
- Shared portal theme: redesigned
- Major owner/tenant pages: Vietnamese-first polish
- Error pages: refreshed

Detailed report:

```text
docs/demo/FINAL_DEMO_WALKTHROUGH_REPORT.md
```

## Remaining Limitations

RentEase is local-demo ready, but not production-ready.

Remaining production work:

- split or harden production settings
- configure production database
- configure deployment/static/media/email/logging
- improve owner-facing billing detail and utility entry workflows
- improve account lifecycle and onboarding
- add CI and automated test coverage
- decide long-term legacy cleanup strategy

## Safety Rules For Demo

- Use fake demo data only.
- Do not publish database files.
- Do not publish backup JSON files.
- Do not show `.env`, secrets, or local database paths.
- Do not show citizen ID values or citizen ID files/images.
- Do not show account/password/permission internals.
- Do not show private data from real users.

## Final Readiness Conclusion

RentEase is ready for a stronger local Python/Django course demo and presentation. The remaining demo task is browser visual review before final screenshots/video.

Recommended next step:

```text
Phase 19B: Browser Visual Review and Small UI Fixes
```

Alternative production track:

```text
Phase 14B-2: Production Settings Split Planning
```
