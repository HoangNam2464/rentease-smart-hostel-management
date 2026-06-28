# RentEase Current State

## Verified Baseline

| Item | Current truth |
|---|---|
| Expected branch | `complete-product` |
| Latest product phase | Phase 14B-2: Production Settings Split |
| Product classification | Local-demo ready; not production-ready |
| Documentation system | Consolidated entry + repo-local RentEase skill |

Always verify the actual commit, branch, worktree, tags, Django check, and migration dry-run locally.

## Runtime Structure

- Django backend: `backend/`
- Django config package: `backend/hostello_backend/`
- Templates and reports templates: `frontend/templates/`
- Static assets: `frontend/static/`
- Local SQLite database: `backend/db.sqlite3` (ignored; do not touch casually)
- Official virtual environment: `backend/venv/`
- Current documentation: `docs/`
- Historical documentation: `docs/archive/`
- Repo-local agent skill: `.agents/skills/rentease/`

## Product and UI State

- Visitor, owner, tenant, admin, and staff-report flows exist.
- Public, owner, tenant, reports, admin, and error-page UI received the Phase 15-20 polish sequence.
- Active CSS: `rentease-design.css`, `rentease-layout.css`, and admin `custom_admin.css`.
- The project is suitable for a polished local demo.
- Manual screenshot/video capture remains optional presentation work.

## Production Settings State

Phase 14B-2 completed environment-driven settings, `DATABASE_URL` support, WhiteNoise, conditional production security settings, RentEase email/logging configuration, `Asia/Ho_Chi_Minh`, and `backend/.env.example`.

Remaining production work includes PostgreSQL migration planning/execution, production deployment verification, media access/storage, backups, email delivery verification, CI, automated tests, and coverage.

## Privacy and Security State

- Owner and tenant portal data must remain scoped to the authenticated profile.
- Citizen identity fields/files are forbidden on public, owner, and tenant surfaces.
- Admin list/search exposure of `citizen_id` is removed.
- Sensitive identity fields are read-only for non-superuser staff in admin detail forms.
- Production-grade access control/storage for uploaded identity media remains a gap.

## Documentation State

- `AGENTS.md` is now a short mandatory entry file.
- `.agents/skills/rentease/` provides progressive task-specific guidance.
- `docs/README.md` defines current sources of truth and archive policy.
- Superseded rules, audits, plans, SPQM status documents, and completed reports are under `docs/archive/`.
- Archive documents are historical evidence, not current instructions.

## Known Product Gaps

- PostgreSQL migration is not planned or executed.
- Owner-facing invoice detail/utility entry is incomplete.
- Account onboarding, invitation, recovery, and lifecycle are incomplete.
- Deployment, media, backup, CI, and automated test coverage remain incomplete.
- Legacy HOSTELLO apps remain installed and intentionally isolated.

## Next Safe Action

See `docs/agent/NEXT_ACTION.md`.
