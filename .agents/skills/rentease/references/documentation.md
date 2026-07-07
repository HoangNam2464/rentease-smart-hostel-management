# Documentation Work

Load this reference for agent instructions, project state, indexes, roadmaps, documentation consolidation, or historical retrieval.

## Authority Model

- Entry and hard rules: `AGENTS.md`
- Current truth: `docs/agent/STATE.md`
- One next task: `docs/agent/NEXT.md`
- Product: `docs/agent/PRODUCT.md`
- Structure: `docs/architecture/STRUCTURE.md`
- Legacy boundary: `docs/architecture/LEGACY.md`
- Security: `docs/agent/SECURITY.md`
- UI: `docs/ui/DESIGN.md`
- Demo: `docs/demo/README.md`
- Documentation index: `docs/README.md`

Do not duplicate one document's responsibility in another.

## History Rules

- Keep only current instructions in the working tree.
- Use Git history and tags when a task requires an old audit, plan, phase report, or work-log entry.
- Read `docs/archive/README.md` for retrieval commands; it is not a source of product truth.
- Verify recovered claims against current source and canonical documents.
- Do not create phase reports or chronological work logs when the current state, roadmap, next action, or Git commit can record the outcome.

## State Updates

- Update current state only for verified current facts.
- Keep next action to one approved recommendation.
- Update roadmap priorities and next action together when priorities change.
- Keep commit hashes out of durable context unless they materially identify a locked milestone; Git remains the commit source of truth.
- Mark unknown facts as unverified rather than guessing.

## Verification

- Check all active Markdown references and paths.
- Confirm removed historical documents are not linked as current sources.
- Run both Django checks even for documentation-only changes.
- Inspect `git status` and `git diff --check`.
- Confirm no application or runtime files changed.
