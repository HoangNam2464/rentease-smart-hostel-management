# RentEase Documentation System

RentEase documentation is organized by responsibility. Future agents should load only the context needed for the current task.

## Read For Every Task

1. `AGENTS.md` - mandatory rules and startup checks
2. `docs/agent/RENTEASE_CURRENT_STATE.md` - verified current truth and known gaps
3. `docs/agent/NEXT_ACTION.md` - one recommended next task

For substantive work, use the repo-local skill at `.agents/skills/rentease/SKILL.md`. It routes tasks to small backend, UI, or documentation references.

## Current Sources of Truth

| Document | Responsibility |
|---|---|
| `AGENTS.md` | Non-negotiable rules, startup, context routing |
| `docs/agent/RENTEASE_CURRENT_STATE.md` | Current branch, phase, verification, gaps |
| `docs/agent/NEXT_ACTION.md` | One immediate next action |
| `docs/agent/RENTEASE_PRODUCT_CONTEXT.md` | Product purpose, users, capabilities, boundaries |
| `docs/architecture/PROJECT_STRUCTURE_MAP.md` | Backend/frontend/docs/database/archive/legacy map |
| `docs/architecture/LEGACY_BOUNDARIES.md` | Current active-versus-legacy editing boundary |
| `docs/agent/RENTEASE_SECURITY_RULES.md` | Owner/tenant scoping and sensitive-data rules |
| `docs/ui/RENTEASE_PROFESSIONAL_DESIGN_SYSTEM.md` | Current UI and design guidance |
| `docs/agent/RENTEASE_PRODUCTION_ROADMAP.md` | Ordered production-readiness work |

## Task-Specific Reading

| Task | Load these documents |
|---|---|
| Django/backend/security/billing/settings | Skill `references/backend-safety.md`, then `RENTEASE_SECURITY_RULES.md` |
| UI/templates/CSS/design | Skill `references/ui-design.md`, then the UI design system |
| Documentation/reorganization | Skill `references/documentation.md`, then this index |
| Architecture or legacy boundaries | `PROJECT_STRUCTURE_MAP.md` and `LEGACY_BOUNDARIES.md`; use `LEGACY_DEPENDENCY_AUDIT.md` only as historical evidence |
| Local demo setup | `docs/demo/LOCAL_SETUP_AND_DEMO_DATA.md` and `DEMO_DATA_SEED_USAGE.md` |
| Demo verification | `docs/demo/FINAL_DEMO_CHECKLIST.md` |

Do not read all of these by default. `AUTONOMOUS_WORK_LOG.md` and `docs/archive/` are historical sources, not startup reading.

## Directory Responsibilities

| Path | Purpose |
|---|---|
| `docs/agent/` | Current product state, next action, security, roadmap, work log |
| `docs/architecture/` | Current structure map and active/legacy boundary; dependency audit retained as historical evidence |
| `docs/ui/` | Current design guidance |
| `docs/demo/` | Current local setup, seed, checklist, and screenshot guidance |
| `docs/archive/` | Superseded audits, old rules, phase logs, old plans, and historical reports |

## Archive Policy

- `docs/agent/AUTONOMOUS_WORK_LOG.md` is an append-only chronology, not current truth or default reading.
- Archive files are retained for traceability, not daily instructions.
- Do not scan `docs/archive/` unless a task needs historical evidence.
- Do not treat a phase log, old plan, audit, or archived rule as current policy.
- Move newly superseded documents into a descriptive archive folder; do not delete them silently.
- Update links in current documents when a source of truth moves.

## Updating Documentation

- Change `RENTEASE_CURRENT_STATE.md` only when current project truth changes.
- Change `NEXT_ACTION.md` only when the recommended next task changes.
- Append to `AUTONOMOUS_WORK_LOG.md`; never rewrite its history.
- Put durable product facts in product context, durable paths in the structure map, durable security rules in security rules, and durable visual rules in the UI guide.
- Avoid copying the same state or rule across multiple files.
