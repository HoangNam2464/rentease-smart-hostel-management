# RentEase Safety

Read `AGENTS.md`, `docs/agent/RENTEASE_CURRENT_STATE.md`, and `docs/agent/NEXT_ACTION.md` before editing.

From the repository root, require:

```powershell
git branch --show-current
git status --short
git log --oneline -15
git tag --list
```

From `backend/`, require:

```powershell
.\venv\Scripts\python.exe manage.py check
.\venv\Scripts\python.exe manage.py makemigrations --check --dry-run
```

Stop if the branch is not `complete-product`, the starting worktree is dirty, or either check fails.

Do not change schema, migrations, settings, auth, permissions, billing, database behavior, URLs, or legacy boundaries without an approved plan. Do not touch `.env`, databases, media, venvs, generated output, or `temp-auto-auth-bypass`.

Never expose citizen identity data/files or unrelated owner/tenant data. Never rename `backend/hostello_backend/` or delete legacy apps.

Do not use destructive Git/filesystem commands. Do not pull, merge, rebase, switch branches, push, or tag without explicit approval.

Use `.agents/skills/rentease/SKILL.md` to load task-specific guidance instead of reading unrelated documentation.
