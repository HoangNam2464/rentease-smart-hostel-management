# RentEase Production Roadmap

RentEase is local-demo ready and not production-ready. `NEXT_ACTION.md` controls the immediate task.

## Completed Foundation

- Public, owner, tenant, reports, and admin workflows
- Local demo data and walkthrough verification
- UI/design-system and responsive polish
- Legacy root route isolation
- Admin citizen-identity privacy hardening
- Phase 14B-2 environment-driven production settings

## Ordered Production Work

### Phase 14C - PostgreSQL Migration

Plan first, then implement only after approval.

- backup and rollback strategy
- target environment and credentials
- fresh schema creation from reviewed Django migrations
- real-data onboarding/import without demo or regression records
- relationship and row-count validation
- local SQLite fallback for development

### Phase 14D - Owner Billing Detail and Utility Entry

- invoice detail lines
- electricity/water readings
- rent, deposit, service, and fee breakdowns
- clear tenant invoice presentation
- calculated-total and overpayment integrity

Schema changes may be required and need separate approval.

### Phase 14E - Account Lifecycle

- owner/tenant onboarding
- tenant account creation or invitation
- password reset and recovery
- profile update and verification rules

### Phase 14F - Deployment Readiness

- production host and process model
- `DEBUG=False` verification
- static and protected media hosting
- email delivery and logging
- backups, restore procedure, HTTPS, and error handling
- deployment documentation

### Phase 14G - Automated Quality Gates

- Django tests for permissions and critical workflows
- CI for checks, migration drift, and tests
- coverage reporting

## Optional Later Work

- planned capability areas cataloged in `docs/features/README.md`
- legacy HOSTELLO retirement after a dedicated dependency/data/contenttypes plan
- report exports
- online payment integration
- advanced analytics

Do not renumber phases casually. If priorities change, update this roadmap and `NEXT_ACTION.md` together.
