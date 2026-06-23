# Phase 20B: Template Reference UI Direction

## Why This Phase Is Needed

Phase 20A made RentEase more coherent, but the UI still needs a reference-led direction before another redesign pass.

The goal of Phase 20B is to stop guessing and define a practical visual direction based on real-world template patterns:

- public pages should feel like a Vietnamese room-rental / property listing website
- owner and tenant pages should feel like a SaaS management dashboard
- future UI work should adapt patterns, not blindly copy external HTML, CSS, images, icons, or assets

This phase does not change application behavior, models, routes, schema, billing logic, or production settings.

## Internet Access Result

Internet access was partially available.

Accessible:

- AdminLTE homepage and feature/license information
- CoreUI Bootstrap page
- Tabler admin template page
- ThemeWagon homepage/category information
- Colorlib real estate template category
- Colorlib real estate theme article
- Start Bootstrap pages, although the fetched content was mostly image-only/minimal in the tool

Partially inaccessible:

- the exact ThemeWagon Property template URL could not be opened by the tool
- the exact BootstrapMade RealEstate template URL could not be opened by the tool
- the exact Colorlib free real estate templates URL failed, but the current Colorlib real estate category was accessible

Because of this, the next implementation phase should use these references as visual inspiration only and should not copy source files or external assets.

## Reference Links Reviewed

### ThemeWagon Property Template

URL:

```text
https://themewagon.com/themes/free-bootstrap-5-html5-real-estate-website-template-property/
```

Type:

- public real-estate/property website reference

Access result:

- exact URL could not be opened by the tool
- ThemeWagon homepage was accessible and confirms the site is a template marketplace with free and premium templates

Useful design ideas:

- property-focused landing page
- strong preview cards
- clear CTA buttons
- template marketplace style with polished card presentation

Adapt for RentEase:

- public room cards
- homepage feature/role sections
- property-style detail blocks

Do not copy:

- template source code
- images
- paid assets
- bundled CSS/JS

License / asset caution:

- treat the specific template as unverified until the user provides screenshots or a downloaded license-safe package

### BootstrapMade RealEstate Template

URL:

```text
https://bootstrapmade.com/real-estate-bootstrap-template/
```

Type:

- public real-estate Bootstrap template reference

Access result:

- exact URL could not be opened by the tool
- BootstrapMade homepage was accessible as a Bootstrap template collection

Useful design ideas:

- clean Bootstrap real-estate layout
- hero area with search/contact emphasis
- property cards
- agent/contact-style CTA areas

Adapt for RentEase:

- public landing structure
- room listing cards
- detail page layout
- viewing registration CTA

Do not copy:

- template assets
- source code
- licensed imagery

License / asset caution:

- verify the specific template license before using any downloaded files

### Colorlib Real Estate Templates

URL requested:

```text
https://colorlib.com/wp/free-real-estate-website-templates/
```

Accessible related URL:

```text
https://colorlib.com/wp/cat/real-estate/
```

Type:

- real-estate website template collection

Useful design ideas:

- grid and list layouts for property browsing
- filters and property metadata
- image-led property cards
- room/property detail pages
- contact/scheduling forms
- responsive property listing patterns

Adapt for RentEase:

- `/rooms/` as property listing grid
- room detail as property detail page
- viewing registration as contact/scheduling form
- homepage as property listing entry point

Do not copy:

- specific images
- demo property content
- template source files

License / asset caution:

- use layout ideas only unless a template is downloaded and license-checked

### Start Bootstrap Landing Page Templates

URL:

```text
https://startbootstrap.com/templates/landing-pages
```

Type:

- general Bootstrap landing page reference

Access result:

- page opened, but fetched content was mostly image-only/minimal

Useful design ideas:

- simple hero section
- compact CTA blocks
- feature rows
- clean Bootstrap spacing

Adapt for RentEase:

- homepage section rhythm
- final CTA
- public login entry point

Do not copy:

- template source code unless license is explicitly verified
- generic marketing copy

License / asset caution:

- use as layout inspiration only

### AdminLTE

URL:

```text
https://adminlte.io/
```

Type:

- admin dashboard / control panel reference

Useful design ideas:

- sidebar dashboard layout
- KPI cards
- reusable tables and forms
- notification/status components
- role-based internal navigation

Adapt for RentEase:

- owner portal dashboard
- owner management tables
- invoice/payment cards
- repair and viewing-registration process screens

Do not copy:

- full AdminLTE package
- plugins not needed for MVP
- complex charting dependencies

License / asset caution:

- AdminLTE is open source / MIT, but RentEase should still use local custom CSS rather than importing the full package blindly

### Start Bootstrap SB Admin

URL:

```text
https://startbootstrap.com/template/sb-admin
```

Type:

- Bootstrap dashboard reference

Access result:

- page opened, but fetched content was minimal

Useful design ideas:

- lightweight admin layout
- simple card metrics
- tables in dashboard pages
- predictable page headings

Adapt for RentEase:

- owner list pages
- reports pages
- small admin-style tables

Do not copy:

- complete template package
- source CSS without checking license and fit

### Start Bootstrap SB Admin 2

URL:

```text
https://startbootstrap.com/theme/sb-admin-2
```

Type:

- dashboard theme reference

Access result:

- page opened, but fetched content was minimal

Useful design ideas:

- metric cards
- grouped dashboard widgets
- compact admin navigation

Adapt for RentEase:

- owner dashboard sections
- tenant dashboard summary cards

Do not copy:

- theme code or assets blindly

### CoreUI Bootstrap

URL:

```text
https://coreui.io/bootstrap/
```

Type:

- Bootstrap UI component/admin dashboard reference

Useful design ideas:

- cohesive UI component library
- dashboard template cards
- table/form consistency
- light and dark mode awareness
- responsive Bootstrap-style admin pages

Adapt for RentEase:

- component consistency
- table and form polish
- owner/tenant portal spacing and information hierarchy

Do not copy:

- paid Pro components
- bundled package
- external assets

License / asset caution:

- distinguish free/open components from Pro templates before using any source

### Tabler

URL:

```text
https://tabler.io/
```

Type:

- modern Bootstrap admin dashboard reference

Useful design ideas:

- clean, spacious dashboard cards
- left sidebar / dashboard layout options
- simple typography
- responsive tables/forms
- badges, alerts, cards, empty pages, invoice pages, and navigation patterns

Adapt for RentEase:

- owner/tenant dashboard visual language
- invoice detail pages
- payment forms
- repair/support ticket pages
- notification center

Do not copy:

- premium illustrations
- icon packs unless license is checked
- full template package

License / asset caution:

- Tabler has an open-source MIT option, but RentEase should still adapt patterns through local CSS and Django templates

## Recommended Public UI Reference Direction

Use a real-estate/property listing direction inspired mainly by:

- Colorlib real estate category patterns
- BootstrapMade / ThemeWagon real-estate style expectations
- Start Bootstrap landing page section rhythm

Homepage layout:

- clean top navigation
- hero with clear room-rental value proposition
- compact property/workflow preview
- feature cards for browsing, contracts, invoices, repairs, and tenant portal
- role section for visitor, owner, tenant
- final CTA for room browsing and login

Room card layout:

- image or branded placeholder at top
- status badge
- title
- short description
- room code/name
- area/floor/capacity metadata
- available date
- price row
- clear detail CTA

Room detail layout:

- large image/placeholder
- price and deposit summary blocks
- public-safe room facts
- viewing registration CTA
- no tenant, contract, invoice, owner-internal, or admin-note data

Viewing form layout:

- card-based form
- short privacy/help text
- clear labels
- no auto-account or tenant creation messaging

CTA style:

- primary teal button for concrete next action
- secondary subtle button for navigation
- no oversized or overdecorated CTA blocks

Color / spacing / card direction:

- warm neutral background
- white cards
- restrained teal/blue accents
- 16px to 24px card spacing
- no heavy gradients except small brand accents

## Recommended Dashboard UI Reference Direction

Use a Tabler/AdminLTE/CoreUI-style dashboard direction.

Primary recommendation:

- Tabler-like clean dashboard surfaces
- AdminLTE-like practical admin information architecture
- CoreUI-like component consistency

Sidebar / role navigation:

- keep RentEase role navigation compact for now
- future Phase 20C may introduce a stronger sidebar-like dashboard shell if it can be done without breaking templates

Topbar:

- persistent RentEase brand
- clear public/portal/admin/report links
- avoid crowding mobile widths

Dashboard metric cards:

- grouped by operational area
- short labels
- obvious values
- avoid overly large empty cards

Tables:

- dashboard table style with horizontal overflow
- readable row spacing
- clear action links
- status badges for state

Forms:

- forms inside cards
- concise help text
- field labels in Vietnamese
- action buttons at bottom

Badges:

- rounded, text-first, restrained colors

Detail cards:

- information grid pattern
- grouped page actions
- no raw technical labels

Mobile behavior:

- single-column cards
- scrollable tables
- compact nav wrapping
- no clipped hero text

## Final Recommended Combination

Use this combination:

```text
Public pages: real-estate/property listing style.
Owner/Tenant portals: Tabler/AdminLTE/CoreUI-style SaaS dashboard.
Reports: light admin report styling aligned with RentEase cards/tables.
Admin: keep Django Admin/Jazzmin; do not replace it.
```

Implementation principle:

```text
Use local CSS and Django templates only. Do not import external template packages at runtime.
```

## RentEase Page Mapping

### Public

| RentEase page | Reference pattern |
| --- | --- |
| `/` | real-estate SaaS landing page |
| `/rooms/` | property listing grid |
| room detail | property detail page |
| viewing registration | contact/application form |
| `/login/` | SaaS login page |

### Owner

| RentEase page | Reference pattern |
| --- | --- |
| `/owner/dashboard/` | admin dashboard overview |
| owner rooms/listings/tenants/contracts/invoices/repairs/viewings | dashboard table/list pages |
| owner detail pages | dashboard detail cards |
| owner forms | admin form cards |
| owner payment page | invoice/payment workflow page |
| owner repair/viewing process pages | support/ticket processing pages |

### Tenant

| RentEase page | Reference pattern |
| --- | --- |
| `/tenant/dashboard/` | simplified user dashboard |
| tenant profile | account profile card |
| tenant contracts | account contract list/detail |
| tenant invoices/payments | account billing cards |
| tenant repairs | support/ticket pages |
| tenant notifications | notification center |

## Visual Rules For Next Implementation Phase

Color palette:

- primary teal `#0f766e`
- dark teal `#0b5f59`
- restrained blue `#2563eb`
- warm neutral background `#f4f6f5`
- white surfaces
- muted text around `#627386`

Typography:

- keep system sans-serif for low risk
- strong page headings
- no negative letter spacing
- avoid hero text that overwhelms the first viewport

Spacing scale:

- 8px base rhythm
- 16px internal component gap
- 24px section/card rhythm
- 32px to 48px for major page sections

Border radius:

- 12px for small controls
- 14px to 18px for cards
- avoid overly rounded large containers

Card shadow:

- soft, low-contrast shadows
- avoid floating-card overload

Button styles:

- teal primary
- subtle secondary
- labels must describe action

Badge styles:

- rounded pills
- text-first
- restrained semantic colors

Table styles:

- clear headers
- horizontal overflow wrapper
- visible action links
- no cramped columns on mobile

Form styles:

- form cards
- visible labels
- short help text
- clear submit/cancel actions

Responsive behavior:

- desktop around 1366px should feel balanced
- mobile around 390px should avoid horizontal page overflow
- tables may scroll horizontally inside wrappers

## Copywriting Rules

Vietnamese-first and natural.

Good examples:

- Quản lý nhà trọ dễ dàng hơn với RentEase
- Theo dõi phòng, hợp đồng, hóa đơn và sửa chữa trong một nơi
- Xem phòng đang cho thuê
- Đăng nhập hệ thống
- Bảng điều hành chủ trọ
- Cổng thông tin khách thuê

Bad examples:

- Nền tảng tuyệt vời cho mọi nhu cầu
- Giải pháp toàn diện tối ưu hóa quy trình
- no-accent Vietnamese
- mixed English/Vietnamese in user-facing UI
- vague AI-style marketing copy

## What Not To Do

- Do not make another oversized hero.
- Do not use too many gradients.
- Do not make cards too empty.
- Do not expose admin/report links prominently on the public homepage.
- Do not use generic AI-looking copy.
- Do not copy template HTML/CSS blindly.
- Do not import external template packages at runtime.
- Do not use paid/commercial assets unless license is clear.
- Do not break existing routes/forms/security.

## Recommended Next Phase

```text
Phase 20C: Apply Reference-Based UI Redesign
```

Goal:

Apply the chosen reference direction to RentEase templates and local CSS.

Phase 20C should be template/CSS-focused and should preserve existing models, migrations, schema, business logic, billing logic, role-based routing, owner/tenant scoping, and privacy rules.
