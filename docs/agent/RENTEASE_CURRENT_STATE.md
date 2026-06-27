# RentEase Current State

## Branch

```text
complete-product
```

Do not rely on this file alone for the latest commit. Always verify with:

```powershell
git log --oneline -15
```

## Current Status

RentEase is **local-demo ready**.

RentEase is **not production-ready yet**.

## Latest Phase Completed

```text
Phase 20N: Admin Search Privacy Hardening
```

Tag:

```text
phase20n-admin-search-privacy-hardening
```

## Recent Commits (as of 2026-06-27)

```text
9bf9051 Set up RentEase agent documentation
c3465c0 Polish realistic demo data
6ba89c4 Consolidate RentEase documentation
549b3de Add final demo checklist
b4c7324 Update README for RentEase project
fbed1d6 Archive unused helper files
```

## Release Tags

Final local demo release tags:

```text
release-rentease-complete-product-v1
release-rentease-polished-local-demo-v2
```

## Current Structure

```text
RentEase/
├── backend/   # Django backend, apps, manage.py, settings
├── frontend/  # Django Templates and static assets
└── docs/      # Documentation
```

Important paths:

- Django project folder: `backend/`
- Django config package: `backend/hostello_backend/`
- Settings module: `hostello_backend.settings`
- Template root: `frontend/templates/`
- Static root: `frontend/static/`
- Official local virtual environment: `backend/venv/`
- Demo seed command: `backend/portal/management/commands/seed_rentease_demo_data.py`

The old root-level `venv/` was removed safely. Use only `backend/venv/` for local Django commands.

## Active CSS Files

The current RentEase UI uses two main CSS files:

- `frontend/static/css/rentease-design.css` — global design system, colors, typography
- `frontend/static/css/rentease-layout.css` — sidebar, dashboard layout, CRUD tables and forms

Also active:

- `frontend/static/admin/css/custom_admin.css` — custom admin overrides

Legacy CSS files remain but are not used for active RentEase UI:

- `frontend/static/css/styles.css`
- `frontend/static/css/student-dashboard.css`

## Completed UI Phases Summary

- Phase 15A–C: UI/UX Audit and Public/Owner/Tenant Polish
- Phase 17A–C: Full UI Completeness Audit and Final Visual QA
- Phase 19A–B: Product-grade UI redesign and Vietnamese copy
- Phase 20A–D: Professional UI redesign system, full redesign
- Phase 20E: Owner CRUD Polish
- Phase 20F: Tenant Portal Bugfix Polish
- Phase 20G: RentEase UI v2 — dark sidebar
- Phase 20H: Full UI Visual QA
- Phase 20I: Full Role UI/UX Audit
- Phase 20J: Browser Visual QA (found citizen_id exposure in admin list)
- Phase 20K-A: Admin Tenant Privacy Hotfix (removed citizen_id from TenantAdmin/CoTenantAdmin list)
- Phase 20K-B: Dashboard Interaction Visual Polish
- Phase 20L: Owner CRUD Form and Table Professionalization
- Phase 20M: Reports and Admin Visual Polish Planning
- Phase 20N: Admin Search Privacy Hardening (removed citizen_id from ContractAdmin/InvoiceAdmin search_fields)

## Current Verification Status

Latest verified state:

- `manage.py check` passed: `System check identified no issues (0 silenced)`.
- `makemigrations --check --dry-run` reported `No changes detected`.
- Admin tenant/co-tenant list pages: confirmed citizen_id not exposed.
- Admin contract/invoice search_fields: confirmed citizen_id lookups removed.
- Owner dashboard, rooms, tenants, contracts, invoices: return 200 for owner role.
- Tenant dashboard, invoices, payments: return 200 for tenant role.
- Staff reports and admin homepage: accessible to staff.

## Current Security/Privacy Status

Known admin privacy hardening done:

1. `TenantAdmin`: removed `citizen_id` from `list_display` and `search_fields`. Moved identity fields to collapsed `Sensitive identity data` fieldset.
2. `CoTenantAdmin`: same treatment.
3. `ContractAdmin`: removed `tenant__citizen_id` from `search_fields`. Replaced with `tenant__phone_number` and `tenant__email`. `CoTenantInline` restricted to safe non-identity fields.
4. `InvoiceAdmin`: removed `contract__tenant__citizen_id` from `search_fields`. Replaced with safe contact fields.

Remaining privacy recommendation (not yet implemented):

- Decide whether to make `citizen_id`, `citizen_id_front`, `citizen_id_back` read-only or superuser-only in admin detail forms (Phase 20O).

## Current Demo Documentation

Primary demo docs:

- `docs/demo/FINAL_DEMO_CHECKLIST.md`
- `docs/demo/DEMO_DATA_SEED_USAGE.md`
- `docs/demo/LOCAL_SETUP_AND_DEMO_DATA.md`
- `docs/demo/FINAL_DEMO_PACKAGE.md`
- `docs/demo/DEMO_SCRIPT.md`

Also at root: `DEMO_SCRIPT.md` (copy/shortcut)

## Current Architecture Documentation

Primary architecture docs:

- `docs/architecture/PROJECT_STRUCTURE_MAP.md`
- `docs/architecture/LEGACY_DEPENDENCY_AUDIT.md`
- `docs/architecture/HELPER_FILE_CLEANUP.md`
- `docs/architecture/CLEANUP_AUDIT.md`

## Legacy Status

Legacy HOSTELLO apps remain in the repository:

- `students`
- `attendance`
- `fees`
- `requests`
- `notices`

They are still installed and have models, migrations, admin registrations, and cross-imports. Do not delete or move them without a dedicated legacy removal plan.

Legacy HOSTELLO routes are isolated under `/legacy/`.

## Current Known Gaps

- Production settings are not hardened (`DEBUG=True`, `SECRET_KEY` not env-driven).
- Production database/static/media/email/logging are not configured.
- Legacy HOSTELLO surfaces still exist under `/legacy/` and in admin legacy templates.
- Admin detail forms still allow all staff to edit sensitive identity fields (Phase 20O pending).
- No automated test suite exists (Django Client checks used in place of formal tests).
- Browser screenshot capture was unavailable in recent phases due to automation instability.

## Recommended Next Action

```text
Phase 20O: Admin Sensitive Detail Permission Planning
```

Then:

```text
Phase 14B-2: Production Settings Split Planning
```

See `docs/agent/NEXT_ACTION.md` for the exact next step.
See `docs/agent/RENTEASE_PRODUCTION_ROADMAP.md` for the full production roadmap.
