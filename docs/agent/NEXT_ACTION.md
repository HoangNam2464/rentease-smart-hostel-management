# RentEase Next Action

## Responsibility of This File

This file answers one question: **what should the agent do next?**

For broader project state, read `docs/agent/RENTEASE_CURRENT_STATE.md`.
For file boundaries and active/legacy rules, read `docs/agent/RENTEASE_PROJECT_MAP.md`.
For workflow and safety rules, read `AGENTS.md`.

---

## Last Completed Phase

```text
Phase 14B-2: Production Settings Split
```

What was done: Refactored `settings.py` to be fully environment-driven via `python-decouple`. Added `whitenoise` for static files, `dj-database-url` for `DATABASE_URL` support, production security headers (conditional on `DEBUG=False`), `Asia/Ho_Chi_Minh` timezone, `RentEase` branding, production-ready logging. Removed legacy `HOSTELLO_EMAIL_SETTINGS` block. Created `.env.example`.

---

## ⚠️ Immediate Next Phase

```text
Phase 14C: PostgreSQL Migration Planning
```

**This is a PLANNING ONLY phase. Do not implement without explicit user approval.**

Goal: Plan migration from SQLite to PostgreSQL for production readiness.

Scope: `DATABASE_URL` configuration, data migration strategy, backup plan, PostgreSQL setup instructions.

---

## Do Not Do Yet

- Do not implement Phase 14C without a separate approved plan.
- Do not delete legacy apps (`students`, `attendance`, `fees`, `requests`, `notices`).
- Do not delete legacy templates or static files.
- Do not rename `backend/hostello_backend/`.
- Do not use real personal data in demo records.
- Do not push to GitHub without explicit approval.
