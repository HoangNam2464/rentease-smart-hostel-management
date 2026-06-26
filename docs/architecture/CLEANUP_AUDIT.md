# Cleanup Audit

## 1. Purpose

This report documents a safe cleanup audit after the RentEase backend/frontend restructure.

The project now uses:

- `backend/` for Django backend code, apps, `manage.py`, and settings.
- `frontend/templates/` for Django templates.
- `frontend/static/` for CSS, JavaScript, images, and UI assets.
- `docs/` for documentation.

This cleanup phase only removed generated Python cache files from project code. It did not delete legacy apps, templates, static files, docs, local databases, media uploads, migrations, or business logic.

For detailed legacy dependency findings, see `docs/architecture/LEGACY_DEPENDENCY_AUDIT.md`.

## 2. Cleaned Now

Deleted generated Python cache folders from project code only:

- `backend/accounts/__pycache__/`
- `backend/accounts/migrations/__pycache__/`
- `backend/attendance/__pycache__/`
- `backend/attendance/migrations/__pycache__/`
- `backend/billing/__pycache__/`
- `backend/billing/migrations/__pycache__/`
- `backend/contracts/__pycache__/`
- `backend/contracts/migrations/__pycache__/`
- `backend/fees/__pycache__/`
- `backend/fees/migrations/__pycache__/`
- `backend/hostello_backend/__pycache__/`
- `backend/listings/__pycache__/`
- `backend/listings/migrations/__pycache__/`
- `backend/maintenance/__pycache__/`
- `backend/maintenance/migrations/__pycache__/`
- `backend/notices/__pycache__/`
- `backend/notices/migrations/__pycache__/`
- `backend/portal/__pycache__/`
- `backend/portal/management/__pycache__/`
- `backend/portal/management/commands/__pycache__/`
- `backend/properties/__pycache__/`
- `backend/properties/migrations/__pycache__/`
- `backend/reports/__pycache__/`
- `backend/requests/__pycache__/`
- `backend/requests/migrations/__pycache__/`
- `backend/students/__pycache__/`
- `backend/students/migrations/__pycache__/`
- `backend/tenants/__pycache__/`
- `backend/tenants/migrations/__pycache__/`

These folders contained generated `.pyc` files only.

Virtual environment cache folders under `venv/` and `backend/venv/` were not cleaned because virtual environments should be ignored/recreated rather than edited as project cleanup.

## 3. Safe To Delete Later

Only generated files are safe to delete without functional review:

- `__pycache__/` folders if they appear again outside virtual environments.
- `*.pyc` files if they appear again outside virtual environments.
- `.pytest_cache/` if it appears later.
- `.coverage` if it appears later.
- Clearly generated temporary logs such as `*.log` or `*.tmp`, if they are not needed for debugging.

No non-cache runtime files should be deleted without a separate review.

## 4. Needs Manual Review

These files or folders may be old, local-only, duplicated, or legacy, but were not deleted:

- `assets/`
  - Contains HOSTELLO screenshots and a demo video. Likely historical/demo material.
- `run_backend.bat`
  - Local helper script. Currently points to `backend/` and may still be useful.
- `run_frontend.bat`
  - Opens the local site but still has old wording. Needs review before removal or rename.
- `Working.py`
  - Small root-level helper/debug file with unclear purpose.
- `backup_phase2.json`, `backup_phase3.json`, `backup_phase4.json`, `backup_phase5.json`
  - Local backup/demo data files. They should not be committed if they contain user/demo data.
- `backend/phase8b2_wip.patch`
  - Old WIP patch mentioned in prior repo hygiene docs, if still present locally.
- `frontend/templates/index.html`
  - Legacy student registration template.
- `frontend/templates/login.html`
  - Legacy student login template. Do not confuse with `frontend/templates/portal/login.html`.
- `frontend/templates/dashboard.html`
  - Legacy student dashboard template.
- `frontend/templates/admin/`
  - Legacy custom admin templates for attendance, room assignment, requests, and fees.
- `frontend/templates/payments/success.html`
  - Legacy fees/payment success template.
- `frontend/static/css/styles.css`
  - HOSTELLO-era public CSS.
- `frontend/static/css/student-dashboard.css`
  - Legacy student dashboard CSS.
- `frontend/static/js/script.js`
  - HOSTELLO-era JavaScript.
- `frontend/static/js/student-dashboard.js`
  - Legacy student dashboard JavaScript.
- Older phase/audit docs under `docs/`
  - Useful for traceability, but could later be archived.

## 5. Do Not Delete

Do not delete or move these without explicit approval and a separate plan:

- `backend/manage.py`
- `backend/hostello_backend/`
- `backend/hostello_backend/settings.py`
- `backend/hostello_backend/urls.py`
- Active RentEase apps:
  - `backend/accounts/`
  - `backend/properties/`
  - `backend/tenants/`
  - `backend/contracts/`
  - `backend/billing/`
  - `backend/maintenance/`
  - `backend/listings/`
  - `backend/portal/`
  - `backend/reports/`
- Legacy apps still in `INSTALLED_APPS`:
  - `backend/students/`
  - `backend/attendance/`
  - `backend/fees/`
  - `backend/requests/`
  - `backend/notices/`
- All `models.py` files.
- All migration folders and migration files.
- `backend/db.sqlite3`
- `backend/media/`
- `frontend/templates/`
- `frontend/static/`
- `docs/`
- `README.md`
- `AGENTS.md`

Also do not remove permission checks, owner-scoped querysets, tenant-scoped querysets, billing calculations, privacy hardening, admin protections, or legacy route isolation.

## 6. Legacy Areas Found

Legacy HOSTELLO apps are still present and still registered in `INSTALLED_APPS`:

- `students`
- `attendance`
- `fees`
- `requests`
- `notices`

Current usage status:

- `students.urls` is still included under `/legacy/`.
- `attendance`, `fees`, `requests`, and `notices` are still installed apps and have model/admin/template dependencies.
- Legacy root `/api/requests/` and `/fees/` routes remain removed from root routing.
- Legacy templates and static files still support old HOSTELLO surfaces and admin custom pages.

Conclusion: legacy apps are high-risk cleanup targets and should not be deleted in this phase.

## 7. Static/Template Usage Review

Active RentEase templates:

- `frontend/templates/home.html`
- `frontend/templates/listings/`
- `frontend/templates/portal/`
- `frontend/templates/reports/`
- `frontend/templates/404.html`
- `frontend/templates/500.html`

Active RentEase static files:

- `frontend/static/css/rentease-design.css`
- `frontend/static/css/rentease-layout.css`
- `frontend/static/admin/css/custom_admin.css`

Legacy or unclear templates/static that need review:

- `frontend/templates/index.html`
- `frontend/templates/login.html`
- `frontend/templates/dashboard.html`
- `frontend/templates/admin/`
- `frontend/templates/payments/success.html`
- `frontend/static/css/styles.css`
- `frontend/static/css/student-dashboard.css`
- `frontend/static/js/script.js`
- `frontend/static/js/student-dashboard.js`

These were not deleted because they are referenced by legacy views/admin/templates or may still be useful for `/legacy/`.

## 8. Python Code Review

Suspicious or legacy code areas found:

- `backend/hostello_backend/urls.py`
  - Contains commented `# from fees.admin import FeesAdminSite`.
  - Contains `from fees import admin as fees_admin`, which appears unused in the URL file.
- `backend/hostello_backend/settings.py`
  - Still contains `HOSTELLO_EMAIL_SETTINGS` and legacy email text for attendance notifications.
- `backend/students/views.py`
  - Contains many legacy print/debug statements and HOSTELLO-era messages.
- `backend/attendance/admin.py`
  - Contains many debug `print()` calls and legacy attendance management behavior.
- `backend/requests/views.py`
  - Contains legacy API/view code and debug `print()` calls.
- `backend/requests/admin.py`
  - Contains print-based notification/debug logging.
- `backend/requests/models.py`
  - Contains print-based notification logging.
- `backend/fees/`
  - Contains legacy fees logic tied to legacy student/attendance models.

These areas may still be connected to legacy routes, admin behavior, installed apps, migrations, or documentation. They were not edited.

## 9. Risk Level

Low risk:

- Project `__pycache__/` folders.
- Project `*.pyc` files.
- `.pytest_cache/`, `.coverage`, and clearly generated temporary logs.

Medium risk:

- Old screenshots or demo media under `assets/`.
- Old docs that could be moved to `docs/archive/`.
- Local helper files such as `.bat` scripts or unclear root-level scripts.
- Backup JSON files after confirming they are not needed and contain no sensitive data.

High risk:

- Templates.
- Static files referenced by templates.
- Views, URLs, settings, admin files, and forms.
- Legacy app code.
- Active reports, portal, listings, billing, maintenance, tenants, contracts, properties, and accounts code.

Do not touch without explicit approval:

- Models.
- Migrations.
- Database files.
- Media uploads.
- Permission checks.
- Owner-scoped querysets.
- Tenant-scoped querysets.
- Billing/payment calculations.
- Privacy hardening behavior.

## 10. Recommended Next Cleanup Phase

Recommended next cleanup phase:

```text
Archive or review old documentation and helper files
```

Suggested scope:

1. Review `run_frontend.bat`, `Working.py`, `assets/`, and backup JSON files.
2. Decide whether to archive old docs into `docs/archive/` rather than deleting them.
3. Keep legacy apps and templates untouched until a dedicated legacy dependency audit is approved.
4. Keep active RentEase templates/static untouched.

Do not start legacy app removal until there is a full dependency audit covering `INSTALLED_APPS`, migrations, admin registrations, URL routing, templates, imports, and local demo behavior.
