# RentEase Project Structure Map

This is the canonical map for repository paths, active/legacy boundaries, runtime data, documentation, and agent resources.

## Top-Level Structure

```text
RentEase/
|-- AGENTS.md                    # mandatory short agent entry
|-- README.md                    # human project overview and setup
|-- .agents/
|   |-- rules/                   # minimal always-on safety rule
|   `-- skills/rentease/         # progressive RentEase workflow and references
|-- assets/                      # tracked historical HOSTELLO media
|-- backend/                     # Django backend and apps
|-- frontend/                    # Django templates and static files
`-- docs/
    |-- agent/                   # current state, next action, product, security, roadmap
    |-- architecture/            # current structure and legacy dependency map
    |-- demo/                    # current local demo guidance
    |-- ui/                      # current design guidance
    `-- archive/                 # superseded and historical documents
```

## Backend

Important paths:

- `backend/manage.py`
- `backend/requirements.txt`
- `backend/.env.example`
- `backend/hostello_backend/` - Django config package; do not rename
- `backend/venv/` - official local venv; ignored and protected
- `backend/db.sqlite3` - local database; ignored and protected
- `backend/media/` - local uploads; ignored and protected

`DJANGO_SETTINGS_MODULE` remains `hostello_backend.settings`.

### Active RentEase Apps

| App | Purpose |
|---|---|
| `accounts` | Users and owner profiles |
| `properties` | Rooms |
| `tenants` | Tenants and co-tenants |
| `contracts` | Rental contracts |
| `billing` | Price configuration, invoices, details, payments |
| `maintenance` | Repairs, maintenance records, notifications |
| `listings` | Public listings and viewing registrations |
| `portal` | Owner/tenant portal and demo seed command |
| `reports` | Staff-only reports |

### Legacy HOSTELLO Apps

`students`, `attendance`, `fees`, `requests`, and `notices` remain installed with models, migrations, admin registrations, or cross-imports. Do not move, rename, or delete them without an approved legacy-removal plan.

Read `docs/architecture/LEGACY_BOUNDARIES.md` for current editing boundaries. Use `docs/architecture/LEGACY_DEPENDENCY_AUDIT.md` only as historical evidence when legacy work requires it.

## Frontend

All current Django templates, including reports, live under `frontend/templates/`.

Current product surfaces:

- `frontend/templates/home.html`
- `frontend/templates/listings/`
- `frontend/templates/portal/`
- `frontend/templates/reports/`
- `frontend/templates/404.html` and `500.html`

Current styles:

- `frontend/static/css/rentease-design.css`
- `frontend/static/css/rentease-layout.css`
- `frontend/static/admin/css/custom_admin.css`

Legacy surfaces not used for normal RentEase UI work:

- `frontend/templates/index.html`, `login.html`, `dashboard.html`
- `frontend/templates/admin/`
- `frontend/templates/payments/success.html`
- `frontend/static/css/styles.css`
- `frontend/static/css/student-dashboard.css`
- `frontend/static/js/script.js`
- `frontend/static/js/student-dashboard.js`
- root `assets/`

## Database and Runtime Data

- SQLite is the current local database.
- PostgreSQL is the production target but has not been migrated.
- Do not scan or edit `db.sqlite3`, media, venvs, logs, static runtime output, backups, or `.env` during ordinary code/documentation work.
- Migrations are part of source control but may be created only with explicit approval.

## Documentation Authority

Read `docs/README.md` for the complete authority and task-routing table.

Current documents live in `docs/agent/`, `docs/architecture/`, `docs/ui/`, and `docs/demo/`. Superseded audits, old rules, SPQM coursework/status files, plans, phase reports, and duplicate root documents live in `docs/archive/`.

Archive content is not current policy. Do not scan it unless historical context is required.

## Agent Resources

- `AGENTS.md` gives mandatory startup and hard rules.
- `.agents/rules/rentease-safety.md` is the minimal tool-facing safety rule.
- `.agents/skills/rentease/SKILL.md` routes substantive tasks.
- Skill references load backend, UI, or documentation context separately.

## Editing Rules

- Inspect the real target before editing.
- Keep active RentEase work out of legacy files unless explicitly requested.
- Preserve owner/tenant scoping and sensitive-data rules.
- Plan before settings, schema, auth, billing, database, deployment, or legacy changes.
- Run Django checks after all changes, including documentation-only reorganizations.
