# Backend and Django Safety

Load this reference for Python, Django, admin, permissions, billing, settings, database, deployment, or legacy work.

## Read Before Editing

- `docs/architecture/PROJECT_STRUCTURE_MAP.md`
- `docs/agent/RENTEASE_SECURITY_RULES.md`
- Directly related source files

Read the production roadmap only for production work. For legacy work, read `docs/architecture/LEGACY_BOUNDARIES.md` and re-audit current imports, settings, URLs, migrations, admin registrations, and data dependencies; do not rely on recovered historical audits.

## Approval Gates

Present a plan and obtain explicit approval before changing:

- `models.py` or migrations
- database schema or data migration
- `settings.py` or deployment configuration
- authentication, permissions, or account lifecycle
- billing calculations or invoice detail behavior
- URL structure or legacy routing
- legacy apps or their templates/static dependencies

Stop if an approved no-schema task unexpectedly needs a migration.

## Data Access

- Scope owner data through `request.user.rentease_profile` and owned relationships.
- Scope tenant data through `request.user.tenant_profile`.
- Use scoped querysets in detail, update, and delete views.
- Verify identifier changes cannot expose another owner or tenant's record.
- Keep reports staff-only.

## Sensitive Data

- Never expose citizen identity fields/files on public, owner, or tenant surfaces.
- Do not add identity fields to admin lists, searches, or contract inlines.
- Keep sensitive admin identity fields read-only for non-superusers.
- Do not commit credentials, `.env`, SQLite databases, dumps, media, or logs.

## Runtime Boundaries

- Run Django commands from `backend/` with `backend/venv/Scripts/python.exe`.
- Keep `hostello_backend.settings` and the inner config package name unchanged.
- Keep local SQLite behavior unless an approved database phase changes it.
- Do not treat DEBUG media serving as production media security.

## Verification

Always run:

```powershell
.\venv\Scripts\python.exe manage.py check
.\venv\Scripts\python.exe manage.py makemigrations --check --dry-run
```

Also verify affected routes, correct/wrong roles, owner/tenant isolation, calculations, admin configuration, or `DEBUG=False` behavior as appropriate.
