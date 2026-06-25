# Local Setup And Demo Data Guide

## Purpose

This guide is for teammates who download RentEase from GitHub ZIP and want to run the local demo.

RentEase code and RentEase database data are different things:

- Code is the Django project files.
- Database data is stored locally in `db.sqlite3`.
- A fresh ZIP download may not include your local demo database.

## Recommended Local Setup

Open PowerShell in the repository root, then go to the Django project folder:

```powershell
cd hostello_backend
```

Use the local virtual environment Python:

```powershell
.\venv\Scripts\python.exe manage.py check
```

Create database tables:

```powershell
.\venv\Scripts\python.exe manage.py migrate
```

Seed local demo data:

```powershell
.\venv\Scripts\python.exe manage.py seed_rentease_demo_data
```

Start the server:

```powershell
.\venv\Scripts\python.exe manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

## Migrate vs Createsuperuser vs Seed Demo Data

### `migrate`

Creates database tables such as rooms, listings, contracts, invoices, tenants, and users.

Run this when you see errors like:

```text
no such table: tin_phong
```

### `createsuperuser`

Creates only an admin account.

It does not create:

- rooms
- tenants
- contracts
- invoices
- room listings
- viewing registrations

So `/rooms/` may still be empty after `createsuperuser`.

### `seed_rentease_demo_data`

Creates fake local demo data for RentEase, including demo rooms, listings, contracts, billing, repairs, notifications, and viewings.

This command exists in:

```text
hostello_backend/portal/management/commands/seed_rentease_demo_data.py
```

Default demo accounts:

| Role | Username |
| --- | --- |
| Owner | `owner_test` |
| Tenant | `tenant_test` |

The seed command expects the demo accounts to exist. If they do not exist, ask Hoàng Nam for the current test database or create the accounts manually before seeding.

## Common Errors And Fixes

### `no such table: tin_phong`

Cause:

- database tables were not created yet.

Fix:

```powershell
.\venv\Scripts\python.exe manage.py migrate
```

### `owner_test does not exist`

Cause:

- demo account is missing in the local database.

Fix options:

1. Ask for the current local demo database if this is only for team demo.
2. Create owner/tenant accounts manually in admin.
3. Ask Hoàng Nam before changing account setup.

### `/rooms/` opens but no rooms appear

Cause:

- database tables exist, but there are no published room listings.

Fix:

```powershell
.\venv\Scripts\python.exe manage.py seed_rentease_demo_data
```

If the seed command cannot run, create data manually:

1. Create superuser.
2. Log in to `/admin/`.
3. Create an owner user and owner profile.
4. Create a room owned by that owner.
5. Create a published room listing.
6. Optional: create tenant, contract, invoice, payment, repair request, and viewing registration.

## If The Seed Command Is Missing

If this command fails because it does not exist:

```powershell
.\venv\Scripts\python.exe manage.py seed_rentease_demo_data
```

then use manual admin setup:

```powershell
.\venv\Scripts\python.exe manage.py createsuperuser
.\venv\Scripts\python.exe manage.py runserver
```

Then open `/admin/` and create demo records manually.

## About `db.sqlite3`

`db.sqlite3` is local demo data.

Important:

- It is not production data.
- It should not be used for real deployment.
- It should not be committed if it contains accounts or personal/demo data.
- Copying it between teammates is acceptable only for local demo and only if it contains no sensitive data.

## Safe Local Demo Checklist

- [ ] `manage.py check` passes
- [ ] `manage.py migrate` completed
- [ ] demo data exists
- [ ] `/rooms/` shows published rooms
- [ ] `owner_test` can log in
- [ ] `tenant_test` can log in
- [ ] no real citizen ID or real personal data is used
