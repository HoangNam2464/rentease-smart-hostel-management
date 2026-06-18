# RentEase Security Rules

## Owner Scoping

Owner data must always be scoped through:

```python
request.user.rentease_profile
```

Safe owner query patterns:

```python
Room.objects.filter(owner=profile)
RoomListing.objects.filter(room__owner=profile)
ViewingRegistration.objects.filter(listing__room__owner=profile)
RepairRequest.objects.filter(room__owner=profile)
Contract.objects.filter(room__owner=profile)
Invoice.objects.filter(contract__room__owner=profile)
PaymentHistory.objects.filter(invoice__contract__room__owner=profile)
Tenant.objects.filter(contracts__room__owner=profile).distinct()
```

## Tenant Scoping

Tenant data must always be scoped through:

```python
request.user.tenant_profile
```

Safe tenant query patterns:

```python
Contract.objects.filter(tenant=tenant)
Invoice.objects.filter(contract__tenant=tenant)
PaymentHistory.objects.filter(invoice__contract__tenant=tenant)
RepairRequest.objects.filter(tenant=tenant)
```

## Forbidden Sensitive Query Patterns

For sensitive detail/update/delete views, do not use:

```python
get_object_or_404(Model, pk=pk)
Model.objects.all()
```

Use scoped querysets:

```python
get_object_or_404(owner_scoped_queryset(profile), pk=pk)
get_object_or_404(tenant_scoped_queryset(tenant), pk=pk)
```

## Sensitive Data

Do not expose:

- password
- account/auth internals
- permission fields
- citizen_id
- citizen_id_front
- citizen_id_back
- citizen ID file/image
- payment collector internals
- other owner data
- other tenant data
- admin-only notes to tenant/public
- owner internal notes to tenant/public

## Legacy Rules

Do not re-add root legacy routes:

```python
path('', include('students.urls'))
path('api/', include('requests.urls'))
path('fees/', include('fees.urls', namespace='fees'))
```

Allowed legacy routes:

- `/legacy/`
- `/legacy/login/`

Do not add `/legacy/api/` or `/legacy/fees/` unless explicitly approved.

## Definition of Done

Security-sensitive work is not done until:

- owner/tenant scoped access is verified
- protected routes reject the wrong roles
- unrelated owner/tenant records are not visible
- sensitive fields are not rendered
- legacy root routes are not re-exposed
- Django check passes
- migration dry-run is clean unless migrations were approved
