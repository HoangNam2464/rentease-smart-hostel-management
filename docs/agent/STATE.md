# RentEase State

Last verified: 2026-07-07.

## Baseline

| Item | Current truth |
|---|---|
| Branch | `complete-product` |
| Public UI baseline | Commit `6a55a62`, pushed to `origin/complete-product` |
| Django check | Pass |
| Migration dry-run | No changes detected |
| Automated tests | 88 passed |
| Product stage | Polished local demo; not production-ready |

Re-run the checks before relying on this snapshot.

## Runtime

- Django backend: `backend/`
- Django configuration: `backend/hostello_backend/` (protected compatibility name)
- Active templates and static assets: `frontend/`
- Production database target: PostgreSQL through environment-driven configuration
- Local development may use the configured fallback; verify the active connection instead of assuming it
- Active apps: `accounts`, `properties`, `tenants`, `contracts`, `billing`, `maintenance`, `listings`, `portal`, and `reports`
- Legacy HOSTELLO apps remain installed and isolated; see `docs/architecture/LEGACY.md`

## Product

- Public room discovery and viewing registration exist.
- Owner property, room, listing, tenant, contract, invoice, payment, repair, and viewing-registration workflows exist.
- Tenant profile, contract, invoice, payment, repair, and notification workflows exist.
- Staff reports and Django Admin exist.
- PayOS integration and billing compatibility foundations exist.
- Owner/tenant query scoping and sensitive identity restrictions remain mandatory.

## Interface

- The public home and room-listing experience has a verified refreshed baseline.
- Owner, tenant, reports, and admin surfaces still require a reference-first consistency pass.
- Public teal branding and the purple DreamPOS-inspired portal tokens are not yet fully unified.
- Interface work must be learned from approved references, adapted to RentEase, and verified at desktop and mobile sizes.

## Language

- Current templates contain mostly hard-coded Vietnamese copy.
- Django currently has i18n enabled but has no complete EN/VI translation catalog or language switcher.
- Code-English and UI-bilingual rules are now canonical in `AGENTS.md` and `docs/ui/DESIGN.md`.
- Runtime i18n conversion is intentionally the final product-language phase after the interface system is stable.

## Known gaps

- Reference-led UI completion across owner, tenant, reports, and admin
- A single shared design-token/component system
- Complete English source messages and Vietnamese translations
- EN/VI language switcher with locale persistence
- Account onboarding and recovery completion
- Protected production media, backups, CI, deployment verification, and broader coverage

## Next

Follow `docs/agent/NEXT.md`.
