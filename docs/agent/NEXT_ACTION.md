# RentEase Next Action

## Responsibility of This File

This file answers one question: **what should the agent do next?**

For broader project state, read `docs/agent/RENTEASE_CURRENT_STATE.md`.
For file boundaries and active/legacy rules, read `docs/agent/RENTEASE_PROJECT_MAP.md`.
For workflow and safety rules, read `AGENTS.md`.

---

## Last Completed Phase

```text
Phase 20O: Admin Sensitive Detail Permission Hardening
```

What was done: Made `citizen_id`, `citizen_id_front`, `citizen_id_back` read-only for non-superuser staff in `TenantAdmin` and `CoTenantAdmin` detail forms. Superusers retain full edit access.

---

## ⚠️ Immediate Next Phase

```text
Phase 14B-2: Production Settings Split Planning
```

**This is a PLANNING ONLY phase. Do not implement without explicit user approval.**

Goal: Make Django settings production-aware while preserving local development.

Scope: `DEBUG`, `SECRET_KEY`, `ALLOWED_HOSTS`, HTTPS headers, secure cookies, database config, static/media, email, logging, `.env` support.

Steps:
1. Produce a written plan with options.
2. Present to user for approval.
3. Implement only after explicit approval.

Files that would likely be affected:
- `backend/hostello_backend/settings.py` (split or extend)
- Possibly a new `backend/hostello_backend/settings_production.py`
- Possibly `.env.example`

---

## Do Not Do Yet

- Do not implement Phase 14B-2 without a separate approved plan.
- Do not delete legacy apps (`students`, `attendance`, `fees`, `requests`, `notices`).
- Do not delete legacy templates or static files.
- Do not rename `backend/hostello_backend/`.
- Do not use real personal data in demo records.
- Do not push to GitHub without explicit approval.
