# Phase 17C Final Visual QA And Screenshot Checklist

## Purpose

Phase 17C defines the final browser-based visual QA checklist for the polished RentEase UI.

This phase is documentation and verification planning only. It does not change models, migrations, database schema, business logic, billing calculations, production settings, or route security.

## Baseline

Branch:

```text
complete-product
```

Latest commit before this phase:

```text
6bebce2 Polish remaining RentEase UI surfaces
```

Latest UI polish tag:

```text
phase17b-remaining-ui-polish
```

## Preparation Commands

From `hostello_backend`:

```powershell
.\venv\Scripts\python.exe manage.py check
.\venv\Scripts\python.exe manage.py makemigrations --check --dry-run
.\venv\Scripts\python.exe manage.py seed_rentease_demo_data --owner-username owner_test --tenant-username tenant_test
.\venv\Scripts\python.exe manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

## Visual QA Viewports

Check at least:

| Viewport | Purpose |
| --- | --- |
| Desktop around 1366px wide | Main presentation/screenshot layout |
| Mobile around 390px wide | Phone-width responsive layout |

If time is short, prioritize desktop screenshots for presentation and mobile checks for public, login, owner dashboard, tenant dashboard, and reports.

## Browser Pages To Inspect

### Public

| Page | Route | Visual Checks |
| --- | --- | --- |
| Landing | `/` | RentEase branding, CTA buttons, spacing, no HOSTELLO branding |
| Room list | `/rooms/` | Cards align, prices readable, no overflow |
| Room detail | `/rooms/<published_id>/` | image/placeholder, room details, CTA buttons |
| Viewing form | `/rooms/<published_id>/register/` | labels readable, form spacing, validation area |
| Viewing success | `/rooms/<published_id>/register/success/` | confirmation message, next action link |
| Login | `/login/` | card alignment, role-routing panel, no demo password exposure |

### Owner

| Page | Route | Visual Checks |
| --- | --- | --- |
| Dashboard | `/owner/dashboard/` | metrics, recent lists, action buttons |
| Rooms | `/owner/rooms/` | table/cards, actions, empty-state style |
| Room detail | `/owner/rooms/<id>/` | info grouping, action buttons |
| Room form | `/owner/rooms/new/` or edit route | form labels, errors, buttons |
| Listings | `/owner/listings/` | listing rows, status badges |
| Tenants | `/owner/tenants/` | no citizen ID, shared tenant notice if present |
| Contracts | `/owner/contracts/` | table overflow, status clarity |
| Invoices | `/owner/invoices/` | status and amount readability |
| Invoice/payment | `/owner/invoices/<id>/` and payment form | payment action is easy to find |
| Repairs | `/owner/repairs/` | priority/status badges, process action |
| Repair process | `/owner/repairs/<id>/process/` | `Internal owner note` label |
| Viewing registrations | `/owner/viewing-registrations/` | status, visitor info, process action |
| Viewing process | `/owner/viewing-registrations/<id>/process/` | `Staff note` label |

### Tenant

| Page | Route | Visual Checks |
| --- | --- | --- |
| Dashboard | `/tenant/dashboard/` | summary cards, recent items |
| Profile | `/tenant/profile/` | no sensitive ID files, readable profile layout |
| Contracts | `/tenant/contracts/` | list/detail clarity |
| Invoices | `/tenant/invoices/` | status and remaining amount clarity |
| Payments | `/tenant/payments/` | history readability |
| Repairs | `/tenant/repairs/` and `/tenant/repairs/new/` | form is tenant-safe and readable |
| Notifications | `/tenant/notifications/` | list/detail readability |

### Reports And Admin

| Page | Route | Visual Checks |
| --- | --- | --- |
| Reports protected | `/reports/` as anonymous | redirects to admin login |
| Reports dashboard | `/reports/` as staff/admin | report header, nav pills, metrics |
| Billing report | `/reports/billing/` | filter form, responsive table |
| Room report | `/reports/rooms/` | table overflow on mobile |
| Tenant/contract report | `/reports/tenants-contracts/` | table readability |
| Maintenance report | `/reports/maintenance/` | metrics/table readability |
| Listing report | `/reports/listings/` | metrics/table readability |
| Admin | `/admin/` | RentEase admin branding still visible |

### Error And Legacy

| Page | Route | Visual Checks |
| --- | --- | --- |
| 404 page | non-existing route with `DEBUG=False` environment | RentEase branded, no system details |
| 500 page | only if safely simulated later | RentEase branded, no system details |
| Legacy home | `/legacy/` | optional, only to show isolation |
| Legacy login | `/legacy/login/` | optional, legacy-only |
| Removed API | `/api/requests/` | remains 404 |
| Removed fees | `/fees/` | remains 404 |

## Public Visual Checklist

- [ ] Landing page has clear RentEase identity.
- [ ] Primary public CTA leads to room browsing.
- [ ] Login link is easy to find.
- [ ] Room cards align on desktop.
- [ ] Room cards stack cleanly on mobile.
- [ ] Room detail image or placeholder is not stretched awkwardly.
- [ ] Viewing registration form labels are readable.
- [ ] Form error messages do not break layout.
- [ ] Success page gives a clear next step.

## Owner Visual Checklist

- [ ] Owner nav is consistent across owner pages.
- [ ] Dashboard metrics align and wrap cleanly.
- [ ] Recent lists are readable.
- [ ] Tables do not overflow the viewport without horizontal scroll.
- [ ] Create/edit forms have clear labels and buttons.
- [ ] Invoice payment flow is easy to find from invoice detail.
- [ ] Repair processing label says `Internal owner note`.
- [ ] Viewing processing label says `Staff note`.
- [ ] Shared tenant read-only message is understandable if shown.

## Tenant Visual Checklist

- [ ] Tenant nav is consistent across tenant pages.
- [ ] Dashboard summary is readable.
- [ ] Profile page does not show citizen ID fields/files.
- [ ] Contract and invoice details are easy to scan.
- [ ] Payment history is readable.
- [ ] Repair submission form exposes tenant-safe fields only.
- [ ] Notifications list/detail pages are readable.

## Reports/Admin Visual Checklist

- [ ] Anonymous `/reports/` access is blocked.
- [ ] Staff reports have RentEase report header.
- [ ] Report nav pills wrap cleanly.
- [ ] Metrics cards align.
- [ ] Filter forms are readable.
- [ ] Report tables scroll horizontally on mobile if needed.
- [ ] Admin retains RentEase branding.

## Error Pages Visual Checklist

- [ ] Custom 404 page is RentEase branded under `DEBUG=False`.
- [ ] 404 page has no stack trace or system details.
- [ ] 404 page links back to `/`.
- [ ] Custom 500 page template exists and is RentEase branded.
- [ ] 500 page template has no stack trace or system details.

## Responsive/Mobile Checklist

Check around 390px wide:

- [ ] Public landing does not overlap.
- [ ] Room cards stack cleanly.
- [ ] Login card and side panel stack cleanly.
- [ ] Owner nav wraps without hiding links.
- [ ] Tenant nav wraps without hiding links.
- [ ] Tables remain usable with horizontal scroll.
- [ ] Buttons stay tappable.
- [ ] Long text does not escape cards.

Check around 1366px wide:

- [ ] Cards and grids are not too sparse.
- [ ] Page headers align consistently.
- [ ] Tables and cards use available width well.
- [ ] CTA buttons are visible without hunting.

## Screenshot Checklist

Minimum screenshot set:

- landing page
- room list
- room detail
- viewing registration form
- viewing registration success page
- login page
- owner dashboard
- owner rooms
- owner invoices
- owner invoice detail or payment form
- owner repairs
- owner viewing registrations
- tenant dashboard
- tenant profile
- tenant invoices
- tenant payments
- tenant repairs
- tenant notifications
- reports dashboard as staff/admin
- custom 404 page if using `DEBUG=False`

Optional screenshot set:

- owner room form
- owner listing detail
- owner contract detail
- owner repair process form
- owner viewing process form
- tenant contract detail
- tenant invoice detail
- legacy route isolation

## Video Demo Checklist

Before recording:

- [ ] Seed demo data.
- [ ] Log in once as owner and tenant to confirm credentials.
- [ ] Close browser tabs that show secrets or filesystem paths.
- [ ] Do not show passwords while typing.
- [ ] Do not show `.env`, `SECRET_KEY`, database files, or backups.
- [ ] Use fake demo data only.

Suggested 3 to 5 minute recording:

1. Open `/` and introduce RentEase.
2. Browse `/rooms/`.
3. Open a room detail page.
4. Show viewing registration form.
5. Log in as owner.
6. Show owner dashboard, invoices/payment, repairs, and viewings.
7. Log in as tenant.
8. Show tenant dashboard, invoices/payments, repairs, and notifications.
9. Mention reports are staff-only.
10. Close with local-demo-ready but not production-ready limitations.

## Security/Privacy Visual Checklist

- [ ] No citizen ID values are visible.
- [ ] No citizen ID images/files are visible.
- [ ] No password/auth/permission internals are visible.
- [ ] No payment collector internals are visible.
- [ ] No private notes are visible on public or tenant pages.
- [ ] No raw Django template tags are visible.
- [ ] No broken static assets are visible.
- [ ] No HOSTELLO branding appears in main RentEase demo paths.

## Known Remaining UI Limitations

- Visual QA still needs manual browser inspection and screenshots.
- Reports are polished but still based on the admin template.
- Normal local `DEBUG=True` still shows Django technical 404 pages; custom 404 is for `DEBUG=False`.
- Legacy HOSTELLO pages remain visually legacy under `/legacy/`.

## Final Visual QA Recommendation

RentEase is ready for manual screenshot capture and demo video preparation.

Recommended next phase:

```text
Phase 18A: Screenshot Capture and Demo Video Preparation
```

