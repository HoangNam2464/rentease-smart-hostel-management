# Cleanup Audit

## 1. Purpose

This document is an audit-only cleanup report for RentEase before any real file cleanup, template migration, static migration, or backend/frontend reorganization.

No files were deleted, moved, renamed, or refactored in this audit phase. The goal is to identify old, unclear, duplicated, legacy, or temporary files so future cleanup can happen safely in small reviewed phases.

## 2. Safe To Delete Immediately

These items are usually safe to delete later because they are generated cache or temporary files. They were not deleted in this phase.

- `__pycache__/` folders under project apps.
- `*.pyc` files under project apps.
- `.pytest_cache/` if it appears later.
- `.coverage` if it appears later.
- Local log files such as `*.log` if they appear later and are not needed for debugging.

Notes:

- Cache/temp files also exist under local virtual environments such as `venv/` and `hostello_backend/venv/`. The better cleanup action is usually to keep virtual environments ignored by Git rather than manually cleaning package internals.
- Do not delete migration files even if they are Python files.

## 3. Needs Manual Review

These files or folders may be unused, old, duplicated, or local-only, but they need human confirmation before cleanup.

- `assets/`
  - Contains original HOSTELLO screenshots and `Hostello_Project_Working_Demo.mp4`.
  - May be useful for historical documentation, but not part of the active RentEase UI.
- `run_backend.bat`
  - Could be a helper script, but should be reviewed against the current `hostello_backend/manage.py` flow.
- `run_frontend.bat`
  - The project currently uses Django Templates, not React. This may be old or misleading.
- `Working.py`
  - Unclear root-level Python file. Needs review before removal.
- `backup_phase2.json`, `backup_phase3.json`, `backup_phase4.json`, `backup_phase5.json`
  - Local backup/demo data files. Should not be committed if they contain account or demo data.
- `hostello_backend/phase8b2_wip.patch`
  - Old work-in-progress patch file. Needs confirmation before deletion.
- `hostello_backend/static/css/styles.css`
  - Appears related to old HOSTELLO public UI.
- `hostello_backend/static/js/script.js`
  - Appears related to old HOSTELLO public/login UI.
- `hostello_backend/templates/payments/success.html`
  - Referenced by legacy `fees/views.py`, so do not delete without reviewing legacy behavior.

## 4. Do Not Delete

These files/folders are important and must not be deleted during cleanup.

- `hostello_backend/manage.py`
- `hostello_backend/hostello_backend/settings.py`
- `hostello_backend/hostello_backend/urls.py`
- `hostello_backend/accounts/`
- `hostello_backend/properties/`
- `hostello_backend/tenants/`
- `hostello_backend/contracts/`
- `hostello_backend/billing/`
- `hostello_backend/maintenance/`
- `hostello_backend/listings/`
- `hostello_backend/portal/`
- `hostello_backend/reports/`
- All `migrations/` folders and migration files.
- All `models.py` files.
- `hostello_backend/templates/portal/`
- `hostello_backend/templates/listings/`
- `hostello_backend/reports/templates/reports/`
- `hostello_backend/static/css/rentease-design.css`
- `hostello_backend/static/css/rentease-layout.css`
- `hostello_backend/static/admin/css/custom_admin.css`
- `hostello_backend/media/`
- `hostello_backend/db.sqlite3`
  - Do not commit it, but do not delete local databases without explicit approval.
- `docs/`
- `AGENTS.md`
- `README.md`
- `frontend/`
  - New prepared folder structure for future templates/static organization.

Do not delete or modify permission checks, owner-scoped querysets, tenant-scoped querysets, billing calculations, or privacy hardening behavior during cleanup.

## 5. Possibly Unused Templates

These templates appear to be legacy, old, or unclear. They must be reviewed before deletion because some are still referenced by legacy views/admin.

- `hostello_backend/templates/index.html`
  - Referenced by `students/views.py` for legacy registration.
- `hostello_backend/templates/login.html`
  - Referenced by `students/views.py` for legacy student login.
- `hostello_backend/templates/dashboard.html`
  - Referenced by `students/views.py` for legacy student dashboard.
- `hostello_backend/templates/admin/attendance_management.html`
  - Legacy attendance admin template.
- `hostello_backend/templates/admin/assign_room.html`
  - Referenced by `students/admin.py`.
- `hostello_backend/templates/admin/request_management.html`
  - Legacy request admin template.
- `hostello_backend/templates/admin/fees/board.html`
  - Referenced by `fees/views.py` and fee admin templates.
- `hostello_backend/templates/admin/fees/feemonth/change_list.html`
  - Legacy/admin fee template.
- `hostello_backend/templates/payments/success.html`
  - Referenced by legacy `fees/views.py`.

Active templates that should not be treated as unused:

- `hostello_backend/templates/home.html`
- `hostello_backend/templates/404.html`
- `hostello_backend/templates/500.html`
- `hostello_backend/templates/listings/*`
- `hostello_backend/templates/portal/*`
- `hostello_backend/reports/templates/reports/*`

## 6. Possibly Unused Static Files

These static files may be legacy or unclear:

- `hostello_backend/static/css/styles.css`
  - HOSTELLO-era styling.
- `hostello_backend/static/css/student-dashboard.css`
  - Used by legacy `templates/dashboard.html`.
- `hostello_backend/static/js/script.js`
  - HOSTELLO-era JavaScript.
- `hostello_backend/static/js/student-dashboard.js`
  - Student dashboard JavaScript.
- `assets/*.png`
  - HOSTELLO screenshots and documentation images.
- `assets/Hostello_Project_Working_Demo.mp4`
  - HOSTELLO demo video.

Active/static files that should not be removed:

- `hostello_backend/static/css/rentease-design.css`
- `hostello_backend/static/css/rentease-layout.css`
- `hostello_backend/static/admin/css/custom_admin.css`
- `frontend/static/**/.gitkeep`

Potential static issue to review later:

- `hostello_backend/templates/payments/success.html` references `{% static 'css/site.css' %}`, but `site.css` was not found in the current static listing. This belongs to the legacy fees/payment area and should be reviewed before any cleanup.

## 7. Possibly Unused Python Code / Imports

These are suspicious or legacy code areas. They were not edited.

- `hostello_backend/hostello_backend/urls.py`
  - Contains commented `# from fees.admin import FeesAdminSite`.
  - Contains `from fees import admin as fees_admin`, which appears unused in the current URL file.
- `hostello_backend/students/views.py`
  - Contains many `print()` debug statements and HOSTELLO-era messages.
- `hostello_backend/attendance/admin.py`
  - Contains many debug `print()` statements and HOSTELLO email content.
- `hostello_backend/requests/views.py`
  - Contains debug `print()` statements, including old request handling logs.
- `hostello_backend/requests/admin.py`
  - Contains debug/notification `print()` statements.
- `hostello_backend/requests/models.py`
  - Contains print-based notification logging.
- `hostello_backend/fees/views.py`
  - Contains TODO around real attendance write behavior.
- `hostello_backend/attendance/utils.py`
  - Uses `HOSTELLO_EMAIL_SETTINGS`.
- `hostello_backend/attendance/signals.py`
  - Uses legacy HOSTELLO absence notification settings.

These areas may still be needed for legacy `/legacy/` behavior. Do not edit or delete without a separate legacy dependency audit.

## 8. Legacy HOSTELLO Areas

These apps and files appear to belong mostly to the original HOSTELLO project:

- `hostello_backend/students/`
- `hostello_backend/attendance/`
- `hostello_backend/fees/`
- `hostello_backend/requests/`
- `hostello_backend/notices/`
- `hostello_backend/templates/index.html`
- `hostello_backend/templates/login.html`
- `hostello_backend/templates/dashboard.html`
- `hostello_backend/templates/admin/`
- `hostello_backend/templates/payments/success.html`
- `hostello_backend/static/css/styles.css`
- `hostello_backend/static/css/student-dashboard.css`
- `hostello_backend/static/js/script.js`
- `hostello_backend/static/js/student-dashboard.js`
- `assets/`
- `HOSTELLO_EMAIL_SETTINGS` in `hostello_backend/hostello_backend/settings.py`

Legacy areas are currently isolated from the main RentEase product path. They should not be removed until their URL usage, model dependencies, admin dependencies, template references, and data dependencies are reviewed.

## 9. Old Docs / Phase Files

The `docs/` folder contains many phase documents. These are useful for traceability, but some may later be moved to `docs/archive/` if the project needs a cleaner documentation surface.

Root-level docs that may need archive review later:

- `docs/CHECKLIST-TIEN-DO.md`
- `docs/CHI-TIET-TASK-RENTEASE.md`
- `docs/DE-XUAT-NANG-CAP-RENTEASE.md`
- `docs/demo-checklist.md`
- `docs/KE-HOACH-CHI-TIET-RENTEASE.md`
- `docs/MO-TA-CHUC-NANG-HIEN-TAI.md`
- `docs/RENTEASE-MASTER-TASKS.md`
- `docs/screenshots-checklist.md`
- `docs/security-notes.md`
- `docs/SPQM-REPORT.md`
- `docs/SPRINT-PLANNING.md`

Do not delete docs. If cleanup is approved later, archive old docs instead of removing them.

## 10. Cleanup Risk Levels

Low risk:

- `__pycache__/`
- `*.pyc`
- `.pytest_cache/`
- `.coverage`
- temporary logs

Medium risk:

- old screenshots under `assets/`
- old demo video under `assets/`
- old root docs that may be moved to `docs/archive/`
- local helper scripts such as `run_backend.bat`, `run_frontend.bat`, and `Working.py`
- old backup JSON files, after confirming they are not needed and contain no sensitive data

High risk:

- templates
- static files referenced by templates
- views
- urls
- settings
- admin files
- legacy app code
- report templates
- portal templates

Do not touch:

- models
- migrations
- database files
- media uploads
- permission checks
- owner-scoped querysets
- tenant-scoped querysets
- billing calculations
- privacy hardening behavior

## 11. Recommended Cleanup Plan

1. Commit this audit report.
2. Delete only cache/temp files in a separate cleanup phase.
3. Archive old docs into `docs/archive/` after review.
4. Review unused templates one group at a time.
5. Review unused static files one group at a time.
6. Only then move templates gradually into `frontend/templates/`.
7. Move static files gradually into `frontend/static/`.
8. Keep old template/static paths active until all references are updated and route-smoke-tested.
9. Run `manage.py check` and `makemigrations --check --dry-run` after every cleanup phase.
10. Do not move Django apps or backend config until a separate high-risk backend migration plan is approved.

## 12. Next Safe Phase

The next safe phase is:

```text
Commit Cleanup Audit Report
```

After that, the safest technical cleanup phase is:

```text
Delete cache/temp files only
```

Do not start template movement until cache cleanup and documentation archiving are handled or explicitly skipped.
