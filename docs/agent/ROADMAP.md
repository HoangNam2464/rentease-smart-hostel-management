# RentEase Roadmap

The current product priority is interface quality. Complete and stabilize the UI before enabling bilingual runtime behavior.

## Delivery order

### 1. Governance and documentation

- Short canonical document names
- English-only code terminology
- Separate bilingual UI vocabulary
- Reference-first design and visual-QA rules

### 2. Design foundation

- Study approved reference interfaces
- Unify brand tokens and component behavior
- Normalize public and authenticated shells
- Establish desktop/mobile component baselines

### 3. Product surfaces

Deliver and verify one focused commit per surface group:

1. Public home, room discovery, room detail, and viewing registration
2. Owner dashboard and navigation
3. Owner properties, rooms, listings, tenants, and contracts
4. Owner invoices, payments, repairs, and viewing operations
5. Tenant dashboard, contracts, invoices, payments, repairs, and notifications
6. Staff reports, Django Admin, errors, empty states, and access-denied states

### 4. Interface hardening

- Long Vietnamese and English content
- Empty, partial, validation, denied, and success states
- Keyboard, focus, contrast, touch targets, and reduced motion
- Performance and static-asset review
- Cross-role privacy verification

### 5. English and Vietnamese

- Configure supported languages as `vi` and `en`
- Add `LocaleMiddleware`, locale paths, and safe language switching
- Use English gettext message IDs in source
- Complete Vietnamese translations
- Translate templates, forms, validation, messages, admin labels, emails, and relevant API-facing text
- Persist the locale and display only the active language
- Run translation completeness and mixed-language scans

### 6. Production readiness

- Account onboarding and recovery
- Protected media storage
- PostgreSQL and real-data verification
- Backups and restore procedure
- Email/logging verification
- CI, coverage, deployment, HTTPS, and operational monitoring

## Iteration contract

Each iteration must be coherent, tested, committed separately, and pushed only after verification. `docs/agent/NEXT.md` names the single active iteration.
