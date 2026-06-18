# RentEase Agent Workflow

## Before Work

Always run:

```powershell
git branch --show-current
git status --short
git log --oneline -15
git tag --list
```

Then run:

```powershell
.\venv\Scripts\python.exe manage.py check
.\venv\Scripts\python.exe manage.py makemigrations --check --dry-run
```

Expected:

- branch is `complete-product`
- working tree is clean
- Django check passes
- migration dry-run says `No changes detected`

## Do Not Assume

Do not assume the project state from memory. Before editing:

- read `AGENTS.md`
- read `docs/agent/RENTEASE_CURRENT_STATE.md`
- verify branch/status/tags
- run Django check
- run migration dry-run
- inspect related files

## Planning First

Always plan before implementation for these areas:

- settings
- security
- billing logic
- models
- migrations
- database schema
- auth/account lifecycle
- deployment
- legacy routing

## Implementation Rules

- Make small phases.
- Modify only intended files.
- Do not create migrations unless approved.
- Do not change schema unless approved.
- Preserve local runserver.
- Preserve owner/tenant scoping.
- Preserve privacy rules.
- Do not touch `temp-auto-auth-bypass`.

## Verification After Implementation

Run:

```powershell
.\venv\Scripts\python.exe manage.py check
.\venv\Scripts\python.exe manage.py makemigrations --check --dry-run
```

Then test affected routes.

Check:

- no raw Django template tags
- no privacy leaks
- no role bypass
- no unrelated owner/tenant data
- no broken public routes
- no reports access regression
- no legacy root re-exposure

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

## Commit Rules

Before commit:

```powershell
git status --short
```

Only intended files should be modified.

Commit message should be short and phase-specific.

Push to:

```text
origin complete-product
```

Do not tag until final check and approval.

## Tag Rules

Tag only after final check.

Use phase tags.

Do not force push tags.

## Keep This Documentation Updated

After each completed and locked phase, update:

- `AGENTS.md` if current phase/status changes
- `docs/agent/RENTEASE_CURRENT_STATE.md` with latest commit/tag
- `docs/agent/RENTEASE_PRODUCTION_ROADMAP.md` if roadmap changes

Do not update these files silently during feature work unless documentation update is part of the approved task.
