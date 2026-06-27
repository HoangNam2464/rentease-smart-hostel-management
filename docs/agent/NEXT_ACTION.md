# RentEase Next Action

## Responsibility of This File

This file answers one question: **what should the agent do next?**

For broader project state, read `docs/agent/RENTEASE_CURRENT_STATE.md`.
For file boundaries and active/legacy rules, read `docs/agent/RENTEASE_PROJECT_MAP.md`.
For workflow and safety rules, read `AGENTS.md`.

---

## Last Completed Phase

```text
Phase 20N: Admin Search Privacy Hardening
```

Tag: `phase20n-admin-search-privacy-hardening`

What was done: Removed `citizen_id` lookups from `ContractAdmin.search_fields` and `InvoiceAdmin.search_fields`. Restricted `CoTenantInline` in `ContractAdmin` to safe non-identity fields only.

---

## ⚠️ Immediate Next Phase (Do Not Skip)

```text
Phase 20O: Admin Sensitive Detail Permission Planning
```

**This is a PLANNING ONLY phase. Do not implement without explicit user approval.**

Goal: decide whether `citizen_id`, `citizen_id_front`, `citizen_id_back` in the Tenant/CoTenant **admin detail forms** should:

- remain editable for all staff (current state — not yet hardened)
- become read-only for non-superuser staff
- become superuser-only fields

Steps:
1. Produce a written plan with options.
2. Present to user for approval.
3. Implement only after explicit approval.

Files that would be affected if implemented:
- `backend/tenants/admin.py`

Files that must NOT be changed until approved:
- all other Python, templates, CSS, migrations

---

## Phase After 20O

```text
Phase 14B-2: Production Settings Split Planning
```

Goal: Make Django settings production-aware while preserving local development.

Scope: `DEBUG`, `SECRET_KEY`, `ALLOWED_HOSTS`, HTTPS headers, secure cookies, database config, static/media, email, logging, `.env` support.

**Also planning only. Do not implement without a separate approved plan.**

---

## Do Not Do Yet

- Do not implement Phase 20O without explicit approval.
- Do not implement Phase 14B-2 without a separate approved plan.
- Do not delete legacy apps (`students`, `attendance`, `fees`, `requests`, `notices`).
- Do not delete legacy templates or static files.
- Do not rename `backend/hostello_backend/`.
- Do not use real personal data in demo records.
- Do not push to GitHub without explicit approval.
