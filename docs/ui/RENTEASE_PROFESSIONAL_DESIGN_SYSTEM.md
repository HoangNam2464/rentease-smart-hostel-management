# RentEase UI and Design Guide

This is the current source of truth for RentEase templates, CSS, UX copy, responsive behavior, and visual QA.

## Design Identity

Creative north star: calm operations for Vietnamese rentals.

The interface should reduce the mental work of finding a room, running a boarding house, or understanding a tenancy. It should feel grounded, legible, and quietly capable rather than decorative or technology-led.

Avoid these visual references:

- the old HOSTELLO school-management interface
- a generic SaaS dashboard made from repeated cards
- a luxury real-estate marketplace that hides operational detail
- a banking interface that makes routine rental tasks feel formal or intimidating

## Product Direction

RentEase is a practical Vietnamese boarding-house management product. It should feel trustworthy, clear, business-ready, and human-written rather than like a generic school admin template.

### Role-Specific Surfaces

- Public pages: room-listing product with clear browsing and viewing-registration actions.
- Owner pages: compact small-business dashboard with strong hierarchy and efficient actions.
- Tenant pages: simpler resident portal with readable status and financial information.
- Admin/reports: operational, compact, staff-oriented, and privacy-safe.

## Active Files

| File | Responsibility |
|---|---|
| `frontend/static/css/rentease-design.css` | Tokens, typography, colors, shared components |
| `frontend/static/css/rentease-layout.css` | Portal shell, sidebar, tables, forms, responsive layout |
| `frontend/static/admin/css/custom_admin.css` | Django Admin overrides |
| `frontend/templates/home.html` | Public landing page |
| `frontend/templates/listings/` | Public room and registration flow |
| `frontend/templates/portal/` | Owner and tenant portals |
| `frontend/templates/reports/` | Staff report UI |

Do not edit legacy HOSTELLO templates or styles for RentEase product work. See `docs/architecture/PROJECT_STRUCTURE_MAP.md` for the boundary.

## Core Visual Tokens

| Role | Value |
|---|---|
| Primary | `#0f766e` |
| Primary dark | `#0b5f59` |
| Accent | `#2563eb` |
| Background | `#f4f6f5` |
| Surface | `#ffffff` |
| Main text | `#17212b` |
| Muted text | `#627386` |
| Border | `#dce5e2` |

Reuse existing CSS variables and component classes before introducing new ones.

## Component Guidance

- Use a clear page title, short supporting copy, and one obvious primary action.
- Keep navigation role-specific; do not show admin/report controls on public pages.
- Make tables scannable with clear headers, status text, and mobile overflow handling.
- Group forms by user intent, keep labels explicit, and show useful validation/help text.
- Use restrained status colors with text labels; never rely on color alone.
- Explain empty states and provide a next action when one exists.
- Keep invoice total, paid, remaining, due date, and status visually distinct.
- Use cards when they improve grouping, not as a wrapper for every element.
- Avoid excessive gradients, decorative shadows, giant radii, and generic dashboard ornament.

## Copy

- Use Vietnamese-first, natural wording with proper diacritics.
- Prefer concrete actions such as `Ghi nhận thanh toán` and `Xử lý yêu cầu sửa chữa`.
- Avoid vague marketing promises, placeholder text, mixed-language labels, and production-readiness claims.
- Never put credentials, identity data, internal notes, or permission fields in UI copy or screenshots.

## Responsive and Accessibility

- Verify desktop around 1366px and mobile around 390px for affected surfaces.
- Keep touch targets usable and focus states visible.
- Preserve semantic headings, form labels, and keyboard navigation.
- Ensure tables remain usable with horizontal scrolling where necessary.
- Prevent long Vietnamese text, amounts, and status labels from overflowing.
- Maintain readable contrast for text, badges, buttons, and form states.
- Respect reduced-motion preferences if animation is introduced.

## Privacy and Role Safety

- Public pages expose only listing-safe data.
- Owner pages show only owner-scoped data.
- Tenant pages show only tenant-scoped data.
- Never render `citizen_id`, identity files, payment collector internals, auth/permission fields, or private notes on product surfaces.
- Reports remain staff-only.

## UI Definition of Done

- Affected routes render for the correct role and reject the wrong role.
- No raw Django template syntax is visible.
- No sensitive or unrelated owner/tenant data is rendered.
- Desktop and mobile layouts remain usable.
- Existing design tokens and patterns are reused where appropriate.
- Django check and migration dry-run pass.
- A browser or Django Client verification is performed in proportion to the change.
