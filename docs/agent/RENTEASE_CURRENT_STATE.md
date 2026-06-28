# RentEase Current State

## Verified Baseline

| Item | Current truth |
|---|---|
| Branch | `complete-product` |
| HEAD at Session A start | `93b56a4 Production settings split with env-driven config (Phase 14B-2)` |
| Latest completed phase | Phase 14B-2: Production Settings Split |
| Latest available phase tag | `phase20o-admin-sensitive-detail-permissions` |
| Product classification | Local-demo ready; not production-ready |

Always verify branch, status, log, tags, Django check, and migration dry-run locally before work.

## Actual Structure

RentEase uses the restructured layout:

- Django backend and `manage.py`: `backend/`
- Django config package: `backend/hostello_backend/`
- Settings module: `hostello_backend.settings`
- Templates: `frontend/templates/`
- Static files: `frontend/static/`
- Documentation: `docs/`
- Official local venv: `backend/venv/`
- Environment template: `backend/.env.example`

The inner package name `hostello_backend` must not be renamed casually. Legacy apps remain installed and isolated; they are not approved for removal.

## Current UI State

- Public room flow, owner portal, tenant portal, reports, admin styling, error pages, and responsive layouts have received the Phase 15-20 polish sequence.
- Active shared CSS is `rentease-design.css` plus `rentease-layout.css`; admin overrides use `custom_admin.css`.
- The UI is suitable for a polished local demo.
- Manual screenshots/video remain incomplete, and several old demo/UI guides contain stale phase links or status text.
- No formal automated browser or Django test suite is established; prior confidence comes from Django Client checks and manual/phase verification.

## Production Settings State

Phase 14B-2 is complete:

- settings are environment-driven through `python-decouple`
- `ALLOWED_HOSTS` is environment-driven
- `DATABASE_URL` is supported through `dj-database-url`, with SQLite fallback for local use
- WhiteNoise and environment-aware static storage are configured
- production security settings are enabled conditionally when `DEBUG=False`
- timezone is `Asia/Ho_Chi_Minh`
- email identity and logging use RentEase-oriented configuration
- `backend/.env.example` exists

This does not make the application production-ready. PostgreSQL data migration, production deployment verification, media access/storage, backups, CI/tests, and operational deployment documentation remain incomplete.

## Privacy and Security State

- Public, owner, and tenant surfaces must never expose citizen identity fields/files or unrelated users' data.
- Owner and tenant querysets must remain scoped to the authenticated owner/tenant.
- Tenant and co-tenant admin lists/search do not include `citizen_id`.
- Contract and invoice admin search use safe contact fields rather than identity lookups.
- Sensitive tenant identity fields remain in collapsed admin detail sections.
- Phase 20O makes those fields read-only for non-superuser staff; superusers retain edit access.
- Production-grade media access control for identity uploads remains a known gap.

## Documentation Cleanup State

Session A inventoried 83 pre-existing Markdown files and created `DOCS_CONSOLIDATION_AUDIT.md` as the 84th. It found:

- stale phase/status data in roadmap, SPQM, demo, UI, and technical-analysis docs
- conflicting automatic push/tag instructions
- duplicate demo and audit documents
- historical files still outside `docs/archive/`
- plaintext demo credentials in two demo-package documents

No files were moved or deleted. `PROJECT_STRUCTURE_MAP.md` and root `README.md` were accurate enough to leave unchanged.

## Known Gaps

- Production database is still SQLite; PostgreSQL migration has not been planned or executed.
- Production deployment and `DEBUG=False` behavior need dedicated verification.
- Media storage/access, backups, email delivery, CI, automated tests, and coverage are incomplete.
- Owner-facing invoice detail/utility entry and account lifecycle remain product gaps.
- Legacy HOSTELLO apps and surfaces remain intentionally present.
- Roadmap/SPQM/demo docs require later reconciliation after agent rules are rebuilt.

## Next Safe Phase

```text
Session B - Rebuild AGENTS.md and Agent Rules from Docs Audit
```

After Session B, the product roadmap can return to Phase 14C PostgreSQL Migration Planning. Phase 14C must be planned and explicitly approved before implementation.
