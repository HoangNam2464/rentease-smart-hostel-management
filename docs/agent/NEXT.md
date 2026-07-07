# RentEase Next

## Immediate iteration

```text
Owner dashboard and navigation vertical slice
```

## Goal

Apply the shared RentEase foundation to the owner's highest-frequency operational surface.

## Scope

- Render the current owner dashboard and navigation with a local demo owner.
- Apply the teal shared tokens, compact operational hierarchy, and consistent icon/control spacing.
- Preserve debt, occupancy, contracts, repairs, viewings, and quick actions as the primary hierarchy.
- Replace hard-coded owner dashboard links with named Django URLs where available.
- Verify desktop/mobile layout, empty data, long text, large amounts, focus, and owner scoping.

## Required evidence

- Reference notes name the exact pattern being learned and its RentEase adaptation.
- Rendered desktop around 1366px and mobile around 390px.
- No owner/tenant privacy regression.
- Django check, migration dry-run, affected tests, and `git diff --check` pass.
- One focused commit and push after the iteration is complete.

## Out of scope

- React migration or importing DreamPOS dependencies
- Copying DreamPOS branding, assets, or POS-specific behavior
- Tenant, reports, admin, runtime language switcher, or bulk translation
- Model, migration, billing, permission, or legacy changes
