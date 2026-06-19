# RentEase Screenshot Checklist

## Purpose

Capture a clean visual set for project presentation, README updates, or a short demo video.

## Public Screenshots

- [ ] Landing page at `/`
- [ ] Public room list at `/rooms/`
- [ ] Public room detail, for example `/rooms/12/`
- [ ] Viewing registration form, for example `/rooms/12/register/`
- [ ] Viewing registration success page, for example `/rooms/12/register/success/`
- [ ] Portal login at `/login/`

## Owner Screenshots

- [ ] Owner dashboard at `/owner/dashboard/`
- [ ] Owner rooms list at `/owner/rooms/`
- [ ] Owner room detail if demo data exists
- [ ] Owner room create/edit form
- [ ] Owner listings list at `/owner/listings/`
- [ ] Owner listing detail if demo data exists
- [ ] Owner tenants list at `/owner/tenants/`
- [ ] Owner contracts list at `/owner/contracts/`
- [ ] Owner invoices list at `/owner/invoices/`
- [ ] Owner invoice detail if demo data exists
- [ ] Owner payment recording form if demo data exists
- [ ] Owner repairs list at `/owner/repairs/`
- [ ] Owner viewing registrations list at `/owner/viewing-registrations/`

## Tenant Screenshots

- [ ] Tenant dashboard at `/tenant/dashboard/`
- [ ] Tenant profile at `/tenant/profile/`
- [ ] Tenant contracts list at `/tenant/contracts/`
- [ ] Tenant contract detail if demo data exists
- [ ] Tenant invoices list at `/tenant/invoices/`
- [ ] Tenant invoice detail if demo data exists
- [ ] Tenant payments list at `/tenant/payments/`
- [ ] Tenant repairs list at `/tenant/repairs/`
- [ ] Tenant repair submission form at `/tenant/repairs/new/`
- [ ] Tenant notifications list at `/tenant/notifications/`

## Admin And Reports Screenshots

- [ ] Admin login redirect from `/admin/`
- [ ] Reports protected redirect from `/reports/` as anonymous
- [ ] Reports dashboard as staff/admin if a staff demo account is available

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

## Current Limitation

At Phase 15C, public listing screenshots are available, but owner and tenant detail screenshots need scoped demo data.

Recommended next phase:

```text
Phase 15D: Demo Data Readiness Plan
```

