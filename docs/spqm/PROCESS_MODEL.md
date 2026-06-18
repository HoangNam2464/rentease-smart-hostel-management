# RentEase Process Model

## SDLC Flow

RentEase uses a small-phase SDLC:

```text
planning -> design -> implementation -> review -> testing -> release -> retrospective
```

The process is intentionally lightweight. It favors clear phase boundaries, scoped changes, and measurable verification over large rewrites.

## Roles

Developer:

- inspects the current codebase
- implements approved changes
- runs checks and route verification
- reports modified files and issues

Reviewer:

- reviews scope, security, privacy, and regression risk
- confirms that only intended files changed
- approves lock/tag steps

Tester:

- verifies affected public, owner, tenant, admin, reports, and legacy routes
- checks role-based access and privacy
- confirms no migration/schema drift unless approved

Product owner/demo owner:

- defines priority and phase scope
- approves plans before implementation
- approves commits/tags for locked milestones

## Step Inputs And Outputs

| Step | Inputs | Outputs |
| --- | --- | --- |
| Planning | user request, AGENTS.md, current state docs, related source files | implementation plan, risks, expected files |
| Design | ERD, model/admin/portal patterns, security rules | scoped design and verification checklist |
| Implementation | approved plan, clean branch | code or documentation changes |
| Review | diff, changed files, security rules | findings, fixes, approval to verify |
| Testing | Django check, migration dry-run, route tests | pass/fail evidence |
| Release | clean working tree, pushed commit, approval | phase tag or release tag |
| Retrospective | phase result, metrics, issues | improvement actions |

## ETVX Process Table

| Entry Criteria | Task | Verification | Exit Criteria |
| --- | --- | --- | --- |
| Branch is `complete-product`; working tree is clean; request scope is clear | Inspect relevant docs and files | `git branch --show-current`, `git status --short`, file inspection | Plan is grounded in actual source |
| Plan is approved for implementation | Make the smallest safe change | Diff contains only intended files | No unrelated source or schema change |
| Implementation is complete | Run quality gates | Django check and migration dry-run | System check passes and no changes detected unless migrations were approved |
| Route or feature is affected | Verify affected behavior | Test client/manual route checks | Affected routes behave as expected |
| Security or data access is affected | Verify owner/tenant scoping and privacy | Scoped query audit and role checks | No privacy/security regression |
| Phase is ready to lock | Commit, push, and tag only after approval | Git log, status, tag list | Working tree clean and phase tag pushed |

## Diagram Note

Future diagrams can be added later. Suggested diagrams:

- phase workflow diagram
- owner/tenant access-control flow
- release readiness flow
- production deployment flow
