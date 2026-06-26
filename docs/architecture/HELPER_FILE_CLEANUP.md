# Helper File Cleanup

Date: 2026-06-26

## Scope

This phase reviewed only low-risk helper and historical files after the legacy dependency audit.

The phase did not touch Django apps, models, migrations, business logic, permissions, templates, static files, or `backend/venv/`.

## Files Inspected

| Item | Reference search result | Action taken | Reason | Risk level | Recommendation |
|---|---|---|---|---|---|
| `Working.py` | Referenced only by docs/audit notes and as a local helper note | Moved to `docs/archive/Working.py` | Not imported by Python runtime and not required by Django | Low | keep archived |
| `run_frontend.bat` | Referenced by `Working.py` and docs/audit notes only | Moved to `docs/archive/run_frontend.bat` | Manual browser opener with old HOSTELLO wording; not required by runtime | Low | keep archived |
| `backup_phase*.json` | Mentioned in security/repo hygiene docs; not tracked by Git | Moved locally to `docs/archive/local-backups/` | Local backup files may contain demo/account data and should remain untracked | Medium | keep ignored/local only or delete later with approval |
| `assets/` | Tracked historical screenshots/video and referenced by architecture docs | Kept in place | Large historical/demo material; moving it would create a noisy rename and may affect documentation references | Low to medium | archive in a separate phase only if approved |

## Reference Search Result

- No runtime Python imports for `Working.py` were found.
- No Django settings, URL routing, app view, template, or static runtime dependency on `run_frontend.bat` was found.
- `backup_phase*.json` files are local data dumps and are covered by ignore rules; they should not be committed.
- `assets/` appears to be historical HOSTELLO screenshot/video material. It is tracked and documented, but no active Django runtime dependency was found.

## Files Moved

- `Working.py` -> `docs/archive/Working.py`
- `run_frontend.bat` -> `docs/archive/run_frontend.bat`
- `backup_phase2.json` -> `docs/archive/local-backups/backup_phase2.json`
- `backup_phase3.json` -> `docs/archive/local-backups/backup_phase3.json`
- `backup_phase4.json` -> `docs/archive/local-backups/backup_phase4.json`
- `backup_phase5.json` -> `docs/archive/local-backups/backup_phase5.json`

The backup JSON files remain ignored/untracked and were not added to Git.

## Files Kept

- `assets/`

Reason: `assets/` contains many tracked historical screenshots and a video. It is not runtime-critical, but moving it would create a broad rename and could break documentation references. Keep it until a dedicated archive/media cleanup phase.

## Risk Notes

- Do not commit backup JSON files because they may contain account/demo data.
- Do not delete legacy Django apps because they still have models, migrations, admin registrations, and cross-app imports.
- Do not delete legacy templates/static files because some are still referenced by `/legacy/` routes or legacy admin views.

## Final Recommendation

The helper cleanup is safe as completed:

1. Keep `Working.py` and `run_frontend.bat` archived for traceability.
2. Keep backup JSON files local and ignored.
3. Keep `assets/` in place for now.
4. If a future phase cleans historical media, plan and verify documentation links before moving `assets/`.

