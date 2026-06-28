# Local Setup And Demo Data Guide

Use this guide after obtaining the RentEase source. Complete the environment and dependency setup in the root `README.md` first; the commands below assume `backend/venv/` is ready.

## Start A Local Demo

From the repository root:

```powershell
cd backend
.\venv\Scripts\python.exe manage.py check
.\venv\Scripts\python.exe manage.py migrate
.\venv\Scripts\python.exe manage.py seed_rentease_demo_data
.\venv\Scripts\python.exe manage.py runserver
```

Then open `http://127.0.0.1:8000/`.

`migrate` creates the database tables. `createsuperuser` creates an admin login only. The seed command creates the fake rooms, listings, contracts, billing, repairs, notifications, and viewing requests needed for the walkthrough.

## Demo Account Prerequisites

By default, the seed command expects local users named `owner_test` and `tenant_test` with their linked owner and tenant profiles. If they are missing:

1. Create a local superuser with `manage.py createsuperuser`.
2. Open `/admin/` and create the demo users and required profiles using fake data.
3. Run the seed command again.

Do not obtain setup by committing, publishing, or casually sharing a populated `db.sqlite3` file.

## Common Problems

| Problem | Action |
|---|---|
| `no such table` | Run `manage.py migrate`. |
| Demo user or profile is missing | Create the local fake account and linked profile in admin. |
| `/rooms/` is empty | Run the seed command and confirm it completes successfully. |
| Seed command refuses to run | Confirm this is a local `DEBUG=True` environment and review its error message. |

## Local Data Rules

- `backend/db.sqlite3` is local runtime data, not source or production data.
- Never commit `.env`, SQLite databases, uploaded media, backups, or real personal information.
- Prefer migrations plus the seed command for reproducible setup.
- Use only fake credentials and fake identity details in demo records.

## Ready Check

- [ ] `manage.py check` passes.
- [ ] Migrations are applied locally.
- [ ] Demo data seeds without errors.
- [ ] `/rooms/` shows published listings.
- [ ] Owner and tenant demo accounts can sign in and see only their own data.
- [ ] No real citizen ID or personal data is present.
