# RentEase Screenshot Checklist

## Purpose

Capture a clean visual set for project presentation, README updates, or a short demo video.

Use this checklist together with:

```text
docs/ui/PHASE_17C_FINAL_VISUAL_QA.md
```

## Public Screenshots

- [ ] Landing page at `/`
- [ ] Public room list at `/rooms/`
- [ ] Public room detail from the first visible published listing
- [ ] Viewing registration form for the selected published listing
- [ ] Viewing registration success page for the selected published listing
- [ ] Portal login at `/login/`

## Owner Screenshots

- [ ] Owner dashboard at `/owner/dashboard/`
- [ ] Owner rooms list at `/owner/rooms/`
- [ ] Owner room detail
- [ ] Owner room create/edit form
- [ ] Owner listings list at `/owner/listings/`
- [ ] Owner listing detail
- [ ] Owner tenants list at `/owner/tenants/`
- [ ] Owner contracts list at `/owner/contracts/`
- [ ] Owner invoices list at `/owner/invoices/`
- [ ] Owner invoice detail
- [ ] Owner payment recording form
- [ ] Owner repairs list at `/owner/repairs/`
- [ ] Owner repair process form
- [ ] Owner viewing registrations list at `/owner/viewing-registrations/`
- [ ] Owner viewing registration process form

## Tenant Screenshots

- [ ] Tenant dashboard at `/tenant/dashboard/`
- [ ] Tenant profile at `/tenant/profile/`
- [ ] Tenant contracts list at `/tenant/contracts/`
- [ ] Tenant contract detail
- [ ] Tenant invoices list at `/tenant/invoices/`
- [ ] Tenant invoice detail
- [ ] Tenant payments list at `/tenant/payments/`
- [ ] Tenant repairs list at `/tenant/repairs/`
- [ ] Tenant repair submission form at `/tenant/repairs/new/`
- [ ] Tenant notifications list at `/tenant/notifications/`

## Admin And Reports Screenshots

- [ ] Admin login redirect from `/admin/`
- [ ] Reports protected redirect from `/reports/` as anonymous
- [ ] Reports dashboard as staff/admin if a staff demo account is available
- [ ] Billing report as staff/admin
- [ ] Room report as staff/admin
- [ ] Listing report as staff/admin

## Error Page Screenshots

- [ ] RentEase 404 page under `DEBUG=False` if environment allows
- [ ] RentEase 500 page only if safely simulated later

## Legacy Safety Screenshots

- [ ] `/legacy/` still loads under legacy prefix
- [ ] `/legacy/login/` still loads under legacy prefix
- [ ] `/api/requests/` returns 404
- [ ] `/fees/` returns 404

## Privacy Review Before Sharing

Before publishing screenshots, confirm:

- [ ] no real passwords are visible
- [ ] no real citizen ID values are visible
- [ ] no citizen ID images/files are visible
- [ ] no `.env`, SECRET_KEY, database path, or backup file names are visible
- [ ] no private owner or tenant data from real users is visible
- [ ] no raw Django template tags are visible
- [ ] no broken static assets are visible

## Current Demo Data Status

After Phase 17C, this checklist is aligned with the final visual QA plan.

Recommended next phase:

```text
Phase 18A: Screenshot Capture and Demo Video Preparation
```
