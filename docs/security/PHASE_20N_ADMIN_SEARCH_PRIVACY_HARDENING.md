# Phase 20N: Admin Search Privacy Hardening

## Status

Completed.

## Goal

Audit Django Admin search/list/detail exposure for sensitive tenant identity data and harden safe admin privacy surfaces without changing database schema, models, migrations, business logic, routes, Jazzmin structure, report calculations, or owner/tenant portal behavior.

## Admin Files Reviewed

Reviewed RentEase/admin files:

- `backend/accounts/admin.py`
- `backend/properties/admin.py`
- `backend/tenants/admin.py`
- `backend/contracts/admin.py`
- `backend/billing/admin.py`
- `backend/maintenance/admin.py`
- `backend/listings/admin.py`

Legacy admin files were also scanned for context but not changed:

- `backend/students/admin.py`
- `backend/attendance/admin.py`
- `backend/fees/admin.py`
- `backend/notices/admin.py`
- `backend/requests/admin.py`

## ModelAdmin Classes Reviewed

- `CustomUserAdmin`
- `UserProfileAdmin`
- `WardenProfileAdmin`
- `RoomAdmin`
- `TenantAdmin`
- `CoTenantAdmin`
- `ContractAdmin`
- `PriceConfigAdmin`
- `InvoiceAdmin`
- `PaymentHistoryAdmin`
- `RepairRequestAdmin`
- `MaintenanceRecordAdmin`
- `NotificationAdmin`
- `RoomListingAdmin`
- `ViewingRegistrationAdmin`

## Sensitive Fields Audited

Sensitive identity markers checked:

- `citizen_id`
- `citizen_id_front`
- `citizen_id_back`
- `Citizen id`
- `CCCD`
- `CMND`
- identity card / ID-card markers

## Sensitive Fields Found

Expected and retained:

- `TenantAdmin` keeps `citizen_id`, `citizen_id_front`, and `citizen_id_back` only inside the collapsed `Sensitive identity data` detail fieldset.
- `CoTenantAdmin` keeps `citizen_id` only inside the collapsed `Sensitive identity data` detail fieldset.

Hardened in this phase:

- `ContractAdmin.search_fields` previously included `tenant__citizen_id`.
- `InvoiceAdmin.search_fields` previously included `contract__tenant__citizen_id`.
- `CoTenantInline` inside `ContractAdmin` previously relied on default inline fields, which could make `citizen_id` visible on the contract detail page.

## Changes Applied

### ContractAdmin

Changed search fields from sensitive identity lookup to safe tenant contact lookup:

- removed `tenant__citizen_id`
- added `tenant__phone_number`
- added `tenant__email`

Restricted `CoTenantInline` fields to non-sensitive values only:

- `full_name`
- `phone_number`
- `relationship`

### InvoiceAdmin

Changed search fields from sensitive identity lookup to safe tenant contact lookup:

- removed `contract__tenant__citizen_id`
- added `contract__tenant__phone_number`
- added `contract__tenant__email`

## Risky Items Deferred

No risky change was required for this phase.

Deferred for future production hardening if needed:

- role-specific admin field visibility for sensitive identity detail fields
- making sensitive identity fields read-only for non-superuser staff
- replacing legacy admin surfaces entirely
- large Jazzmin/admin redesign

## Verification

### Django

- `.\venv\Scripts\python.exe manage.py check` passed.
- `.\venv\Scripts\python.exe manage.py makemigrations --check --dry-run` reported `No changes detected`.

### Admin Search Introspection

Verified current search fields:

- `ContractAdmin.search_fields` no longer includes `tenant__citizen_id`.
- `InvoiceAdmin.search_fields` no longer includes `contract__tenant__citizen_id`.
- `TenantAdmin.search_fields` remains safe.
- `CoTenantAdmin.search_fields` remains safe.
- `CoTenantInline.fields` exposes only safe non-identity fields.

### Route Checks

Verified active admin routes:

- `/admin/`
- `/admin/tenants/tenant/`
- `/admin/tenants/cotenant/`
- `/admin/properties/room/`
- `/admin/contracts/contract/`
- `/admin/billing/invoice/`
- `/admin/billing/paymenthistory/`
- `/admin/contracts/contract/<demo_id>/change/`

Verified product/report routes:

- `/reports/`
- `/owner/dashboard/`
- `/tenant/dashboard/`

## Route Alias Note

The prompt listed these generic admin routes:

- `/admin/rooms/room/`
- `/admin/invoices/invoice/`
- `/admin/payments/paymenthistory/`

The current Django app labels are:

- `properties` for `Room`
- `billing` for `Invoice`
- `billing` for `PaymentHistory`

Therefore the active canonical routes are:

- `/admin/properties/room/`
- `/admin/billing/invoice/`
- `/admin/billing/paymenthistory/`

No alias routes were added because adding admin URL aliases would be an unrelated route behavior change.

## Privacy Verification Result

The checked admin changelist pages did not render:

- `citizen_id`
- `Citizen id`
- `CCCD`
- `CMND`
- ID-card markers

The checked contract admin detail page did not render sensitive identity markers after limiting `CoTenantInline` fields.

## Browser Automation Note

Browser screenshot capture was not used in this phase because browser automation had previously become unstable after screenshot timeouts. Verification used Django Client route/render/privacy checks and direct Django Admin registry introspection.

## Recommended Next Phase

```text
Phase 20O: Admin Sensitive Detail Permission Planning
```

Goal: plan whether sensitive identity fields in Tenant/CoTenant admin detail forms should remain editable for all staff, become read-only, or become superuser-only in a future production-hardening phase.
