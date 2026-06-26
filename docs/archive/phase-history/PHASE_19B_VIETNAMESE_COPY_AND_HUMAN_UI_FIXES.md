# Phase 19B: Vietnamese Copy And Human Product UI Fixes

## Browser Issue Found

After Phase 19A, the UI looked more polished, but browser review exposed two important presentation issues:

- Vietnamese user-facing text was written without diacritics.
- The landing page still felt too generic and demo-like in its spacing, hero copy, and right-side panel.

This phase fixes those issues without changing models, migrations, database schema, billing logic, production settings, route behavior, or access control.

## Vietnamese Missing Accent Problem

Examples seen before this phase:

- `Nen tang quan ly nha tro thong minh`
- `Xem phong`
- `Dang nhap`
- `Tu dang phong den thanh toan`
- `Mot luong demo lien mach...`

These were template copy issues, not a font problem.

Fix direction:

- use proper Vietnamese with diacritics in visible product UI
- preserve internal code names, URL names, Django identifiers, and model values
- keep all templates encoded as UTF-8

## AI / Demo-Like Visual Problem

The landing page needed to feel more like a real Vietnamese boarding-house management product.

Problems:

- hero headline was too large
- page had too much empty vertical space
- right-side panel felt generic
- copy sounded artificial
- product value was not specific enough

Fix direction:

- reduce hero size and whitespace
- use more natural Vietnamese copy
- make the right-side card describe a concrete boarding-house workflow
- keep CTA buttons simple and practical
- avoid overusing gradients

## Pages Fixed

### Public

- `/`
- `/rooms/`
- public room detail
- viewing registration form
- viewing registration success page
- `/login/`

### Owner

- owner navigation
- owner dashboard
- rooms
- listings
- tenants
- contracts
- invoices
- repairs
- viewing registrations

### Tenant

- tenant navigation
- tenant dashboard
- invoices
- payments
- repairs
- notifications

### Error

- 404 page
- 500 page

## Copywriting Direction

User-facing text should sound like a practical Vietnamese rental-management tool:

- clear, direct, and human
- not marketing-heavy
- not overly technical
- no unaccented Vietnamese in main RentEase UI
- honest about local-demo status where needed

## UI Direction

Applied UI direction:

- smaller and more balanced hero headline
- tighter page spacing
- more useful right-side workflow card
- realistic workflow wording: đăng phòng, hợp đồng, hóa đơn, thanh toán, sửa chữa
- consistent CTA labels
- cleaner role cards
- maintain responsive layout

## Safety Constraints

Observed constraints:

- no model changes
- no schema changes
- no migrations
- no billing logic changes
- no production settings changes
- no route behavior changes
- no database files committed
- no citizen ID fields/files exposed
- no password/auth/permission fields exposed
- no payment collector internals exposed
- no other-owner or other-tenant data exposed
- no legacy root routes re-added

## Verification Checklist

Required:

- Django check passes
- migration dry-run reports `No changes detected`
- demo seed command succeeds
- public routes load
- owner routes load
- tenant routes load
- reports/admin remain protected for anonymous users
- `/api/requests/` remains 404
- `/fees/` remains 404
- obvious unaccented Vietnamese phrases are not present in main RentEase templates
- no sensitive fields are rendered in public pages
- no raw Django template tags are rendered

## Result

Phase 19B made the UI more human and locally presentable:

- landing page copy is more natural and specific
- main Vietnamese UI labels now use diacritics
- public, owner, tenant, and error pages read more professionally
- the project remains local-demo ready, not production-ready

Recommended next phase:

```text
Phase 19C: Browser Screenshot Review After Vietnamese UI Fix
```
