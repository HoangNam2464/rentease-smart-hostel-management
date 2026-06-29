# RentEase Next Action

## Immediate Next Phase

```text
Phase 14C-3A3 - Owner/Admin Property Integration
```

Status: waiting for explicit user approval. This first integration slice must not expand into public listings, reports, or schema constraints.

## Goal

Let owners and administrators manage Property records safely, and require owner room forms to select only a Property owned by the authenticated owner.

## Required Context

- `AGENTS.md`
- `docs/agent/RENTEASE_CURRENT_STATE.md`
- `docs/architecture/PROJECT_STRUCTURE_MAP.md`
- `docs/architecture/LEGACY_BOUNDARIES.md`
- `docs/architecture/DATA_MODEL_ALIGNMENT.md`
- `docs/architecture/TARGET_DATA_MODEL.md`
- `docs/agent/RENTEASE_SECURITY_RULES.md`
- `.agents/skills/rentease/references/backend-safety.md`
- `.agents/skills/rentease-design/SKILL.md` and the RentEase design system
- current Property/Room admin, portal URLs/views/forms/templates, owner navigation, migrations, and tests inspected directly

## Approval Decisions Required Before Editing

- approve owner Property list/detail/create/update routes and templates
- confirm owners may manage only their own Properties and may never reassign ownership
- confirm owner room create/update requires an owner-owned Property even while the database column remains nullable
- confirm admin may manage all Properties and inspect Room-to-Property ownership consistency
- keep exact address, coordinates, owner contact, and house rules out of public/tenant surfaces in this slice

## Expected Scope After Approval

- register Property in Django Admin with owner-safe search/filter fields
- add owner-scoped Property list/detail/create/update forms and templates
- filter owner room forms to the authenticated owner's Properties and reject cross-owner identifiers
- preserve existing room/listing/contract/invoice/repair query scoping through `Room.owner`
- add correct-owner, cross-owner rejection, and regression tests
- keep models/migrations, public listings, reports, disposable seed data, authentication, billing, settings, legacy apps, and real data unchanged

## Required Checks

- `manage.py check`
- `manage.py makemigrations --check --dry-run`
- targeted tests and full test suite
- `git diff --check`
- owner Property CRUD route tests and cross-owner identifier rejection
- owner room create/update tests using own versus foreign Property identifiers
- existing role, owner/tenant isolation, listing, billing, and migration tests
- clean final worktree after the requested local commit

## Stop Conditions

- explicit Phase 14C-3A3 owner/admin-slice approval has not been given
- a Property can be read or modified by another owner
- a room form can accept a Property owned by another owner
- existing owner/tenant/listing/report isolation differs
- a model, migration, public/tenant exposure, billing, authentication, settings, legacy runtime, or real-data change becomes necessary
- the starting worktree or Django checks are not clean

The public listing/report/seed-data slice of Phase 14C-3A3, Phase 14C-3A4 constraints, billing/meter work, and production legacy exclusion remain separately approval-gated.
