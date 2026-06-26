# RentEase Professional Design System

## Product Identity

RentEase is a Vietnamese boarding-house management platform for:

- people looking for rooms
- landlords and owners
- tenants
- staff and admins

RentEase should feel like a practical management product for small rental operations, not a generic student demo.

## UI Goal

The interface should feel:

- trustworthy
- practical
- Vietnamese-first
- clean
- business-ready
- human-written
- consistent across public, owner, tenant, reports, and error pages

The UI must not feel AI-generated, overly decorative, or like a temporary template.

## Visual Style

Use:

- warm neutral background
- deep teal primary color
- restrained blue accent
- soft white surfaces
- clear page hierarchy
- compact but readable spacing
- clean dashboard cards
- readable tables
- predictable forms
- professional status badges

Avoid:

- oversized hero text
- excessive blank space
- too many gradients
- random colors
- mixed English/Vietnamese labels
- placeholder wording
- unaccented Vietnamese
- public pages that look like admin pages

## Core Tokens

Primary color:

```text
#0f766e
```

Primary dark:

```text
#0b5f59
```

Accent:

```text
#2563eb
```

Background:

```text
#f4f6f5
```

Surface:

```text
#ffffff
```

Main text:

```text
#17212b
```

Muted text:

```text
#627386
```

Border:

```text
#dce5e2
```

## Component Rules

Header and navbar:

- use the RentEase brand mark consistently
- keep links short and Vietnamese-first
- foreground public room browsing and login
- show admin/report links only where appropriate

Hero section:

- balanced headline size
- natural Vietnamese copy
- clear primary CTA
- practical workflow preview
- no unnecessary full-screen blank area

CTA buttons:

- primary actions use teal
- secondary actions stay white or subtle
- labels must describe concrete actions

Feature cards:

- explain real boarding-house workflows
- avoid vague claims
- keep copy short and useful

Role cards:

- public visitors, owners, and tenants should each have clear value
- avoid mixing role responsibilities

Room cards:

- show room title, public-safe room metadata, available date, and price
- use clear detail CTA
- do not expose private owner, contract, invoice, or tenant data

Dashboard metric cards:

- use short labels
- group related metrics
- avoid making all metrics visually equal when a section needs context

Tables:

- wrap horizontally on small screens
- use clear headers
- preserve readable row spacing

Forms:

- use clear labels
- keep help text concise
- avoid exposing protected internal fields

Badges:

- use rounded status pills
- keep colors restrained
- rely on text, not color alone

Alerts and empty states:

- explain what happened
- tell the user what to do next when useful
- do not show technical internals

Sidebars and role navigation:

- keep role navigation compact
- separate owner and tenant navigation
- avoid showing tenant navigation to anonymous users

Detail pages:

- use information grids
- group actions at the bottom
- keep labels Vietnamese-first

Error pages:

- keep RentEase branding
- use helpful text
- provide a path back to the home page

## Copywriting Rules

Use Vietnamese-first, natural wording.

Prefer:

- Quáº£n lÃ½ nhÃ  trá» dá»… dÃ ng hÆ¡n
- Theo dÃµi phÃ²ng, há»£p Ä‘á»“ng, hÃ³a Ä‘Æ¡n vÃ  sá»­a chá»¯a trong má»™t nÆ¡i
- DÃ nh cho chá»§ trá», khÃ¡ch thuÃª vÃ  ngÆ°á»i Ä‘ang tÃ¬m phÃ²ng
- Xem phÃ²ng Ä‘ang cho thuÃª
- ÄÄƒng nháº­p há»‡ thá»‘ng
- Ghi nháº­n thanh toÃ¡n
- Xá»­ lÃ½ yÃªu cáº§u sá»­a chá»¯a

Avoid:

- English labels on user-facing pages
- unaccented Vietnamese
- machine-like phrases
- vague all-in-one promises
- claims that imply production readiness

## Implementation Notes

The shared design system is implemented in:

```text
frontend/static/css/rentease-design.css
```

The main public and portal templates load this CSS through Django static files.

The design system is local-demo oriented. It improves presentation quality but does not make RentEase production-ready.
