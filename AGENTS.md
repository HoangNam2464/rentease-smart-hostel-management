# RentEase Agent Entry

This is the mandatory starting point for every agent working in this repository. Keep this file short; detailed guidance is loaded by task through the repo-local `rentease` skill.

## Start Here

1. Read `docs/agent/STATE.md`.
2. Read `docs/agent/NEXT.md`.
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

## Language Contract

- Code is English-only: file names, identifiers, classes, functions, variables, URL names, CSS classes, tests, comments, docstrings, API fields, and new technical documentation.
- Existing database names and migration history are compatibility exceptions; do not rename them without an approved migration plan.
- Product UI supports exactly Vietnamese (`vi`) and English (`en`). Render only the selected language; do not mix both languages except proper nouns, trademarks, currency codes, or standard units.
- UI wording belongs to the translation layer, never to Python identifiers or business-state values.
- English is the source message language. Vietnamese is the default product locale and must be complete before the language switcher ships.

## Reference-First Design Contract

- Interface quality is the primary product priority until the UI program is complete.
- Study the approved reference product or supplied source before creating a new surface. Record the layout, hierarchy, components, density, responsive behavior, and interactions being learned.
- Adapt patterns to RentEase workflows and branding. Do not copy reference code, assets, branding, or irrelevant POS behavior.
- Do not treat an AI-invented generic dashboard as design evidence. Every material UI change requires rendered desktop and mobile verification.

## Load Only Relevant Context

| Task | Read |
|---|---|
| Product behavior or scope | `docs/agent/PRODUCT.md` |
| Project paths | `docs/architecture/STRUCTURE.md` |
| Active/legacy boundaries | `docs/architecture/LEGACY.md` |
| Django, permissions, data, billing, settings | `.agents/skills/rentease/references/backend-safety.md` and `docs/agent/SECURITY.md` |
| Templates, CSS, UX, responsive work | `.agents/skills/rentease-design/SKILL.md` and `docs/ui/DESIGN.md` |
| Documentation maintenance | `.agents/skills/rentease/references/documentation.md` and `docs/README.md` |
| Historical decisions only | Git history/tags; retrieval guidance in `docs/archive/README.md` |

Do not inspect historical documents by default. Do not scan venvs, media, databases, or generated files unless the task specifically requires them.

## Source-of-Truth Order

When documents disagree, use this order:

1. User's current request
2. `AGENTS.md`
3. `docs/agent/STATE.md`
4. `docs/agent/NEXT.md`
5. Task-specific canonical document from the table above
6. Git history or recovered historical documents

## Finish Safely

- Inspect `git diff` and `git status --short`.
- Run both Django checks again.
- Test affected routes when behavior changed.
- Confirm no privacy or owner/tenant scoping regression.
- Stage only intended files.
- Commit locally when the task requests a commit.
- Never push or tag without explicit approval.
