# Phase 21B Repo Hygiene Audit

## Scope

This is a read-only repo hygiene audit. No files were deleted and no files were untracked in this phase.

## Commands Used

```powershell
git status --short
git ls-files | findstr /i "db.sqlite3 venv backup_phase .env media"
dir
dir hostello_backend
dir hostello_backend\media
```

## Local Files Present

Repository root contains:

- `venv/`
- `backup_phase2.json`
- `backup_phase3.json`
- `backup_phase4.json`
- `backup_phase5.json`

`backend/` contains:

- `db.sqlite3`
- `venv/`
- `media/`
- `phase8b2_wip.patch`

`backend/media/` contains legacy media files such as:

- `about-bg.jpg`
- `bed*.jpg/png`
- `facilities*.jpg`
- `header*.jpg/png`
- `menu-*.jpg`
- `*.mp4`

## Git Tracking Result

The tracked-file check returned no output for:

- `db.sqlite3`
- `venv`
- `backup_phase`
- `.env`
- `media`

Interpretation:

- these sensitive/local files appear to be untracked at the time of this audit
- they should still remain ignored and should not be staged manually

## Sensitive File Risk

Potentially sensitive or local-only files exist in the working folder:

- SQLite database
- virtual environments
- backup JSON files
- media files
- old WIP patch file

These files can be useful locally but should not be committed without explicit approval.

## Current `.gitignore` Notes

Existing `.gitignore` already includes:

- `*.sqlite3`
- `db.sqlite3`
- `backup_phase*.json`
- `venv/`
- `.env`
- `.env.*`
- `media/`
- `/backend/media/`

## Suggested Phase 21C Cleanup

Phase 21C should safely verify and improve repo hygiene:

- confirm `.gitignore` covers all local-only files
- check whether any sensitive files are tracked
- use `git rm --cached` only if a sensitive file is tracked
- do not delete local files blindly
- do not touch migrations/schema

## Do Not Do Yet

- Do not delete `db.sqlite3`.
- Do not delete `venv`.
- Do not delete backup JSON files.
- Do not delete `media/`.
- Do not delete legacy apps.
- Do not remove files from Git history in this phase.
