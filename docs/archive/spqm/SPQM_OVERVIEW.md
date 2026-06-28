# RentEase SPQM Overview

## Purpose

RentEase uses Software Process & Quality Management style documentation to make future work safer, easier to review, and easier to measure.

This documentation is adapted to the actual RentEase technology stack:

- Python
- Django
- Django Admin/Jazzmin
- Django templates
- SQLite for local development at the current state

Generic Node.js/Express process requirements are adapted, not copied. Do not convert RentEase to Node.js, Express, Jest, or ESLint to satisfy SPQM documentation.

## Why This Exists

RentEase started from the HOSTELLO project and has been evolved through small locked phases. The project now has local-demo readiness and is being hardened toward real production use.

The SPQM documentation supports:

- planning clear phases before implementation
- defining quality gates before work is accepted
- measuring current project health
- tracking release readiness
- identifying production gaps honestly
- guiding continuous improvement

## Document Set

The SPQM baseline includes:

- `PROCESS_MODEL.md` for lifecycle and ETVX process control
- `DEFINITION_OF_DONE.md` for phase completion rules
- `BACKLOG_AND_PRIORITIES.md` for prioritized work
- `CHANGE_MANAGEMENT.md` for safe change handling
- `QUALITY_METRICS.md` for measurable quality signals
- `RETROSPECTIVE_TEMPLATE.md` for improvement review
- `CMMI_SELF_ASSESSMENT.md` for maturity assessment
- `RELEASE_CHECKLIST.md` for release readiness
- `PYTHON_DJANGO_QUALITY_STACK.md` for Python/Django equivalents of generic quality tooling

## Current Baseline

Current classification:

```text
C. Usable locally, but not production-ready.
```

Known current state:

- local demo release exists
- production-hardening has started
- root legacy `/api/` and `/fees/` exposure has been removed
- Django check passes
- migration dry-run reports no changes
- production settings, production database, CI, coverage, and deployment readiness are not complete

## How To Use These Documents

Before each phase:

1. Read `AGENTS.md`.
2. Read the relevant `docs/agent/` files.
3. Read the relevant SPQM file.
4. Verify branch, git status, tags, Django check, and migration dry-run.
5. Produce a plan before implementation for risky areas.

After each locked phase:

1. Record the result in current-state documentation if approved.
2. Update backlog or metrics if the phase changes priorities.
3. Do not silently rewrite SPQM docs during unrelated feature work.
