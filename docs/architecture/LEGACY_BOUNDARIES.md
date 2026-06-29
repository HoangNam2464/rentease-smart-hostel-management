# RentEase Legacy Boundaries

This is the current reference for deciding whether a RentEase task belongs to active product code or retained HOSTELLO code. Use `PROJECT_STRUCTURE_MAP.md` for the full repository map.

## Active RentEase Areas

- Backend apps: `accounts`, `properties`, `tenants`, `contracts`, `billing`, `maintenance`, `listings`, `portal`, and `reports`
- Templates: `frontend/templates/home.html`, `frontend/templates/listings/`, `frontend/templates/portal/`, `frontend/templates/reports/`, `404.html`, and `500.html`
- Styles: `rentease-design.css`, `rentease-layout.css`, and `admin/css/custom_admin.css`
- Product routes: public room pages, owner portal, tenant portal, admin, and staff reports

Normal RentEase feature, security, and UI work should target these areas.

## Retained Legacy Areas

- Django apps: `students`, `attendance`, `fees`, `requests`, and `notices`
- Templates: root `index.html`, `login.html`, `dashboard.html`, `frontend/templates/admin/`, and `frontend/templates/payments/success.html`
- Static assets: `styles.css`, `student-dashboard.css`, `script.js`, `student-dashboard.js`, and root `assets/`
- Allowed routes: `/legacy/` and `/legacy/login/`

These areas remain for compatibility and historical completeness. Some still have models, migrations, admin registrations, imports, or route dependencies.

## Clean-Migration Audit

The Phase 14C-2 audit confirmed the following current behavior:

- all five legacy apps are unconditional members of `INSTALLED_APPS`
- `/legacy/` includes `students.urls`, and the root URL configuration imports `fees.admin`
- legacy models import one another; active RentEase source does not import legacy models
- legacy migrations depend on `accounts`; no active RentEase migration depends on a legacy app
- Django Admin registers models from all five legacy apps
- a clean migration therefore creates legacy content types, permissions, and tables

Expected active application tables are:

```text
accounts_user, accounts_user_groups, accounts_user_user_permissions
nguoi_dung, accounts_wardenprofile
co_so_cho_thue, phong
khach_thue, nguoi_o_cung
hop_dong
cau_hinh_gia, hoa_don, chi_tiet_hoa_don, lich_su_thanh_toan
yeu_cau_sua_chua, bao_tri, thong_bao
tin_phong, dang_ky_xem_phong
```

`portal` and `reports` currently add no database tables. Standard Django tables such as migrations, content types, permissions, groups, admin log, and sessions are also expected.

Expected legacy tables under the current settings are:

```text
students_student, students_room
attendance_roomattendance, attendance_messattendance
attendance_attendancenotification, attendance_attendancestats
student_requests, request_notifications
fees_feeconfig, fees_feemonth, fees_fine, fees_feepayment
notices_notice, notices_noticereadstatus, notices_systemnotification
```

## Production Disposition

Do not silently carry these legacy tables into the intended clean PostgreSQL database. Schedule a separate approval-gated legacy-exclusion phase before PostgreSQL provisioning. That phase must remove the five apps from the production installed-app set, remove their admin and URL dependencies, verify content-type/permission behavior, and prove a clean migration from zero.

Until that phase is implemented and verified, retain the legacy apps and tables in local development. Removing tables alone would leave settings, imports, URLs, and admin startup inconsistent.

## Editing Boundary

- Do not move, rename, delete, or modernize legacy areas during ordinary RentEase work.
- Do not re-add legacy root routes such as the old students root, `/api/`, or `/fees/` routes.
- Legacy cleanup requires a dedicated dependency review, an approved plan, and the standard Django checks.
- Re-audit the current source before legacy work. Previous dependency-audit evidence is available through Git history but is not proof that dependencies are unchanged.
