# RentEase Release Checklist

## Local Demo Release Checklist

- [ ] README complete
- [ ] run instructions verified
- [ ] demo script available
- [ ] screenshots prepared
- [ ] test accounts available locally
- [ ] Django check passes
- [ ] migration dry-run says `No changes detected`
- [ ] public landing page works
- [ ] public rooms work
- [ ] login works
- [ ] owner portal works
- [ ] tenant portal works
- [ ] admin works
- [ ] reports remain staff-only
- [ ] route regression checked
- [ ] privacy/security checks completed
- [ ] GitHub tag created after approval

## Production Readiness Checklist

- [ ] production settings split or hardened
- [ ] `DEBUG=False` behavior verified
- [ ] `SECRET_KEY` loaded from environment
- [ ] `ALLOWED_HOSTS` configured
- [ ] CSRF trusted origins configured
- [ ] secure cookies reviewed
- [ ] HTTPS/security headers reviewed
- [ ] production database configured
- [ ] static/media handling configured
- [ ] email settings configured
- [ ] logging configured
- [ ] backup plan documented
- [ ] deployment instructions documented
- [ ] CI configured
- [ ] automated tests run in CI
- [ ] no `.env`, database, or backup files committed

## UI Demo Readiness Checklist

- [x] UI/UX audit and redesign planning completed
- [x] public landing page looks like RentEase
- [x] public room list is readable
- [x] public room detail is readable
- [x] viewing registration form is understandable
- [ ] login page is clear
- [x] owner dashboard layout is clear
- [x] owner sidebar/navigation is consistent
- [x] owner rooms/listings/contracts/invoices pages are readable
- [x] owner payment recording is easy to find from invoice detail
- [x] tenant dashboard is clear
- [x] tenant invoices/payments/repairs/notifications are readable
- [x] empty states are understandable
- [ ] no HOSTELLO branding appears in RentEase demo paths
- [ ] no raw Django template tags are visible
- [ ] no private data appears on public pages

## Documentation Readiness Checklist

- [ ] AGENTS.md updated if status changed
- [ ] current state docs updated
- [ ] production roadmap updated
- [ ] SPQM docs updated if process changed
- [ ] README matches current run process
- [ ] demo checklist matches current UI
- [ ] security notes mention known production gaps
- [ ] unknown items marked `Not verified`
- [ ] future items marked `Planned`

## Video Demo Checklist

- [ ] video is planned before recording
- [ ] video length is <= 5 minutes if required
- [ ] demo account data is fake
- [ ] no passwords or secrets are shown
- [ ] no real citizen ID data is shown
- [ ] public room browsing is shown
- [ ] owner dashboard is shown
- [ ] owner billing/payment flow is shown if ready
- [ ] tenant dashboard is shown
- [ ] repair/viewing registration flow is shown
- [ ] reports/admin are shown only if appropriate

## Final Git Checklist

- [ ] branch is `complete-product`
- [ ] working tree is clean
- [ ] latest commit is pushed
- [ ] required tag is created only after approval
- [ ] tag is pushed
- [ ] old tags are not moved
- [ ] no force push was used
