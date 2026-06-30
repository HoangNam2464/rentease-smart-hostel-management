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

### Phase 14C - Target Schema and PostgreSQL

Follow `docs/architecture/TARGET_DATA_MODEL.md`. Each implementation stage needs separate approval.

- `14C-1` target architecture planning and ERD decision
- `14C-2` schema safety baseline and legacy production-table audit
- `14C-3A1` additive Property schema and nullable room relationship (complete)
- `14C-3A2` reversible default-Property backfill (complete)
- `14C-3A3` staged Property integration: owner/admin complete; listings/reports/seed data next
- `14C-3A4` required room relationship and Property-scoped room-code constraint
- `14C-3B` invoice-line, service, meter, and reading schema/domain foundation; UI workflow remains Phase 14D
- `14C-3C1` maintenance lifecycle correction
- `14C-3C2` protected-document and audit foundation
- `14C-3D` production legacy-app exclusion and clean-schema verification
- `14C-4` fresh PostgreSQL provisioning from reviewed migrations
- `14C-5` owner-approved real-data onboarding without demo or regression records
- backup, rollback, relationship, financial-total, privacy, and row-count validation throughout
- explicit local SQLite fallback for development

### Phase 14D - Owner Billing Workflow Completion

- invoice detail lines
- electricity/water readings
- rent, deposit, service, and fee breakdowns
- clear tenant invoice presentation
- calculated-total and overpayment integrity

This phase builds the owner/tenant workflows on the approved 14C billing foundation. Any remaining schema change needs separate approval.

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
