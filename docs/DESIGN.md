# RentEase Design

This is the canonical source for product UI, reference study, bilingual vocabulary, responsive behavior, accessibility, and visual QA.

## Product character

RentEase should feel like calm, capable rental operations for Vietnam: trustworthy for visitors, efficient for owners, clear for tenants, and compact for staff.

Avoid:

- the old HOSTELLO school-management aesthetic
- generic AI-generated dashboards made from repeated cards
- decorative gradients, excessive shadows, and oversized radii
- luxury real-estate styling that hides operational facts
- copying another product's branding, assets, code, or irrelevant behavior

## Reference-first workflow

Interface work starts with evidence, not invention.

1. Inspect the current rendered RentEase surface.
2. Study the approved reference source or product.
3. Record what is learned: hierarchy, navigation, density, component anatomy, states, responsive behavior, and interaction feedback.
4. State what will be adapted, rejected, or changed for RentEase.
5. Implement the smallest complete workflow slice.
6. Render and inspect desktop around 1366px and mobile around 390px.
7. Check long EN/VI copy, keyboard use, focus, contrast, overflow, empty/error states, and role privacy.

DreamPOS is approved for learning admin shell, navigation, cards, tables, forms, badges, spacing, and dense operational layouts. Buildium/AppFolio may inform property-management workflows. Neither is a source for copied code or branding.

### Applied foundation: 2026-07-07

- Learned from DreamPOS: fixed 260px operational sidebar, grouped navigation, compact topbar, scannable status treatments, and dense table/form spacing.
- Adapted for RentEase: teal brand, calmer shadows, visible borders, property-management vocabulary, role-specific navigation, and privacy-safe content.
- Rejected: purple DreamPOS branding, POS modules, frontend dependencies, copied assets, decorative theme controls, and generic card-heavy dashboards.
- Shared implementation source: `frontend/static/css/rentease-tokens.css`.

## Visual identity

Use one RentEase identity across public and authenticated surfaces.

| Role | Token |
|---|---|
| Primary | `#0f766e` |
| Primary dark | `#0b5f59` |
| Primary soft | `#dff3ef` |
| Accent | `#2563eb` |
| Page background | `#f4f6f5` |
| Surface | `#ffffff` |
| Heading | `#0f2433` |
| Body text | `#17212b` |
| Muted text | `#627386` |
| Border | `#dce5e2` |
| Success | `#15803d` |
| Warning | `#b7791f` |
| Danger | `#c24135` |

- Use Inter with system fallbacks.
- Prefer an 8px spacing rhythm.
- Use restrained 8-16px radii according to component size.
- Shadows communicate elevation, not decoration.
- Color never replaces a visible text status.

## Surface rules

### Public

- Lead with finding and evaluating a room.
- Show price, location-safe context, area, capacity, availability, and one clear viewing action.
- Never expose exact private address, identity data, internal notes, or owner-only operations.

### Owner

- Prioritize money due, occupancy, expiring contracts, repairs, viewings, and frequent actions.
- Use dense, scannable tables and attention lists where they outperform cards.
- Keep financial totals, dates, and statuses visually distinct.

### Tenant

- Prioritize amount due, due date, payment state, current contract, repairs, and unread notices.
- Explain financial and workflow status in plain language.

### Reports and admin

- Stay compact, operational, searchable, and staff-only.
- Preserve all sensitive-data restrictions in `docs/SECURITY.md`.

## Shared components

Reuse shared tokens and patterns before adding page-specific CSS.

- App shell: sidebar, topbar, breadcrumbs, account controls
- Page header: title, supporting copy, one primary action
- Buttons: primary, secondary, ghost, danger
- Forms: explicit labels, help, validation, grouped intent
- Tables/lists: filters, status text, row action, responsive overflow
- Cards: only when grouping materially improves comprehension
- Status badge: semantic color plus translated label
- Feedback: loading, empty, error, success, and denied states

Do not put page-specific style blocks in templates once a shared pattern exists. Move interactive shell behavior to static JavaScript rather than growing inline scripts.

## Language architecture

### Code vocabulary

Code is English-only and follows `AGENTS.md`. Business status values remain stable internal codes and are translated only at presentation time.

### Interface vocabulary

English is the gettext source language. Vietnamese translations must be natural, concise, and correctly accented.

| Concept/code | English UI | Vietnamese UI |
|---|---|---|
| `property` | Property | CÆ¡ sá»Ÿ cho thuÃª |
| `room` | Room | PhÃ²ng trá» |
| `listing` | Listing | Tin Ä‘Äƒng |
| `tenant` | Tenant | KhÃ¡ch thuÃª |
| `contract` | Contract | Há»£p Ä‘á»“ng |
| `invoice` | Invoice | HÃ³a Ä‘Æ¡n |
| `payment` | Payment | Thanh toÃ¡n |
| `repair_request` | Repair request | YÃªu cáº§u sá»­a chá»¯a |
| `viewing_registration` | Viewing request | Lá»‹ch xem phÃ²ng |
| `dashboard` | Overview | Tá»•ng quan |
| `amount_due` | Amount due | Sá»‘ tiá»n cáº§n thanh toÃ¡n |
| `due_date` | Due date | Háº¡n thanh toÃ¡n |
| `available` | Available | CÃ²n phÃ²ng |
| `occupied` | Occupied | Äang thuÃª |
| `overdue` | Overdue | QuÃ¡ háº¡n |
| `save` | Save | LÆ°u |
| `cancel` | Cancel | Há»§y |
| `search` | Search | TÃ¬m kiáº¿m |
| `filter` | Filter | Bá»™ lá»c |

Add terms here before introducing competing translations. Do not translate brand names, `VND`, `mÂ²`, email addresses, or standard technical units.

### Display rule

- A page renders either English or Vietnamese, never both at once.
- Navigation, headings, form labels, placeholders, validation, messages, statuses, dates, and accessibility labels follow the active locale.
- Dynamic user-entered content is not automatically translated.
- Do not concatenate translated fragments; translate complete messages with placeholders.

## Responsive and accessibility

- Desktop target: about 1366px; mobile target: about 390px.
- Use fluid grids, wrapping, and `minmax(0, 1fr)` before adding breakpoints.
- Keep touch targets usable and focus indicators visible.
- Preserve semantic headings, labels, keyboard order, reduced motion, and readable contrast.
- Test long English and Vietnamese labels, large currency values, and empty data.
- Tables may scroll horizontally when a card transformation would hide operational context.

## Definition of done

- Reference notes explain the adapted patterns.
- The correct role can use the workflow and the wrong role is rejected.
- No sensitive or cross-owner/cross-tenant data is rendered.
- No raw template syntax, broken asset, overflow, or mixed-language UI appears.
- Desktop and mobile are visually inspected from the current build.
- Django check, migration dry-run, affected tests, and `git diff --check` pass.
