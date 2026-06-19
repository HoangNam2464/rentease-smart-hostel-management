# RentEase Demo Script

## Target Length

3 to 5 minutes.

## Demo Goal

Show RentEase as a role-based Django boarding-house management system with public room browsing, owner management workflows, tenant self-service pages, and protected admin/reporting areas.

## Before Recording Or Presenting

Use fake local-only data.

Recommended preparation:

- create at least one owner with rooms
- create at least one published room listing
- create at least one tenant linked to a contract
- create at least one invoice and payment
- create at least one repair request
- create at least one viewing registration

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

Open one published room detail page.

Example from current local data:

```text
/rooms/12/
```

Talk track:

The public detail page shows listing information and public-safe room details only.

### 4. Viewing Registration

Open:

```text
/rooms/12/register/
```

Talk track:

A visitor can submit a room viewing registration without automatically creating a user account, tenant record, or contract.

If demo data is not ready, show the form without submitting.

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

If current local test data is empty, explain that Phase 15D will prepare safe demo data for richer detail-page walkthroughs.

### 8. Owner Billing And Payment

Open an owner invoice detail page if sample data exists.

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

## Current Demo Data Limitation

At the Phase 15C checkpoint:

- `owner_test` has no scoped owner sample records.
- `tenant_test` has no scoped tenant sample records.
- published public listings exist, including listing id `12`.

Recommended next phase:

```text
Phase 15D: Demo Data Readiness Plan
```

