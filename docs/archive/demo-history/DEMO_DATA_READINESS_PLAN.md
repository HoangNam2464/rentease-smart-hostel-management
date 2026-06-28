# RentEase Demo Data Readiness Plan

## Phase

Phase 15D: Demo Data Readiness Plan

## Status

Planning complete in Phase 15D.

Implementation completed in Phase 15E with:

```text
seed_rentease_demo_data
```

See:

```text
docs/demo/DEMO_DATA_SEED_USAGE.md
```

## Current Demo Data Problem

The polished RentEase UI can be opened and smoke tested, but the default local demo accounts do not currently have scoped records for realistic owner and tenant walkthroughs.

Existing local account snapshot:

| Account | Exists | Role | Linked Profile | Scoped Demo Records |
| --- | --- | --- | --- | --- |
| `admin_test` | Yes | ADMIN | Staff/superuser | Not applicable |
| `owner_test` | Yes | OWNER | `Local Test Owner` | 0 rooms, listings, tenants, contracts, invoices, payments, repairs, viewings |
| `tenant_test` | Yes | TENANT | `Local Test Tenant` | 0 contracts, invoices, payments, repairs, notifications, viewings |

Global database snapshot:

| Data | Count |
| --- | --- |
| Users | 36 |
| Owner profiles | 17 |
| Rooms | 13 |
| Published listings | 6 |
| Tenants | 12 |
| Contracts | 13 |
| Invoices | 16 |
| Payments | 8 |
| Repairs | 4 |
| Notifications | 0 |
| Viewing registrations | 4 |

Conclusion:

- the database has general sample data
- the current local demo accounts are not connected to that data
- public room browsing can be demonstrated because published listings exist
- owner and tenant detail-page demos need scoped fake local data

## Safe Fake Data Principles

- Use fake local-only people, addresses, phone numbers, and emails.
- Do not use real citizen ID values.
- Do not attach citizen ID images or files.
- Do not attach repair images.
- Use predictable demo prefixes such as `DEMO-`.
- Keep demo records scoped to `owner_test` and `tenant_test`.
- Avoid overwriting non-demo data.
- Avoid deleting non-demo data.
- Avoid committing database files.
- Avoid migrations and schema changes.
- Make demo data reproducible and resettable.

## Model Relationship Map

Recommended data chain:

```text
accounts.User(owner_test)
  -> accounts.UserProfile
      -> properties.Room
          -> listings.RoomListing
              -> listings.ViewingRegistration
          -> contracts.Contract
              -> tenants.Tenant(account=tenant_test)
              -> billing.Invoice
                  -> billing.InvoiceDetail
                  -> billing.PaymentHistory
              -> maintenance.RepairRequest
                  -> maintenance.Notification
          -> billing.PriceConfig
```

Important dependencies:

- `Room.owner` points to `UserProfile`.
- `Room.room_code` must be unique per owner.
- `Tenant.account` can link to `tenant_test`.
- `Tenant.citizen_id` is required and unique, but must be fake.
- `Contract.room` and `Contract.tenant` connect owner and tenant.
- Active contract rooms allow tenant repair submission.
- `PriceConfig` is needed before `InvoiceDetail`.
- `Invoice` is unique per contract, month, and year.
- `InvoiceDetail` is one-to-one with `Invoice`.
- `PaymentHistory` must not overpay the invoice.
- `ViewingRegistration` must target a published listing.
- `Notification` can target the tenant and optionally invoice or repair request.

## Required Demo Objects

### Public Demo

Minimum:

- 3 published room listings
- complete room detail data
- 1 pending viewing registration
- 1 confirmed viewing registration

Recommended room/listing names:

- `DEMO-A101` - Sunny Studio Near Campus
- `DEMO-A102` - Quiet Private Room
- `DEMO-A201` - Shared Room With Balcony

### Owner Demo

Minimum:

- 3 rooms owned by `owner_test`
- 3 listings for those rooms
- 2 tenants linked through contracts
- 2 active contracts
- 1 contract ending soon
- 2 invoices
- 1 partially paid invoice
- 1 fully paid invoice
- 2 payment history rows
- 2 repair requests
- 2 viewing registrations

Dashboard should show:

- room totals
- active contracts
- invoice totals
- paid and remaining amount
- pending repairs
- pending viewing registrations

### Tenant Demo

Minimum for `tenant_test`:

- tenant profile linked through `Tenant.account`
- active contract
- current room
- invoice list
- payment history
- one pending or in-progress repair request
- one completed repair request if possible
- one invoice notification
- one repair notification

Tenant pages should show:

- current contract
- unpaid or partial invoice count
- open repair request count
- unread notification count

## Exact Proposed Demo Scenario

### Demo Accounts

| Role | Username | Purpose |
| --- | --- | --- |
| Admin | `admin_test` | Admin/Jazzmin and reports access |
| Owner | `owner_test` | Owner portal walkthrough |
| Tenant | `tenant_test` | Tenant portal walkthrough |

### Demo Owner

Use existing `owner_test.rentease_profile`.

If missing in a future database, create:

```text
full_name: Demo Owner
phone_number: 0900000001
rental_address: 123 Demo Street, District Demo
```

### Demo Tenant

Use or update existing tenant profile linked to `tenant_test`.

Fake values:

```text
full_name: Demo Tenant
email: tenant.demo@example.test
phone_number: 0900000002
citizen_id: DEMO-TENANT-001
address: Demo Tenant Address
status: active
```

Do not attach `citizen_id_front` or `citizen_id_back`.

### Demo Rooms

| Code | Name | Status | Rent |
| --- | --- | --- | --- |
| `DEMO-A101` | Sunny Studio Near Campus | occupied | 3500000 |
| `DEMO-A102` | Quiet Private Room | available | 2800000 |
| `DEMO-A201` | Shared Room With Balcony | available | 2200000 |

### Demo Listings

| Room | Status | Price | Deposit |
| --- | --- | --- | --- |
| `DEMO-A101` | hidden or rented | 3500000 | 3500000 |
| `DEMO-A102` | published | 2800000 | 2800000 |
| `DEMO-A201` | published | 2200000 | 2200000 |

To keep public browsing rich, create at least 3 published listings only if each listing uses a different room.

### Demo Contracts

| Code | Room | Tenant | Status | Purpose |
| --- | --- | --- | --- | --- |
| `DEMO-CTR-001` | `DEMO-A101` | `Demo Tenant` | active | tenant portal active contract |
| `DEMO-CTR-002` | `DEMO-A102` | second fake tenant | active | owner dashboard variety |

### Demo Billing

For `DEMO-CTR-001`:

- create `PriceConfig` for current or fixed demo month
- create `Invoice`
- create `InvoiceDetail`
- create one partial `PaymentHistory`

For `DEMO-CTR-002`:

- create `Invoice`
- create `InvoiceDetail`
- create full payment

Use rounded values to keep presentation easy:

```text
electricity_unit_price: 3500
water_unit_price: 15000
service_fee: 150000
```

### Demo Repairs

Create for `Demo Tenant` and `DEMO-A101`:

- `DEMO Repair - Leaking faucet`, status `pending`
- `DEMO Repair - Light replacement`, status `completed`

Do not attach image files.

### Demo Notifications

Create for `Demo Tenant`:

- invoice notification linked to demo invoice
- repair notification linked to demo repair request

### Demo Viewing Registrations

Create for public visitors:

- `Demo Visitor One`, status `pending`
- `Demo Visitor Two`, status `confirmed`

Use future dates only.

## Recommended Data Creation Method

Recommended:

```text
local-only Django management command
```

Why this is safest:

- can use ORM validation and existing model methods
- can be idempotent with `update_or_create`
- can create relationships in the right order
- can avoid committing database files
- can include a dry-run mode
- can include a reset mode that deletes only records with safe demo prefixes
- can avoid touching production settings or schema

Recommended command name:

```text
seed_demo_data
```

Recommended options:

```text
--dry-run
--reset
--confirm-reset
```

Alternative: fixture JSON.

Pros:

- simple to load
- transparent data

Cons:

- fragile primary keys
- harder to keep idempotent
- harder to avoid collisions
- easier to accidentally commit data that looks real

Alternative: manual admin setup.

Pros:

- no code needed
- safest for one-time classroom demo

Cons:

- slow
- inconsistent
- easy to miss relationships
- hard to reset

Final recommendation:

Use a local-only management command in Phase 15E, but implement it only after approval.

## Migration Risk

No migrations are needed.

Phase 15E should only create a management command and maybe documentation updates.

If implementing demo data requires a model or schema change, stop and request approval before proceeding.

## Rollback / Reset Plan

Preferred reset method:

- delete only records created by the seed command
- identify records by safe prefixes:
  - `DEMO-`
  - `demo.`
  - `@example.test`
- delete in dependency order:
  1. Notifications
  2. Payment histories
  3. Invoice details
  4. Invoices
  5. Repair requests
  6. Viewing registrations
  7. Room listings
  8. Contracts
  9. Price configs
  10. Rooms
  11. Demo-only tenants not linked to `tenant_test`
  12. Optional demo-only users, if created by command

Do not delete:

- `admin_test`
- `owner_test`
- `tenant_test`
- non-demo records
- records without the approved demo prefix

## Risks

| Risk | Mitigation |
| --- | --- |
| Accidentally overwriting real data | Use `update_or_create` only on `DEMO-` keys |
| Accidentally deleting real data | Reset only records with demo prefixes |
| Fake citizen ID appears in admin | Use obviously fake values and do not use screenshots that show citizen ID |
| Invoice validation fails | Create PriceConfig before InvoiceDetail |
| Payment overpayment fails validation | Calculate totals first and keep payments below or equal total |
| Active contract conflict | Use one active contract per room |
| Published listing conflict | Use one published listing per room |
| Viewing registration date validation fails | Use today or future dates |
| Demo command run in production | Require explicit `--allow-local-demo-data` or `DEBUG=True` guard |

## Verification Checklist For Phase 15E

Before implementation:

- [ ] branch is `complete-product`
- [ ] working tree is clean
- [ ] Django check passes
- [ ] migration dry-run reports `No changes detected`

After implementation:

- [ ] no migrations created
- [ ] no schema changes
- [ ] management command supports dry-run
- [ ] command creates or updates only demo-prefixed records
- [ ] owner dashboard metrics are populated for `owner_test`
- [ ] owner rooms/listings/contracts/invoices/repairs/viewings show data
- [ ] tenant dashboard metrics are populated for `tenant_test`
- [ ] tenant contracts/invoices/payments/repairs/notifications show data
- [ ] public room list shows at least 3 published demo listings
- [ ] viewing registration pages work
- [ ] reset mode removes only demo data
- [ ] Django check passes
- [ ] migration dry-run reports `No changes detected`
- [ ] database file is not committed

## Phase 15E Result

The safe demo data seed implementation is complete.

Verified seed result:

- 5 owner-scoped demo rooms
- 3 published demo listings
- 2 demo contracts
- 2 demo invoices
- 2 demo payments
- 2 demo repair requests
- 3 demo viewing registrations
- 1 tenant-scoped active contract
- 1 tenant-scoped invoice
- 1 tenant-scoped payment
- 2 tenant-scoped repair requests
- 2 tenant notifications

No migrations were created.

## Final Recommendation

Proceed next with:

```text
Phase 15F: Final Demo Walkthrough Verification
```

Goal:

Use seeded demo data to verify the full 3-5 minute demo flow and prepare the final demo package.
