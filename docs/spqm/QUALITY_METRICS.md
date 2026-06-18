# RentEase Quality Metrics

## Current Measurable Items

| Metric | Current Baseline | Status |
| --- | --- | --- |
| Local demo ready | Yes | Verified by prior release tag |
| Production ready | No | Known gap |
| Latest hardening phase | Phase 14B-1 Legacy Root API / Fees Cleanup | Verified by tag |
| Latest docs phase | Agent guidance docs baseline | Commit exists; separate tag not verified |
| Django system check | Passes | Verified before this SPQM baseline |
| Migration dry-run | No changes detected | Verified before this SPQM baseline |
| Full regression before hardening | 128/128 passed | Recorded from Phase 12B |
| Migrations pending | No | Verified by dry-run |
| Root legacy `/api/` exposure | Removed | Phase 14B-1 |
| Root legacy `/fees/` exposure | Removed | Phase 14B-1 |
| Documented phases | 12 listed locked phases | Baseline count |
| Locked documentation baselines | Agent docs baseline planned; SPQM baseline planned | Tags pending during SPQM integration |
| UI pages audited | Not verified | Planned |
| UI pages polished | Not verified | Planned |
| Demo checklist status | Partially complete | Needs final review per release checklist |
| Production blockers remaining | 7 known blockers | See production blockers section |
| CI pass rate | Not verified | Planned |
| Test coverage | Not verified | Planned |

## Completed Locked Phase Count

Current known locked product/hardening tags include:

- Phase 8B-2
- Phase 8C-1
- Phase 8D-1
- Phase 8E-1
- Phase 8F-1
- Phase 8G-1
- Phase 12A-1
- Phase 12A-2
- Phase 12B-1
- Phase 12B
- Phase 12C
- Phase 14B-1

Count: 12 listed locked phases.

## Production Blockers Remaining

Known production blockers:

- production settings not hardened
- production database not configured
- owner-facing billing details and utility entry incomplete
- account lifecycle incomplete
- deployment/static/media/email/logging not production-ready
- automated CI and test coverage not verified
- legacy apps still present, though root exposure has been reduced

## UI And Documentation Quality Metrics

Track these during demo/product polish:

- number of documented phases
- number of locked documentation baselines
- UI pages audited
- UI pages polished
- demo checklist status
- documentation readiness checklist status
- production blockers remaining

Baseline:

| Metric | Baseline |
| --- | --- |
| Documented phases | 12 listed locked phases |
| Locked documentation baselines | Agent guidance docs baseline and SPQM baseline expected after integration |
| UI pages audited | Not verified |
| UI pages polished | Not verified |
| Demo checklist status | Partially complete |
| Production blockers remaining | 7 known blockers |

## Future Metrics

Track later:

- test coverage percentage
- failed test count
- CI pass rate
- lead time from commit to merge
- bug count by severity
- escaped defects after release
- SonarQube issues if added later
- production incident count
- mean time to restore service

## Metric Collection Rules

Do not claim a metric is complete unless verified.

Mark unknown items as:

```text
Not verified
```

Mark future items as:

```text
Planned
```

Prefer evidence from:

- Django check output
- migration dry-run output
- route regression results
- git tags
- committed test results
- CI logs when CI exists
