# RentEase Project Structure Map

## Purpose

This document describes the current RentEase repository layout after the backend/frontend restructure and documentation consolidation.

RentEase uses Django Templates, not React/Vite.

## Current Top-Level Structure

```text
RentEase/
├── AGENTS.md
├── README.md
├── assets/                       # historical tracked HOSTELLO media, kept for now
├── backend/                      # Django backend
├── frontend/                     # Django Templates and static assets
└── docs/                         # documentation
```

## Backend Structure

```text
backend/
├── manage.py
├── requirements.txt
├── venv/                         # official local virtual environment, ignored by Git
├── db.sqlite3                    # local database, ignored by Git
├── media/                        # local uploaded/demo media, ignored by Git
├── hostello_backend/             # Django config package, do not rename casually
├── accounts/
├── properties/
├── tenants/
├── contracts/
├── billing/
├── maintenance/
├── listings/
├── portal/
├── reports/
├── students/                     # legacy HOSTELLO app
├── attendance/                   # legacy HOSTELLO app
├── fees/                         # legacy HOSTELLO app
├── requests/                     # legacy HOSTELLO app
└── notices/                      # legacy HOSTELLO app
```

## Django Config Package

```text
backend/hostello_backend/
├── settings.py
├── urls.py
├── wsgi.py
└── asgi.py
```

Important:

- `DJANGO_SETTINGS_MODULE` remains `hostello_backend.settings`.
- `ROOT_URLCONF` remains `hostello_backend.urls`.
- Do not rename `backend/hostello_backend/` without a dedicated migration/refactor plan.

## Frontend Structure

```text
frontend/
├── templates/
└── static/
```

Main template groups:

```text
frontend/templates/home.html
frontend/templates/404.html
frontend/templates/500.html
frontend/templates/portal/
frontend/templates/listings/
frontend/templates/reports/
frontend/templates/admin/
frontend/templates/payments/
```

Main static groups:

```text
frontend/static/css/
frontend/static/js/
frontend/static/admin/
frontend/static/rentease/
frontend/static/vendor/
```

Current RentEase UI mainly uses:

```text
frontend/static/css/rentease-design.css
frontend/static/css/rentease-layout.css
frontend/static/admin/css/custom_admin.css
```

Legacy frontend files remain for `/legacy/` and old admin surfaces:

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

Do not delete these without a dedicated legacy template/static removal audit.

## Archived Helper Files

These files are no longer active root helper files:

```text
docs/archive/Working.py
docs/archive/run_frontend.bat
```

Local backup JSON files were moved to:

```text
docs/archive/local-backups/
```

The backup JSON files remain ignored/local and should not be committed.

## Historical Media

`assets/` is kept at the repository root for now because it contains tracked historical HOSTELLO screenshots/video. It is not known to be required by Django runtime, but moving it would create a large rename and may affect documentation history.

Future cleanup should handle `assets/` in a separate media/archive phase.

## Documentation Structure

```text
docs/
├── README.md
├── architecture/
├── demo/
├── security/
├── spqm/
├── ui/
├── agent/
└── archive/
```

Archived phase history and old plans are stored under:

```text
docs/archive/phase-history/
docs/archive/old-plans/
```

## Runtime Safety Rules

- Do not change models or migrations unless explicitly approved.
- Do not move Django apps unless explicitly approved.
- Do not rename `backend/hostello_backend/` unless explicitly approved.
- Do not delete legacy apps `students`, `attendance`, `fees`, `requests`, `notices` without a dedicated removal plan.
- Do not delete templates/static/media without dependency review.
- Use `backend/venv/` for local Django commands.
- Do not use a root-level `venv/`.

