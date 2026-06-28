# RentEase Documentation

This directory contains only current, project-specific guidance. Load the minimum context required for the task.

## Read For Every Task

1. `AGENTS.md` - mandatory rules and startup checks
2. `docs/agent/RENTEASE_CURRENT_STATE.md` - verified current truth and known gaps
3. `docs/agent/NEXT_ACTION.md` - one recommended next task

Use `.agents/skills/rentease/SKILL.md` for substantive project work and `$rentease-design` for focused UI design or visual QA.

## Current Documents

| Document | Responsibility |
|---|---|
| `agent/RENTEASE_CURRENT_STATE.md` | Current product, runtime, security, and documentation state |
| `agent/NEXT_ACTION.md` | One immediate next action |
| `agent/RENTEASE_PRODUCT_CONTEXT.md` | Product purpose, users, capabilities, and boundaries |
| `agent/RENTEASE_SECURITY_RULES.md` | Owner/tenant scoping and sensitive-data rules |
| `agent/RENTEASE_PRODUCTION_ROADMAP.md` | Ordered production-readiness work |
| `architecture/PROJECT_STRUCTURE_MAP.md` | Backend, frontend, data, docs, and agent-resource map |
| `architecture/LEGACY_BOUNDARIES.md` | Current RentEase-versus-HOSTELLO editing boundary |
| `ui/RENTEASE_PROFESSIONAL_DESIGN_SYSTEM.md` | Product-specific UI and design direction |
| `demo/README.md` | Local setup, seed data, walkthrough, verification, and screenshots |
| `archive/README.md` | How to retrieve removed historical documents from Git |

## Task Routing

| Task | Load after the three startup documents |
|---|---|
| Django, permissions, billing, settings, database | Skill `references/backend-safety.md` and `RENTEASE_SECURITY_RULES.md` |
| UI, templates, CSS, UX copy, responsive behavior | `$rentease-design` and the UI design system |
| Architecture or legacy work | `PROJECT_STRUCTURE_MAP.md` and `LEGACY_BOUNDARIES.md` |
| Local setup, demo data, presentation | `demo/README.md` |
| Documentation maintenance | Skill `references/documentation.md` and this index |

Do not read all documents by default.

## History Policy

- Phase reports, completed audits, old plans, SPQM coursework, duplicate guides, and the former work log are not kept in the active tree.
- Git commits and tags remain the historical record. Use `archive/README.md` only when retrieval is necessary.
- Recovered historical content is evidence, not current policy; verify it against source and the documents above.
- Do not create a new phase report or chronological work log when a current source of truth can be updated instead.

## Updating Documentation

- Change current state only when verified project truth changes.
- Change next action only when the recommended task changes.
- Keep roadmap priorities and next action consistent.
- Put durable product facts in product context, paths in the structure map, security rules in security rules, and visual rules in the UI guide.
- Replace superseded instructions instead of creating another parallel document.
