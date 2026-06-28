# RentEase Agent Workflow

Standard workflow every agent must follow on this project. Follow in order.

## 1. Read Agent Docs First

Read these files before doing anything else:

| File | What it contains |
|---|---|
| `AGENTS.md` | Mandatory rules, structure, forbidden actions |
| `docs/agent/RENTEASE_CURRENT_STATE.md` | Latest phase, commits, CSS files, security status, known gaps |
| `docs/agent/NEXT_ACTION.md` | The one recommended next phase |
| `docs/agent/RENTEASE_PROJECT_MAP.md` | Active/legacy boundary for apps, templates, CSS |

Do not rely on conversation memory. Read the files directly.

## 2. Confirm Project State

From the repository root:

```powershell
git branch --show-current   # expect: complete-product
git status --short           # expect: clean
git log --oneline -15
```

From `backend/`:

```powershell
.\venv\Scripts\python.exe manage.py check
.\venv\Scripts\python.exe manage.py makemigrations --check --dry-run
```

Stop if branch is wrong, working tree is dirty, or any check fails.

## 3. Confirm Project Structure

Verify the real layout before editing:

```text
RentEase/
├── backend/    # Django backend — manage.py, apps, venv/, hostello_backend/
├── frontend/   # Django templates and static assets
└── docs/       # Documentation
```

If the structure differs from the above, stop and report.

## 4. Plan Before Editing

- Identify the exact files you will change.
- Confirm none of them are forbidden (see `rentease-safety.md` and `rentease-file-boundaries.md`).
- Keep the phase small. One logical unit of work per phase.
- If the scope is unclear, stop and ask. Do not guess.

## 5. Implement

- Change only the files identified in step 4.
- Verify no unintended files are modified (`git status --short`).
- For Python code, templates, CSS, or admin changes: run Django check after editing.

## 6. Verify After Editing

```powershell
.\venv\Scripts\python.exe manage.py check
.\venv\Scripts\python.exe manage.py makemigrations --check --dry-run
```

Both must pass before committing.

Test affected routes if code was changed.

## 7. Commit

```powershell
git status --short   # confirm only intended files are staged
git add <specific files only>
git commit -m "<short phase-specific message>"
```

Do not use `git add .` or `git add -A` — stage specific files only.

Do not push unless explicitly requested.

## 8. Update Agent Docs

After each completed phase, update:

- `docs/agent/RENTEASE_CURRENT_STATE.md` — latest commit, phase, and status
- `docs/agent/NEXT_ACTION.md` — next recommended phase
- `docs/agent/AUTONOMOUS_WORK_LOG.md` — append a new chronological entry

Do not update agent docs silently during feature work unless the documentation update is part of the approved task.
