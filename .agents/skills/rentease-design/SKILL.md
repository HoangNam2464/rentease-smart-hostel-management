---
name: rentease-design
description: Design, redesign, shape, critique, audit, polish, adapt, harden, or clarify RentEase interfaces in Django templates and CSS. Use for public listings, owner dashboards, tenant portals, reports, admin styling, UX copy, responsive behavior, accessibility, component consistency, and visual QA. Enforces the RentEase design system, Vietnamese product voice, active/legacy boundaries, role privacy, and repository verification rules. Do not use for backend-only tasks.
---

# RentEase Design

Design and refine RentEase as a practical Vietnamese rental-management product. Use project evidence and the canonical design system instead of importing a generic dashboard aesthetic.

## Start Safely

Before editing:

1. Read `AGENTS.md` and `docs/agent/RENTEASE_CURRENT_STATE.md`.
2. Read `docs/ui/RENTEASE_PROFESSIONAL_DESIGN_SYSTEM.md` and `docs/architecture/LEGACY_BOUNDARIES.md`.
3. Inspect the affected template, its loaded CSS, and a representative neighboring surface.
4. Read `docs/agent/RENTEASE_SECURITY_RULES.md` when the surface renders user, tenancy, billing, payment, repair, or identity-related data.
5. Run the Git and Django startup checks required by `AGENTS.md`. Stop if a gate fails.

Read `docs/agent/RENTEASE_PRODUCT_CONTEXT.md` when shaping a new surface or changing user-facing behavior.

## Route The Request

Treat the first word as a mode when it matches this table. Read `references/workflows.md` and follow the matching workflow.

| Mode | Purpose |
|---|---|
| `shape` | Plan hierarchy, interaction, states, and responsive behavior before code |
| `craft` | Shape, implement, and visually verify a complete UI change |
| `critique` | Review usability and visual hierarchy without editing |
| `audit` | Check accessibility, responsiveness, consistency, privacy, and edge cases |
| `polish` | Implement a focused final-quality pass |
| `adapt` | Improve desktop/mobile behavior and content resilience |
| `harden` | Add empty, error, loading, permission, and long-content handling |
| `clarify` | Improve Vietnamese labels, help text, validation, and actions |

Examples:

```text
$rentease-design shape owner invoice detail
$rentease-design critique tenant dashboard
$rentease-design audit public room listing
$rentease-design polish viewing registration form
```

If no mode is named, infer it from the request. Review-only language means `critique` or `audit`; do not edit unless the user asks for implementation.

## Preserve The RentEase Contract

- Public pages should feel like a trustworthy room-listing product.
- Owner pages should optimize frequent small-business operations and scanning.
- Tenant pages should prioritize readable status, payment, contract, and repair information.
- Admin and reports should remain compact, operational, staff-only, and privacy-safe.
- Reuse existing tokens, components, template structure, and Django form behavior before inventing new patterns.
- Keep Vietnamese copy natural, specific, concise, and correctly accented.
- Do not edit legacy HOSTELLO surfaces for normal RentEase work.
- Do not change views, forms, URLs, models, settings, permissions, or business logic during a design-only task without a separately approved plan.
- Never expose citizen identity data, internal permission fields, private notes, or another owner/tenant's data.

## Work In A Visual Loop

1. Identify the user, job, primary action, information hierarchy, and required states.
2. Inspect the current rendered behavior before deciding what to change.
3. Make the smallest coherent template/CSS/copy change when implementation is requested.
4. Render the affected route for the correct role and test wrong-role or anonymous behavior where relevant.
5. Inspect desktop around 1366px and mobile around 390px when layout changes.
6. Check focus, keyboard use, contrast, long Vietnamese text, empty/error states, and overflow.
7. Run Django check, migration dry-run, `git diff --check`, and inspect the final scope.

Use browser inspection when a page can be rendered. Do not claim visual verification from source inspection alone.
