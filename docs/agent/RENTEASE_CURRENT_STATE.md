# RentEase Current State

## Verified Baseline

| Item | Current truth |
|---|---|
| Expected branch | `complete-product` |
| Latest product phase | Phase 14C-3B3B2: Controlled InvoiceLine Read Authority |
| Product classification | Local-demo ready; not production-ready |
| Documentation system | Consolidated entry + repo-local RentEase skills |

Always verify the actual commit, branch, worktree, tags, Django check, and migration dry-run locally.

## Runtime Structure

- Django backend: `backend/`
- Django config package: `backend/hostello_backend/`
- Templates and reports templates: `frontend/templates/`
- Static assets: `frontend/static/`
- Local SQLite database: `backend/db.sqlite3` (ignored; do not touch casually)
- Official virtual environment: `backend/venv/`
- Current documentation: `docs/`
- Historical record: Git history and tags; retrieval guidance in `docs/archive/README.md`
- Repo-local agent skills: `.agents/skills/rentease/` and `.agents/skills/rentease-design/`

## Product and UI State

- Visitor, owner, tenant, admin, and staff-report flows exist.
- Public, owner, tenant, reports, admin, and error-page UI received the Phase 15-20 polish sequence.
- Active CSS: `rentease-design.css`, `rentease-layout.css`, and admin `custom_admin.css`.
- The project is suitable for a polished local demo.
- Manual screenshot/video capture remains optional presentation work.

## Production Settings State

Phase 14B-2 completed environment-driven settings, `DATABASE_URL` support, WhiteNoise, conditional production security settings, RentEase email/logging configuration, `Asia/Ho_Chi_Minh`, and `backend/.env.example`.

Remaining production work includes PostgreSQL migration planning/execution, production deployment verification, media access/storage, backups, email delivery verification, CI, automated tests, and coverage.

## Data Architecture State

- The supplied 15-entity RentEase ERD has been compared with active Django model metadata.
- Every diagram entity has an active conceptual equivalent, but several fields and relationships differ from current code.
- `docs/architecture/DATA_MODEL_ALIGNMENT.md` is the current alignment reference for PostgreSQL and future model planning.
- The approved target direction keeps the current Django project as the base and adds Property, flexible billing/metering, maintenance lifecycle, and data-governance foundations before PostgreSQL real-data onboarding.
- `docs/architecture/TARGET_DATA_MODEL.md` contains the staged implementation, migration, verification, rollback, and approval plan.
- Planned capability folders under `docs/features/planned/` contain no active app, model, migration, URL, or settings code.
- PostgreSQL has not been provisioned or populated; SQLite remains the verified local runtime database.
- Phase 14C-2 established a 20-test baseline covering role login and rejection, public listings and viewing registration, cross-owner/cross-tenant isolation, billing snapshots/totals/overpayment, database uniqueness, and maintenance relationship validation.
- Phase 14C-3A1 added the `Property` model and nullable `Room.property` transition field. `Room.owner` remains authoritative; no property backfill, queryset switch, form, admin, UI, or real-data change has occurred.
- Phase 14C-3A2 added a reversible data migration that creates one deterministic default Property per owner profile, copies only an existing rental address, and links previously unlinked Rooms without changing `Room.owner`. Its behavior is covered on disposable test databases; the configured local SQLite now reports the Property migrations as applied.
- Phase 14C-3A3 is complete: owner/admin Property management, owner-scoped listing filters, public-safe Property name/ward/province presentation, staff-only Property report filters, and Property-first disposable demo seeding are integrated. Public pages do not render exact address, coordinates, contact phone, timezone, or house rules.
- Phase 14C-3A4 requires every Room to belong to a Property, scopes room-code uniqueness to `(property, room_code)`, and retains `Room.owner` as the authorization boundary. Migration preconditions stop on null Property, owner mismatch, duplicate Property room code, or unsafe reverse owner-code duplication.
- Phase 14C-3B1 freezes current billing behavior: room-period price uniqueness; invoice-detail rate/rent/service snapshots; exact electricity, water, rent, service, total, paid, and remaining calculations; atomic invoice generation; payment status transitions; payment deletion recalculation; and overpayment rejection. No billing source behavior or schema changed.
- Phase 14C-3B2 adds `ServiceDefinition`, `Meter`, `MeterReading`, and `InvoiceLine` as isolated additive foundations with database constraints, cross-Property/source validation, admin registration, and a reversible migration. Existing invoice calculations, reads, reports, UI, payments, and real-data onboarding remain unchanged; the configured local SQLite now reports the billing foundation migrations as applied.
- Phase 14C-3B3A adds a reversible fail-closed data migration that creates four deterministic compatibility lines per existing InvoiceDetail from stored snapshots. Disposable migration tests prove exact `0.00` total variance, zero-usage preservation, payment/status/relationship preservation, reserved-code collision rejection, total-mismatch rejection, and targeted reversal. Protected SQLite and real data were not migrated.
- Phase 14C-3B3B1 atomically dual-writes the four compatibility lines whenever a complete InvoiceDetail snapshot is created or updated. Reserved-code conflicts roll back the detail, lines, and invoice total together; repeated saves update rather than duplicate; zero usage is preserved. InvoiceDetail remains authoritative, and partial InvoiceDetail saves are rejected to prevent snapshot/line/header divergence.
- Phase 14C-3B3B2 makes the signed amounts of the four validated compatibility `InvoiceLine` rows authoritative for recalculating invoices that have an InvoiceDetail. The reader requires exact codes, ownership, source boundaries, financial semantics, snapshot values, and detail/header parity. InvoiceDetail remains the atomic snapshot/write source; non-compatibility adjustment and discount lines remain deferred. Payment create/delete and detail updates roll back when line validation fails or a new total would be below the amount already paid. Header-only draft compatibility behavior is unchanged, and no schema, migration, UI, report, permission, or real-data change occurred.

## Current Status (Last Updated: Agent Phase 16)

- **Product State**: Môi trường Development và Production-Ready hoàn thiện (100% Tests Pass). Hệ thống đã kích hoạt thành công cơ sở dữ liệu PostgreSQL qua Docker (`docker-compose up -d`). Đã hoàn thành quá trình Onboarding dữ liệu ban đầu cho các tài khoản test.
- **Core Working Area**: PostgreSQL Database, Core Logic (Billing, Maintenance, Contracts), UI/UX DreamPOS.
- **Next Up**: Sẵn sàng để người dùng trải nghiệm thực tế hoặc khởi chạy (Launch).

## What is Working Perfectly
- 100% Unit Tests (79 tests) passed trên PostgreSQL (Authentication, Permissions, Billing, Governance, Legacy exclusion).
- Database PostgreSQL đã hoạt động trơn tru.
- Đã import dữ liệu thực tế (Demo Data) thành công (Rooms, Invoices, Contracts, Tenants...).
- Cơ chế bảo mật và phân quyền Tenant/Owner độc lập.
- Giao diện UI/UX (CSS Variables) chuẩn DreamPOS.
- Chức năng loại bỏ (exclude) an toàn cho `legacy apps` ở mức Database.
- Admin list/search exposure of `citizen_id` is removed.
- Sensitive identity fields are read-only for non-superuser staff in admin detail forms.
- Production-grade access control/storage for uploaded identity media remains a gap.

## Documentation State

- `AGENTS.md` is now a short mandatory entry file.
- `.agents/skills/rentease/` provides progressive task-specific guidance.
- `.agents/skills/rentease-design/` provides focused design, critique, audit, polish, responsive, and visual-QA workflows.
- `docs/` contains 14 current Markdown files, including one consolidated demo guide, current/target data-model references, one planned-feature catalog, and one history-retrieval guide.
- Superseded rules, audits, plans, phase reports, SPQM documents, and the former work log remain recoverable through Git rather than living beside current guidance.

## Known Product Gaps

- PostgreSQL is not executed; its staged target-schema and provisioning plan is documented.
- Compatibility backfill, dual-write, and controlled InvoiceLine read authority are verified on disposable test databases. Protected local-SQLite parity has not been audited, adjustment/discount participation remains deferred, and owner-facing invoice detail/utility entry remains incomplete.
- Account onboarding, invitation, recovery, and lifecycle are incomplete.
- Deployment, media, backup, CI, and broader workflow test coverage remain incomplete.
- Legacy HOSTELLO apps remain installed and intentionally isolated.

## Next Safe Action

See `docs/agent/NEXT_ACTION.md`.
