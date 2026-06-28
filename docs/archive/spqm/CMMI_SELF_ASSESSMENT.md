# RentEase CMMI-Style Self Assessment

## Scope

This is a lightweight self-assessment for process maturity. It is not a formal CMMI certification.

## Maturity Levels Used

Level 1 Initial:

- work is mostly ad hoc
- success depends on individual effort
- process is not consistently documented

Level 2 Managed:

- work is planned and tracked
- phases and commits are controlled
- basic verification exists
- risks are identified before work

Level 3 Defined:

- processes are documented and repeatable
- quality gates are standard
- metrics are collected
- improvement loops exist
- automated quality support is expected

## Current RentEase Assessment

RentEase is between Level 2 and early Level 3 for process documentation.

Reasons:

- phase-based work is used
- commits and tags lock milestones
- agent guidance docs exist
- SPQM baseline docs now exist
- Django check and migration dry-run are standard gates
- route and privacy verification are commonly required

RentEase is not fully Level 3 yet.

Reasons:

- CI is not verified
- coverage is not verified
- automated regression tests are incomplete or not confirmed
- production settings are not complete
- deployment documentation is incomplete
- quality metrics are partially manual

## Strengths

- clear branch safety rules
- phase-based implementation
- locked tags for milestones
- documented owner/tenant scoping rules
- documented privacy constraints
- production gaps are acknowledged honestly

## Gaps

- CI not complete
- coverage not complete
- production settings not complete
- UI polish incomplete for a full production product
- billing workflow incomplete
- deployment docs incomplete
- production database not configured
- account lifecycle incomplete

## Recommended Improvement Path

1. Complete Phase 14B-2 Production Settings Split.
2. Add automated Django tests for core owner/tenant permissions.
3. Add CI for Django check, migrations check, and tests.
4. Add coverage reporting.
5. Complete owner billing details and utility entry.
6. Complete deployment documentation and production environment setup.

## Target Maturity

Near-term target:

```text
Solid Level 2 with repeatable quality gates.
```

Medium-term target:

```text
Level 3-style defined process with CI, tests, metrics, and documented deployment.
```
