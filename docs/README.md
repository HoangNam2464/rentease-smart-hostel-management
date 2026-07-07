# RentEase Documentation

Only current project guidance belongs in this directory. Git history is the record for completed phases and superseded plans.

## Required reading

1. `AGENTS.md`
2. `docs/agent/STATE.md`
3. `docs/agent/NEXT.md`

Use `.agents/skills/rentease/SKILL.md` for substantive work and `.agents/skills/rentease-design/SKILL.md` for interface work.

## Current documents

| Document | Responsibility |
|---|---|
| `agent/STATE.md` | Verified runtime, product, UI, language, and delivery state |
| `agent/NEXT.md` | The single immediate iteration |
| `agent/PRODUCT.md` | Users, capabilities, product boundaries, and language direction |
| `agent/SECURITY.md` | Permissions, privacy, billing, and sensitive-data rules |
| `agent/ROADMAP.md` | Ordered work from UI completion through i18n and production readiness |
| `architecture/STRUCTURE.md` | Repository structure and active paths |
| `architecture/LEGACY.md` | RentEase/HOSTELLO boundary |
| `architecture/DATA.md` | Current model alignment |
| `architecture/TARGET.md` | Approved target data direction |
| `ui/DESIGN.md` | Reference-first design system and bilingual UI vocabulary |
| `features/README.md` | Inactive future capability placeholders |
| `demo/README.md` | Local demo setup and walkthrough |
| `archive/README.md` | Historical retrieval from Git |

## Maintenance rules

- Keep file names short, English, uppercase for canonical documents, and stable after this consolidation.
- Do not create phase reports, duplicate plans, work logs, or another design guide.
- Update `STATE.md` only with verified facts.
- Keep `NEXT.md` to one iteration and update it after every completed commit.
- Keep UI terminology in `ui/DESIGN.md`; keep code naming rules in `AGENTS.md`.
- Update every Markdown reference when a canonical path changes.
