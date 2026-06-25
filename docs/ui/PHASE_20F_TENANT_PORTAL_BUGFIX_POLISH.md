# Phase 20F: Tenant Portal Bugfix, Layout Separation, and Polish

## Purpose

Phase 20F focused on the active RentEase tenant portal surfaces after the owner CRUD polish pass.

The goal was to fix tenant-facing template issues first, then apply a consistent visual polish without changing backend behavior, models, routes, permissions, billing, migrations, or schema.

## Tenant Route Inventory

Audited active tenant routes:

- `/tenant/dashboard/`
- `/tenant/profile/`
- `/tenant/contracts/`
- `/tenant/contracts/<id>/`
- `/tenant/invoices/`
- `/tenant/invoices/<id>/`
- `/tenant/payments/`
- `/tenant/repairs/`
- `/tenant/repairs/new/`
- `/tenant/repairs/<id>/`
- `/tenant/notifications/`
- `/tenant/notifications/<id>/`

## Base Layout Findings

- `portal/base.html` still allowed owner and tenant role navigation blocks to render independently.
- A user with overlapping role flags could see both owner and tenant navigation.
- The shared base template contained mojibake Vietnamese copy from an older encoding pass.

## Tenant Template Findings

- Several tenant templates contained mojibake Vietnamese labels.
- Some tenant detail templates still mixed English and Vietnamese copy.
- `tenant_dashboard.html` referenced `recent.invoices`, `recent.repairs`, and `recent.notifications`, but the current view only passes `tenant` and `metrics`.
- The missing `recent` context caused the dashboard recent sections to appear empty even when demo data existed.
- Tenant pages were readable, but visually less aligned with the owner CRUD polish system.

## Fixes Applied

- Rebuilt `portal/base.html` with clean UTF-8 Vietnamese copy.
- Changed role navigation to an `if tenant / elif owner-staff-admin` layout so tenant pages do not show owner sidebar links.
- Rebuilt tenant templates with clean Vietnamese labels and consistent icons.
- Replaced the dashboard's missing `recent.*` sections with quick action cards that use existing routes and current context.
- Kept tenant dashboard metrics based only on the existing `metrics` object.
- Improved tenant page headers, tables, detail cards, form cards, empty states, buttons, and responsive behavior.
- Kept all tenant views, URL names, form fields, querysets, model fields, billing behavior, and permissions unchanged.

## CSS Updated

Added tenant-specific polish to `hostello_backend/static/css/rentease-design.css`:

- tenant hero card
- tenant metric grid
- tenant quick action grid
- tenant section card spacing
- tenant nav unread-count badge
- mobile/responsive handling for tenant cards and actions

## Verification Summary

Checks run:

- `.\venv\Scripts\python.exe manage.py check`
- `.\venv\Scripts\python.exe manage.py makemigrations --check --dry-run`
- Django Client smoke test for tenant list/detail/form pages with `tenant_test`
- Django Client regression smoke test for key owner pages with `owner_test`
- Rendered-page scan for raw template tags and sensitive field names
- Rendered-page scan to ensure tenant pages did not show owner sidebar links

Smoke-tested tenant pages:

- tenant dashboard
- tenant profile
- tenant contracts list/detail
- tenant invoices list/detail
- tenant payments
- tenant repairs list/create/detail
- tenant notifications list/detail

Owner regression pages:

- owner dashboard
- owner rooms
- owner invoices

## Security and Privacy Result

No tenant template was changed to expose:

- `citizen_id`
- citizen ID image/file fields
- password/auth fields
- permission fields
- payment collector internals
- owner/internal notes
- unrelated owner data
- unrelated tenant data

## Files Changed

- `hostello_backend/templates/portal/base.html`
- `hostello_backend/templates/portal/tenant_dashboard.html`
- `hostello_backend/templates/portal/tenant_profile.html`
- `hostello_backend/templates/portal/tenant_contracts_list.html`
- `hostello_backend/templates/portal/tenant_contract_detail.html`
- `hostello_backend/templates/portal/tenant_invoices_list.html`
- `hostello_backend/templates/portal/tenant_invoice_detail.html`
- `hostello_backend/templates/portal/tenant_payments_list.html`
- `hostello_backend/templates/portal/tenant_repairs_list.html`
- `hostello_backend/templates/portal/tenant_repair_form.html`
- `hostello_backend/templates/portal/tenant_repair_detail.html`
- `hostello_backend/templates/portal/tenant_notifications_list.html`
- `hostello_backend/templates/portal/tenant_notification_detail.html`
- `hostello_backend/static/css/rentease-design.css`

## Remaining Notes

- A manual browser pass is still useful for checking exact mobile table overflow and visual spacing.
- The tenant portal is still local-demo oriented. Production readiness still requires production settings, deployment hardening, and broader automated test coverage.

## Next Recommended Phase

```text
Phase 20G: Reports, Error Pages, and Final UI Consistency Review
```

Recommended scope:

- staff reports visual consistency
- custom error-page consistency
- remaining public/portal visual edge cases
- no model, schema, billing, permission, or route changes unless explicitly approved
