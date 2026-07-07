---
name: rentease
description: Use for RentEase repository tasks involving Django backend code, permissions, billing, settings, databases, templates, CSS, UI/UX, documentation, architecture, demo workflows, verification, or planning. Routes work to task-specific references while enforcing the repository startup checks, active/legacy boundaries, owner/tenant privacy, and approval gates.
---

# RentEase

Work on RentEase with the minimum relevant context. Treat current source files and canonical documents as truth; treat recovered historical material as evidence only.

## Setup

Before editing:

1. Read `AGENTS.md`.
2. Read `docs/agent/STATE.md`.
3. Read `docs/agent/NEXT.md`.
4. Run the root Git checks and backend Django checks required by `AGENTS.md`.
5. Stop if the branch, worktree, Django check, or migration dry-run fails its gate.

Do not replace source inspection with documentation assumptions.

## Route the Task

Load only the matching reference:

| Task | Required reference |
|---|---|
| Python, Django, permissions, admin, billing, settings, database, deployment | `references/backend-safety.md` |
| Templates, CSS, UX copy, responsive behavior, visual QA | Use `$rentease-design`; for mixed tasks also load `references/ui-design.md` |
| Documentation, agent rules, audits, history retrieval, project-state updates | `references/documentation.md` |

For mixed tasks, load each relevant reference. Do not retrieve historical documents unless the task requires evidence from them.

## Core Workflow

1. Inspect the real target files and current Git state.
2. Identify intended files, protected files, risk, and verification before editing.
3. Produce a plan and obtain approval before settings, schema, migration, authentication, permission, billing, database, deployment, or legacy work.
4. Make the smallest coherent change and preserve unrelated user work.
5. Run Django check and migration dry-run after editing.
6. Verify affected routes, roles, privacy, or documentation links in proportion to the change.
7. Inspect the final diff and stage only intended files.
8. Commit only when requested or clearly part of the approved phase. Never push or tag without explicit approval.

## Canonical Context

- Product: `docs/agent/PRODUCT.md`
- Structure and active/legacy map: `docs/architecture/STRUCTURE.md`
- Security: `docs/agent/SECURITY.md`
- UI: `docs/ui/DESIGN.md`
- Production order: `docs/agent/ROADMAP.md`
- Documentation authority: `docs/README.md`
- History retrieval: `docs/archive/README.md` and Git history/tags

If canonical documents disagree, follow the authority order in `AGENTS.md` and verify against source.
