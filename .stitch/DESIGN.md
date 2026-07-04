---
name: RentEase Calm Operations
colors:
  background: '#F5F7F6'
  surface: '#FFFFFF'
  surface-subtle: '#EEF2F0'
  surface-strong: '#E4EBE8'
  on-surface: '#16221F'
  on-surface-muted: '#62706B'
  outline: '#DCE4E0'
  outline-strong: '#BCCBC5'
  primary: '#0F766E'
  on-primary: '#FFFFFF'
  primary-hover: '#0B5F59'
  primary-soft: '#DCF1ED'
  sidebar: '#182522'
  on-sidebar: '#D5E1DD'
  on-sidebar-muted: '#91A39D'
  success: '#18794E'
  success-soft: '#E4F5EA'
  warning: '#A15C00'
  warning-soft: '#FFF1D6'
  error: '#B42318'
  error-soft: '#FDE8E7'
  info: '#3D5A80'
  info-soft: '#E8EEF6'
typography:
  display-lg:
    fontFamily: Geist
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.035em
  headline-lg:
    fontFamily: Geist
    fontSize: 30px
    fontWeight: '700'
    lineHeight: 38px
    letterSpacing: -0.025em
  headline-md:
    fontFamily: Geist
    fontSize: 22px
    fontWeight: '650'
    lineHeight: 30px
    letterSpacing: -0.015em
  title-sm:
    fontFamily: Geist
    fontSize: 17px
    fontWeight: '650'
    lineHeight: 24px
    letterSpacing: -0.005em
  body-base:
    fontFamily: Geist
    fontSize: 15px
    fontWeight: '400'
    lineHeight: 24px
    letterSpacing: '0'
  body-public:
    fontFamily: Geist
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 26px
    letterSpacing: '0'
  label:
    fontFamily: Geist
    fontSize: 13px
    fontWeight: '600'
    lineHeight: 18px
    letterSpacing: 0.01em
  numeric:
    fontFamily: Geist Mono
    fontSize: 15px
    fontWeight: '600'
    lineHeight: 22px
    letterSpacing: -0.01em
rounded:
  sm: 0.5rem
  DEFAULT: 0.625rem
  md: 0.75rem
  lg: 1rem
  full: 9999px
spacing:
  unit: 4px
  xs: 4px
  sm: 8px
  md: 12px
  lg: 16px
  xl: 24px
  2xl: 32px
  3xl: 48px
  gutter-mobile: 16px
  gutter-tablet: 24px
  gutter-desktop: 32px
---

# Design System: RentEase Calm Operations

## 1. Visual Theme & Atmosphere

RentEase is a calm operations workspace for Vietnamese rental rooms. It should feel like a well-run property desk: clear, grounded, compact enough for daily work, and warm enough for tenants and room seekers. The design is practical rather than technology-led. Information hierarchy, status clarity, and action confidence matter more than decoration.

Use a balanced operational density of 6/10, low layout variance of 3/10, and restrained motion of 2/10. Public pages may breathe more; owner pages prioritize scan speed; tenant pages reduce choices and foreground obligations; reports stay compact. Avoid generic card grids, luxury real-estate styling, banking severity, school-management visuals, neon gradients, glass effects, and decorative dashboard metrics.

The current teal identity remains the single interactive accent. Cool green-gray neutrals unify public and authenticated surfaces. Blue is no longer a competing CTA color; it is reserved for informational status when teal, success, warning, or error would be semantically wrong.

## 2. Color Palette & Roles

### Primary Foundation

- **Operations Canvas** (`#F5F7F6`) — default page background; quiet contrast against white working surfaces.
- **Working Surface** (`#FFFFFF`) — forms, tables, side panels, dialogs, and primary content regions.
- **Subtle Surface** (`#EEF2F0`) — grouped rows, filters, empty states, and noninteractive emphasis.
- **Strong Surface** (`#E4EBE8`) — selected neutral states and stronger structural separation.
- **Quiet Outline** (`#DCE4E0`) — default 1px borders and dividers.
- **Strong Outline** (`#BCCBC5`) — hover borders and high-priority separation.

### Accent & Interactive

- **RentEase Teal** (`#0F766E`) — the only general interactive accent: primary actions, links, focus rings, and active navigation.
- **Deep Teal** (`#0B5F59`) — hover and pressed state for primary actions.
- **Teal Wash** (`#DCF1ED`) — selected rows, active navigation background, and low-emphasis teal tags.
- **Night Green Sidebar** (`#182522`) — owner and tenant desktop navigation shell.
- **Sidebar Text** (`#D5E1DD`) — primary labels on the dark sidebar.
- **Sidebar Muted** (`#91A39D`) — navigation group labels and role metadata.

Do not use teal and blue as equal CTA colors. Do not use gradients for buttons, brand marks, avatars, or status surfaces.

### Typography & Text Hierarchy

- **Near-Black Ink** (`#16221F`) — headings, primary data, table values, and form labels.
- **Muted Eucalyptus** (`#62706B`) — helper text, metadata, secondary navigation, and descriptions.
- Text on colored surfaces must use an explicitly paired on-color token; never rely on opacity alone for essential information.

### Functional States

- **Settled Green** (`#18794E`) and **Settled Green Wash** (`#E4F5EA`) — paid, completed, active, published.
- **Attention Amber** (`#A15C00`) and **Attention Amber Wash** (`#FFF1D6`) — partial, pending, due soon, awaiting action.
- **Action Red** (`#B42318`) and **Action Red Wash** (`#FDE8E7`) — overdue, failed, rejected, destructive actions.
- **Information Slate** (`#3D5A80`) and **Information Slate Wash** (`#E8EEF6`) — neutral informational notices only.
- Every state must include a Vietnamese text label. Color never carries status alone.

## 3. Typography Rules

### Family and Character

- **Primary:** Geist — clean, compact, and neutral enough for operational screens while remaining less generic than the current Inter treatment.
- **Numeric:** Geist Mono — currency, meter values, dates in dense tables, invoice totals, and report figures.
- **Fallback:** `"Segoe UI", Arial, sans-serif` until Geist is locally or reliably loaded.
- Verify Vietnamese diacritics at all supported weights before implementation. If a chosen webfont build lacks full Vietnamese coverage, keep the system fallback rather than mixing glyph sources.
- Do not mix decorative serif faces into dashboards, reports, forms, or listings.

### Hierarchy & Weights

- Public display: `clamp(2.25rem, 4.5vw, 3rem)`, weight 700, line-height 1.15; one per page.
- Portal page title: 30px/38px on desktop, 26px/34px on mobile, weight 700.
- Section title: 22px/30px, weight 650.
- Card or panel title: 17px/24px, weight 650.
- Body: 15px/24px in portals; 16px/26px on public reading surfaces.
- Label: 13px/18px, weight 600. Use sentence case; do not uppercase ordinary Vietnamese labels.
- Table header: 12px/18px, weight 650. Sentence case is preferred over all-caps tracking.
- Currency and operational figures: numeric face, tabular numerals, weight 600–700.
- Body copy should stay below 65 characters per line where it is intended to be read as prose.

### Spacing Principles

- Use a strict 4px base with an 8px working rhythm.
- Text-to-related-content gap: 4–8px.
- Control-to-control gap: 8–12px.
- Card padding: 16px compact, 20–24px default.
- Section gap: 24px portal, 32–48px public.
- Page gutters: 16px mobile, 24px tablet, 32px desktop.
- Do not create one-off gaps unless content density or accessibility requires them.

## 4. Component Stylings

### Buttons

- Minimum visible height and touch target: 44px. Compact table actions may appear 36px high only when their hit area remains at least 44px.
- Default radius: 10px. Use pill shapes only for filters, tags, and status—not for every action.
- Primary: solid RentEase Teal, white label, no gradient, no glow.
- Secondary: white surface, strong outline, near-black label.
- Ghost: transparent, muted label; teal only on hover/focus.
- Destructive: Action Red is used only for an explicit destructive action.
- Active feedback: translate down 1px or reduce shadow; do not lift routine controls on hover.
- Use one primary action per page header or form action row. Preserve the existing action order and Django URL behavior.
- All interactive states require visible `:focus-visible` treatment with a 3px teal ring and 2px offset.

### Cards & Operational Containers

- Use cards only when a boundary communicates grouping. Do not wrap every section in an elevated rectangle.
- Default container: white surface, 1px Quiet Outline, 12px radius, no shadow.
- Elevated container: 16px radius with one subtle, background-tinted shadow; reserve for sticky summaries or modal layers.
- Static cards do not animate on hover. Clickable cards may change border and background without vertical movement.
- Public room cards use a consistent image ratio, then price, availability, title, safe Property location, and one clear action.
- Empty states use a subtle surface, concise explanation, and a real next action when one exists. Never fabricate data to fill an empty state.

### Navigation

- Desktop portal sidebar: 240–252px fixed width, Night Green Sidebar background, grouped by user job rather than model names.
- Owner priority: Overview; Properties and Rooms; Tenants and Contracts; Invoices and Payments; Repairs and Viewings.
- Tenant priority: Overview; Invoices and Payments; Contract; Repairs; Notifications; Profile.
- Active item uses Teal Wash on dark-neutral adaptation, a 3px teal indicator, strong text, and `aria-current="page"`.
- Group labels are sentence case, 12px/16px, not heavily tracked all-caps.
- User identity is informational. Logout must be a semantic button/form action, never a clickable `div`.
- Public navigation is shared by home and listing pages and exposes only Home, Find a room, and Login/account state.
- Mobile portal navigation becomes an off-canvas drawer with a visible scrim, close control, Escape handling, focus containment, and body scroll lock. Do not leave it as a transform-only panel.

### Inputs & Forms

- Keep labels above controls for public/mobile forms and use the existing aligned two-column label layout only for wide owner forms where scanning benefits.
- Input minimum height: 44px; radius: 10px; border: Strong Outline; white surface.
- Label above or beside; optional help below; error immediately below the related field.
- Required state must be conveyed in text, not only with color or an asterisk.
- Group long forms by intent with headings and short help text. Do not introduce wizard behavior without a separate product decision.
- Keep CSRF tokens, Django field rendering, validation lists, context variables, and existing permissions intact.
- Form actions become stacked full-width buttons below 430px; destructive actions remain visually separated.

### Tables

- Use tables for comparison and operational scanning, not as a default container for every list.
- Header uses Subtle Surface, sentence-case labels, 12px/18px type, and a 1px bottom divider.
- Rows are 48–56px high with 12–16px horizontal padding.
- Currency and numeric values align right and use tabular numerals. Status and actions align consistently by table type.
- Row hover uses a subtle background only. Links remain teal and underlined on hover/focus.
- On small screens, preserve semantic tables inside a labeled horizontal scroll region. Provide an overflow cue; do not hide critical columns without a task-specific decision.
- Repeated action links become consistent compact buttons or a single disclosed action menu in a later, separately tested phase.

### Status, Alerts, and Feedback

- Badges use 8px radius rather than full pills by default, semantic soft fill, and text labels.
- Alerts contain a clear outcome, the affected object when safe, and the next available action.
- Loading states should match the dimensions of their final content. Avoid generic full-page spinners.
- Success feedback may auto-dismiss only if the same outcome remains visible in page state.

## 5. Layout Principles

### Base Layout

- Keep the existing Django template inheritance and role checks. Consolidate repeated public chrome into the existing public base before introducing new page shells.
- Portal shell: fixed desktop sidebar, sticky top bar, fluid working canvas, and a constrained inner content region.
- Public shell: centered max-width 1180px with asymmetric editorial sections and clear listing actions.
- Owner content max-width: 1440px for dense operations. Tenant content max-width: 1120px for simpler reading. Reports max-width: 1280px.
- Use CSS Grid for page-level structure and Flexbox for one-dimensional control groups.
- Use `min-height: 100dvh` with a safe `100vh` fallback for full-height shells.

### Whitespace Strategy

- Public pages: 48–64px between major sections, with 24–32px inside grouped content.
- Owner pages: 24px between page sections and 16px between operational groups.
- Tenant pages: 24–32px between financial/status sections, with fewer simultaneous panels than owner pages.
- Reports: 16–24px gaps and restrained card usage to support dense scanning.

### Alignment & Visual Balance

- Left-align operational content and form copy. Center only short empty/error states.
- Page headers use title and support copy on the left, one primary action on the right.
- Financial summaries prioritize remaining balance, due state, and next action; totals and paid amounts remain visible but subordinate.
- Public listing cards maintain consistent media ratios and avoid large decorative imagery that pushes rental facts below the fold.

### Responsive Behavior & Touch

- `>= 1200px`: full sidebar, wide operational layouts, constrained content width.
- `992–1199px`: full sidebar; four-column metrics reduce to two; split details may collapse.
- `768–991px`: sidebar becomes drawer; page grids reduce to one or two columns based on content.
- `< 768px`: all composed multi-column layouts collapse to one column; no page-level horizontal scrolling.
- `< 430px`: form actions and page-header actions stack; navigation labels remain readable; primary controls span the available width where appropriate.
- Minimum touch target: 44px. Do not use 30–38px controls as the only target.
- Verify at 1366px desktop and 390px mobile. Test long Vietnamese names, large VND values, multi-line statuses, validation errors, and empty tables.

## 6. Motion & Interaction

- Motion is functional and restrained: 120–180ms for color, border, opacity, and small transform changes.
- Animate only `transform` and `opacity`; never animate layout dimensions for routine interaction.
- No perpetual decorative motion, pulsing metrics, parallax, shimmer outside active loading states, or cascade animation on operational tables.
- Provide `prefers-reduced-motion: reduce` rules that remove nonessential transitions and smooth scrolling.
- Keyboard focus, drawer state, validation feedback, and success messages take priority over animation.

## 7. Current-State UI Audit

### Confirmed Source Problems

1. **Competing design systems:** `rentease-design.css` and `rentease-layout.css` define overlapping teal, blue, surface, text, card, radius, button, table, and form tokens under different names. Public and portal pages therefore drift even when they intend to express the same component.
2. **Append-only cascade:** phase-specific blocks repeatedly redefine `.button`, `.card`, `.data-table`, `.form-field`, `.info-list`, `.empty-state`, and responsive layouts. Final appearance depends on source order instead of one component contract.
3. **Undefined token:** owner CRUD styles reference `--re-card`, but that custom property is not declared in the active public stylesheet. The browser falls back to a transparent background for those declarations.
4. **Navigation divergence:** home and public listing pages duplicate header markup, while the portal base mixes `{% url %}` with hard-coded paths and path-substring active checks. Active links do not expose `aria-current`.
5. **Nonsemantic account actions:** sidebar and topbar logout behavior is attached to clickable `div` elements with inline JavaScript. These controls are not reliably keyboard-operable or announced as buttons.
6. **Touch targets are inconsistent:** portal buttons, topbar controls, table actions, report filters, and public navigation include 30–42px controls, below the 44px target.
7. **Mobile drawer is incomplete:** the sidebar translates on and off screen but has no scrim, close button, focus containment, Escape behavior, or body scroll lock.
8. **Viewport and motion gaps:** full-height shells use `100vh`, and active styles provide no reduced-motion rules.
9. **Typography is generic and externally dependent:** both active stylesheets import Inter from Google Fonts, while Bootstrap Icons are loaded from a CDN. Local/demo rendering can change when external assets are unavailable.
10. **Reports are visually isolated:** report components are embedded in a template-level `<style>` block on top of Django Admin, producing another token and component layer rather than reusing the active system.
11. **Table scanning is inconsistent:** public and portal styles assign different minimum widths and link treatments. Mobile relies on overflow, but scroll regions have no visible cue or accessible label contract.
12. **Forms lack one canonical anatomy:** public fields, portal fields, filter fields, and report filters use different heights, label alignment, border tokens, error presentation, and focus behavior.

### Unverified Risks

- Visual behavior with real data, authenticated role navigation, keyboard focus order, drawer interaction, and exact contrast were not rendered in this planning step because no in-app browser surface was available.
- CDN font/icon failure behavior and long-content overflow require browser verification in the implementation phase.

## 8. Redesign Plan Before Template Changes

### Phase 1 — Foundation and Base Shell

- Consolidate shared tokens and component primitives without changing models, views, forms, URLs, permissions, or context data.
- Refine `portal/base.html` and `rentease-layout.css` as one vertical slice: semantic logout, URL-tag reuse, active state semantics, 44px targets, complete mobile drawer behavior, `100dvh`, and reduced motion.
- Keep all existing role conditions, badges, CSRF behavior, and navigation destinations.
- Verify owner, tenant, staff, wrong-role, anonymous, 1366px, and 390px states.

### Phase 2 — Public Shell and Listings

- Make home reuse the public navigation contract and eliminate duplicated chrome while preserving existing listing URLs and template logic.
- Normalize typography, room-card hierarchy, filters, buttons, and listing detail summary.
- Verify public-safe Property data only; never expose exact private addresses or identity data.

### Phase 3 — Owner Operational Components

- Apply the system to one representative list, detail, and form first, recommended: rooms.
- Validate table density, form anatomy, empty/error states, and responsive behavior before propagating classes to properties, tenants, contracts, invoices, repairs, listings, payments, and viewings.
- Preserve every existing `{% url %}`, context variable, form field, permission check, and workflow action.

### Phase 4 — Tenant Financial and Support Flows

- Prioritize invoice status, remaining balance, payment history, contract dates, repairs, and notifications.
- Reduce owner-style density and remove actions tenants cannot perform.
- Re-test tenant-only scoping and ensure payment collector/internal fields remain hidden.

### Phase 5 — Reports and Admin Alignment

- Move report presentation from inline template CSS into a staff-only reusable stylesheet contract.
- Align report navigation, filters, tables, and status colors while retaining Django Admin structure and staff permissions.
- Treat legacy HOSTELLO admin/templates as out of scope.

### Approval Boundary

This document authorizes no backend, model, migration, permission, billing, settings, or business-logic change. Each implementation phase should remain a small, reviewable template/CSS slice with route and role verification before broader propagation.

## 9. Design System Notes for Stitch Generation

### Language to Use

Use: calm Vietnamese rental operations, grounded green-gray palette, compact small-business workspace, clear financial hierarchy, restrained borders, sentence-case labels, strong table scanning, human-written Vietnamese copy, asymmetric but predictable public layouts.

Avoid: generic SaaS dashboard, repeated metric-card wall, neon blue or purple, gradient CTAs, glassmorphism, giant radii, luxury property marketplace, school administration, fake analytics, fabricated names, fake currency values, or placeholder statistics.

### Color References

- RentEase Teal `#0F766E` for actions, links, focus, and active navigation.
- Operations Canvas `#F5F7F6` and Working Surface `#FFFFFF` for the application foundation.
- Near-Black Ink `#16221F` and Muted Eucalyptus `#62706B` for hierarchy.
- Night Green Sidebar `#182522` for authenticated desktop navigation.
- Functional colors are semantic only and always paired with text labels.

### Component Prompts

- “Design an owner rental-room operations shell using the existing role-specific navigation. Use a 248px night-green sidebar, a white sticky topbar, a calm green-gray canvas, one teal primary action, 44px controls, restrained 12px containers, and a dense but readable room table. Use only `[existing context data]`; do not invent metrics or records.”
- “Design a tenant invoice page that foregrounds `[remaining amount]`, `[due state]`, and `[next available action]`, then shows total, paid amount, contract, room, and payment history. Use semantic labeled states, Geist typography, tabular numerals, and a single-column mobile layout.”
- “Design a public room-listing page with a shared RentEase header, practical filters, consistent 16:10 room media, price and availability first, public-safe Property location, and one viewing action. Do not show exact private addresses or fabricated listings.”

### Incremental Iteration

- Generate and review one shell or one representative CRUD flow at a time.
- Keep Django template logic as fixed implementation constraints in every prompt.
- Compare each output against this document before adopting any new token or component.
- Reject outputs that invent data, add unauthorized actions, expose private fields, or require backend changes.

## 10. Anti-Patterns (Banned)

- No emojis as interface icons.
- No pure black, neon accent, outer glow, or oversaturated gradient.
- No Inter as the target design font; keep the current fallback only until a verified typography phase.
- No generic serif fonts in product surfaces.
- No three-equal-card feature wall as the default dashboard composition.
- No card wrapper around every section.
- No giant radii or pill buttons for ordinary actions.
- No overlapping content or absolute-positioned layout decoration.
- No custom cursor, parallax, decorative perpetual motion, or animated operational metrics.
- No AI copy clichés, fake names, fake round numbers, fake performance claims, or fabricated dashboard data.
- No hard-coded user, invoice, contract, room, payment, repair, or report data.
- No removal or rewriting of Django URL tags, static tags, blocks, context variables, forms, CSRF tokens, or permission checks.
