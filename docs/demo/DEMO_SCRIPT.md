# RentEase Demo Script

## Target Length

3 to 5 minutes.

## Demo Goal

Show RentEase as a role-based Django boarding-house management system with public room browsing, owner management workflows, tenant self-service pages, and protected admin/reporting areas.

## Before Recording Or Presenting

Use fake local-only data.

Recommended preparation:

- run the safe local demo seed command from `docs/demo/DEMO_DATA_SEED_USAGE.md`
- verify `owner_test`, `tenant_test`, and `admin_test` can log in
- confirm `/rooms/` shows published demo listings
- confirm owner and tenant dashboards show demo records

Do not show:

- real passwords
- real citizen ID data
- citizen ID images/files
- secrets or `.env` values
- private backup/database files

## Script

### 1. Landing Page

Open:

```text
/
```

Talk track:

RentEase is a Django-based boarding-house management system. The landing page gives visitors a clean entry point to browse rooms or log in.

### 2. Public Room Browsing

Open:

```text
/rooms/
```

Talk track:

Visitors can browse published room listings without seeing private tenant, contract, invoice, or owner-internal data.

### 3. Public Room Detail

Open one published room detail page from `/rooms/`.

Example from the Phase 15F local verification:

```text
/rooms/17/
```

Talk track:

The public detail page shows listing information and public-safe room details only.

### 4. Viewing Registration

Open:

```text
/rooms/<published_id>/register/
```

Talk track:

A visitor can submit a room viewing registration without automatically creating a user account, tenant record, or contract.

For a fast presentation, show the form without submitting. If a submission is needed, use fake visitor data only.

### 5. Owner Login

Open:

```text
/login/
```

Log in as an owner test account if configured.

Talk track:

After login, RentEase redirects users by role. Owners see owner-focused management pages.

### 6. Owner Dashboard

Open:

```text
/owner/dashboard/
```

Talk track:

The owner dashboard summarizes rooms, contracts, invoices, payments, repairs, listings, and viewing registrations for the current owner only.

### 7. Owner Management Pages

Open:

```text
/owner/rooms/
/owner/listings/
/owner/tenants/
/owner/contracts/
/owner/invoices/
/owner/repairs/
/owner/viewing-registrations/
```

Talk track:

Owners can manage their own rooms, listings, linked tenants, contracts, invoice headers, payments, repairs, and viewing registrations. Each page is owner-scoped.

Seeded demo data is available after Phase 15E and was verified in Phase 15F. Use the owner pages to open demo rooms, contracts, invoices, repairs, and viewing registrations.

### 8. Owner Billing And Payment

Open a demo owner invoice detail page.

Talk track:

Payment recording is reached from invoice detail. Billing calculations and payment status are handled by existing billing logic.

### 9. Tenant Login

Log out and log in as a tenant test account if configured.

Open:

```text
/tenant/dashboard/
```

Talk track:

Tenants see only their own profile, contracts, invoices, payments, repair requests, and notifications.

### 10. Tenant Self-Service Pages

Open:

```text
/tenant/profile/
/tenant/contracts/
/tenant/invoices/
/tenant/payments/
/tenant/repairs/
/tenant/notifications/
```

Talk track:

Tenant pages are read-only where appropriate, and repair submission is limited to tenant-safe fields.

### 11. Security And Privacy Scope

Talk track:

RentEase keeps public, owner, tenant, admin, and legacy surfaces separated. Owner pages are owner-scoped, tenant pages are tenant-scoped, reports are staff-only, and legacy root API and fees routes are not exposed.

### 12. Admin And Reports

Optionally show:

```text
/admin/
/reports/
```

Talk track:

Admin and reports remain protected. Reports are intended for staff/admin use, not public access.

### 13. Remaining Limitations

Talk track:

The current project is strong for local demo and controlled testing, but it is not production-ready yet. Remaining production work includes production settings, production database configuration, deployment setup, account lifecycle, and owner billing detail/utility entry.

## Current Demo Data Status

After Phase 15F:

- `owner_test` has scoped demo rooms, listings, contracts, invoices, payments, repairs, and viewing registrations.
- `tenant_test` has scoped demo contract, invoice, payment, repairs, and notifications.
- public demo listings are available.
- the final walkthrough route smoke test passed with seeded demo data.

Recommended next phase:

```text
Phase 16A: README and Final Demo Package Polish
```
