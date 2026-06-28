# UI and Design Work

Load this reference for templates, CSS, UX copy, responsive behavior, screenshots, or visual QA.

## Read Before Editing

- `docs/ui/RENTEASE_PROFESSIONAL_DESIGN_SYSTEM.md`
- `docs/architecture/PROJECT_STRUCTURE_MAP.md`
- The affected template and its loaded CSS

## Active Surfaces

- Public: `frontend/templates/home.html` and `frontend/templates/listings/`
- Owner/tenant: `frontend/templates/portal/`
- Reports: `frontend/templates/reports/`
- Shared design CSS: `frontend/static/css/rentease-design.css`
- Layout/portal CSS: `frontend/static/css/rentease-layout.css`
- Admin CSS: `frontend/static/admin/css/custom_admin.css`

Do not use legacy HOSTELLO templates, CSS, JavaScript, or root `assets/` for normal RentEase UI changes.

## Design Priorities

- Keep Vietnamese copy natural, concrete, and properly accented.
- Preserve the public listing, owner dashboard, tenant portal, and staff/admin distinctions.
- Reuse existing tokens and patterns before creating new ones.
- Keep financial status and actions easy to scan.
- Handle desktop and mobile layouts, long text, empty states, errors, and keyboard focus.
- Avoid generic decoration, excessive cards, gradients, shadows, and oversized radii.

## Privacy

- Render only public-safe data on public pages.
- Preserve owner and tenant scoping.
- Never render citizen identity data/files, auth internals, collector fields, or private notes.

## Verification

- Run both Django checks.
- Render affected routes for the correct role and verify wrong-role behavior.
- Check for raw template syntax and broken static references.
- Inspect desktop and mobile behavior with a browser when layout changed.
- Confirm no sensitive markers appear in rendered output.
