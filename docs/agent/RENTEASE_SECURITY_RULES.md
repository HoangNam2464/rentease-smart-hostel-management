# RentEase Security Rules

This file is the canonical durable security reference. Read it for permissions, data access, admin, billing, account, settings, or media work.

## Owner Scoping

Resolve the owner through `request.user.rentease_profile` and scope data through owned rooms or related objects.

Examples:

```python
Room.objects.filter(owner=profile)
Contract.objects.filter(room__owner=profile)
Invoice.objects.filter(contract__room__owner=profile)
PaymentHistory.objects.filter(invoice__contract__room__owner=profile)
Tenant.objects.filter(contracts__room__owner=profile).distinct()
```

## Tenant Scoping

Resolve the tenant through `request.user.tenant_profile` and scope every query to that tenant.

Examples:

```python
Contract.objects.filter(tenant=tenant)
Invoice.objects.filter(contract__tenant=tenant)
PaymentHistory.objects.filter(invoice__contract__tenant=tenant)
RepairRequest.objects.filter(tenant=tenant)
```

For sensitive detail, update, or delete views, never use unrestricted `Model.objects.all()` or `get_object_or_404(Model, pk=pk)`.

## Sensitive Data

Never expose on public, owner, or tenant surfaces:

- `citizen_id`, `citizen_id_front`, `citizen_id_back`
- identity files or direct media URLs
- passwords, hashes, tokens, permission/auth internals
- payment collector internals
- admin/private owner notes
- unrelated owner or tenant records

Use fake data only in demos and screenshots.

## Admin Identity Rules

- Do not add identity fields to `list_display` or `search_fields`.
- Keep identity fields only in the collapsed `Sensitive identity data` detail section.
- Keep sensitive identity fields read-only for non-superuser staff.
- Do not expose co-tenant identity fields through contract inlines.
- Use phone/email/name for safe search when needed.

## Billing Integrity

- Scope invoices and payments through the owner or tenant relationship.
- Preserve calculated totals, paid amount, remaining amount, and status transitions.
- Reject overpayment.
- Do not expose collector/internal payment fields to tenants.
- Plan before changing invoice detail or utility logic.

## Settings, Database, and Media

- Do not commit `.env`, databases, dumps, credentials, or uploaded media.
- Treat PostgreSQL migration and production media storage as separate approved phases.
- Do not assume Django's DEBUG media serving is production access control.
- Preserve environment-driven security settings and local development behavior.

## Legacy Boundaries

Do not re-add these root routes:

```python
path('', include('students.urls'))
path('api/', include('requests.urls'))
path('fees/', include('fees.urls', namespace='fees'))
```

Only `/legacy/` and `/legacy/login/` are approved legacy entry points.

## Security Definition of Done

- Verify correct-role access and wrong-role rejection.
- Verify unrelated owner/tenant records cannot be accessed by identifier changes.
- Scan rendered output for sensitive fields and raw template syntax.
- Run Django check and migration dry-run.
- Test affected routes.
- Confirm no legacy root route was restored.
