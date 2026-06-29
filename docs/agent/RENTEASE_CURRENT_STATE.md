# RentEase Current State

## Verified Baseline

| Item | Current truth |
|---|---|
| Expected branch | `complete-product` |
| Latest product phase | Phase 14B-2: Production Settings Split |
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

## Privacy and Security State

- Owner and tenant portal data must remain scoped to the authenticated profile.
- Citizen identity fields/files are forbidden on public, owner, and tenant surfaces.
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
- Owner-facing invoice detail/utility entry is incomplete.
- Account onboarding, invitation, recovery, and lifecycle are incomplete.
- Deployment, media, backup, CI, and automated test coverage remain incomplete.
- Legacy HOSTELLO apps remain installed and intentionally isolated.

## Next Safe Action

See `docs/agent/NEXT_ACTION.md`.
