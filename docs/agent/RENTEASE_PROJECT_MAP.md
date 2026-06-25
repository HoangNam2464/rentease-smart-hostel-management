# RentEase Project Map

## Purpose

This file tells future developers and agents which files are active RentEase surfaces and which files are old HOSTELLO legacy surfaces.

Read this before editing UI, templates, CSS, production settings, cleanup tasks, or productization work.

## Active RentEase Templates

Use these for current RentEase product UI work:

- `hostello_backend/templates/home.html`
- `hostello_backend/templates/listings/public_listing_list.html`
- `hostello_backend/templates/listings/public_listing_detail.html`
- `hostello_backend/templates/listings/viewing_registration_form.html`
- `hostello_backend/templates/listings/viewing_registration_success.html`
- `hostello_backend/templates/portal/base.html`
- `hostello_backend/templates/portal/login.html`
- `hostello_backend/templates/portal/owner_dashboard.html`
- `hostello_backend/templates/portal/owner_*.html`
- `hostello_backend/templates/portal/tenant_*.html`
- `hostello_backend/templates/404.html`
- `hostello_backend/templates/500.html`

## Active CSS

Use this CSS for current RentEase UI work:

- `hostello_backend/static/css/rentease-design.css`

Avoid editing old student dashboard CSS for RentEase UI.

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

- `hostello_backend/templates/dashboard.html`
- `hostello_backend/templates/index.html`
- `hostello_backend/templates/login.html`
- `hostello_backend/templates/admin/`
- `hostello_backend/templates/payments/success.html`
- `hostello_backend/static/css/student-dashboard.css`
- `hostello_backend/static/js/student-dashboard.js`
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
- Do not rename `hostello_backend`.
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
