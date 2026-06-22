# RentEase Release Checklist

## Local Demo Release Checklist

- [x] README complete
- [x] run instructions verified
- [x] demo script available
- [ ] screenshots prepared
- [x] demo data plan available
- [x] demo data seeded locally
- [x] final demo walkthrough verified
- [x] test accounts available locally
- [x] Django check passes
- [x] migration dry-run says `No changes detected`
- [x] public landing page works
- [x] public rooms work
- [x] login works
- [x] owner portal works
- [x] tenant portal works
- [x] admin works
- [x] reports remain staff-only
- [x] route regression checked
- [x] privacy/security checks completed
- [x] GitHub tag created after approval

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
- [x] landing page looks like a real room-rental product
- [x] Vietnamese wording is consistent across major public/owner/tenant paths
- [x] major Vietnamese UI copy uses proper diacritics
- [x] landing page copy feels human and practical
- [x] public room list is readable
- [x] public room pages look realistic enough for product-grade demo
- [x] public room detail is readable
- [x] viewing registration form is understandable
- [x] login page is clear
- [x] owner dashboard layout is clear
- [x] owner portal looks business-ready for local demo
- [x] owner sidebar/navigation is consistent
- [x] owner rooms/listings/contracts/invoices pages are readable
- [x] owner payment recording is easy to find from invoice detail
- [x] tenant dashboard is clear
- [x] tenant portal looks user-ready for local demo
- [x] tenant invoices/payments/repairs/notifications are readable
- [x] empty states are understandable
- [x] no demo-looking placeholder text appears in major product pages
- [x] no HOSTELLO branding appears in RentEase demo paths
- [x] no raw Django template tags are visible
- [x] no private data appears on public pages
- [x] full UI completeness audit completed
- [x] remaining UI polish items resolved
- [x] final visual QA checklist completed
- [ ] manual visual QA completed
- [x] screenshot/video preparation guide completed
- [ ] screenshots prepared

## Documentation Readiness Checklist

- [ ] AGENTS.md updated if status changed
- [x] current state docs updated
- [ ] production roadmap updated
- [ ] SPQM docs updated if process changed
- [x] README matches current run process
- [x] demo checklist matches current UI
- [ ] security notes mention known production gaps
- [x] unknown items marked `Not verified`
- [x] future items marked `Planned`

## Video Demo Checklist

- [x] video is planned before recording
- [x] video checklist is planned
- [x] Vietnamese narration script is prepared
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

- [x] branch is `complete-product`
- [x] working tree is clean
- [x] latest commit is pushed
- [x] required tag is created only after approval
- [x] tag is pushed
- [x] old tags are not moved
- [x] no force push was used
