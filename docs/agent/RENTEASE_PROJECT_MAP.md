# RentEase Project Map

## Purpose

This file tells future developers and agents which files are active RentEase surfaces and which files are old HOSTELLO legacy surfaces.

Read this before editing UI, templates, CSS, production settings, cleanup tasks, or productization work.

## Active RentEase Templates

Use these for current RentEase product UI work:

- `frontend/templates/home.html`
- `frontend/templates/listings/public_listing_list.html`
- `frontend/templates/listings/public_listing_detail.html`
- `frontend/templates/listings/viewing_registration_form.html`
- `frontend/templates/listings/viewing_registration_success.html`
- `frontend/templates/portal/base.html`
- `frontend/templates/portal/login.html`
- `frontend/templates/portal/owner_dashboard.html`
- `frontend/templates/portal/owner_*.html`
- `frontend/templates/portal/tenant_*.html`
- `frontend/templates/404.html`
- `frontend/templates/500.html`

## Active CSS

Use these CSS files for current RentEase UI work:

- `frontend/static/css/rentease-design.css` — global design system, colors, typography, spacing
- `frontend/static/css/rentease-layout.css` — sidebar, dashboard layout, CRUD tables, forms, responsive
- `frontend/static/admin/css/custom_admin.css` — custom Django Admin overrides

Both `rentease-design.css` and `rentease-layout.css` are active. Edits to owner dashboard, sidebar, tables, or forms typically go into `rentease-layout.css`. Global design tokens, typography, and component styles go into `rentease-design.css`.

Avoid editing legacy CSS files for RentEase UI:

- `frontend/static/css/styles.css` — legacy HOSTELLO styles
- `frontend/static/css/student-dashboard.css` — legacy HOSTELLO student dashboard

## Active RentEase Apps

Current product apps:

- `accounts`
- `tenants`
- `properties`
- `contracts`
- `billing`
- `maintenance`
- `listings`
- `portal`
- `reports`

## Legacy HOSTELLO Files

These files are old HOSTELLO surfaces. Do not edit them for RentEase UI unless explicitly approved:

- `frontend/templates/dashboard.html`
- `frontend/templates/index.html`
- `frontend/templates/login.html`
- `frontend/templates/admin/`
- `frontend/templates/payments/success.html`
- `frontend/static/css/student-dashboard.css`
- `frontend/static/js/student-dashboard.js`
- `assets/`

## Legacy Apps

These legacy apps still exist for compatibility/history and must not be deleted in normal feature work:

- `students`
- `attendance`
- `fees`
- `requests`
- `notices`

Do not delete them without a separate dependency audit.

## Safe Editing Rules

- Prefer active RentEase templates and `rentease-design.css`.
- Do not rename the inner Django config package `backend/hostello_backend` or the Python module path `hostello_backend`.
- Do not rename Django apps.
- Do not delete legacy apps in normal UI/product work.
- Do not create migrations unless explicitly approved.
- Do not change schema for UI-only or documentation-only work.
- Do not re-add legacy root routes.

## UI Rules

- Public pages should feel like a room/property listing product.
- Owner pages should feel like a clean SaaS dashboard.
- Tenant pages should stay simple, readable, and privacy-safe.
- Use Vietnamese-first copy with proper accents.
- Do not foreground admin/report links on public landing pages.

## Image Handling Rules

- Do not hotlink external images at runtime.
- Do not commit random copyrighted images.
- Do not commit images with visible trademarks/logos or identifiable people.
- Do not commit sensitive media uploads.
- If safe local static images are added later, document source and license.

## Privacy And Security Rules

Never expose:

- `citizen_id`
- `citizen_id_front`
- `citizen_id_back`
- citizen ID files/images
- password/auth internals
- permission fields
- payment collector internals
- other owner data
- other tenant data
- private notes to public/tenant pages

Owner data must stay owner-scoped. Tenant data must stay tenant-scoped.
