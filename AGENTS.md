# RentEase Agent Instructions

## Read This First

Every future coding agent must read this file before changing code. Do not rely on conversation memory alone. Verify the repository state locally before planning or editing.

## Project

Project name: RentEase

RentEase is a Django-based hostel/boarding-house management system developed from the original HOSTELLO project.

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

RentEase is local-demo ready.

RentEase is not production-ready yet.

Final local demo release tag:

```text
release-rentease-complete-product-v1
```

Latest production-hardening phase:

```text
Phase 14B-1: Legacy Root API / Fees Cleanup
```

Latest production-hardening tag:

```text
phase14b1-remove-legacy-root-api-fees
```

Latest known commit:

```text
6c6023a Remove legacy API and fees root routes
```

## Next Action

Current recommended next action:

```text
Phase 14B-2: Production Settings Split Planning
```

Goal: make settings production-aware while preserving local development.

Do not implement Phase 14B-2 before producing a plan and receiving approval.

## Non-Negotiable Rules

- Do NOT rename `hostello_backend`.
- Do NOT delete legacy apps unless explicitly approved.
- Do NOT create migrations unless explicitly approved.
- Do NOT change database schema unless explicitly approved.
- Do NOT merge branches unless explicitly approved.
- Do NOT force push.
- Do NOT run `git pull` unless explicitly approved.
- Do NOT touch `temp-auto-auth-bypass`.
- Do NOT switch branches if working tree has changes.
- Do NOT use `git reset --hard` or `git restore .` unless explicitly approved.

## Environment Rules

Global python may not be available.

Use direct venv Python:

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

## Required Start Procedure

Every task must start with:

```powershell
git branch --show-current
git status --short
git log --oneline -15
git tag --list
```

Then:

```powershell
.\venv\Scripts\python.exe manage.py check
.\venv\Scripts\python.exe manage.py makemigrations --check --dry-run
```

## Do Not Assume

Future agents must not assume the project state from memory. They must:

- read `AGENTS.md` first
- read `docs/agent/RENTEASE_CURRENT_STATE.md`
- verify branch/status/tags
- run Django check
- run migration dry-run
- inspect related files before editing

## Definition of Done

A phase is only considered done when:

- branch is `complete-product`
- working tree is clean
- Django check passes
- migration dry-run says `No changes detected` unless migrations were explicitly approved
- affected routes/features were verified
- no privacy/security regression exists
- only intended files changed
- commit was created and pushed
- final tag was created only after approval

## Keep This Documentation Updated

After each completed and locked phase, future agents should update:

- `AGENTS.md` if current phase/status changes
- `docs/agent/RENTEASE_CURRENT_STATE.md` with latest commit/tag
- `docs/agent/RENTEASE_PRODUCTION_ROADMAP.md` if roadmap changes

Do not update these files silently during feature work unless documentation update is part of the approved task.

## More Documentation

Read these files before implementation work:

- `docs/agent/RENTEASE_PRODUCT_CONTEXT.md`
- `docs/agent/RENTEASE_CURRENT_STATE.md`
- `docs/agent/RENTEASE_SECURITY_RULES.md`
- `docs/agent/RENTEASE_PRODUCTION_ROADMAP.md`
- `docs/agent/RENTEASE_WORKFLOW.md`

## SPQM Documentation

Future agents must also read the SPQM documentation when doing planning, quality, release, UI, production, billing, or documentation work.

SPQM files:

- `docs/spqm/SPQM_OVERVIEW.md`
- `docs/spqm/PROCESS_MODEL.md`
- `docs/spqm/DEFINITION_OF_DONE.md`
- `docs/spqm/BACKLOG_AND_PRIORITIES.md`
- `docs/spqm/CHANGE_MANAGEMENT.md`
- `docs/spqm/QUALITY_METRICS.md`
- `docs/spqm/RELEASE_CHECKLIST.md`
- `docs/spqm/PYTHON_DJANGO_QUALITY_STACK.md`
