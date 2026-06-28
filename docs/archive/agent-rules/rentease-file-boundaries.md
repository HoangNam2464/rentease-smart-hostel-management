# RentEase File Boundaries

This file defines which files and apps are active RentEase surfaces versus legacy HOSTELLO surfaces.

Read this before editing any template, CSS, app, or admin file.
For full details see `docs/agent/RENTEASE_PROJECT_MAP.md`.

---

## Active Django Apps (RentEase)

Edit these apps for current product work:

| App | Purpose |
|---|---|
| `accounts` | Users and owner profiles |
| `properties` | Rooms |
| `tenants` | Tenants and co-tenants |
| `contracts` | Rental contracts |
| `billing` | Invoices, invoice details, payment history |
| `maintenance` | Repair requests, maintenance records, notifications |
| `listings` | Room listings and viewing registrations |
| `portal` | Owner/tenant portal views, demo seed command |
| `reports` | Staff-only report pages |

All apps live under `backend/<app_name>/`.

---

## Legacy HOSTELLO Apps — Do Not Edit

These apps exist for compatibility. Do not edit, move, or delete them without a dedicated removal audit phase:

- `backend/students/`
- `backend/attendance/`
- `backend/fees/`
- `backend/requests/`
- `backend/notices/`

---

## Active Templates

Templates for current RentEase UI are under `frontend/templates/`:

- `home.html`
- `404.html`, `500.html`
- `portal/base.html`, `portal/login.html`
- `portal/owner_*.html`
- `portal/tenant_*.html`
- `listings/public_listing_list.html`, `listings/public_listing_detail.html`
- `listings/viewing_registration_form.html`, `listings/viewing_registration_success.html`

Reports templates live under `backend/reports/templates/reports/` (exception to the frontend/ rule).

---

## Legacy Templates — Do Not Edit For RentEase UI

- `frontend/templates/dashboard.html`
- `frontend/templates/index.html`
- `frontend/templates/login.html`
- `frontend/templates/admin/`
- `frontend/templates/payments/success.html`
- `assets/` (historical HOSTELLO media)

---

## Active CSS Files

| File | Purpose |
|---|---|
| `frontend/static/css/rentease-design.css` | Global design system: colors, typography, spacing, components |
| `frontend/static/css/rentease-layout.css` | Sidebar, dashboard layout, CRUD tables, forms, responsive behavior |
| `frontend/static/admin/css/custom_admin.css` | Django Admin custom overrides |

**When editing layout or dashboard:** use `rentease-layout.css`.
**When editing global tokens or component styles:** use `rentease-design.css`.

---

## Legacy CSS — Do Not Edit For RentEase UI

- `frontend/static/css/styles.css`
- `frontend/static/css/student-dashboard.css`
- `frontend/static/js/script.js`
- `frontend/static/js/student-dashboard.js`

---

## Sensitive Tenant Fields

The following fields are considered sensitive identity data:

- `citizen_id`
- `citizen_id_front`
- `citizen_id_back`

**Rules:**

- Never expose these fields in admin `list_display` or `search_fields`.
- Never expose these fields on public, owner, or tenant portal surfaces.
- In admin detail forms, these fields must appear only inside a collapsed `Sensitive identity data` fieldset.
- Do not add identity field lookups to any admin `search_fields` configuration.

---

## Django Config Package

The inner Django config package is `backend/hostello_backend/`.

- `DJANGO_SETTINGS_MODULE` = `hostello_backend.settings`
- Do NOT rename this package or change the module path.

---

## Virtual Environment

Official local virtual environment: `backend/venv/`

Always run Django commands from `backend/` using:

```powershell
.\venv\Scripts\python.exe manage.py <command>
```

Do NOT use a root-level venv. The old root-level `venv/` was removed.
