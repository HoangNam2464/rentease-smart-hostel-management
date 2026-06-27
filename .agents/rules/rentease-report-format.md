# RentEase Final Report Format

Every agent must end its turn with a final report in this format. Do not omit sections.

---

## Final Report Template

```
Current Branch: <branch name>

Working Tree Before:
<clean / not clean — describe if not clean>

Project Structure Confirmed:
<backend/frontend/docs or describe what differs>

Files Changed:
- <file path>
- <file path>

Files Not Changed (but reviewed):
- <file path>

Checks Run:
- manage.py check
- makemigrations --check --dry-run

Checks Result:
- manage.py check: <passed / failed — paste output if failed>
- makemigrations: <No changes detected / failed — paste output if failed>

Commit:
<commit hash and message, or "no commit — reason">

Safety Confirmation:
- No Python code changed: <yes/no>
- No models changed: <yes/no>
- No migrations created: <yes/no>
- No templates or static files touched: <yes/no>
- No database/media/venv files touched: <yes/no>
- Nothing pushed: <yes/no>

Recommended Next Phase:
<phase name and one-line goal>
```

---

## Rules for the Report

- Always include every section. Do not skip.
- If a check failed, paste the relevant error output.
- If no commit was made, explain why.
- The Safety Confirmation must be explicit — do not write "N/A".
- Keep the Recommended Next Phase consistent with `docs/agent/NEXT_ACTION.md`.
