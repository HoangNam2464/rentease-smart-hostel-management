# Legacy Dependency Audit

Date: 2026-06-26

## Scope

This audit checks old HOSTELLO-related areas after the RentEase backend/frontend restructure.

The audit covers legacy Django apps, old templates, static assets, helper files, screenshot assets, and local backup files. This is documentation only. No files were deleted, moved, renamed, or refactored.

## Summary Table

| Target | Type | Current status | Referenced where | Runtime risk if removed | Recommendation |
|---|---|---|---|---|---|
| `backend/students/` | Legacy Django app | Installed and routed under `/legacy/` | `INSTALLED_APPS`, `backend/hostello_backend/urls.py`, legacy templates, other legacy apps | High | keep |
| `backend/attendance/` | Legacy Django app | Installed, admin/model dependency active | `INSTALLED_APPS`, `attendance.admin`, `students.views`, `fees.*` | High | keep |
| `backend/fees/` | Legacy Django app | Installed, root `/fees/` removed, admin templates still referenced | `INSTALLED_APPS`, `fees.admin`, `fees.views`, `frontend/templates/admin/fees/`, `frontend/templates/payments/` | High | keep |
| `backend/requests/` | Legacy Django app | Installed, root `/api/` removed, admin/model dependency active | `INSTALLED_APPS`, `requests.admin`, `requests.models`, admin custom template | High | keep |
| `backend/notices/` | Legacy Django app | Installed, used by legacy student views | `INSTALLED_APPS`, `students.views`, `notices.admin`, `notices.models` | High | keep |
| `assets/` | Historical screenshots/video | Tracked project assets, not runtime-required by Django | README/docs references; no runtime template/static reference found | Low | archive later |
| `Working.py` | Root helper note/script | Tracked helper file with unclear purpose | References `run_backend.bat` and `run_frontend.bat` text only | Low | needs manual review |
| `run_frontend.bat` | Root helper script | Tracked helper script with HOSTELLO wording | Manual local helper only | Low | archive later |
| `backup_phase*.json` | Local backups | Present locally, ignored/untracked | Repo hygiene docs; not runtime-required | Medium if contains data | safe to delete later |
| `frontend/templates/index.html` | Legacy template | Used by legacy student registration | `students.views.home_view` under `/legacy/` | Medium | keep |
| `frontend/templates/dashboard.html` | Legacy template | Used by legacy student dashboard | `students.views.dashboard_view` under `/legacy/dashboard/` | Medium | keep |
| `frontend/templates/admin/` | Legacy admin templates | Used by legacy admin custom pages | `attendance.admin`, `requests.admin`, `fees.admin` | High | keep |
| `frontend/templates/payments/success.html` | Legacy payment template | Used by legacy fees views | `fees.views.payment_success` | Medium | keep |
| `frontend/static/css/styles.css` | Legacy public CSS | Referenced by legacy templates | Legacy templates/static references | Medium | keep |
| `frontend/static/css/student-dashboard.css` | Legacy dashboard CSS | Referenced by `dashboard.html` | Legacy student dashboard | Medium | keep |
| `frontend/static/js/script.js` | Legacy public JS | Referenced by legacy templates | Legacy student pages | Medium | keep |
| `frontend/static/js/student-dashboard.js` | Legacy dashboard JS | Referenced by legacy dashboard assets | Legacy student dashboard | Medium | keep |

## Detailed Findings

### `backend/students/`

- What it is: original HOSTELLO student app with `Student` and legacy `Room` models, forms, views, URLs, and admin.
- Still referenced: yes.
- Referenced where:
  - `backend/hostello_backend/settings.py` includes `students` in `INSTALLED_APPS`.
  - `backend/hostello_backend/urls.py` mounts `students.urls` under `/legacy/`.
  - `backend/attendance/models.py`, `backend/fees/models.py`, `backend/requests/models.py`, and `backend/notices/models.py` depend on `students.models.Student`.
  - `backend/students/views.py` renders `index.html` and `dashboard.html`.
- Active runtime code: yes, under `/legacy/` and through admin/model dependencies.
- Risk level: high.
- Recommendation: keep.
- Notes: do not delete without a separate migration/contenttypes/admin dependency plan.

### `backend/attendance/`

- What it is: legacy attendance app with room/mess attendance models, admin tools, utils, signals, and views.
- Still referenced: yes.
- Referenced where:
  - `INSTALLED_APPS`.
  - `backend/attendance/admin.py` registers legacy admin views and imports `students.models.Student`.
  - `backend/students/views.py` imports attendance models for legacy dashboard/API data.
  - `backend/fees/admin.py` and `backend/fees/services.py` import attendance data.
- Active runtime code: yes through Django admin and legacy imports.
- Risk level: high.
- Recommendation: keep.
- Notes: deleting it could break Django startup, admin, fees calculations, and legacy student dashboard behavior.

### `backend/fees/`

- What it is: legacy fees/payment app with fee models, admin board, API/service helpers, URLs, and templates.
- Still referenced: yes.
- Referenced where:
  - `INSTALLED_APPS`.
  - `backend/hostello_backend/urls.py` still imports `from fees import admin as fees_admin`, although root `/fees/` route was removed.
  - `backend/fees/admin.py` registers legacy models and uses `frontend/templates/admin/fees/board.html`.
  - `backend/fees/views.py` renders `admin/fees/board.html` and `payments/success.html`.
  - `backend/fees/services.py` imports `attendance.models.MessAttendance`.
- Active runtime code: yes through admin and imports; public root `/fees/` is no longer mounted.
- Risk level: high.
- Recommendation: keep.
- Notes: route exposure is reduced, but app deletion is not safe yet because models/admin/templates still exist.

### `backend/requests/`

- What it is: legacy student request app with request models, DRF views/serializers, admin customization, and URLs.
- Still referenced: yes.
- Referenced where:
  - `INSTALLED_APPS`.
  - `backend/requests/models.py` imports `students.models.Student`.
  - `backend/requests/admin.py` registers `StudentRequest` and uses `admin/request_management.html`.
  - `backend/requests/urls.py` defines legacy API routes, but root `/api/` is no longer mounted by project URLs.
  - `backend/hostello_backend/settings.py` contains logging configuration for `requests.views`.
- Active runtime code: yes through installed models/admin; root API routes are not active.
- Risk level: high.
- Recommendation: keep.
- Notes: the old Unicode/emoji print risk is less exposed after route cleanup, but the app remains installed and should be reviewed separately before archive/removal.

### `backend/notices/`

- What it is: legacy notice/notification app with notice models and admin.
- Still referenced: yes.
- Referenced where:
  - `INSTALLED_APPS`.
  - `backend/students/views.py` imports `Notice` and `NoticeReadStatus`.
  - `backend/notices/models.py` references `students.models.Student`.
  - `backend/notices/admin.py` registers notice models.
- Active runtime code: yes through legacy student dashboard and admin.
- Risk level: high.
- Recommendation: keep.
- Notes: do not remove while `students.views` still imports it.

### `assets/`

- What it is: HOSTELLO-era screenshots and demo video files.
- Still referenced: yes in documentation/project maps, but not found as runtime template/static dependencies.
- Active runtime code: no.
- Risk level: low.
- Recommendation: archive later.
- Notes: safe archive candidate after confirming screenshots/video are no longer needed for reports or submission history.

### `Working.py`

- What it is: small root helper note telling the user to run backend/frontend helper scripts.
- Still referenced: documented in cleanup/project map docs.
- Active runtime code: no.
- Risk level: low.
- Recommendation: needs manual review.
- Notes: it can likely be replaced by README instructions in a future cleanup phase.

### `run_frontend.bat`

- What it is: Windows helper script that opens `http://127.0.0.1:8000/` and still says `Opening Hostello Frontend...`.
- Still referenced: `Working.py` and cleanup docs.
- Active runtime code: no, manual helper only.
- Risk level: low.
- Recommendation: archive later or rename/update in a separate helper-script cleanup.
- Notes: do not delete in this audit.

### `backup_phase*.json`

- What it is: local backup/demo dump files such as `backup_phase2.json` through `backup_phase5.json`.
- Still referenced: repo hygiene and cleanup docs.
- Active runtime code: no.
- Risk level: medium because dump files may contain account/demo data.
- Recommendation: safe to delete later after confirming they are local-only and not needed.
- Notes: these files are ignored/untracked and should not be committed.

### Legacy templates

- What they are:
  - `frontend/templates/index.html`: legacy registration/home template.
  - `frontend/templates/dashboard.html`: legacy student dashboard template.
  - `frontend/templates/admin/`: legacy custom admin templates.
  - `frontend/templates/payments/success.html`: legacy fees/payment success template.
- Still referenced: yes.
- Referenced where:
  - `backend/students/views.py` renders `index.html` and `dashboard.html`.
  - `backend/requests/admin.py` uses `admin/request_management.html`.
  - `backend/fees/admin.py` and `backend/fees/views.py` use `admin/fees/board.html`.
  - `backend/fees/views.py` uses `payments/success.html`.
- Active runtime code: yes, mostly through `/legacy/` and Django admin.
- Risk level: medium to high.
- Recommendation: keep.
- Notes: archive only after the matching legacy app/admin route is disabled or replaced.

### Legacy static files

- What they are:
  - `frontend/static/css/styles.css`
  - `frontend/static/css/student-dashboard.css`
  - `frontend/static/js/script.js`
  - `frontend/static/js/student-dashboard.js`
- Still referenced: yes by legacy templates.
- Active runtime code: only for legacy UI surfaces.
- Risk level: medium.
- Recommendation: keep.
- Notes: deleting these could make legacy pages visually broken. Archive with legacy templates as a separate phase.

## Legacy Django Apps Matrix

| App | In `INSTALLED_APPS`? | Project URLs connected? | Defines models? | Has migrations? | Admin references? | Safe to delete now? |
|---|---:|---:|---:|---:|---:|---:|
| `students` | Yes | Yes, under `/legacy/` | Yes | Yes | Yes | No |
| `attendance` | Yes | No direct project URL found | Yes | Yes | Yes | No |
| `fees` | Yes | No root `/fees/`; app URLs exist but are not mounted at root | Yes | Yes | Yes | No |
| `requests` | Yes | No root `/api/`; app URLs exist but are not mounted at root | Yes | Yes | Yes | No |
| `notices` | Yes | No direct project URL found | Yes | Yes | Yes | No |

## Legacy Templates And Static

The legacy templates/static files are not part of the polished RentEase owner/tenant/public portal, but they still support legacy pages and custom admin surfaces:

- `index.html` and `dashboard.html` are still used by `students.views` under `/legacy/`.
- `admin/request_management.html` is still used by `requests.admin`.
- `admin/fees/board.html` and `admin/fees/feemonth/change_list.html` are still used by `fees.admin`/`fees.views`.
- `payments/success.html` is still used by `fees.views`.
- legacy CSS/JS files are still tied to those legacy templates.

Do not delete these files until the corresponding legacy routes/admin views are retired or archived in a separate phase.

## Helper Files And Backups

- `assets/`: likely historical screenshots/video. Not runtime-required by Django, but useful for documentation history.
- `Working.py`: unclear root helper note. Not runtime-required.
- `run_frontend.bat`: manual browser opener with old HOSTELLO wording. Not runtime-required.
- `backup_phase*.json`: local backup/demo data files. Should stay ignored and should not be committed.

These are lower-risk than legacy apps, but they should still be archived/deleted only in a dedicated cleanup phase.

## Final Recommendation

1. Keep high-risk legacy apps for now.
2. Do not delete apps that have models, migrations, admin registrations, or cross-app imports without a dedicated migration/contenttypes/admin dependency plan.
3. Keep legacy templates/static while `/legacy/` and legacy admin surfaces still exist.
4. Archive or delete only low-risk helper files in a separate future phase.
5. If legacy UI removal is desired, first plan a phase that disables or replaces matching legacy routes/admin templates, then remove templates/static after verification.
6. Keep root `/api/requests/` and `/fees/` unavailable; do not re-add legacy root exposure.

