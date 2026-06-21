# RentEase - Python/Django Boarding House Management System

RentEase is a Django web application for managing boarding-house rooms, listings, tenants, contracts, invoices, payments, repairs, and viewing registrations.

The project started from the original HOSTELLO codebase and has been reshaped into a role-based RentEase application for a Python/Django course demo. It is local-demo ready, with polished public, owner, tenant, admin, and report surfaces.

## Current Status

- Local demo ready.
- UI polished for public, owner, and tenant flows.
- Safe local demo data seed command available.
- Final demo walkthrough verified in Phase 15F.
- Final polished local demo release verified in Phase 16B.
- Not production-ready yet.

Final local demo release tag:

```text
release-rentease-polished-local-demo-v2
```

Known production gaps:

- production settings are not hardened
- production database is not configured
- deployment/static/media/email/logging are not production-ready
- owner-facing billing detail and utility workflows need more work for real deployment
- account lifecycle and onboarding are incomplete
- legacy HOSTELLO apps still exist, though root legacy API/fees routes are removed

## User Roles

| Role | Purpose |
| --- | --- |
| Public visitor | Browse published rooms and submit viewing registrations |
| Owner | Manage owned rooms, listings, tenants, contracts, invoices, payments, repairs, and viewing registrations |
| Tenant | View own profile, contracts, invoices, payments, repairs, and notifications |
| Admin/Staff | Use Django Admin and staff-only reports |

## Main Features

### Public

- Landing page
- Room browsing
- Room detail page
- Viewing registration form

### Owner

- Owner dashboard
- Room management
- Listing management
- Linked tenant views and safe updates
- Contract create/update
- Invoice create/update
- Payment recording
- Repair request processing
- Viewing registration processing

### Tenant

- Tenant dashboard
- Tenant profile
- Contract views
- Invoice views
- Payment history
- Repair request views and submission
- Notifications

### Admin And Reports

- Django Admin with RentEase branding
- Staff-only reports dashboard
- Billing, room, tenant/contract, maintenance, and listing reports

## Tech Stack

- Python
- Django
- SQLite for local development
- Django templates and Bootstrap-style UI
- Django Admin and Jazzmin
- Django management command for safe demo data

Do not assume PostgreSQL, CI, SonarQube, or automated coverage exists unless those items are later implemented and verified.

## Project Structure

```text
hostello_backend/
  accounts/       User and owner profile models
  properties/     Room management
  tenants/        Tenant and co-tenant management
  contracts/      Rental contracts
  billing/        Price config, invoices, invoice details, payments
  maintenance/    Repair requests, maintenance records, notifications
  listings/       Public listings and viewing registrations
  portal/         Public login and owner/tenant portal pages
  reports/        Staff-only report pages
  hostello_backend/
    settings.py
    urls.py
```

Legacy HOSTELLO apps remain in the repository but are not the main RentEase demo path:

```text
students/
attendance/
fees/
requests/
notices/
```

Legacy routes are isolated under `/legacy/`. Root legacy API and fees routes such as `/api/requests/` and `/fees/` have been removed.

## Setup For Local Development

From the repository root:

```powershell
cd hostello_backend
```

Create and activate a virtual environment if one is not already available:

```powershell
py -m venv venv
.\venv\Scripts\activate
```

Install dependencies:

```powershell
.\venv\Scripts\python.exe -m pip install -r requirements.txt
```

Run migrations if needed:

```powershell
.\venv\Scripts\python.exe manage.py migrate
```

Run project checks:

```powershell
.\venv\Scripts\python.exe manage.py check
.\venv\Scripts\python.exe manage.py makemigrations --check --dry-run
```

Start the local development server:

```powershell
.\venv\Scripts\python.exe manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

## Main Local URLs

| Area | URL |
| --- | --- |
| Public landing | `http://127.0.0.1:8000/` |
| Public rooms | `http://127.0.0.1:8000/rooms/` |
| Login | `http://127.0.0.1:8000/login/` |
| Owner dashboard | `http://127.0.0.1:8000/owner/dashboard/` |
| Tenant dashboard | `http://127.0.0.1:8000/tenant/dashboard/` |
| Django Admin | `http://127.0.0.1:8000/admin/` |
| Staff reports | `http://127.0.0.1:8000/reports/` |
| Legacy prefix | `http://127.0.0.1:8000/legacy/` |

## Demo Data

RentEase includes a local-only seed command for fake demo records.

Dry run first:

```powershell
.\venv\Scripts\python.exe manage.py seed_rentease_demo_data --dry-run --owner-username owner_test --tenant-username tenant_test
```

Seed data:

```powershell
.\venv\Scripts\python.exe manage.py seed_rentease_demo_data --owner-username owner_test --tenant-username tenant_test
```

The seed command is intended for local demo databases only. It is idempotent, creates fake `DEMO-` records, and should not create migrations or schema changes.

A reset option exists, but use it carefully because it deletes command-created demo records before recreating them:

```powershell
.\venv\Scripts\python.exe manage.py seed_rentease_demo_data --reset-demo-data --owner-username owner_test --tenant-username tenant_test
```

Do not commit database files after seeding.

## Local Demo Accounts

These accounts are for local demo only:

| Role | Username | Password |
| --- | --- | --- |
| Admin | `admin_test` | `Test@12345` |
| Owner | `owner_test` | `Test@12345` |
| Tenant | `tenant_test` | `Test@12345` |

Do not use these credentials in production. Do not show passwords in screenshots or recorded videos.

## 3 To 5 Minute Demo Flow

1. Open `/` and introduce RentEase.
2. Open `/rooms/` and show published room listings.
3. Open one room detail page and the viewing registration form.
4. Log in as `owner_test`.
5. Show owner dashboard metrics.
6. Open owner rooms, contracts, invoices, payment recording, repairs, and viewing registrations.
7. Log out and log in as `tenant_test`.
8. Show tenant dashboard, profile, contracts, invoices, payments, repairs, and notifications.
9. Mention that `/reports/` is staff-only and legacy pages are isolated under `/legacy/`.

Full script:

```text
docs/demo/DEMO_SCRIPT.md
```

## Phase 15F Verification Summary

The final demo walkthrough verification passed with seeded local data:

- Django check passed.
- Migration dry-run reported `No changes detected`.
- 53 route smoke tests passed.
- 28 public/owner/tenant privacy scan pages passed.
- No sensitive leaks were detected on tested public, owner, or tenant product pages.
- No raw Django template tags were detected.
- Local demo is ready.

Final local demo release verification in Phase 16B also passed:

- Django check passed.
- Migration dry-run reported `No changes detected`.
- Demo seed command reran successfully.
- 42 final route smoke tests passed.
- 32 public/owner/tenant product pages passed privacy scanning.
- Root legacy `/api/requests/` and `/fees/` remained unavailable.

## Documentation Map

| Path | Purpose |
| --- | --- |
| `AGENTS.md` | Agent rules and project safety instructions |
| `docs/agent/` | Current state, next action, workflow, security rules, and autonomous work notes |
| `docs/spqm/` | Process, quality, backlog, metrics, and release checklists |
| `docs/demo/` | Demo script, seed usage, walkthrough report, screenshot checklist, final demo package |
| `docs/ui/` | UI regression and demo readiness notes |

## Safety Notes

- Use fake local demo data only.
- Do not use or publish real personal data.
- Do not show citizen ID values.
- Do not show citizen ID images/files.
- Do not show `.env`, `SECRET_KEY`, database paths, or backup files.
- Do not commit `db.sqlite3`, `*.sqlite3`, backup JSON files, `.env`, or uploaded local media.
- Do not expose auth/password/permission fields.
- Do not expose owner-only or tenant-only private data to public pages.

## Final Demo Package

See:

```text
docs/demo/FINAL_DEMO_PACKAGE.md
```

Recommended next step after this polished local demo release:

```text
Track A: Capture screenshots and record demo video
```

Alternative production track:

```text
Phase 14B-2: Production Settings Split Planning
```
