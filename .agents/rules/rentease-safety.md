# RentEase Safety Rules

These rules apply to every agent working on the RentEase project. They are non-negotiable.

## Branch

Always work on branch `complete-product` unless the user explicitly names a different branch.

If the current branch is not `complete-product`, stop immediately and report.

## Before Starting Any Work

Run these commands from the repository root and verify the output:

```powershell
git branch --show-current    # must be: complete-product
git status --short           # must be: clean (no uncommitted changes)
git log --oneline -15
git tag --list
```

Then from `backend/`:

```powershell
.\venv\Scripts\python.exe manage.py check
.\venv\Scripts\python.exe manage.py makemigrations --check --dry-run
```

Stop and report if any check fails.

## Forbidden Actions — No Exceptions

- Do NOT change `models.py` or any database schema without an approved plan.
- Do NOT create migration files unless explicitly approved.
- Do NOT touch `db.sqlite3`, `media/`, `venv/`, or `.env`.
- Do NOT delete legacy HOSTELLO apps: `students`, `attendance`, `fees`, `requests`, `notices`.
- Do NOT delete legacy HOSTELLO templates or static files without a dedicated removal audit.
- Do NOT use `git reset --hard`, `git restore .`, `git clean`, or force push (`--force`).
- Do NOT run `git pull` unless explicitly approved.
- Do NOT run `git push` unless explicitly approved.
- Do NOT rename `backend/hostello_backend/` or change the Python module path `hostello_backend`.
- Do NOT touch `temp-auto-auth-bypass`.
- Do NOT switch branches if the working tree has uncommitted changes.
- Do NOT merge or rebase branches without explicit approval.

## Stop Conditions

Stop immediately and report (do not continue editing) if:

- Branch is not `complete-product`.
- Working tree is not clean before starting.
- Django check fails with any issue.
- Migration dry-run reports pending changes.
- The task requires touching Python code, models, migrations, templates, static files, media, or database without an approved plan.
- The scope is unclear or the task would require destructive operations.
