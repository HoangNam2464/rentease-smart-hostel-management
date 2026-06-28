# RentEase Documentation History

The active documentation tree intentionally keeps only current project guidance. Superseded phase reports, audits, plans, coursework notes, and the former chronological work log were removed from the working tree to prevent them from being mistaken for current instructions.

Git retains the complete history. Retrieve an older document only when a task requires historical evidence:

```powershell
git log --all --name-only -- docs/
git log --all -- <previous-document-path>
git show <commit>:<previous-document-path>
git tag --list
```

Historical content is not current policy. Verify all recovered claims against the present source code, `AGENTS.md`, and the current documents listed in `docs/README.md`.
