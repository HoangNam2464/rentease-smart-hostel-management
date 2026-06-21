# RentEase Screenshot Checklist

## Purpose

Capture a clean visual set for project presentation, README updates, or a short demo video.

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
- [ ] Owner viewing registrations list at `/owner/viewing-registrations/`

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

## Current Demo Data Status

After Phase 15F, scoped owner and tenant demo records were verified for screenshots.

Recommended next phase:

```text
Phase 16A: README and Final Demo Package Polish
```
