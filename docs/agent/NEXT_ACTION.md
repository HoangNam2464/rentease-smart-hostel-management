# RentEase Next Action

## Immediate Next Phase

```text
Phase 14C-3A3 - Listing, Report, and Seed Property Integration
```

Status: waiting for explicit user approval. This second integration slice must not change models, migrations, billing, or the required-Property constraint.

## Goal

Carry verified Property context into listings, staff reports, and disposable demo seeding without exposing private location/contact data publicly.

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
- current public/owner listing views and templates, reports views/services/templates, disposable seed command, Property/Room relationships, and tests inspected directly

## Approval Decisions Required Before Editing

- approve Property name, ward, and province/city as the only public-safe Property fields
- keep exact address, coordinates, owner contact, timezone, and house rules private
- confirm staff reports may use full Property context but remain staff-only
- confirm the disposable seed command creates owner Properties before Rooms and links every seeded Room
- keep `Room.owner` as the authorization boundary throughout this slice

## Expected Scope After Approval

- add public-safe Property context to published room list/detail pages
- add Property context/filtering to owner listing pages and staff-only room/listing reports
- update the disposable seed command so seeded Rooms always belong to seeded Properties
- preserve every owner/tenant/staff queryset boundary and test public privacy markers
- keep models/migrations, authentication, billing, settings, legacy apps, and real data unchanged

## Required Checks

- `manage.py check`
- `manage.py makemigrations --check --dry-run`
- targeted tests and full test suite
- `git diff --check`
- public listing tests proving safe fields are visible and private fields are absent
- staff report access/filter tests and wrong-role rejection
- seed idempotency and zero-unlinked-seeded-room checks
- existing role, Property isolation, billing, and migration tests
- clean final worktree after the requested local commit

## Stop Conditions

- explicit Phase 14C-3A3 second-slice approval has not been given
- exact address, coordinates, contact phone, timezone, or house rules would appear publicly
- a report becomes accessible to an owner, tenant, or anonymous visitor
- seeded Rooms can remain unlinked or link across owners
- existing owner/tenant/listing/report isolation differs
- a model, migration, billing, authentication, settings, legacy runtime, or real-data change becomes necessary
- the starting worktree or Django checks are not clean

Phase 14C-3A4 constraints, billing/meter work, maintenance/data-governance work, and production legacy exclusion remain separately approval-gated.
