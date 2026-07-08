# RentEase Next

## Immediate iteration

```text
Owner core management (properties, rooms, listings, tenants, contracts) vertical slice
```

## Goal

Apply the shared RentEase foundation to the owner's core management surfaces.

## Scope

- Render the owner properties, rooms, listings, tenants, and contracts lists, detail views, and forms.
- Apply the teal shared tokens, consistent icon/control spacing, and a clean card/list layout.
- Replace legacy classes (`button primary`, `status-badge`) with the standard ones (`btn btn-primary`, `badge badge-...`).
- Ensure consistent data tables, empty states, and action buttons.
- Verify desktop/mobile layout, empty data, long text, and responsive behavior.

## Required evidence

- Reference notes name the exact pattern being learned and its RentEase adaptation.
- Rendered desktop around 1366px and mobile around 390px.
- No cross-tenant privacy regression.
- Django check, migration dry-run, affected tests, and `git diff --check` pass.
- One focused commit and push after the iteration is complete.

## Out of scope

- React migration or importing DreamPOS dependencies
- Copying DreamPOS branding, assets, or POS-specific behavior
- Owner workflows, reports, admin, runtime language switcher, or bulk translation
- Model, migration, billing, permission, or legacy changes
