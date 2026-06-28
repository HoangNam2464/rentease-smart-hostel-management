# RentEase Docs Consolidation Audit

- **Session:** Session A - Documentation Audit and Current State Cleanup
- **Date:** 2026-06-28
- **Branch verified:** `complete-product`
- **Baseline audited:** 83 existing Markdown files
- **Final Markdown count:** 84, including this report

## 1. Current Project Structure Detected

The repository uses **Option A**, the restructured monorepo layout:

```text
RentEase/
|-- AGENTS.md
|-- README.md
|-- .agents/rules/
|-- assets/
|-- backend/
|   |-- manage.py
|   |-- requirements.txt
|   |-- .env.example
|   |-- venv/
|   `-- hostello_backend/
|-- frontend/
|   |-- templates/
|   `-- static/
`-- docs/
    |-- agent/
    |-- architecture/
    |-- archive/
    |-- demo/
    |-- security/
    |-- spqm/
    `-- ui/
```

Verified paths:

| Item | Actual path or value |
|---|---|
| Repository agent instructions | `AGENTS.md` |
| Agent rule directory | `.agents/rules/` |
| `manage.py` | `backend/manage.py` |
| Django config package | `backend/hostello_backend/` |
| `DJANGO_SETTINGS_MODULE` | `hostello_backend.settings` |
| Templates | `frontend/templates/` |
| Static files | `frontend/static/` |
| Documentation | `docs/` |
| Agent documentation | `docs/agent/` |
| Official virtual environment | `backend/venv/` |
| Requirements | `backend/requirements.txt` |
| Environment example | `backend/.env.example` |

There is no `docs/deployment/` directory and no `PHASE_14B_3_PRODUCTION_SETTINGS_VERIFICATION.md` file. No files were moved during this audit.

## 2. Markdown Inventory Summary

Final grouping after creation of this audit:

| Group | Count |
|---|---:|
| Repository root | 4 |
| `docs/` root | 6 |
| `docs/agent/` | 11 |
| `docs/architecture/` | 7 |
| `docs/ui/` | 3 |
| `docs/security/` | 2 |
| `docs/demo/` | 10 |
| `docs/spqm/` | 10 |
| `docs/archive/` | 31 |
| **Total** | **84** |

Status meanings used below: **Active**, **Outdated**, **Duplicate**, **Historical**, and **Conflicting/risky**. Decisions are recommendations only; nothing was moved or deleted.

### Root and `docs/` root

| File | Purpose | Status | Keep / Merge / Archive Later / Remove Later | Notes |
|---|---|---|---|---|
| `AGENTS.md` | Mandatory agent rules and start procedure | Active; needs consolidation | Keep | Rebuild in Session B; do not change in Session A. |
| `README.md` | Product overview and local setup | Active and useful | Keep | Structure and venv paths are correct; no clear need to edit now. |
| `PROJECT_SUMMARY.md` | Early MVP/module summary | Useful but outdated | Merge later | Still describes an admin-first MVP and omits later portal, UI, security, and production-setting work. |
| `DEMO_SCRIPT.md` | Early admin-first demo flow | Duplicate; conflicting/risky | Merge, then remove later | Superseded by `docs/demo/DEMO_SCRIPT.md`; ends with global `python manage.py check`. |
| `docs/README.md` | Documentation index | Active; partly outdated | Keep and update later | Reading order does not foreground the current agent state/audit. |
| `docs/MO-TA-CHUC-NANG-HIEN-TAI.md` | Concise role/feature list | Active and useful | Keep | Short, accurate functional summary. |
| `docs/DE-XUAT-NANG-CAP-RENTEASE.md` | Short upgrade list | Useful but outdated | Merge later | Lists repo hygiene and production settings as future work although both completed. |
| `docs/PHAN-CONG-THANH-VIEN.md` | Human team task guide | Useful but outdated | Keep and update later | Omits `rentease-layout.css` and contains person-specific escalation wording. |
| `docs/security-notes.md` | Repository/data safety notes | Candidate for merge | Merge later | Useful content overlaps `RENTEASE_SECURITY_RULES.md` and `docs/security/`. |
| `docs/SPQM-REPORT.md` | Short SPQM status stub | Conflicting/risky | Merge, then remove later | Says Phase 21C is next even though it is complete. |

### `docs/agent/`

| File | Purpose | Status | Keep / Merge / Archive Later / Remove Later | Notes |
|---|---|---|---|---|
| `docs/agent/AUTONOMOUS_EXECUTION_PLAN.md` | Autonomous operating policy | Conflicting/risky | Keep; rewrite in Session B | Authorizes automatic pushes/tags, conflicting with `AGENTS.md` explicit-approval rules. |
| `docs/agent/AUTONOMOUS_WORK_LOG.md` | Append-only chronological record | Active and useful | Keep | Current through Phase 14B-2; appended in this session. |
| `docs/agent/DOCS_AND_AGENT_SETUP_AUDIT.md` | 2026-06-27 docs audit | Useful but outdated; duplicate | Archive later | Superseded by this audit; contains pre-20O/pre-14B-2 findings. |
| `docs/agent/DOCS_CONSOLIDATION_AUDIT.md` | Current consolidation audit | Active and useful | Keep | Canonical input for Session B. |
| `docs/agent/NEXT_ACTION.md` | One immediate next action | Active and useful | Keep | Updated to Session B. |
| `docs/agent/RENTEASE_CURRENT_STATE.md` | Concise current truth | Active and useful | Keep | Updated to verified HEAD and current gaps. |
| `docs/agent/RENTEASE_PRODUCT_CONTEXT.md` | Product vision and roles | Active and useful | Keep | Stable high-level context. |
| `docs/agent/RENTEASE_PRODUCTION_ROADMAP.md` | Production work sequence | Conflicting/outdated | Keep and update later | Calls 14B-2 pending and uses Phase 14C for billing, while current Phase 14C is PostgreSQL planning. |
| `docs/agent/RENTEASE_PROJECT_MAP.md` | Active/legacy boundary | Active and useful | Keep | Correct app, template, CSS, and privacy boundaries. |
| `docs/agent/RENTEASE_SECURITY_RULES.md` | Scoping/privacy rules | Active and useful | Keep | Canonical security rule reference. |
| `docs/agent/RENTEASE_WORKFLOW.md` | Agent workflow | Conflicting/risky | Keep; reconcile in Session B | Definition of Done requires push and tells agents to push to origin. |

### `docs/architecture/`

| File | Purpose | Status | Keep / Merge / Archive Later / Remove Later | Notes |
|---|---|---|---|---|
| `docs/architecture/PROJECT_STRUCTURE_MAP.md` | Current repository layout | Active and useful | Keep | Accurate enough; no edit required in this session. |
| `docs/architecture/RENTEASE_FULL_PROJECT_ANALYSIS.md` | Detailed technical analysis | Useful but outdated | Keep; add supersession note later | Predates Phase 20O and 14B-2; settings/security risks listed there are partly resolved. |
| `docs/architecture/LEGACY_DEPENDENCY_AUDIT.md` | Legacy dependency map | Active and useful | Keep | Still the best evidence for retaining legacy apps/files. |
| `docs/architecture/CLEANUP_AUDIT.md` | Completed cleanup summary | Historical; partly outdated | Archive later | Stale recommendation is realistic demo-data polish. |
| `docs/architecture/HELPER_FILE_CLEANUP.md` | Helper/archive record | Historical | Archive later | Useful provenance, not current operating guidance. |
| `docs/architecture/POST_RESTRUCTURE_SMOKE_TEST.md` | Restructure verification | Historical | Archive later | Completed-point-in-time verification. |
| `docs/architecture/FOODIEGO_STRUCTURE_REFERENCE.md` | External structure inspiration | Historical | Archive later | Reference rationale is preserved; no longer needed for routine work. |

### `docs/demo/`

| File | Purpose | Status | Keep / Merge / Archive Later / Remove Later | Notes |
|---|---|---|---|---|
| `docs/demo/FINAL_DEMO_CHECKLIST.md` | Current pre-demo checklist | Active and useful | Keep | Correct backend/venv paths and privacy checks. |
| `docs/demo/DEMO_DATA_SEED_USAGE.md` | Seed command usage | Active and useful | Keep | Canonical seed instructions. |
| `docs/demo/LOCAL_SETUP_AND_DEMO_DATA.md` | Setup and local demo guide | Active; minor review needed | Keep | Useful, though account/database handoff wording should be reviewed later. |
| `docs/demo/DEMO_SCRIPT.md` | Portal-oriented demo narration | Useful but outdated | Merge/update later | References UI files at old locations and recommends completed Phase 20D. |
| `docs/demo/FINAL_DEMO_PACKAGE.md` | Consolidated demo package | Conflicting/risky | Merge/update later | Contains plaintext demo passwords, stale links, stale next phase, and says production settings remain unfinished. |
| `docs/demo/SCREENSHOT_CHECKLIST.md` | Screenshot targets | Useful but outdated | Merge/update later | References archived UI docs and completed Phase 20D. |
| `docs/demo/PHASE_18A_SCREENSHOT_VIDEO_PREP.md` | Capture/video plan | Historical; conflicting | Archive later | Contains plaintext demo passwords and says production settings are not configured. |
| `docs/demo/FINAL_DEMO_WALKTHROUGH_REPORT.md` | Phase 15F verification | Historical | Archive later | Valuable evidence, not current instructions. |
| `docs/demo/DEMO_DATA_SEED_IMPLEMENTATION_NOTES.md` | Phase 15E implementation record | Historical | Archive later | Implementation provenance only. |
| `docs/demo/DEMO_DATA_READINESS_PLAN.md` | Phase 15D plan/result | Historical | Archive later | Planning is complete and superseded by seed usage docs. |

### `docs/security/` and `docs/ui/`

| File | Purpose | Status | Keep / Merge / Archive Later / Remove Later | Notes |
|---|---|---|---|---|
| `docs/security/PHASE_20K_A_ADMIN_TENANT_PRIVACY_HOTFIX.md` | Admin list privacy record | Historical; partly outdated | Keep as security record | Its deferred read-only recommendation was completed in Phase 20O. |
| `docs/security/PHASE_20N_ADMIN_SEARCH_PRIVACY_HARDENING.md` | Admin search privacy record | Historical; partly outdated | Keep as security record | Its recommended Phase 20O is complete. |
| `docs/ui/RENTEASE_PROFESSIONAL_DESIGN_SYSTEM.md` | UI tokens and product style | Active and useful | Keep | Canonical design reference. |
| `docs/ui/PHASE_17C_FINAL_VISUAL_QA.md` | Visual QA checklist | Historical; outdated | Archive later | Uses old `hostello_backend` working-directory wording and stale next phase. |
| `docs/ui/RENTEASE_UI_REGRESSION_REPORT.md` | Earlier route/UI regression | Historical | Archive later | Point-in-time Phase 15 evidence. |

### `docs/spqm/`

| File | Purpose | Status | Keep / Merge / Archive Later / Remove Later | Notes |
|---|---|---|---|---|
| `docs/spqm/SPQM_OVERVIEW.md` | SPQM index and baseline | Useful but outdated | Keep and update later | Says production settings are incomplete. |
| `docs/spqm/PROCESS_MODEL.md` | Lifecycle/ETVX process | Active; policy conflict | Keep; reconcile in Session B | Release step assumes push/tag behavior. |
| `docs/spqm/DEFINITION_OF_DONE.md` | Completion gates | Conflicting/risky | Keep; reconcile in Session B | Global DoD requires push; documentation DoD wording differs from approved task flow. |
| `docs/spqm/BACKLOG_AND_PRIORITIES.md` | Prioritized backlog | Strongly outdated | Keep and update later | Multiple completed UI/settings items remain marked planned. |
| `docs/spqm/CHANGE_MANAGEMENT.md` | Change-control rules | Active and useful | Keep | Mostly consistent with current safety rules. |
| `docs/spqm/QUALITY_METRICS.md` | Quality baseline | Strongly outdated | Keep and update later | Latest phase, blocker count, UI state, and settings state are stale. |
| `docs/spqm/RELEASE_CHECKLIST.md` | Demo/production readiness checklist | Strongly outdated | Keep and update later | Production settings boxes remain unchecked after Phase 14B-2. |
| `docs/spqm/PYTHON_DJANGO_QUALITY_STACK.md` | Django quality-tool mapping | Active and useful | Keep | Correctly treats CI/tests/lint as planned. |
| `docs/spqm/CMMI_SELF_ASSESSMENT.md` | Process maturity assessment | Useful but outdated | Keep and update later | Still lists production settings as incomplete. |
| `docs/spqm/RETROSPECTIVE_TEMPLATE.md` | Reusable retrospective template | Active and useful | Keep | Stable template. |

### `docs/archive/old-plans/`

| File | Purpose | Status | Keep / Merge / Archive Later / Remove Later | Notes |
|---|---|---|---|---|
| `docs/archive/old-plans/CHECKLIST-TIEN-DO.md` | Old progress checklist | Historical/archive only | Keep archived | Do not use as current state. |
| `docs/archive/old-plans/CHI-TIET-TASK-RENTEASE.md` | Old detailed task list | Historical/archive only | Keep archived | Do not use as current plan. |
| `docs/archive/old-plans/demo-checklist.md` | Old demo checklist | Historical/archive only | Keep archived | Superseded by `docs/demo/FINAL_DEMO_CHECKLIST.md`. |
| `docs/archive/old-plans/KE-HOACH-CHI-TIET-RENTEASE.md` | Old detailed plan | Historical/archive only | Keep archived | Historical planning only. |
| `docs/archive/old-plans/RENTEASE-MASTER-TASKS.md` | Old master backlog | Historical/archive only | Keep archived | Historical planning only. |
| `docs/archive/old-plans/screenshots-checklist.md` | Old screenshot checklist | Historical/archive only | Keep archived | Superseded by current demo checklist. |
| `docs/archive/old-plans/SPRINT-PLANNING.md` | Old sprint plan | Historical/archive only | Keep archived | Historical planning only. |

### `docs/archive/phase-history/`

| File | Purpose | Status | Keep / Merge / Archive Later / Remove Later | Notes |
|---|---|---|---|---|
| `PHASE_15A_UI_UX_AUDIT_PLAN.md` | Phase 15A record | Historical/archive only | Keep archived | Completed phase. |
| `PHASE_15B1_PUBLIC_UI_POLISH.md` | Phase 15B1 record | Historical/archive only | Keep archived | Completed phase. |
| `PHASE_15B2_OWNER_LAYOUT_DASHBOARD_POLISH.md` | Phase 15B2 record | Historical/archive only | Keep archived | Completed phase. |
| `PHASE_15B3_OWNER_CRUD_POLISH.md` | Phase 15B3 record | Historical/archive only | Keep archived | Completed phase. |
| `PHASE_15B4_TENANT_PORTAL_POLISH.md` | Phase 15B4 record | Historical/archive only | Keep archived | Completed phase. |
| `PHASE_17A_FULL_UI_COMPLETENESS_AUDIT.md` | Phase 17A record | Historical/archive only | Keep archived | Completed phase. |
| `PHASE_17B_REMAINING_UI_POLISH.md` | Phase 17B record | Historical/archive only | Keep archived | Completed phase. |
| `PHASE_19A_PRODUCT_GRADE_UI_REDESIGN.md` | Phase 19A record | Historical/archive only | Keep archived | Completed phase. |
| `PHASE_19B_VIETNAMESE_COPY_AND_HUMAN_UI_FIXES.md` | Phase 19B record | Historical/archive only | Keep archived | Completed phase. |
| `PHASE_20A_PROFESSIONAL_UI_REDESIGN.md` | Phase 20A record | Historical/archive only | Keep archived | Completed phase. |
| `PHASE_20B_TEMPLATE_REFERENCE_UI_DIRECTION.md` | Phase 20B record | Historical/archive only | Keep archived | Completed phase. |
| `PHASE_20C_REFERENCE_BASED_UI_REDESIGN.md` | Phase 20C record | Historical/archive only | Keep archived | Completed phase. |
| `PHASE_20D_UI_PACKAGE_APPLICATION.md` | Phase 20D record | Historical/archive only | Keep archived | Completed phase. |
| `PHASE_20E_OWNER_CRUD_POLISH.md` | Phase 20E record | Historical/archive only | Keep archived | Completed phase. |
| `PHASE_20F_TENANT_PORTAL_BUGFIX_POLISH.md` | Phase 20F record | Historical/archive only | Keep archived | Completed phase. |
| `PHASE_20G_RENTEASE_UI_V2_DARK_SIDEBAR.md` | Phase 20G record | Historical/archive only | Keep archived | Completed phase. |
| `PHASE_20H_FULL_UI_VISUAL_QA.md` | Phase 20H record | Historical/archive only | Keep archived | Completed phase. |
| `PHASE_20I_FULL_ROLE_UI_UX_AUDIT.md` | Phase 20I record | Historical/archive only | Keep archived | Completed audit. |
| `PHASE_20J_BROWSER_VISUAL_QA.md` | Phase 20J record | Historical/archive only | Keep archived | Source of the citizen-ID exposure finding. |
| `PHASE_20K_B_DASHBOARD_INTERACTION_VISUAL_POLISH.md` | Phase 20K-B record | Historical/archive only | Keep archived | Completed phase. |
| `PHASE_20L_OWNER_CRUD_FORM_TABLE_PROFESSIONALIZATION.md` | Phase 20L record | Historical/archive only | Keep archived | Completed phase. |
| `PHASE_20M_REPORTS_ADMIN_VISUAL_POLISH_PLANNING.md` | Phase 20M record | Historical/archive only | Keep archived | Planning record. |
| `PHASE_21B_REPO_HYGIENE_AUDIT.md` | Phase 21B record | Historical/archive only | Keep archived | Completed phase. |
| `PHASE_21C_SAFE_REPO_HYGIENE_CLEANUP.md` | Phase 21C record | Historical/archive only | Keep archived | Completed phase. |

Archive rows above use filenames relative to `docs/archive/phase-history/`.

## 3. Active Docs To Keep

Future agents should begin with this minimal set:

1. `AGENTS.md`
2. `docs/agent/RENTEASE_CURRENT_STATE.md`
3. `docs/agent/NEXT_ACTION.md`
4. `docs/agent/RENTEASE_PROJECT_MAP.md` when file boundaries matter
5. `docs/agent/RENTEASE_SECURITY_RULES.md` when data access/privacy matters
6. The relevant SPQM document for planning, quality, release, UI, production, billing, or documentation work

Use `docs/agent/AUTONOMOUS_WORK_LOG.md` for chronology, not as the first source of current truth. Use archive files only for historical evidence.

## 4. Outdated or Conflicting Docs

Main conflicts found:

- The actual structure is `backend/`, `frontend/`, and `docs/`; older instructions that say to run from `hostello_backend/` or use a root venv are obsolete.
- The official venv is `backend/venv/`; global `python manage.py ...` wording remains in the root demo script.
- Both `rentease-design.css` and `rentease-layout.css` are active; some human/team docs mention only the design file.
- Phase numbering conflicts: the current product sequence uses Phase 14C for PostgreSQL planning, while `RENTEASE_PRODUCTION_ROADMAP.md` assigns Phase 14C to owner billing details.
- Phase 14B-2 is complete at commit `93b56a4`, but the production roadmap and several SPQM/demo documents still mark production settings as pending.
- Phase 20O is complete, but the full technical analysis and security phase reports still present its read-only admin hardening as pending.
- Many demo/UI docs recommend completed phases such as 20D or link to phase files that have moved into `docs/archive/phase-history/`.
- `AUTONOMOUS_EXECUTION_PLAN.md`, `RENTEASE_WORKFLOW.md`, and parts of SPQM define push/tag as automatic completion steps; `AGENTS.md` requires explicit approval before push or tag.
- `docs/demo/FINAL_DEMO_PACKAGE.md` and `PHASE_18A_SCREENSHOT_VIDEO_PREP.md` contain plaintext demo passwords. They should not be the long-term canonical onboarding surface.
- Root `DEMO_SCRIPT.md` and `docs/demo/DEMO_SCRIPT.md` describe different product eras.
- The old workflow of sending or embedding long prompts is no longer necessary once Session B makes `AGENTS.md` and `.agents/rules/` concise and authoritative.

## 5. Docs To Merge Later

- Merge safe repository/data guidance from `docs/security-notes.md` into the canonical security documentation.
- Merge useful MVP context from `PROJECT_SUMMARY.md` into README/product context, then mark the old summary historical.
- Consolidate the two demo scripts into one canonical portal-first script.
- Consolidate demo package, screenshot, and recording guidance; remove plaintext credentials from canonical docs.
- Fold the useful conclusions of `DOCS_AND_AGENT_SETUP_AUDIT.md` into this audit, then archive the older audit.
- Replace the `docs/SPQM-REPORT.md` stub with links to current SPQM documents or remove it after approval.

## 6. Docs To Archive Later

- `docs/agent/DOCS_AND_AGENT_SETUP_AUDIT.md`
- `docs/architecture/CLEANUP_AUDIT.md`
- `docs/architecture/HELPER_FILE_CLEANUP.md`
- `docs/architecture/POST_RESTRUCTURE_SMOKE_TEST.md`
- `docs/architecture/FOODIEGO_STRUCTURE_REFERENCE.md`
- `docs/demo/DEMO_DATA_READINESS_PLAN.md`
- `docs/demo/DEMO_DATA_SEED_IMPLEMENTATION_NOTES.md`
- `docs/demo/FINAL_DEMO_WALKTHROUGH_REPORT.md`
- `docs/demo/PHASE_18A_SCREENSHOT_VIDEO_PREP.md`
- `docs/ui/PHASE_17C_FINAL_VISUAL_QA.md`
- `docs/ui/RENTEASE_UI_REGRESSION_REPORT.md`

All existing files under `docs/archive/` should remain archived.

## 7. Docs To Remove Later

Only after content is merged and explicit approval is received:

- Root `DEMO_SCRIPT.md`
- `docs/SPQM-REPORT.md`

No document is safe to remove during Session A.

## 8. Recommended Clean Documentation Structure

```text
AGENTS.md                         # concise mandatory rules and startup
.agents/rules/                    # short scoped rules; no duplicated state
docs/
|-- README.md                    # documentation index
|-- agent/
|   |-- RENTEASE_CURRENT_STATE.md
|   |-- NEXT_ACTION.md
|   |-- RENTEASE_PROJECT_MAP.md
|   |-- RENTEASE_SECURITY_RULES.md
|   |-- RENTEASE_PRODUCT_CONTEXT.md
|   |-- RENTEASE_PRODUCTION_ROADMAP.md
|   |-- DOCS_CONSOLIDATION_AUDIT.md
|   `-- AUTONOMOUS_WORK_LOG.md
|-- architecture/                # current architecture/reference only
|-- demo/                        # one setup guide, one seed guide, one demo guide
|-- security/                    # current security rules plus locked records
|-- spqm/                        # process/quality source of truth
|-- ui/                          # current design system and current QA guide
`-- archive/                     # completed phase records and superseded plans
```

State, history, policy, and next action should remain separate. Current facts belong in `RENTEASE_CURRENT_STATE.md`; chronology belongs in the append-only work log; mandatory policy belongs in `AGENTS.md`; only one immediate task belongs in `NEXT_ACTION.md`.

## 9. Next Session Recommendation

```text
Session B - Rebuild AGENTS.md and Agent Rules from Docs Audit
```

Session B should use this audit to make `AGENTS.md` concise and authoritative, reconcile `.agents/rules/`, remove push/tag ambiguity, and let future agents start from short local instructions instead of long prompts. It must remain a rules/documentation task and must not implement Phase 14C.
