# Final Demo Checklist

RentEase is ready for a local demo, but it is not production-ready. Run this checklist against the current local database before presenting or recording.

## Pre-Demo Setup

From the repository root:

```powershell
cd backend
.\venv\Scripts\python.exe manage.py check
.\venv\Scripts\python.exe manage.py makemigrations --check --dry-run
.\venv\Scripts\python.exe manage.py seed_rentease_demo_data
.\venv\Scripts\python.exe manage.py runserver
```

Open `http://127.0.0.1:8000/`. See `DEMO_DATA_SEED_USAGE.md` if the demo accounts or profiles are missing.

## Public Visitor Flow

1. Open `/` and `/rooms/`.
2. Select a visible published listing rather than relying on a fixed room ID.
3. Open its detail and viewing-registration pages.
4. Submit a viewing request only when it is safe to change the local demo database.

## Owner Flow

1. Sign in as `owner_test` when that local account is configured.
2. Open the dashboard, rooms, tenants, contracts, invoices, repairs, and viewing registrations.
3. Confirm that displayed records belong to the signed-in owner.
4. Create, update, or record a payment only when local demo data may be changed.

## Tenant Flow

1. Sign in as `tenant_test` when that local account is configured.
2. Open the dashboard, profile, contracts, invoices, payments, repairs, and notifications.
3. Confirm that only the signed-in tenant's data is visible.
4. Submit a repair request only when local demo data may be changed.

## Admin And Reports Flow

1. Sign in with a local staff/superuser account.
2. Open `/admin/` and `/reports/`.
3. Confirm reports remain staff-only.
4. Confirm admin lists and searches do not expose citizen IDs or identity files.

## Verification Before Presenting

- [ ] Django system check passes.
- [ ] Migration dry-run reports `No changes detected`.
- [ ] Public pages load and protected pages redirect anonymous users.
- [ ] Owner and tenant pages enforce role and data boundaries.
- [ ] `/legacy/` remains isolated; old `/api/` and `/fees/` routes are unavailable.
- [ ] No secrets, real personal data, citizen IDs, or identity files are visible.
- [ ] Static assets load without obvious layout errors.

## Known Limitations

- The demo uses local SQLite data and fake accounts; it is not a production deployment.
- Retained HOSTELLO apps and assets are outside normal RentEase demo work.
- Demo records can vary between local databases, so choose visible records instead of fixed numeric IDs.
