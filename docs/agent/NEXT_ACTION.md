# RentEase Next Action

## Immediate Next Session

```text
Session B - Rebuild AGENTS.md and Agent Rules from Docs Audit
```

## Goal

Use `docs/agent/DOCS_CONSOLIDATION_AUDIT.md` to make the local agent instructions short, authoritative, and sufficient for future sessions without long prompts.

Session B should:

- rebuild `AGENTS.md` from the verified audit
- create or update a minimal `.agents/rules/` set
- remove duplicated state from rule files
- reconcile commit, push, and tag approval language
- preserve the current structure, privacy rules, and mandatory checks
- keep `NEXT_ACTION.md` limited to one recommended action

Do not implement Phase 14C in Session B.

## Allowed Files

- `AGENTS.md`
- `.agents/rules/*.md`
- `docs/agent/DOCS_CONSOLIDATION_AUDIT.md` only for factual corrections
- `docs/agent/RENTEASE_CURRENT_STATE.md`
- `docs/agent/NEXT_ACTION.md`
- `docs/agent/AUTONOMOUS_WORK_LOG.md`

## Forbidden Files and Actions

- Do not modify Python application code.
- Do not modify models, views, URLs, forms, settings, admin code, or migrations.
- Do not modify templates or static files.
- Do not touch `.env`, databases, media, venvs, or generated runtime output.
- Do not move/delete legacy apps or documentation.
- Do not implement PostgreSQL migration or change database configuration/schema.
- Do not pull, merge, force push, push, or tag without explicit approval.

## Required Checks

From the repository root:

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

Repeat the Django checks and `git status --short` after edits.

## Stop Conditions

Stop and report without editing if:

- branch is not `complete-product`
- the starting worktree is not clean
- either Django check fails
- the task would require application code, schema, migration, database, template, or static changes
- resolving a rule conflict would expand permissions beyond the user's explicit approval model

## Final Report Format

```text
Current Branch:
Working Tree Before:
Rules Rebuilt:
Conflicts Resolved:
Files Changed:
Checks Result:
Commit:
Safety Confirmation:
Recommended Next Phase:
```

Recommended product phase after Session B:

```text
Phase 14C - PostgreSQL Migration Planning
```
