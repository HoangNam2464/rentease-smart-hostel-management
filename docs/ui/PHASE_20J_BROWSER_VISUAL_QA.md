# Phase 20J - Browser-Based Visual QA

## 1. Scope

Phase 20J performed a browser-based visual QA pass for the areas that Phase 20I did not inspect deeply:

- Public pages
- Owner portal pages
- Tenant portal pages
- Admin/Jazzmin pages after login
- Staff reports after login
- Desktop and mobile responsive rendering
- Form/error states
- Empty states
- Interactions and visual effects

This phase was audit-only. No backend files, templates, CSS, models, views, URLs, forms, settings, migrations, legacy HOSTELLO files, runtime files, or database schema were changed.

## 2. Browser/Preview Method

| Item | Result |
|---|---|
| Server URL | `http://127.0.0.1:8000/` |
| Server status | Port `8000` was already open and reachable |
| Browser tool | In-app browser with desktop and mobile viewport checks |
| Desktop viewport | Default browser viewport around `1280px` wide |
| Mobile viewport | `390px x 844px` |
| Accounts used | `admin_test`, `owner_test`, `tenant_test` |
| Screenshots captured | Yes |
| Screenshots saved under | `docs/ui/screenshots/phase20j-browser-qa/` |

Notes:

- Full-page mobile screenshots show repeated sticky headers in some long pages. This is a screenshot-capture artifact caused by sticky/fixed UI during full-page capture, not necessarily a live browsing bug.
- Invalid form submissions were used only to trigger validation errors. No delete, approval, rejection, password, permission, or valid production-like save action was performed.

## 3. Screenshots

Captured 44 PNG screenshots:

- `admin-index-desktop.png`
- `admin-login-desktop.png`
- `admin-room-model-desktop.png`
- `admin-tenant-model-desktop.png`
- `login-desktop.png`
- `login-error-desktop.png`
- `login-mobile.png`
- `owner-contract-form-error-desktop.png`
- `owner-contracts-desktop.png`
- `owner-dashboard-desktop.png`
- `owner-dashboard-mobile.png`
- `owner-invoice-detail-desktop.png`
- `owner-invoice-form-error-desktop.png`
- `owner-invoices-desktop.png`
- `owner-invoices-mobile.png`
- `owner-payment-form-error-desktop.png`
- `owner-repairs-desktop.png`
- `owner-room-form-desktop.png`
- `owner-room-form-error-desktop.png`
- `owner-rooms-desktop.png`
- `owner-rooms-mobile.png`
- `owner-viewing-registrations-desktop.png`
- `public-home-desktop.png`
- `public-room-detail-desktop.png`
- `public-rooms-desktop.png`
- `public-rooms-mobile.png`
- `public-viewing-form-desktop.png`
- `public-viewing-form-error-desktop.png`
- `public-viewing-success-desktop.png`
- `reports-billing-desktop.png`
- `reports-index-desktop.png`
- `reports-listings-desktop.png`
- `reports-maintenance-desktop.png`
- `reports-rooms-desktop.png`
- `reports-tenants-contracts-desktop.png`
- `tenant-dashboard-desktop.png`
- `tenant-dashboard-mobile.png`
- `tenant-invoices-desktop.png`
- `tenant-invoices-mobile.png`
- `tenant-notifications-desktop.png`
- `tenant-profile-desktop.png`
- `tenant-repair-form-error-desktop.png`
- `tenant-repairs-desktop.png`
- `tenant-repairs-mobile.png`

## 4. Admin/Staff Findings

| Page | URL | Score | Issue | Suggested Fix | Priority |
|---|---|---:|---|---|---|
| Admin login | `/admin/login/` | 7 | RentEase branding is visible and acceptable for staff. | No urgent change. | P3 |
| Admin index | `/admin/` | 6 | Jazzmin sidebar/topbar feels crowded. Several search boxes in the top bar compress the layout. | Simplify Jazzmin top search models or move some searches out of the topbar. | P2 |
| Admin index | `/admin/` | 6 | Left sidebar visually overlaps/crowds content in full-page screenshot. This may be partly capture behavior, but it weakens screenshot quality. | Review Jazzmin layout width and screenshot mode before final demo capture. | P2 |
| Admin model list | `/admin/properties/room/` | 6 | Table-heavy but acceptable for staff. | Keep admin internal; no urgent UI change. | P3 |
| Tenant model list | `/admin/tenants/tenant/` | 5 | `Citizen id` is visible as a list column. Admin/staff can access it, but it is sensitive and unnecessary for routine browsing. | Hide citizen ID from default admin list display or move it to restricted detail-only review if truly required. | P1 |
| Admin apps | `/admin/` | 6 | Legacy names such as `Warden Profiles` and auth groups still appear, which can confuse demo users. | Later admin cleanup: hide or rename legacy/admin-only labels without deleting apps. | P2 |

## 5. Reports Findings

| Page | URL | Score | Issue | Suggested Fix | Priority |
|---|---|---:|---|---|---|
| Reports dashboard | `/reports/` | 6 | Metrics work, but the page inherits Jazzmin/staff shell and looks less polished than the owner portal. | Add staff report layout polish after owner/tenant surfaces are complete. | P3 |
| Billing report | `/reports/billing/` | 6 | Data is visible, but filters/summary hierarchy are basic. | Add clearer filter bar, currency formatting, status badges, and export affordance. | P3 |
| Room report | `/reports/rooms/` | 6 | Functional table, limited visual hierarchy. | Add summary cards and readable occupancy breakdown. | P3 |
| Tenant/contract report | `/reports/tenants-contracts/` | 6 | Multiple tables are readable but dense. | Add sections, spacing, and stronger upcoming-expiry callouts. | P3 |
| Maintenance report | `/reports/maintenance/` | 6 | Pending/completed sections are usable but plain. | Add priority/status visual treatment and cost summary cards. | P3 |
| Listings report | `/reports/listings/` | 6 | Several tables make the page feel operational but heavy. | Add report cards, status chips, and export-ready layout later. | P3 |

## 6. Responsive Findings

| Page | Width | Problem | Suggested Fix | Priority |
|---|---:|---|---|---|
| Public rooms | 390px | Cards stack correctly and no horizontal overflow was detected. Full-page screenshot repeats sticky header as capture artifact. | No urgent fix; use viewport screenshots instead of full-page screenshots for final mobile presentation. | P3 |
| Login | 390px | Login page remains usable with no overflow. | No urgent fix. | P3 |
| Owner dashboard | 390px | Slight horizontal overflow detected: page width around `416px` on a `390px` viewport. | Tighten dashboard mobile padding/card widths and check sticky topbar/footer width. | P2 |
| Owner rooms | 390px | No measured page overflow, but table still reads like desktop table inside a narrow viewport. | Consider card-based mobile rows or stronger table wrapper cues. | P2 |
| Owner invoices | 390px | No measured page overflow, but invoice table remains dense. | Add mobile invoice cards or reduce visible columns. | P2 |
| Tenant dashboard | 390px | Layout stacks acceptably and no overflow was detected. | No urgent fix. | P3 |
| Tenant invoices | 390px | Table is cramped; invoice code wraps into many short lines. | Convert tenant invoice list to mobile cards with total/status/date emphasis. | P2 |
| Tenant repairs | 390px | Page remains usable; table-heavy list could still become cards. | Add mobile repair cards later. | P3 |

## 7. Form/Error State Findings

| Page/Form | Problem | Suggested Fix | Files likely affected | Priority |
|---|---|---|---|---|
| Login form | Invalid credentials did not show a clearly detected error message in the browser audit. | Add a prominent form-level error message for invalid login. | `hostello_backend/templates/portal/login.html` | P2 |
| Public viewing registration | Blank submit shows validation errors and stays on form. | Improve error styling if desired; behavior is acceptable. | `hostello_backend/templates/listings/viewing_registration_form.html`, public CSS | P3 |
| Owner room create | Validation errors appear, but fields look like raw browser-default inputs and buttons. | Apply existing form-card styling consistently to all fields, errors, and actions. | `hostello_backend/templates/portal/owner_room_form.html`, `hostello_backend/static/css/rentease-layout.css` | P1 |
| Owner contract create | Validation errors appear; dense form needs grouping. | Group room/tenant/dates/financial fields and style errors consistently. | `hostello_backend/templates/portal/owner_contract_form.html`, portal CSS | P2 |
| Owner invoice create | Validation errors appear; form is safe but plain. | Add invoice context helper text and styled error blocks. | `hostello_backend/templates/portal/owner_invoice_form.html`, portal CSS | P2 |
| Owner payment form | Blank submit shows errors; page needs stronger balance context. | Highlight invoice total, paid, remaining, and safe payment warning. | `hostello_backend/templates/portal/owner_payment_form.html`, portal CSS | P2 |
| Tenant repair form | Blank submit shows errors and no save occurs. | Add friendlier examples and consistent styled errors. | `hostello_backend/templates/portal/tenant_repair_form.html`, portal CSS | P3 |

## 8. Empty State Findings

| Area | Empty state present? | Quality | Suggested Fix | Priority |
|---|---|---|---|---|
| Public no available listings | Yes, template contains `empty-state`. | Acceptable. | Add primary CTA back to home/login if needed. | P3 |
| Owner no rooms | Yes. | Good message with next action. | Keep. | P3 |
| Owner no listings | Yes. | Good message. | Add CTA to create listing if not already visually clear. | P3 |
| Owner no tenants | Yes. | Clear but passive. | Explain tenants appear through contracts. | P3 |
| Owner no contracts | Yes. | Clear. | Add CTA to create contract. | P3 |
| Owner no invoices/payments | Yes. | Clear. | Add stronger invoice/payment next-step copy. | P3 |
| Owner no repairs/viewing registrations | Yes. | Clear. | Keep or add lighter icon treatment. | P3 |
| Tenant no contracts | Yes. | Clear. | Keep. | P3 |
| Tenant no invoices/payments | Yes. | Clear but table pages stay plain. | Use card-style empty state later. | P3 |
| Tenant no repairs/notifications | Yes. | Clear. | Keep or add support guidance. | P3 |
| Reports empty sections | Yes, reports templates contain `{% empty %}` blocks. | Functional. | Staff-report polish can improve empty-state visuals later. | P3 |

## 9. Interaction/Effect Findings

| Component | Current state | Recommended effect | Files likely affected | Priority |
|---|---|---|---|---|
| Sidebar nav | Hover and active states exist. | Keep, but add clearer active section marker on mobile. | `hostello_backend/static/css/rentease-layout.css` | P3 |
| Topbar buttons | Hover exists, but search/bell/avatar are not fully meaningful yet. | Either wire meaningful dropdown/search later or visually simplify. | Portal base template/CSS | P3 |
| Owner list action links | Some action links render like plain underlined browser links. | Convert primary actions such as `Tạo phòng` into consistent buttons. | Owner list/form templates and CSS | P1 |
| Tables | Row hover and overflow wrappers exist. | Add mobile card alternative for tenant invoices and key owner financial tables. | Portal templates/CSS | P2 |
| Forms | Focus styling exists in CSS, but some rendered widgets do not pick up the intended field classes. | Ensure all form inputs/selects/textareas use the shared styled class. | Owner/tenant form templates and CSS | P1 |
| Cards | Some cards have shadows and spacing. | Add subtle hover only for clickable cards; keep metric cards stable. | Portal CSS | P3 |
| Reports filters | Reports have basic forms and tables. | Improve filter bar grouping and add export-like affordance. | Reports templates/CSS | P3 |

## 10. Updated Scores

| Area | Score | Reason |
|---|---:|---|
| Public | 7/10 | Public pages render well on desktop/mobile; room media and mobile capture artifacts remain. |
| Owner | 6/10 | Dashboard shell is good, but owner CRUD forms and links still look browser-default in places. |
| Tenant | 6.5/10 | Tenant pages are safe and readable, but table-heavy pages need mobile cards. |
| Admin/Reports | 5.5/10 | Internal tools work, but Jazzmin topbar/sidebar feels crowded and tenant admin list exposes citizen ID. |
| Mobile/responsive | 6/10 | Most pages avoid major overflow; owner dashboard and financial tables need targeted mobile polish. |
| Interaction/effects | 6/10 | Core hover/focus states exist, but action hierarchy and form styling are inconsistent. |

## 11. Exact Recommended Next Fixes

### 1. Phase 20K - Dashboard Interaction Polish

- Pages to edit: owner dashboard, tenant dashboard, shared portal base.
- Files likely affected: `hostello_backend/templates/portal/owner_dashboard.html`, `hostello_backend/templates/portal/tenant_dashboard.html`, `hostello_backend/templates/portal/base.html`, `hostello_backend/static/css/rentease-layout.css`.
- Changes: fix owner dashboard mobile overflow, improve dashboard card hierarchy, tune active/hover states, reduce topbar clutter if safe.
- Risk: low to medium, template/CSS-only.

### 2. Phase 20L - Owner CRUD Professionalization

- Pages to edit: owner rooms, listings, tenants, contracts, invoices, payments, repairs, viewing registrations.
- Files likely affected: `hostello_backend/templates/portal/owner_*.html`, `hostello_backend/static/css/rentease-layout.css`.
- Changes: convert plain links to buttons, style all forms, group fields, improve validation/error styling, add mobile card/table patterns.
- Risk: medium, because many templates are touched.

### 3. Phase 20M - Tenant Readability Polish

- Pages to edit: tenant contracts, invoices, payments, repairs, notifications, profile.
- Files likely affected: `hostello_backend/templates/portal/tenant_*.html`, portal CSS.
- Changes: convert mobile financial tables into cards, improve status labels, add friendlier empty/help text.
- Risk: medium, privacy rules must remain strict.

### 4. Phase 20N - Public Listing Polish

- Pages to edit: public room list/detail, viewing registration form/success, login if needed.
- Files likely affected: listing templates, login template, `rentease-design.css`.
- Changes: improve room media handling, CTA hierarchy, form error styling, and mobile screenshot quality.
- Risk: low to medium.

### 5. Phase 20O - Admin/Reports Professionalization

- Pages to edit: Jazzmin settings/admin display if approved, reports templates.
- Files likely affected: reports templates/CSS and possibly admin configuration.
- Changes: hide sensitive `Citizen id` from default tenant admin list, simplify Jazzmin topbar search, polish report filter/table layout.
- Risk: medium, because admin display settings can affect staff workflows.

## Final Recommendation

Do not start a broad redesign immediately. The most important next work is targeted and visible:

```text
Phase 20K: Dashboard Interaction Polish
```

Then follow with owner CRUD professionalization because owner forms currently show the clearest product-quality gap.
