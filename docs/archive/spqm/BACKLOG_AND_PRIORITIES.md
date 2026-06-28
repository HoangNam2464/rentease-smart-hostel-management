# RentEase Backlog And Priorities

## Priority Labels

P0 Critical:

- blocks production readiness or creates significant security risk

P1 High:

- important for real user adoption or operational completeness

P2 Medium:

- improves maintainability, documentation, or quality confidence

P3 Low:

- useful polish or long-term cleanup

## Demo / Presentation Track

Purpose: make the current Python/Django project look and feel more like a real usable product for demo and presentation.

| Priority | Item | Current Status | Rationale |
| --- | --- | --- | --- |
| P0 Critical | Product-grade UI redesign | Completed in Phase 19A | Demo quality requires RentEase to feel like a real room-rental product, not only a working admin-first app |
| P0 Critical | Vietnamese copy and human UI fixes | Completed in Phase 19B | Browser review found unaccented Vietnamese and generic landing copy that weakened product credibility |
| P0 Critical | Professional UI design system and full visual redesign | Completed in Phase 20A | The UI needed one coherent SaaS-style system instead of repeated small patches |
| P0 Critical | Template reference selection and UI direction | Completed in Phase 20B | The next redesign pass needs a concrete public property-listing and dashboard portal reference direction |
| P0 Critical | Apply reference-based UI redesign | Completed in Phase 20C | Phase 20C translated the selected direction into local templates and CSS without copying external template packages |
| P1 High | Browser visual review and final UI fixes | Planned | The reference-based redesign now needs real desktop/mobile browser review before final screenshots |
| P0 Critical | UI/UX Audit and Redesign Planning | Planned | Demo quality depends on clear public, owner, and tenant flows |
| P0 Critical | Public UI Polish | Planned | Public landing and room browsing are the first visible product surface |
| P1 High | Owner Portal Layout Polish | Planned | Owner workflows need consistent navigation and page structure |
| P1 High | Tenant Portal Polish | Planned | Tenant pages need readability and clear status presentation |
| P1 High | README and Demo Documentation | Partially complete | Demo docs exist, but final presentation packaging may need polish |
| P2 Medium | Screenshots / Video Demo Support | Planned | Helps course presentation and review |
| P3 Low | Reports Polish | Planned | Reports work, but visual/export polish can wait |

## Real Production Readiness Track

Purpose: make the project safer for real deployment later.

| Priority | Item | Current Status | Rationale |
| --- | --- | --- | --- |
| P0 Critical | Production Settings Split | Planned | Current settings are local-demo oriented, not production-hardened |
| P0 Critical | Owner Billing Detail / Utility Entry | Planned | Owner can create invoice headers and record payments, but invoice details/utility entry are incomplete |
| P1 High | Account Lifecycle | Planned | Password reset, onboarding, and tenant account creation/invitation are incomplete |
| P1 High | Deployment Readiness | Planned | Production database, static/media, email, logging, and deployment docs are not complete |
| P2 Medium | GitHub Actions CI | Planned | Automated quality gates are not verified |
| P2 Medium | Test Coverage | Planned | Regression has been manually verified, but automated coverage is not complete |
| P3 Low | Legacy Cleanup | Planned | Legacy is isolated but still present |

## Combined Priority View

Use this view when choosing work across both tracks.

| Priority | Item | Track |
| --- | --- | --- |
| P0 Critical | Product-grade UI redesign | Demo/Product Polish |
| P0 Critical | Vietnamese copy and human UI fixes | Demo/Product Polish |
| P0 Critical | Professional UI design system and full visual redesign | Demo/Product Polish |
| P0 Critical | Template reference selection and UI direction | Demo/Product Polish |
| P0 Critical | Apply reference-based UI redesign | Demo/Product Polish |
| P0 Critical | UI/UX Audit and Redesign Planning | Demo/Product Polish |
| P0 Critical | Public UI Polish | Demo/Product Polish |
| P1 High | Browser visual review and final UI fixes | Demo/Product Polish |
| P0 Critical | Production Settings Split | Real Production Readiness |
| P0 Critical | Owner Billing Detail / Utility Entry | Real Production Readiness |
| P1 High | Owner Portal Layout Polish | Demo/Product Polish |
| P1 High | Tenant Portal Polish | Demo/Product Polish |
| P1 High | README and Demo Documentation | Demo/Product Polish |
| P1 High | Account Lifecycle | Real Production Readiness |
| P1 High | Deployment Readiness | Real Production Readiness |
| P2 Medium | GitHub Actions CI | Real Production Readiness |
| P2 Medium | Test Coverage | Real Production Readiness |
| P3 Low | Legacy Cleanup | Real Production Readiness |

## SMART-Q Goals For Top Priorities

### P0 Production Settings Split

Specific: split or harden settings so local and production configurations are clearly separated.

Measurable: Django check passes; migration dry-run is clean; no secrets are committed; production-required environment variables are documented.

Achievable: settings-only phase with no schema changes expected.

Relevant: required before real deployment.

Time-bound: complete before production deployment work.

Quality-focused: preserve local runserver and avoid weakening security defaults.

### P0 Owner Billing Detail / Utility Entry

Specific: add owner-facing workflow for invoice details, utility readings, and service/rent breakdown.

Measurable: owner can create meaningful invoice totals from portal; tenant can view clear invoice details; payment totals remain consistent.

Achievable: build on existing billing models and owner invoice/payment portal.

Relevant: billing is core to boarding-house operation.

Time-bound: complete before real owner pilot testing.

Quality-focused: maintain owner scoping, block overpayment, and preserve calculated amount integrity.

### P1 Account Lifecycle

Specific: add real-world account recovery and onboarding flows.

Measurable: supported user roles can recover access and link to proper profiles without exposing sensitive data.

Achievable: use Django auth patterns before adding more complex identity features.

Relevant: required for non-admin users in production.

Time-bound: complete before public launch.

Quality-focused: avoid leaking account internals or citizen ID data.
