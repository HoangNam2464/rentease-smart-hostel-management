# RentEase Definition Of Done

## Global Phase Definition Of Done

A RentEase phase is done only when:

- branch is `complete-product`
- working tree is clean
- Django check passes
- migration dry-run passes
- affected routes or features were tested
- no privacy/security regression exists
- owner/tenant data scoping is preserved
- only intended files changed
- commit was created
- push completed
- tag was created only after approval

## Documentation Phase DoD

Documentation work is done when:

- only approved documentation files changed
- content uses actual RentEase state
- unknown or future items are marked as `Not verified` or `Planned`
- no application source code changed
- Django check still passes
- migration dry-run still reports `No changes detected`
- docs are committed only after review/approval

## UI Phase DoD

UI work is done when:

- affected pages render successfully
- no raw Django template tags are visible
- public pages expose only public-safe data
- owner pages remain owner-scoped
- tenant pages remain tenant-scoped
- reports remain staff-only
- no unrelated workflow or business logic changed

## Security Phase DoD

Security work is done when:

- owner-scoped queries use `request.user.rentease_profile`
- tenant-scoped queries use `request.user.tenant_profile`
- sensitive detail/update views do not use unrestricted `Model.objects.all()`
- sensitive detail/update views do not use unrestricted `get_object_or_404(Model, pk=pk)`
- forbidden fields are not exposed
- legacy root routes are not reintroduced
- wrong roles are blocked or redirected

## Production Settings Phase DoD

Production settings work is done when:

- local development still runs
- production values are environment-driven
- `DEBUG` is controlled safely
- `SECRET_KEY` is not hardcoded for production
- `ALLOWED_HOSTS` is production-aware
- CSRF and secure cookie settings are documented
- static/media behavior is documented
- database configuration supports a production target
- no secret files are committed

## Billing Phase DoD

Billing work is done when:

- owner data is scoped by owned rooms/contracts
- tenant data is scoped by the linked tenant profile
- invoice totals remain consistent
- overpayment is blocked
- payment status transitions are correct
- no manual editing bypasses calculated amounts unless explicitly approved
- tenant pages do not expose collector internals
- admin and report behavior does not regress
