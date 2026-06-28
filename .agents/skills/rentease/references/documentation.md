# Documentation Work

Load this reference for agent instructions, project state, audits, indexes, roadmaps, work logs, or archive changes.

## Authority Model

- Entry and hard rules: `AGENTS.md`
- Current truth: `docs/agent/RENTEASE_CURRENT_STATE.md`
- One next task: `docs/agent/NEXT_ACTION.md`
- Product: `docs/agent/RENTEASE_PRODUCT_CONTEXT.md`
- Structure: `docs/architecture/PROJECT_STRUCTURE_MAP.md`
- Security: `docs/agent/RENTEASE_SECURITY_RULES.md`
- UI: `docs/ui/RENTEASE_PROFESSIONAL_DESIGN_SYSTEM.md`
- Documentation index: `docs/README.md`
- Chronology: `docs/agent/AUTONOMOUS_WORK_LOG.md`

Do not duplicate one document's responsibility in another.

## Archive Rules

- Treat `docs/archive/` as historical evidence, not current policy.
- Do not scan the archive by default.
- Move superseded documents into a descriptive archive folder; do not delete them silently.
- Preserve filenames where practical and update active links after moves.
- Never rewrite the chronological work log; append a new entry.

## State Updates

- Update current state only for verified current facts.
- Keep next action to one approved recommendation.
- Update roadmap numbering and next action together when priorities change.
- Keep commit hashes out of durable context unless they materially identify a locked milestone; Git remains the commit source of truth.
- Mark unknown facts as unverified rather than guessing.

## Verification

- Check active Markdown links and referenced paths.
- Confirm archive documents are not listed as current sources.
- Run both Django checks even for documentation-only phases.
- Inspect `git status` and `git diff --check`.
- Confirm no application or runtime files changed.
