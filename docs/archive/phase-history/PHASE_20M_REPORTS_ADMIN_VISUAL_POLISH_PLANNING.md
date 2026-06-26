# Phase 20M: Reports And Admin Visual Polish Planning

## Status

Completed.

## Goal

Review staff-facing reports and Django Admin/Jazzmin surfaces, apply only safe display-level polish, and document any risky admin/privacy changes for a later focused phase.

This phase did not change models, migrations, schema, views, URLs, report calculations, query logic, billing logic, owner/tenant scoping, admin permissions, or legacy apps.

## Areas Reviewed

### Reports

Reviewed staff report routes:

- `/reports/`
- `/reports/billing/`
- `/reports/rooms/`
- `/reports/tenants-contracts/`
- `/reports/maintenance/`
- `/reports/listings/`

Reviewed report templates:

- `backend/reports/templates/reports/base.html`
- `backend/reports/templates/reports/dashboard.html`
- `backend/reports/templates/reports/billing_report.html`
- `backend/reports/templates/reports/room_report.html`
- `backend/reports/templates/reports/tenant_contract_report.html`
- `backend/reports/templates/reports/maintenance_report.html`
- `backend/reports/templates/reports/listing_report.html`

### Admin

Reviewed admin-facing surfaces through route/render checks:

- `/admin/`
- `/admin/tenants/tenant/`
- `/admin/tenants/cotenant/`
- `/admin/properties/room/`
- `/admin/contracts/contract/`
- `/admin/billing/invoice/`
- `/admin/billing/paymenthistory/`

Reviewed admin-related files:

- `backend/tenants/admin.py`
- `backend/properties/admin.py`
- `backend/contracts/admin.py`
- `backend/billing/admin.py`
- `frontend/static/admin/css/custom_admin.css`
- Jazzmin settings in `backend/backend/settings.py`

## Current Visual Issues Found

### Reports

- Several report pages still had English labels and empty-state text.
- Some Vietnamese text in report templates was mojibake/encoding-damaged.
- Tables were not consistently wrapped in the existing `report-table-wrap` container.
- Filter layout worked, but could use better mobile wrapping and clearer button styling.
- Report summary cards were functional, but needed clearer text hierarchy.

### Admin

- Jazzmin/admin pages are usable and branded as RentEase.
- Tenant and CoTenant admin list pages no longer show citizen ID fields after Phase 20K-A.
- Room, Contract, Invoice, and Payment admin changelists render successfully.
- Larger admin visual redesign was considered risky for this phase because it can affect all staff admin screens.

## Safe Changes Applied

Applied report-template polish only:

- Replaced mojibake report copy with readable Vietnamese.
- Converted report headings, table headers, filters, and empty states to Vietnamese.
- Improved report shell CSS inside `reports/base.html`.
- Improved report navigation spacing and hover state.
- Improved metric card hierarchy.
- Improved filter form spacing and mobile wrapping.
- Wrapped report tables consistently in `report-table-wrap`.
- Added clearer empty-state table rows through `empty-report-row`.

No admin/Jazzmin styling or admin model configuration was changed in this phase.

## Risky Changes Deferred

Deferred to a later admin/privacy hardening phase:

- Removing `tenant__citizen_id` from admin `search_fields` in non-tenant admin classes.
- Changing admin fieldsets or read-only rules outside Tenant/CoTenant.
- Large Jazzmin layout or sidebar redesign.
- Custom admin changelist templates.
- Any admin permission model changes.

Reason: those changes can affect staff workflows and should be handled in a focused admin/privacy phase with explicit review.

## Privacy And Security Checks

Verified that the following pages do not render `citizen_id`, `Citizen id`, `CCCD`, or `CMND` in list/page HTML:

- `/admin/tenants/tenant/`
- `/admin/tenants/cotenant/`
- `/admin/properties/room/`
- `/admin/contracts/contract/`
- `/admin/billing/invoice/`
- `/admin/billing/paymenthistory/`

Report routes were also checked for raw template tags and sensitive markers.

## Verification

### Django

- `.\venv\Scripts\python.exe manage.py check` passed.
- `.\venv\Scripts\python.exe manage.py makemigrations --check --dry-run` reported `No changes detected`.

### Route Checks

The following routes returned HTTP 200 with the correct authenticated demo account:

- `/owner/dashboard/`
- `/owner/rooms/`
- `/owner/tenants/`
- `/owner/contracts/`
- `/owner/invoices/`
- `/tenant/dashboard/`
- `/tenant/invoices/`
- `/reports/`
- `/reports/billing/`
- `/reports/rooms/`
- `/reports/tenants-contracts/`
- `/reports/maintenance/`
- `/reports/listings/`
- `/admin/`
- `/admin/tenants/tenant/`
- `/admin/tenants/cotenant/`

Additional admin model changelists checked:

- `/admin/properties/room/`
- `/admin/contracts/contract/`
- `/admin/billing/invoice/`
- `/admin/billing/paymenthistory/`

## Browser Automation Note

Browser automation was not used for new screenshot capture in this phase because prior browser automation was unstable after screenshot timeouts. Verification used Django Client route/render/privacy checks instead.

## Recommended Next Phase

```text
Phase 20N: Admin Search Privacy Hardening Planning
```

Goal: review admin `search_fields`, list displays, fieldsets, and read-only behavior across non-tenant admin classes to remove or reduce sensitive identity lookup surfaces without disrupting staff workflows.
