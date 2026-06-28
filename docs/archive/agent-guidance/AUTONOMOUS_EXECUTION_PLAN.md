# RentEase Autonomous Execution Plan

## Purpose

This file tells future Codex/agent sessions how to continue the RentEase project autonomously without requiring a long prompt every time.

The agent must read this file together with `AGENTS.md` before starting work.

## Autonomous Permission Scope

The agent is allowed to perform safe project work without asking for approval every time.

Allowed without additional approval:

- inspect files
- create or update documentation
- improve templates and UI
- improve static CSS/JS/assets
- run Django checks
- run migration dry-run
- run route regression checks
- create work logs
- update SPQM metrics/checklists
- git add intended files
- git commit phase-specific changes
- git push origin `complete-product`
- create and push phase tags after checks pass

Not allowed without explicit new approval:

- `git pull`
- `git merge`
- `git rebase`
- `git push --force`
- `git reset --hard`
- deleting branches
- deleting tags
- switching branches with uncommitted changes
- touching `temp-auto-auth-bypass`
- deleting legacy apps
- changing database schema
- creating migrations
- replacing authentication logic
- exposing sensitive owner/tenant data
- re-adding legacy root routes

## Mandatory Start Procedure

At the start of every autonomous run:

1. Read `AGENTS.md`.
2. Read `docs/agent/NEXT_ACTION.md`.
3. Read this file.
4. Read `docs/agent/RENTEASE_CURRENT_STATE.md`.
5. Read `docs/agent/RENTEASE_SECURITY_RULES.md`.
6. Read `docs/spqm/BACKLOG_AND_PRIORITIES.md`.
7. Read `docs/spqm/DEFINITION_OF_DONE.md`.

Then run:

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

## Autonomous Working Rule

The agent should continue working through `NEXT_ACTION.md` and the roadmap until one of these happens:

- the project is complete according to the current roadmap and release checklist
- a dangerous operation is required
- schema/migration changes are required but not explicitly approved
- required information is missing
- tests/checks fail and cannot be fixed safely
- the agent is near context/usage limit
- the local time stop condition is reached if one is specified
- the environment blocks further work

## Phase Completion Rule

After each completed phase:

1. Run Django check.
2. Run migration dry-run.
3. Test affected routes/pages.
4. Confirm no privacy/security regression.
5. Update `docs/agent/RENTEASE_CURRENT_STATE.md` if project status changed.
6. Update `docs/agent/NEXT_ACTION.md` with the next recommended phase.
7. Update `docs/spqm/QUALITY_METRICS.md` if metrics changed.
8. Update `docs/spqm/RELEASE_CHECKLIST.md` if readiness changed.
9. Update `docs/agent/AUTONOMOUS_WORK_LOG.md`.
10. Commit.
11. Push.
12. Create and push a phase tag if the phase is stable.

## Stop Rule Near Limit

If the agent is near context limit, time limit, tool limit, or usage limit, it must stop safely.

Before stopping, it must update:

```text
docs/agent/AUTONOMOUS_WORK_LOG.md
```

The log must include:

- what was completed
- latest commit
- tags created
- checks run
- files changed
- current blockers
- exact next recommended action
- whether working tree is clean

If possible, commit and push the log before stopping.

## Safe Priority Order

Unless `NEXT_ACTION.md` says otherwise, use this priority order:

1. Lock pending documentation baselines.
2. UI/UX audit and redesign plan.
3. Public UI polish.
4. Owner dashboard/sidebar/layout polish.
5. Owner CRUD page polish.
6. Tenant portal polish.
7. UI regression and demo documentation.
8. Production settings planning.
9. Owner billing detail gap analysis.
10. Account lifecycle planning.
11. Deployment readiness planning.
12. README/demo package.

## Product Target

RentEase should become a practical, presentable, Python/Django boarding-house management system.

The immediate goal is:

- clean project documentation
- clear process/quality documentation
- usable local demo
- better UI/UX
- safe owner/tenant data isolation
- clear demo flow

The later production goal is:

- production settings
- production database support
- complete owner-facing billing
- account lifecycle
- deployment readiness
- CI/test coverage
- optional legacy cleanup
