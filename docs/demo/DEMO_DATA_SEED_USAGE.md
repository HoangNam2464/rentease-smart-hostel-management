# RentEase Demo Data Seed Usage

## Command Name

```text
seed_rentease_demo_data
```

## Purpose

Create safe local-only fake demo data for RentEase public, owner, and tenant walkthroughs.

The command is intended for local demo databases only.

## Safety Notes

- Requires `DEBUG=True`.
- Uses existing `owner_test` and `tenant_test` accounts by default.
- Fails if required users or linked profiles are missing.
- Creates fake `DEMO-` records only.
- Does not upload or reference citizen ID image/file fields.
- Does not create migrations.
- Does not change schema.
- Does not commit database files.
- Reset mode deletes only command-created demo-prefixed records.

## Dry Run

Use dry-run before writing data:

```powershell
.\venv\Scripts\python.exe manage.py seed_rentease_demo_data --dry-run --owner-username owner_test --tenant-username tenant_test
```

Expected:

- no database writes
- summary of records that would be created or updated

## Seed Demo Data

```powershell
.\venv\Scripts\python.exe manage.py seed_rentease_demo_data --owner-username owner_test --tenant-username tenant_test
```

Expected:

- creates or updates demo rooms, listings, contracts, billing records, repairs, notifications, and viewing registrations
- can be safely run multiple times without duplicate demo records

## Reset Demo Data

Use only when you intentionally want to remove the generated demo records:

```powershell
.\venv\Scripts\python.exe manage.py seed_rentease_demo_data --reset-demo-data --owner-username owner_test --tenant-username tenant_test
```

Expected:

- deletes only known `DEMO-` / `INV-DEMO-` command-created records
- recreates the demo data after reset
- does not delete `admin_test`, `owner_test`, `tenant_test`, or non-demo records

## Expected Demo Accounts

| Role | Username |
| --- | --- |
| Admin | `admin_test` |
| Owner | `owner_test` |
| Tenant | `tenant_test` |

## Data Created

The command creates or updates:

- 5 demo rooms for `owner_test`
- 3 published demo room listings
- 2 internal demo listings
- 2 demo contracts
- 2 demo invoices
- 2 invoice detail rows
- 2 demo payment records
- 2 repair requests
- 2 tenant notifications
- 3 viewing registrations
- 1 demo-only second tenant

## What Not To Commit

Do not commit:

- `db.sqlite3`
- any `*.sqlite3` file
- backup JSON files
- uploaded media files
- `.env` files
- local screenshots containing secrets or real personal data

## Verification After Seeding

Open:

```text
/
/rooms/
/owner/dashboard/
/owner/rooms/
/owner/contracts/
/owner/invoices/
/owner/repairs/
/owner/viewing-registrations/
/tenant/dashboard/
/tenant/contracts/
/tenant/invoices/
/tenant/payments/
/tenant/repairs/
/tenant/notifications/
```

Confirm:

- owner pages show owner-scoped demo data
- tenant pages show tenant-scoped demo data
- public room browsing shows demo listings
- no citizen ID values/files are shown in demo pages

## Phase 15F Walkthrough Verification

Phase 15F reran the seed command and verified the local demo flow with:

- 5 owner demo rooms
- at least 3 published demo listings
- 2 owner demo contracts
- 2 owner demo invoices
- 2 demo payment records
- 2 demo repair requests
- 2 tenant notifications
- 3 viewing registrations

The current local database may contain additional published listings from earlier tests. For presentation, open `/rooms/` and select a visible published demo listing instead of relying on a fixed numeric ID.
