# RentEase Next Action

## Current Project State

RentEase is on branch:

```text
complete-product
```

Current status:

- local demo ready
- not production-ready
- owner/tenant security scoping improved
- legacy root API and fees routes removed
- agent guidance docs created
- SPQM documentation baseline created and locked
- UI is still weak and needs redesign
- production settings are not hardened
- owner billing detail/utility entry is incomplete

## Immediate Next Step

SPQM Documentation Baseline Lock is complete.

Completed documentation baselines:

- `agent-guidance-docs-baseline`
- `spqm-documentation-baseline`

## Completed Current Step

Phase 15A UI/UX Audit and Redesign Planning is complete.

Audit document:

```text
docs/agent/PHASE_15A_UI_UX_AUDIT_PLAN.md
```

## Immediate Next Step

Start:

```text
Phase 15B-1: Public UI Polish
```

Goal:

Improve the public RentEase UI before login.

Initial scope:

- fix public landing headline encoding
- improve `/`
- improve `/rooms/`
- improve `/rooms/<id>/`
- improve `/rooms/<id>/register/`
- improve `/rooms/<id>/register/success/`

Do not change models, migrations, routes, settings, or business logic.

## Recommended Demo Track

1. Phase 15A: UI/UX Audit and Redesign Planning - completed
2. Phase 15B-1: Public UI Polish - next
3. Phase 15B-2: Owner Layout and Dashboard Polish
4. Phase 15B-3: Owner CRUD Page Polish
5. Phase 15B-4: Tenant Portal Polish
6. Phase 15C: UI Regression and Demo Package

## Recommended Production Track

1. Phase 14B-2: Production Settings Split Planning
2. Phase 14C: Owner Billing Detail / Utility Entry
3. Phase 14D: Account Lifecycle
4. Phase 14E: Deployment Readiness
5. CI/test coverage
6. Optional legacy cleanup

## Current Recommendation

Because the current UI feels weak and less realistic than expected, prioritize the Demo Track first.

Do not start production settings implementation until UI/demo polish has a clear plan or unless the user explicitly changes priority.
