# RentEase Legacy Boundaries

This is the current reference for deciding whether a RentEase task belongs to active product code or retained HOSTELLO code. Use `PROJECT_STRUCTURE_MAP.md` for the full repository map.

## Active RentEase Areas

- Backend apps: `accounts`, `properties`, `tenants`, `contracts`, `billing`, `maintenance`, `listings`, `portal`, and `reports`
- Templates: `frontend/templates/home.html`, `frontend/templates/listings/`, `frontend/templates/portal/`, `frontend/templates/reports/`, `404.html`, and `500.html`
- Styles: `rentease-design.css`, `rentease-layout.css`, and `admin/css/custom_admin.css`
- Product routes: public room pages, owner portal, tenant portal, admin, and staff reports

Normal RentEase feature, security, and UI work should target these areas.

## Retained Legacy Areas

- Django apps: `students`, `attendance`, `fees`, `requests`, and `notices`
- Templates: root `index.html`, `login.html`, `dashboard.html`, `frontend/templates/admin/`, and `frontend/templates/payments/success.html`
- Static assets: `styles.css`, `student-dashboard.css`, `script.js`, `student-dashboard.js`, and root `assets/`
- Allowed routes: `/legacy/` and `/legacy/login/`

These areas remain for compatibility and historical completeness. Some still have models, migrations, admin registrations, imports, or route dependencies.

## Editing Boundary

- Do not move, rename, delete, or modernize legacy areas during ordinary RentEase work.
- Do not re-add legacy root routes such as the old students root, `/api/`, or `/fees/` routes.
- Legacy cleanup requires a dedicated dependency review, an approved plan, and the standard Django checks.
- Treat `LEGACY_DEPENDENCY_AUDIT.md` as historical evidence, not current policy or proof that dependencies are unchanged.
