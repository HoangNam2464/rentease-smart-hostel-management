# RentEase SPQM Report

## Summary

RentEase uses SPQM documentation to track process, quality, risks, backlog, and release readiness.

Related files:

- `docs/spqm/SPQM_OVERVIEW.md`
- `docs/spqm/PROCESS_MODEL.md`
- `docs/spqm/DEFINITION_OF_DONE.md`
- `docs/spqm/BACKLOG_AND_PRIORITIES.md`
- `docs/spqm/QUALITY_METRICS.md`
- `docs/spqm/RELEASE_CHECKLIST.md`

## Current Classification

RentEase is local-demo ready, not production-ready.

## Quality Gates

- Django check must pass.
- Migration dry-run must show `No changes detected` unless migrations are approved.
- Owner/tenant privacy must be preserved.
- Sensitive local files must not be committed.
- Legacy root routes must not be re-added.

## Next Quality Focus

Phase 21C should safely clean repo hygiene without deleting local work blindly.
