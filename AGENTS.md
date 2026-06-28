# RentEase Agent Entry

This is the mandatory starting point for every agent working in this repository. Keep this file short; detailed guidance is loaded by task through the repo-local `rentease` skill.

## Start Here

1. Read `docs/agent/RENTEASE_CURRENT_STATE.md`.
2. Read `docs/agent/NEXT_ACTION.md`.
3. Use `.agents/skills/rentease/SKILL.md` for substantive RentEase work. It routes backend, UI, and documentation tasks to separate references.
4. Verify the repository from the root:

```powershell
git branch --show-current
git status --short
git log --oneline -15
git tag --list
```

5. From `backend/`, run:

```powershell
.\venv\Scripts\python.exe manage.py check
.\venv\Scripts\python.exe manage.py makemigrations --check --dry-run
```

Stop before editing if the branch is not `complete-product`, the starting worktree is not clean, or either Django check fails.

## Non-Negotiable Rules

- Do not rename `backend/hostello_backend/` or the module path `hostello_backend`.
- Do not change models, migrations, database schema, settings, authentication, permissions, or billing logic without an approved plan.
- Do not create migrations unless explicitly approved.
- Do not touch `.env`, `db.sqlite3`, `backend/venv/`, `backend/media/`, generated output, or `temp-auto-auth-bypass`.
- Do not delete or casually edit legacy apps: `students`, `attendance`, `fees`, `requests`, `notices`.
- Do not re-add legacy root routes for `students`, `requests`, or `fees`.
- Do not expose citizen identity fields/files, credentials, permission internals, other owners' data, or other tenants' data.
- Do not use `git reset --hard`, `git restore .`, `git clean`, force push, or destructive bulk operations.
- Do not pull, merge, rebase, switch branches, push, or tag without explicit approval.
- Preserve unrelated user changes if the worktree is already modified; this repository normally requires a clean starting tree.

## Load Only Relevant Context

| Task | Read |
|---|---|
| Product behavior or scope | `docs/agent/RENTEASE_PRODUCT_CONTEXT.md` |
| Project paths | `docs/architecture/PROJECT_STRUCTURE_MAP.md` |
| Active/legacy boundaries | `docs/architecture/LEGACY_BOUNDARIES.md` |
| Django, permissions, data, billing, settings | `.agents/skills/rentease/references/backend-safety.md` and `docs/agent/RENTEASE_SECURITY_RULES.md` |
| Templates, CSS, UX, responsive work | `.agents/skills/rentease/references/ui-design.md` and `docs/ui/RENTEASE_PROFESSIONAL_DESIGN_SYSTEM.md` |
| Documentation maintenance | `.agents/skills/rentease/references/documentation.md` and `docs/README.md` |
| Historical decisions only | `docs/agent/AUTONOMOUS_WORK_LOG.md` and `docs/archive/` |

Do not read the work log or scan `docs/archive/` by default. Do not scan venvs, media, databases, or generated files unless the task specifically requires them.

## Source-of-Truth Order

When documents disagree, use this order:

1. User's current request
2. `AGENTS.md`
3. `docs/agent/RENTEASE_CURRENT_STATE.md`
4. `docs/agent/NEXT_ACTION.md`
5. Task-specific canonical document from the table above
6. Historical/archive documents

## Finish Safely

- Inspect `git diff` and `git status --short`.
- Run both Django checks again.
- Test affected routes when behavior changed.
- Confirm no privacy or owner/tenant scoping regression.
- Stage only intended files.
- Commit locally when the task requests a commit.
- Never push or tag without explicit approval.
