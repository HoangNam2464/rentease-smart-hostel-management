# Final Demo Checklist

Date: 2026-06-26

## Current Project Status

- Branch: `complete-product`
- Backend location: `backend/`
- Frontend location: `frontend/`
- Official virtual environment: `backend/venv/`
- Django config package: `backend/hostello_backend/`
- `DJANGO_SETTINGS_MODULE`: `hostello_backend.settings`
- Current structure: Django backend + Django Templates frontend + documentation folders
- Status: local demo ready

## Pre-Demo Setup

Run commands from the repository root:

```powershell
cd backend
.\venv\Scripts\python.exe manage.py check
.\venv\Scripts\python.exe manage.py makemigrations --check --dry-run
.\venv\Scripts\python.exe manage.py seed_rentease_demo_data
.\venv\Scripts\python.exe manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

## Public Visitor Demo Flow

1. Open the home page: `/`
2. Open the room listing page: `/rooms/`
3. Open one published Vietnamese demo room detail page from the `/rooms/` list.
4. Open that room's viewing registration form.
5. Submit a viewing registration only if safe in the local demo database.
6. Confirm the viewing registration success page.

## Owner Demo Flow

1. Login as `owner_test` if the account is available.
2. Open `/owner/dashboard/`.
3. View rooms at `/owner/rooms/`.
4. Create/update a room only if safe in the local demo database.
5. View tenants at `/owner/tenants/`.
6. View contracts at `/owner/contracts/`.
7. View invoices at `/owner/invoices/`.
8. Record a payment only if safe in the local demo database.
9. Check the payment status update on the invoice/payment views.

## Tenant Demo Flow

1. Login as `tenant_test` if the account is available.
2. Open `/tenant/dashboard/`.
3. View invoices at `/tenant/invoices/`.
4. View payment history at `/tenant/payments/`.
5. View contract/profile pages if needed.
6. Submit a maintenance request only if safe in the local demo database.

## Admin Demo Flow

1. Login as `admin_test` if the account is available.
2. Open `/admin/`.
3. Open `/reports/`.
4. Verify key models are visible in Django Admin/Jazzmin.
5. Verify tenant admin/search surfaces do not expose sensitive identity data such as citizen ID values or ID-card files.

## Smoke Test Result Table

| Route | Anonymous expected result | Authenticated expected result if applicable | Actual result | Status | Notes |
|---|---|---|---|---|---|
| `/` | 200 | N/A | 200 | Passed | Public landing page loads. |
| `/rooms/` | 200 | N/A | 200 | Passed | Public listings page loads. |
| Published room detail | 200 if published demo listing exists | N/A | 200 | Passed | Use a published room from `/rooms/` instead of a hard-coded ID. |
| Published room registration form | 200 if published demo listing exists | N/A | 200 | Passed | Viewing registration form loads for the selected room. |
| Published room registration success | 200 if published demo listing exists | N/A | 200 | Passed | Success page loads for the selected room. |
| `/login/` | 200 | N/A | 200 | Passed | Portal login page loads. |
| `/legacy/login/` | 200 | N/A | 200 | Passed | Legacy route remains isolated under `/legacy/`. |
| `/admin/` | Redirect to login | 200 as `admin_test` | 302 anonymous, 200 admin | Passed | Admin remains protected. |
| `/reports/` | Redirect to admin login | 200 as `admin_test` | 302 anonymous, 200 admin | Passed | Reports remain staff-protected. |
| `/owner/dashboard/` | Redirect to login | 200 as `owner_test` | 302 anonymous, 200 owner | Passed | Owner route protected and loads when authenticated. |
| `/owner/rooms/` | Redirect to login | 200 as `owner_test` | 302 anonymous, 200 owner | Passed | Owner rooms load. |
| `/owner/tenants/` | Redirect to login | 200 as `owner_test` | 302 anonymous, 200 owner | Passed | Owner tenants load. |
| `/owner/contracts/` | Redirect to login | 200 as `owner_test` | 302 anonymous, 200 owner | Passed | Owner contracts load. |
| `/owner/invoices/` | Redirect to login | 200 as `owner_test` | 302 anonymous, 200 owner | Passed | Owner invoices load. |
| `/tenant/dashboard/` | Redirect to login | 200 as `tenant_test` | 302 anonymous, 200 tenant | Passed | Tenant route protected and loads when authenticated. |
| `/tenant/invoices/` | Redirect to login | 200 as `tenant_test` | 302 anonymous, 200 tenant | Passed | Tenant invoices load. |
| `/tenant/payments/` | Redirect to login | 200 as `tenant_test` | 302 anonymous, 200 tenant | Passed | Tenant payments load. |

## Known Safe Limitations

- Legacy apps `students`, `attendance`, `fees`, `requests`, and `notices` are still kept because they are installed and have models, migrations, admin registrations, and cross-imports.
- Legacy templates/static files are kept because some are still referenced by `/legacy/` routes or old admin/views.
- `assets/` is kept as historical HOSTELLO media for now.
- Root `venv/` was removed; use `backend/venv/` only.
- This phase does not change code, models, schema, templates, static files, or business logic.
- Authenticated smoke tests used existing local accounts: `admin_test`, `owner_test`, and `tenant_test`.

## Final Demo Readiness

The project is ready for local demo based on this smoke test:

- Django system check passed.
- Migration dry-run reported `No changes detected`.
- Public routes loaded successfully.
- Anonymous protected routes redirected as expected.
- Admin, owner, and tenant authenticated smoke routes loaded successfully.
- No runtime route failure was found in this checklist.

Before recording or presenting, run the pre-demo setup commands again and confirm the local database still contains the expected demo data.
