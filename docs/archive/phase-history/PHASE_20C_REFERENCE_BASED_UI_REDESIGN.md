# Phase 20C: Reference-Based RentEase UI Redesign

## Chosen Reference Direction

Phase 20C applies the Phase 20B direction to the actual RentEase templates and local CSS.

The selected direction is:

- public pages: real-estate / room-rental listing style
- owner portal: clean SaaS dashboard style inspired by Tabler, AdminLTE, CoreUI, and Airtable-like data tables
- tenant portal: simple, readable Notion/Vercel-light style

No external template package, remote asset, CDN, model change, migration, schema change, billing logic change, or authorization change was added.

## Public Real-Estate / Airbnb-Like UI Summary

Updated public surfaces:

- homepage
- public room list
- public room detail
- viewing registration form
- viewing registration success page
- portal login entry point

Main changes:

- homepage now reads more like a real RentEase product page
- primary CTAs are room browsing and login
- admin/report links are not foregrounded in the hero
- public room cards use property-style visual panels, status badges, metadata chips, price rows, and clear detail CTAs
- room detail uses a two-column property detail layout with a sticky price/action summary
- viewing registration uses a friendly form with a room summary panel
- login copy was tightened around role-based access

## Owner Dashboard Summary

Owner portal pages now inherit a more dashboard-like visual system through local CSS and the shared portal base.

Main changes:

- owner role navigation is styled as a dashboard sidebar on desktop where supported
- owner dashboard cards, tables, actions, detail pages, and forms use cleaner dashboard spacing
- tables use clearer admin-style row and action treatment
- owner invoice list copy was corrected from `Thang` to `Tháng`
- owner-only internal process forms remain owner-only and were not exposed to public or tenant pages

No owner-scoped queryset, payment workflow, invoice calculation, repair workflow, listing workflow, or viewing-registration workflow was changed.

## Tenant Portal Summary

Tenant pages keep a simple, readable portal direction.

Main changes:

- tenant navigation labels were clarified
- tenant cards and tables inherit the lighter dashboard/card system
- tenant invoice list copy was corrected from `Thang` to `Tháng`
- access-denied copy was converted to Vietnamese

No tenant-scoped queryset, tenant permission rule, or tenant data relationship was changed.

## Image Usage Summary

No real image files were added in Phase 20C.

Reason:

- license-safe image sources were not downloaded in this phase
- the project should not hotlink external images at runtime
- no copyrighted random images, people, trademarks, or sensitive media should be committed

Public pages now use safe local CSS visual panels for room/property previews. Real room photos can be added later only after source, license, and storage rules are approved.

## Image Source / License Notes

No `RENTEASE_IMAGE_SOURCES.md` file was created because no image files were added.

Future image work should document:

- source URL
- license note
- local filename
- intended page usage

## Route Smoke Result

Verified with Django test client after implementation:

- `/`
- `/rooms/`
- `/login/`
- one demo published room detail
- viewing registration form
- viewing registration success page
- `/owner/dashboard/`
- owner rooms, listings, tenants, contracts, invoices, repairs, viewing registrations
- `/tenant/dashboard/`
- tenant profile, contracts, invoices, payments, repairs, notifications
- `/reports/` anonymous protected
- `/admin/` anonymous protected
- `/legacy/`
- `/legacy/login/`
- `/api/requests/` remains 404
- `/fees/` remains 404
- custom missing route returns 404

Result:

```text
BAD_COUNT 0
```

## Security / Privacy Result

The redesign did not change:

- models
- migrations
- schema
- billing logic
- production settings
- authentication
- authorization
- owner/tenant scoping
- legacy route isolation

Scans were run for common sensitive terms and user-facing unaccented Vietnamese patterns.

Expected owner-only matches remain:

- login password field on `/login/`
- owner repair internal note on owner repair processing page
- owner viewing-registration internal note on owner viewing-registration processing page

No public or tenant template was intentionally changed to expose citizen ID data, citizen ID files, auth internals, payment collector internals, other-owner data, or other-tenant data.

## Remaining Limitations

- Browser visual review is still needed after the reference-based redesign.
- Public room visual panels are CSS placeholders, not real room photos.
- Production settings remain unready.
- Owner-facing utility/billing detail workflow remains a production gap.
- Account lifecycle and deployment readiness remain future production work.

## Next Recommendation

```text
Phase 20D: Browser Visual Review and Final UI Fixes
```

Phase 20D should run the local server, inspect the redesigned pages in desktop and mobile browser widths, capture screenshots if useful, and make only small template/CSS fixes if needed.
