# Cleanup Audit

## Purpose

This document summarizes safe cleanup work completed after the RentEase backend/frontend restructure.

The cleanup work did not change models, migrations, database schema, permissions, business logic, templates, static runtime files, or legacy app code.

For detailed dependency findings, see:

- `docs/architecture/LEGACY_DEPENDENCY_AUDIT.md`
- `docs/architecture/HELPER_FILE_CLEANUP.md`

## Completed Cleanup

### Generated Python Cache Cleanup

Generated `__pycache__/` folders were removed from project code folders in a previous cleanup pass.

Virtual environment folders were not edited as part of cache cleanup. The official venv is:

```text
backend/venv/
```

### Root Virtual Environment Cleanup

The old root-level `venv/` was removed after `backend/venv/` was verified working.

Current rule:

- Use `backend/venv/`.
- Do not recreate or use a root-level `venv/`.

### Helper File Cleanup

Completed helper archive:

```text
Working.py -> docs/archive/Working.py
run_frontend.bat -> docs/archive/run_frontend.bat
```

Local backup JSON files were moved to:

```text
docs/archive/local-backups/
```

These backup JSON files are ignored/local and should not be committed.

### Documentation Consolidation

Old phase logs and old planning/checklist documents may be archived under:

```text
docs/archive/phase-history/
docs/archive/old-plans/
```

Do not delete useful history permanently during cleanup phases. Archive first.

## Still Kept Intentionally

### Legacy Django Apps

The following legacy HOSTELLO apps remain installed and must not be deleted casually:

```text
backend/students/
backend/attendance/
backend/fees/
backend/requests/
backend/notices/
```

Reason:

- They still have models.
- They still have migrations.
- They still have admin registrations.
- They still have cross-app imports.
- `students.urls` is still mounted under `/legacy/`.

Deletion requires a dedicated removal plan covering migrations, contenttypes, admin, data, and URL behavior.

### Legacy Templates And Static Files

The following areas remain because some are still referenced by `/legacy/` routes or legacy admin/views:

```text
frontend/templates/index.html
frontend/templates/login.html
frontend/templates/dashboard.html
frontend/templates/admin/
frontend/templates/payments/success.html
frontend/static/css/styles.css
frontend/static/css/student-dashboard.css
frontend/static/js/script.js
frontend/static/js/student-dashboard.js
```

Do not delete these without a separate template/static dependency audit.

### Historical Media

`assets/` is kept for now as historical tracked HOSTELLO screenshots/video.

Reason:

- It is not runtime-critical, but it is tracked history.
- Moving it would create a large rename.
- Documentation may still refer to historical media.

Recommendation:

- Keep `assets/` until a dedicated historical media archive phase is approved.

## Safe To Clean Later

Only after review:

- Archive or remove old historical media under `assets/`.
- Archive remaining outdated phase logs.
- Consolidate old demo/checklist docs into current `docs/demo/FINAL_DEMO_CHECKLIST.md`.
- Remove or isolate legacy apps only after a dedicated dependency and migration/contenttypes plan.

## Do Not Delete Without Dedicated Plan

- `backend/manage.py`
- `backend/hostello_backend/`
- Active RentEase apps
- Legacy apps with models/migrations
- `frontend/templates/`
- `frontend/static/`
- `backend/media/`
- `backend/db.sqlite3` unless intentionally resetting local demo data
- `backend/venv/`

## Current Recommendation

Cleanup is in a safe state for local demo.

Next safe improvement:

```text
Realistic Demo Data Polish
```

Goal: keep the existing seeded demo coverage but make room names, listing copy, tenant names, invoices, repairs, and viewing registrations feel more realistic for presentation.

