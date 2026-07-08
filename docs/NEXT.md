# RentEase Next

## Immediate iteration

```text
Tenant dashboard and navigation vertical slice
```

## Goal

Apply the shared RentEase foundation to the tenant's primary operational surface.

## Scope

- Render the current tenant dashboard and navigation with a local demo tenant.
- Apply the teal shared tokens, consistent icon/control spacing, and a clean card/list layout.
- Prioritize amount due, due date, payment state, current contract, repairs, and unread notices.
- Explain financial and workflow status in plain language.
- Verify desktop/mobile layout, empty data, long text, large amounts, focus, and tenant scoping.

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
