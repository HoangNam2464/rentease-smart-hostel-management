# RentEase Documentation Index

This folder contains the working documentation for RentEase, a Django-based boarding-house / rental-room management system.

RentEase is currently **local-demo ready**, but it is **not production-ready yet**.

## Recommended Reading Order

For demo, submission, or onboarding, read in this order:

1. `README.md`
2. `docs/architecture/PROJECT_STRUCTURE_MAP.md`
3. `docs/demo/FINAL_DEMO_CHECKLIST.md`
4. `docs/demo/DEMO_DATA_SEED_USAGE.md`
5. `docs/demo/LOCAL_SETUP_AND_DEMO_DATA.md`
6. `docs/architecture/LEGACY_DEPENDENCY_AUDIT.md`
7. `docs/architecture/HELPER_FILE_CLEANUP.md`
8. `docs/security/PHASE_20N_ADMIN_SEARCH_PRIVACY_HARDENING.md`

## Main Documentation Areas

| Folder | Purpose |
|---|---|
| `docs/architecture/` | Project structure, cleanup audits, legacy dependency notes |
| `docs/demo/` | Demo setup, seed data, final demo checklist, walkthrough docs |
| `docs/security/` | Privacy and admin exposure hardening notes |
| `docs/spqm/` | Software process and quality management documentation |
| `docs/ui/` | Current UI/design system documentation and selected UI audit outputs |
| `docs/agent/` | Agent operating rules and current project state |
| `docs/archive/` | Old phase logs, old plans, helper files, and local ignored backup archive |

## Current Runtime Layout

```text
backend/   # Django backend, apps, manage.py, settings
frontend/  # Django templates and static assets
docs/      # Documentation
```

Official virtual environment:

```text
backend/venv/
```

Run Django commands from `backend/`:

```powershell
.\venv\Scripts\python.exe manage.py check
.\venv\Scripts\python.exe manage.py makemigrations --check --dry-run
```

## Important Notes

- The inner Django config package remains `backend/hostello_backend/`.
- `DJANGO_SETTINGS_MODULE` remains `hostello_backend.settings`.
- Legacy HOSTELLO apps still exist and should not be deleted without a dedicated dependency/removal plan.
- Historical phase logs and old plans are archived, not deleted.
- Demo data must remain fake/local-only and must not include real citizen identity data.

