# RentEase Demo Data Seed Implementation Notes

## Phase

Phase 15E: Safe Demo Data Seed Implementation

## Implementation Choice

Use a Django management command in the existing `portal` app:

```text
portal.management.commands.seed_rentease_demo_data
```

Reason:

- the seed is for portal/demo walkthroughs
- no model ownership changes are needed
- no migrations or schema changes are needed
- command discovery works through the existing installed `portal` app

## Command

```powershell
.\venv\Scripts\python.exe manage.py seed_rentease_demo_data --dry-run --owner-username owner_test --tenant-username tenant_test
.\venv\Scripts\python.exe manage.py seed_rentease_demo_data --owner-username owner_test --tenant-username tenant_test
```

Optional reset:

```powershell
.\venv\Scripts\python.exe manage.py seed_rentease_demo_data --reset-demo-data --owner-username owner_test --tenant-username tenant_test
```

## Safety Guards

- fail unless `settings.DEBUG` is true
- fail if `owner_test` or `tenant_test` is missing
- fail if owner profile or tenant profile is missing
- never create real users
- never create citizen ID files or repair image files
- never delete non-demo data
- reset only known demo-prefixed records
- dry-run must not write database data

## Demo Data Strategy

Create/update fake records using stable `DEMO-` identifiers:

- `DEMO-R001` to `DEMO-R005` rooms
- `DEMO-LIST-*` listing titles
- `DEMO-CTR-*` contracts
- fake tenants with `DEMO-TENANT-*` citizen IDs
- demo invoices, invoice details, and payments
- demo repairs and notifications
- demo viewing registrations

Use existing model validation by calling `full_clean()` or model `save()` methods where model logic already enforces calculations.

## Verification Targets

After seeding:

- public rooms show at least 3 demo published listings
- owner dashboard has room, contract, invoice, payment, repair, listing, and viewing metrics
- tenant dashboard has current contract, invoice/payment, repairs, and notifications
- owner and tenant list/detail routes have scoped demo records
- legacy root `/api/requests/` and `/fees/` remain unavailable

