# RentEase Demo Data Seed Usage

The `seed_rentease_demo_data` command creates fake local data for public, owner, and tenant walkthroughs. Use it only with a local demo database.

## Prerequisites

- Run commands from `backend/` with `backend/venv/`.
- `DEBUG` must be enabled.
- Local users `owner_test` and `tenant_test` must exist with their required owner and tenant profiles.

## Preview Changes

```powershell
.\venv\Scripts\python.exe manage.py seed_rentease_demo_data --dry-run --owner-username owner_test --tenant-username tenant_test
```

Dry-run reports the intended changes without writing to the database.

## Create Or Refresh Demo Data

```powershell
.\venv\Scripts\python.exe manage.py seed_rentease_demo_data --owner-username owner_test --tenant-username tenant_test
```

The command is designed to be repeatable. It creates or updates demo rooms, listings, contracts, invoices, payments, repairs, notifications, and viewing registrations.

## Reset Command-Created Records

```powershell
.\venv\Scripts\python.exe manage.py seed_rentease_demo_data --reset-demo-data --owner-username owner_test --tenant-username tenant_test
```

Reset removes known command-created demo records and recreates them. It should not remove the demo accounts or unrelated records; review the command output before relying on a shared local database.

## Safety Rules

- Use fake data only; never seed real citizen IDs, identity files, or private personal data.
- The command does not create migrations or change the schema.
- Do not commit or share `db.sqlite3`, `.env`, uploaded media, database backups, or screenshots containing secrets.
- Do not use this command against a production or otherwise valuable database.

## Verify The Demo

Check `/rooms/`, the owner portal, and the tenant portal. Confirm that public listings are visible, owner data is owner-scoped, tenant data is tenant-scoped, and no citizen identity values or files appear.
