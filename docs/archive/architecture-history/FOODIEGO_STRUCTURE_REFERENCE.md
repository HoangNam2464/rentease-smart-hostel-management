# FoodieGo Structure Reference

## Purpose

This document records how the FoodieGo monorepo structure influenced the RentEase folder organization.

It is documentation-only. It does not propose immediate runtime changes, schema changes, app moves, or frontend framework changes.

## Extracted FoodieGo Structure Summary

FoodieGo uses a clean monorepo layout:

```text
FoodieGo/
|-- backend/
|   |-- config/
|   |-- apps/
|   |-- manage.py
|   `-- requirements.txt
|-- frontend/
|   |-- src/
|   |-- public/
|   `-- package.json
`-- README.md
```

Key idea:

- backend code is grouped under `backend/`
- frontend code is grouped under `frontend/`
- project documentation and root files stay at the repository root

## What RentEase Copied

RentEase copied the high-level monorepo separation:

```text
RentEase/
|-- backend/
|-- frontend/
|-- docs/
|-- README.md
`-- run_backend.bat
```

Current RentEase mapping:

- `backend/` contains Django backend code, apps, `manage.py`, settings, URLs, admin, forms, views, models, services, and migrations.
- `frontend/templates/` contains Django HTML templates.
- `frontend/static/` contains CSS, JavaScript, admin CSS, and UI assets.
- `docs/` contains architecture, UI, security, demo, SPQM, and agent documentation.

## What RentEase Should Not Copy Yet

RentEase should not copy these FoodieGo details immediately:

- Do not rename `backend/hostello_backend/` to `backend/config/` yet.
- Do not move Django apps into `backend/apps/` yet.
- Do not convert the frontend to React/Vite.
- Do not add `frontend/package.json` unless a real JavaScript build system is approved later.
- Do not replace Django server-rendered templates with static demo pages.

Reason:

RentEase currently works as a Django Templates application. Changing package names, app paths, or frontend runtime structure would introduce avoidable risk.

## Current RentEase Structure

```text
RentEase/
|-- backend/
|   |-- hostello_backend/
|   |-- accounts/
|   |-- properties/
|   |-- tenants/
|   |-- contracts/
|   |-- billing/
|   |-- maintenance/
|   |-- listings/
|   |-- portal/
|   |-- reports/
|   |-- students/
|   |-- attendance/
|   |-- fees/
|   |-- requests/
|   |-- notices/
|   |-- manage.py
|   `-- requirements.txt
|-- frontend/
|   |-- templates/
|   `-- static/
|-- docs/
|-- README.md
`-- run_backend.bat
```

Important notes:

- `backend/hostello_backend/` is still the Django config package.
- `DJANGO_SETTINGS_MODULE` is still `hostello_backend.settings`.
- Active RentEase apps and legacy HOSTELLO apps still live directly under `backend/`.
- The frontend remains Django Templates plus static CSS/JS.

## Recommended Future Structure If Apps Are Moved Later

If RentEase later decides to move apps into `backend/apps/`, the target could look like:

```text
backend/
|-- hostello_backend/
|-- apps/
|   |-- accounts/
|   |-- properties/
|   |-- tenants/
|   |-- contracts/
|   |-- billing/
|   |-- maintenance/
|   |-- listings/
|   |-- portal/
|   `-- reports/
|-- legacy/
|   |-- students/
|   |-- attendance/
|   |-- fees/
|   |-- requests/
|   `-- notices/
|-- manage.py
`-- requirements.txt
```

This is only a possible future structure, not an approved implementation plan.

## Risk Notes

Moving apps into `backend/apps/` is risky because it may affect:

- Python import paths
- `INSTALLED_APPS`
- `AppConfig.name`
- migration dependencies
- admin registrations
- tests and management commands
- historical app labels and content types
- local demo data

Renaming `hostello_backend` to `config` is risky because it may affect:

- `DJANGO_SETTINGS_MODULE`
- `ROOT_URLCONF`
- WSGI and ASGI imports
- scripts and documentation
- deployment settings
- local developer setup

Converting to React/Vite is risky because it would change:

- routing ownership
- authentication flow
- CSRF/session assumptions
- template rendering
- static asset pipeline
- current owner/tenant/admin workflows

## Recommendation

Keep the current RentEase structure for now:

- `backend/` for Django backend and apps
- `frontend/templates/` for Django templates
- `frontend/static/` for static assets
- `docs/` for documentation

Use FoodieGo as a naming and organization reference only. Any deeper migration should be planned, reviewed, tested, and committed as a dedicated phase.
