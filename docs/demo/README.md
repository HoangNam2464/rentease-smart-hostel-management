# RentEase Local Demo Guide

RentEase is ready for a local demonstration, not a production deployment. This guide covers setup, fake demo data, the walkthrough, verification, and optional screenshots.

## Prerequisites

- Complete the environment and dependency setup in the root `README.md`.
- Use `backend/venv/` and run Django commands from `backend/`.
- Keep `DEBUG=True` and use only a disposable local database.
- Local users `owner_test` and `tenant_test` need their linked owner and tenant profiles before seeding.

If the demo users are missing, create a local superuser, open `/admin/`, and create the users and profiles with fake data.

## Prepare And Run

From the repository root:

```powershell
cd backend
.\venv\Scripts\python.exe manage.py check
.\venv\Scripts\python.exe manage.py migrate
.\venv\Scripts\python.exe manage.py seed_rentease_demo_data
.\venv\Scripts\python.exe manage.py runserver
```

Open `http://127.0.0.1:8000/`.

Common setup problems:

| Problem | Action |
|---|---|
| `no such table` | Run `manage.py migrate`. |
| Demo user or profile missing | Create the local fake account and linked profile in admin. |
| `/rooms/` is empty | Run the seed command and confirm it completes. |
| Seed command refuses to run | Confirm the environment is local with `DEBUG=True` and read the command error. |

## Seed Command

Preview without writing:

```powershell
.\venv\Scripts\python.exe manage.py seed_rentease_demo_data --dry-run --owner-username owner_test --tenant-username tenant_test
```

Create or refresh the fake Property, linked rooms, listings, contracts, invoices, payments, repairs, notifications, and viewing registrations:

```powershell
.\venv\Scripts\python.exe manage.py seed_rentease_demo_data --owner-username owner_test --tenant-username tenant_test
```

Reset known command-created records and seed them again:

```powershell
.\venv\Scripts\python.exe manage.py seed_rentease_demo_data --reset-demo-data --owner-username owner_test --tenant-username tenant_test
```

Do not run the command against production or valuable data. Never commit or share `db.sqlite3`, `.env`, uploaded media, database backups, credentials, citizen IDs, identity files, or real personal information.

## Walkthrough

### Visitor

1. Open `/` and `/rooms/`.
2. Select a visible published listing instead of relying on a fixed ID.
3. Open its detail and viewing-registration pages.
4. Submit a viewing request only when the local database may be changed.

### Owner

1. Sign in as `owner_test`.
2. Review the dashboard, rooms, tenants, contracts, invoices, repairs, and viewing registrations.
3. Confirm all displayed records belong to the signed-in owner.
4. Mutate rooms, invoices, payments, or requests only when demo data may be changed.

### Tenant

1. Sign in as `tenant_test`.
2. Review the dashboard, profile, contracts, invoices, payments, repairs, and notifications.
3. Confirm only the signed-in tenant's data is visible.

### Admin And Reports

1. Sign in with a local staff or superuser account.
2. Open `/admin/` and `/reports/`.
3. Confirm reports remain staff-only.
4. Confirm admin lists and searches do not expose citizen IDs or identity files.

## Verification Checklist

- [ ] `manage.py check` passes.
- [ ] `manage.py makemigrations --check --dry-run` reports `No changes detected`.
- [ ] Public pages load and protected pages redirect anonymous users.
- [ ] Owner and tenant pages enforce role and data boundaries.
- [ ] `/legacy/` remains isolated; old `/api/` and `/fees/` routes are unavailable.
- [ ] No secrets, real personal data, citizen IDs, or identity files are visible.
- [ ] Desktop around 1366px and mobile around 390px remain usable.
- [ ] Static assets load without broken layout or raw Django template syntax.

## Optional Screenshot Set

Capture the landing page, room list/detail, viewing form, owner dashboard and invoice flow, tenant dashboard and payment flow, admin/reports, and one mobile view. Before sharing, hide terminals, passwords, environment files, database paths, backups, and all private identity data.

Use `docs/ui/RENTEASE_PROFESSIONAL_DESIGN_SYSTEM.md` as the visual reference.
