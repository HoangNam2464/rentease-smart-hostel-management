# RentEase

RentEase is a Django-based web application for managing rental rooms, tenants, contracts, billing, maintenance requests, room listings, viewing registrations, and demo reports.

The project was migrated from the original HOSTELLO codebase into a RentEase MVP suitable for a course project and stable final demo.

## Tech Stack

- Python
- Django
- SQLite
- Django Admin
- Jazzmin admin theme

## MVP Features

- Account and owner management
- Room management
- Tenant management
- Co-tenant management
- Contract management
- Billing, invoice, and payment tracking
- Repair requests
- Maintenance records
- Internal notifications
- Room listings
- Viewing registrations
- Reports dashboard

## Installation

1. Create and activate a virtual environment.

```powershell
python -m venv venv
.\venv\Scripts\activate
```

2. Install dependencies.

```powershell
cd hostello_backend
pip install -r requirements.txt
```

3. Run migrations.

```powershell
python manage.py migrate
```

4. Create a superuser.

```powershell
python manage.py createsuperuser
```

5. Start the development server.

```powershell
python manage.py runserver
```

## Main URLs

- Django Admin: `http://127.0.0.1:8000/admin/`
- Reports Dashboard: `http://127.0.0.1:8000/reports/`

## Demo Account Note

Create a demo superuser with `python manage.py createsuperuser`.

Use demo data only. Do not use real tenant identity information, real phone numbers, real citizen IDs, or real payment records.

## Phase Summary

- Phase 1 Rental Core: accounts, owner profiles, rooms, tenants, co-tenants, contracts
- Phase 2 Billing: price configuration, invoices, invoice details, payment history
- Phase 3 Maintenance: repair requests, maintenance records, notifications
- Phase 4 Listings: room listings and viewing registrations
- Phase 5 Reports: admin-only dashboard and report pages

## Folder Structure

```text
hostello_backend/
  accounts/       User and owner profile models
  properties/     Room management
  tenants/        Tenant and co-tenant management
  contracts/      Rental contracts
  billing/        Price config, invoices, payments
  maintenance/    Repair, maintenance, notifications
  listings/       Room listings and viewing registrations
  reports/        Admin-only dashboard and report pages
  hostello_backend/
    settings.py
    urls.py
```

Legacy HOSTELLO apps remain in the repository for compatibility:

```text
students/
attendance/
fees/
requests/
notices/
```

## Security Notes

- Do not commit `.env` files.
- Do not commit `db.sqlite3` for public repositories.
- Do not commit `backup_phase*.json` because dumps may contain password hashes and personal data.
- Use environment variables for production `SECRET_KEY`, email credentials, and payment credentials.
- Rotate demo/admin passwords if database backups were ever exposed publicly.

## Final Demo Docs

- `DEMO_SCRIPT.md`
- `PROJECT_SUMMARY.md`
- `docs/demo-checklist.md`
- `docs/screenshots-checklist.md`
- `docs/security-notes.md`
