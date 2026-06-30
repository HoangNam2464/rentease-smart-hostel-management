# RentEase Product Context

## Product

RentEase is a Django boarding-house and rental-room management system evolved from the original HOSTELLO project. RentEase is the active product; HOSTELLO apps remain only for compatibility and historical continuity.

## Users

### Visitor

- Browse published rooms with public-safe Property name/ward/province context and room details.
- Submit viewing registrations without gaining private system access.

### Owner

- Manage owned properties/buildings and their rooms.
- Manage owned rooms and listings.
- Manage linked tenants, contracts, invoices, payments, repairs, and viewing registrations.
- See only data connected to the owner's profile.

### Tenant

- View the tenant's own profile, contracts, invoices, payments, repairs, and notifications.
- Submit tenant-safe repair requests.

### Admin and Staff

- Manage system-wide data through Django Admin.
- Access staff-only reports.
- Handle sensitive identity data only under the documented admin restrictions.

## Product Stage

RentEase is a polished local demo, not a production-ready service. The product direction is a practical Vietnamese rental-management system, not a generic school admin dashboard.

Completed foundations include role-based portals, public listings, owner workflows, tenant self-service, reports, demo data, UI polish, privacy hardening, and environment-driven production settings.

## Production Target

Production readiness requires:

- PostgreSQL and a validated data migration
- secure deployment and environment management
- protected production media storage
- backups and recovery
- verified email delivery and logging
- owner-facing billing details and utility/service entry
- account onboarding and lifecycle
- automated tests, CI, and coverage
- a deliberate long-term legacy strategy

## Product Boundaries

- RentEase routes and UI are the main product surface.
- Legacy routes remain limited to `/legacy/` and `/legacy/login/`.
- Public pages expose only listing-safe data.
- Owner data is owner-scoped; tenant data is tenant-scoped.
- Citizen identity data and authentication internals are never product UI content.
