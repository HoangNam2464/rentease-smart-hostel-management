# Phase 20K-A - Admin Tenant Privacy Hotfix

## 1. Issue Found

Phase 20J browser-based visual QA found that the Django Admin/Jazzmin tenant list page exposed tenant `citizen_id` values in the default list view.

This was treated as a privacy issue because tenant identity numbers should not appear in routine admin list browsing, screenshots, search results, or dropdown labels.

## 2. Files Inspected

- `backend/tenants/models.py`
- `backend/tenants/admin.py`
- `docs/ui/PHASE_20J_BROWSER_VISUAL_QA.md`

Read-only context was also taken from the project security rules and project map.

## 3. Fields Considered Sensitive

- `citizen_id`
- `citizen_id_front`
- `citizen_id_back`

Related rule: these fields must not be exposed to public, tenant, owner, or routine list-style surfaces.

## 4. Changes Applied

File changed:

- `backend/tenants/admin.py`

Tenant admin changes:

- Removed `citizen_id` from `TenantAdmin.list_display`.
- Removed `citizen_id` from `TenantAdmin.search_fields`.
- Added explicit `fieldsets`.
- Moved `citizen_id`, `citizen_id_front`, and `citizen_id_back` into a collapsed `Sensitive identity data` section on the admin detail form.

Co-tenant admin changes:

- Removed `citizen_id` from `CoTenantAdmin.list_display`.
- Removed `citizen_id` from `CoTenantAdmin.search_fields`.
- Added explicit `fieldsets`.
- Moved `citizen_id` into a collapsed `Sensitive identity data` section on the admin detail form.

No model fields were changed. No database data was removed. No migrations were created.

## 5. Tenant Model String Result

`Tenant.__str__` already returned:

```python
return self.full_name
```

No model change was needed.

`CoTenant.__str__` also returns `full_name`, so dropdown labels do not expose citizen ID through model string representation.

## 6. Admin List Privacy Result

Django Client verification:

- `/admin/tenants/tenant/` returned HTTP 200 after admin login.
- `/admin/tenants/cotenant/` returned HTTP 200 after admin login.
- Existing tenant and co-tenant citizen ID values were not found in the tenant changelist HTML.
- Existing tenant and co-tenant citizen ID values were not found in the co-tenant changelist HTML.
- The string `citizen_id` was not present in the tenant changelist HTML.
- The string `citizen_id` was not present in the co-tenant changelist HTML.

Result: default tenant and co-tenant admin list pages no longer expose citizen ID values.

## 7. Admin Detail Privacy Result

Django Client verification:

- Tenant admin detail page returned HTTP 200.
- `Sensitive identity data` section was present.
- `citizen_id` remains available in the detail form for admin/superuser review.

This is acceptable for this hotfix because the immediate Phase 20J issue was default list-page exposure. A later admin privacy phase can decide whether to further restrict or make these fields readonly.

## 8. Remaining Admin Privacy Recommendations

Recommended later admin-hardening phase:

- Review whether `citizen_id`, `citizen_id_front`, and `citizen_id_back` should be readonly for non-superuser staff.
- Review whether tenant identity images/files should be hidden from normal staff entirely.
- Review other admin model list pages for sensitive columns.
- Reduce Jazzmin topbar search clutter if it continues to expose too much operational data in screenshots.
- Consider separate staff permission groups before real production use.

## 9. Schema And Migration Confirmation

- No model field definitions changed.
- No migrations were created.
- No database schema changes were introduced.
- Django check passed.
- Migration dry-run reported `No changes detected`.
