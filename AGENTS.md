# RentEase Agent Instructions

## Read This First

Every future coding agent must read this file before changing code. Do not rely on conversation memory alone. Verify the repository state locally before planning or editing.

## How Future Agents Should Start

Follow these steps in order every time:

1. **Read** `AGENTS.md` (this file) — rules, structure, forbidden actions.
2. **Read** `docs/agent/RENTEASE_CURRENT_STATE.md` — latest phase, commits, known gaps.
3. **Read** `docs/agent/NEXT_ACTION.md` — the one recommended next phase.
4. **Run** the required checks from the repository root:

```powershell
git branch --show-current
git status --short
git log --oneline -15
git tag --list
```

Then from `backend/`:

```powershell
.\venv\Scripts\python.exe manage.py check
.\venv\Scripts\python.exe manage.py makemigrations --check --dry-run
```

Stop if branch is not `complete-product`, working tree is not clean, or either check fails.

## Agent Doc Responsibilities

Each agent doc has a single responsibility. Do not duplicate information across them:

| File | Responsibility |
|---|---|
| `AGENTS.md` | Mandatory rules, structure, forbidden actions, start procedure |
| `docs/agent/RENTEASE_CURRENT_STATE.md` | Current truth: phase, commits, CSS, security status, known gaps |
| `docs/agent/NEXT_ACTION.md` | One recommended next phase only |
| `docs/agent/RENTEASE_PROJECT_MAP.md` | Active/legacy boundary: apps, templates, CSS, editing rules |
| `docs/agent/AUTONOMOUS_WORK_LOG.md` | Chronological work log — append only |
| `docs/agent/DOCS_AND_AGENT_SETUP_AUDIT.md` | Documentation audit results and archive candidates |

## Project

Project name: RentEase

RentEase is a Django-based boarding-house / rental-room management system developed from the original HOSTELLO project.

## Product Target

RentEase should become a real production-ready boarding-house management system, not only a local demo.

It should eventually support:

- secure production settings
- production database
- owner-facing billing details and utility/service charges
- proper account lifecycle
- owner tenant creation/onboarding
- deployment-ready static/media/email/logging
- clean legacy isolation or removal
- strong owner/tenant data isolation

## Current Branch

Expected branch:

```powershell
complete-product
```

## Current Status

RentEase is **local-demo ready**.

RentEase is **not production-ready yet**.

Final local demo release tags:

```text
release-rentease-complete-product-v1
release-rentease-polished-local-demo-v2
```

Latest completed phase:

```text
Phase 20O: Admin Sensitive Detail Permission Hardening
```

Latest phase tag:

```text
phase20n-admin-search-privacy-hardening
```

Latest known recent commits (verify with `git log --oneline -5`):

```text
eb50f98 Add full RentEase technical analysis
7228f0b Add Antigravity rules for RentEase agents
f84bf69 Normalize agent documentation for clarity
9bf9051 Set up RentEase agent documentation
```

## Next Action

Current recommended next action:

```text
Phase 14B-2: Production Settings Split Planning
```

Goal: Make Django settings production-aware while preserving local development. Must address: `DEBUG`, `SECRET_KEY`, `ALLOWED_HOSTS`, HTTPS/security headers, secure cookies, database config, static/media, email, logging, `.env` support.

Do not implement Phase 14B-2 without first producing a plan and receiving explicit approval.

## Non-Negotiable Rules

- Do NOT rename the inner Django config package `backend/hostello_backend` or the Python module path `hostello_backend`.
- Do NOT delete legacy apps (`students`, `attendance`, `fees`, `requests`, `notices`) unless explicitly approved.
- Do NOT create migrations unless explicitly approved.
- Do NOT change database schema unless explicitly approved.
- Do NOT merge branches unless explicitly approved.
- Do NOT force push.
- Do NOT run `git pull` unless explicitly approved.
- Do NOT touch `temp-auto-auth-bypass`.
- Do NOT switch branches if working tree has changes.
- Do NOT use `git reset --hard` or `git restore .` unless explicitly approved.
- Do NOT push to GitHub unless explicitly approved.
- Do NOT modify models.py, views.py, urls.py, forms.py, or settings.py without an approved plan.
- Do NOT touch db.sqlite3, venv/, media/, or .env.
- Do NOT use `git clean` unless explicitly approved.

## Repository Structure

Confirmed real structure (Option A — restructured):

```text
RentEase/                            # repository root
├── AGENTS.md                        # THIS FILE — read first
├── README.md                        # project overview and setup
├── PROJECT_SUMMARY.md               # project feature summary
├── DEMO_SCRIPT.md                   # demo script at root
├── run_backend.bat                  # local convenience script
├── assets/                          # historical tracked HOSTELLO media
├── backend/                         # Django backend
│   ├── manage.py
│   ├── requirements.txt
│   ├── venv/                        # official local virtual environment (git-ignored)
│   ├── db.sqlite3                   # local SQLite database (git-ignored)
│   ├── media/                       # local uploaded/demo media (git-ignored)
│   ├── hostello_backend/            # Django config package — do NOT rename
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── asgi.py
│   ├── accounts/                    # active RentEase app
│   ├── properties/                  # active RentEase app
│   ├── tenants/                     # active RentEase app
│   ├── contracts/                   # active RentEase app
│   ├── billing/                     # active RentEase app
│   ├── maintenance/                 # active RentEase app
│   ├── listings/                    # active RentEase app
│   ├── portal/                      # active RentEase app (includes demo seed command)
│   ├── reports/                     # active RentEase app
│   ├── students/                    # LEGACY HOSTELLO app — do not delete
│   ├── attendance/                  # LEGACY HOSTELLO app — do not delete
│   ├── fees/                        # LEGACY HOSTELLO app — do not delete
│   ├── requests/                    # LEGACY HOSTELLO app — do not delete
│   └── notices/                     # LEGACY HOSTELLO app — do not delete
├── frontend/                        # Django Templates and static assets
│   ├── templates/                   # Django HTML templates
│   └── static/                      # CSS, JS, static assets
├── docs/                            # project documentation
│   ├── README.md
│   ├── agent/                       # agent operating instructions
│   ├── architecture/                # project structure and cleanup docs
│   ├── demo/                        # demo setup and walkthrough docs
│   ├── security/                    # privacy and security notes
│   ├── spqm/                        # quality and process docs
│   ├── ui/                          # UI audit and design system docs
│   └── archive/                     # old phase logs, old plans, archived helpers
└── .agents/                         # agent customization config (do not edit casually)
```

Important paths:

- `manage.py` is at: `backend/manage.py`
- Django config package: `backend/hostello_backend/`
- `DJANGO_SETTINGS_MODULE`: `hostello_backend.settings`
- Template root: `frontend/templates/`
- Static root: `frontend/static/`
- Official local virtual environment: `backend/venv/`
- Demo seed command: `backend/portal/management/commands/seed_rentease_demo_data.py`

## Environment Rules

Global Python may not be available.

Always run Django commands from the `backend/` directory using the venv Python directly:

```powershell
.\venv\Scripts\python.exe manage.py check
.\venv\Scripts\python.exe manage.py makemigrations --check --dry-run
.\venv\Scripts\python.exe manage.py runserver
```

Do NOT use:

```powershell
python manage.py check
python manage.py runserver
```

The old root-level `venv/` was removed safely. Use only `backend/venv/`.

## Required Start Procedure

Every task must start with these commands from the repository root:

```powershell
git branch --show-current
git status --short
git log --oneline -15
git tag --list
```

Expected before proceeding:

- branch is `complete-product`
- working tree is clean (no uncommitted changes)

Then from `backend/`:

```powershell
.\venv\Scripts\python.exe manage.py check
.\venv\Scripts\python.exe manage.py makemigrations --check --dry-run
```

Expected:

- Django check: `System check identified no issues (0 silenced)`
- Migration dry-run: `No changes detected`

If either check fails, stop and report. Do not proceed with code changes.

## Do Not Assume

Future agents must not assume the project state from memory. They must:

- read `AGENTS.md` first
- read `docs/agent/RENTEASE_CURRENT_STATE.md`
- verify branch/status/tags
- run Django check
- run migration dry-run
- inspect related files before editing

## Active Apps (RentEase)

These are the current product-relevant Django apps:

- `accounts` — users and owner profiles
- `properties` — rooms
- `tenants` — tenants and co-tenants
- `contracts` — rental contracts
- `billing` — invoices, invoice details, payment history
- `maintenance` — repair requests, maintenance records, notifications
- `listings` — room listings and viewing registrations
- `portal` — portal views for owner/tenant, demo seed command
- `reports` — staff-only report pages

## Legacy Apps (HOSTELLO — Do Not Delete)

These apps exist for compatibility and historical completeness. They must NOT be deleted without a dedicated legacy removal plan and explicit approval:

- `students`
- `attendance`
- `fees`
- `requests`
- `notices`

## Active Templates

Main active RentEase templates (in `frontend/templates/`):

- `home.html`
- `404.html`
- `500.html`
- `portal/base.html`
- `portal/login.html`
- `portal/owner_dashboard.html`
- `portal/owner_*.html`
- `portal/tenant_*.html`
- `listings/public_listing_list.html`
- `listings/public_listing_detail.html`
- `listings/viewing_registration_form.html`
- `listings/viewing_registration_success.html`

## Active CSS

Main active RentEase CSS files (in `frontend/static/css/`):

- `rentease-design.css` — global design system
- `rentease-layout.css` — sidebar, dashboard layout, CRUD tables and forms
- `admin/css/custom_admin.css` — custom admin overrides

## Legacy Templates and Static (Do Not Edit For RentEase UI)

Legacy HOSTELLO surfaces that should not be edited for RentEase UI unless explicitly approved:

- `frontend/templates/dashboard.html`
- `frontend/templates/index.html`
- `frontend/templates/login.html`
- `frontend/templates/admin/`
- `frontend/templates/payments/success.html`
- `frontend/static/css/styles.css`
- `frontend/static/css/student-dashboard.css`
- `frontend/static/js/script.js`
- `frontend/static/js/student-dashboard.js`
- `assets/` (historical tracked HOSTELLO media)

## RentEase Project Map

Before editing templates, CSS, UI, legacy cleanup, production settings, or productization tasks, always read:

```text
docs/agent/RENTEASE_PROJECT_MAP.md
```

This file defines active/legacy templates, apps, CSS files, editing rules, UI rules, and privacy rules.

## Privacy And Security Rules

**Never expose to public/tenant/owner surfaces:**

- `citizen_id`
- `citizen_id_front`
- `citizen_id_back`
- citizen ID files/images
- password/auth internals
- permission fields
- payment collector internals
- other owner data
- other tenant data
- admin-only notes

Owner data must always be scoped to the owner's own data. Tenant data must always be scoped to the tenant's own data.

Do not use unscoped querysets in detail/update/delete views.

## Admin Privacy Rules

Sensitive identity fields must only appear in the collapsed `Sensitive identity data` section in admin detail forms — never in list_display or search_fields.

Tenant and CoTenant admin search_fields must not include `citizen_id`.

Contract and Invoice admin search_fields must not use identity lookups. Use safe contact fields (phone_number, email) instead.

## Legacy Route Rules

Do not re-add legacy root routes:

- `path('', include('students.urls'))`
- `path('api/', include('requests.urls'))`
- `path('fees/', include('fees.urls', namespace='fees'))`

Allowed legacy routes:

- `/legacy/`
- `/legacy/login/`

## Definition of Done

A phase is only considered done when:

- branch is `complete-product`
- working tree is clean
- Django check passes with 0 issues
- migration dry-run says `No changes detected` unless migrations were explicitly approved
- affected routes/features were verified
- no privacy/security regression exists
- only intended files changed
- commit was created
- tag was created only after approval
- push was done only after approval

## Keep This Documentation Updated

After each completed and locked phase, update:

- `AGENTS.md` — current phase/status section
- `docs/agent/RENTEASE_CURRENT_STATE.md` — latest commit/tag/phase
- `docs/agent/RENTEASE_PRODUCTION_ROADMAP.md` — if roadmap priorities change
- `docs/agent/NEXT_ACTION.md` — next recommended phase
- `docs/agent/AUTONOMOUS_WORK_LOG.md` — append new entry

Do not update these files silently during feature work unless documentation update is part of the approved task.

## More Documentation

Read these files before implementation work:

- `docs/agent/NEXT_ACTION.md`
- `docs/agent/AUTONOMOUS_EXECUTION_PLAN.md`
- `docs/agent/RENTEASE_PRODUCT_CONTEXT.md`
- `docs/agent/RENTEASE_CURRENT_STATE.md`
- `docs/agent/RENTEASE_SECURITY_RULES.md`
- `docs/agent/RENTEASE_PRODUCTION_ROADMAP.md`
- `docs/agent/RENTEASE_WORKFLOW.md`
- `docs/agent/RENTEASE_PROJECT_MAP.md`

## Autonomous Work

Future agents may continue autonomously by reading:

- `AGENTS.md`
- `docs/agent/NEXT_ACTION.md`
- `docs/agent/AUTONOMOUS_EXECUTION_PLAN.md`

The user can start autonomous work with:

```text
Read AGENTS.md, docs/agent/NEXT_ACTION.md, and docs/agent/AUTONOMOUS_EXECUTION_PLAN.md. Continue RentEase autonomously until the project is complete, blocked, or near limit.
```

## SPQM Documentation

Future agents must also read SPQM documentation when doing planning, quality, release, UI, production, billing, or documentation work.

SPQM files:

- `docs/spqm/SPQM_OVERVIEW.md`
- `docs/spqm/PROCESS_MODEL.md`
- `docs/spqm/DEFINITION_OF_DONE.md`
- `docs/spqm/BACKLOG_AND_PRIORITIES.md`
- `docs/spqm/CHANGE_MANAGEMENT.md`
- `docs/spqm/QUALITY_METRICS.md`
- `docs/spqm/RELEASE_CHECKLIST.md`
- `docs/spqm/PYTHON_DJANGO_QUALITY_STACK.md`
