# RentEase Next

## Immediate iteration

```text
Reference-first design foundation
```

## Goal

Stabilize the shared interface language before redesigning more screens.

## Scope

- Audit DreamPOS and other approved property-management references for reusable layout and interaction patterns.
- Choose one RentEase visual identity and reconcile public/portal token differences.
- Define shared shell, navigation, button, form, table, badge, card, empty-state, and responsive patterns.
- Define the EN/VI terminology matrix for those components without enabling runtime i18n yet.
- Select one representative owner page and one tenant page for the first vertical slice.

## Required evidence

- Reference notes name the exact pattern being learned and its RentEase adaptation.
- Rendered desktop around 1366px and mobile around 390px.
- No owner/tenant privacy regression.
- Django check, migration dry-run, affected tests, and `git diff --check` pass.
- One focused commit and push after the iteration is complete.

## Out of scope

- React migration or importing DreamPOS dependencies
- Copying DreamPOS branding, assets, or POS-specific behavior
- Runtime language switcher or bulk translation; that is the final UI phase
- Model, migration, billing, permission, or legacy changes
