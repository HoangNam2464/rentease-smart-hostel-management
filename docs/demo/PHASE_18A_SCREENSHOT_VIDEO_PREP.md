# Phase 18A: Screenshot Capture And Demo Video Preparation

## Purpose

This guide prepares the final manual screenshot capture and 3 to 5 minute demo video recording for RentEase.

It does not change application code, database schema, billing logic, permissions, or production settings.

Use this guide together with:

```text
docs/ui/PHASE_17C_FINAL_VISUAL_QA.md
docs/demo/SCREENSHOT_CHECKLIST.md
docs/demo/DEMO_SCRIPT.md
docs/demo/FINAL_DEMO_PACKAGE.md
```

## Pre-Recording Setup

From the repository root:

```powershell
cd hostello_backend
```

Run safety checks:

```powershell
.\venv\Scripts\python.exe manage.py check
.\venv\Scripts\python.exe manage.py makemigrations --check --dry-run
```

Seed fake local demo data:

```powershell
.\venv\Scripts\python.exe manage.py seed_rentease_demo_data --owner-username owner_test --tenant-username tenant_test
```

Start the local server:

```powershell
.\venv\Scripts\python.exe manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

Recommended browser setup:

- Browser zoom: 100%
- Desktop recording width: about 1366px
- Optional mobile check width: about 390px
- Use a clean browser window with bookmarks/sidebar hidden
- Do not show terminal windows containing passwords, paths, secrets, or database files

Demo accounts:

| Role | Username | Password |
| --- | --- | --- |
| Admin | `admin_test` | `Test@12345` |
| Owner | `owner_test` | `Test@12345` |
| Tenant | `tenant_test` | `Test@12345` |

Do not show passwords in screenshots or the recorded video.

## Screenshot Capture Order

### Public

1. Landing page: `/`
2. Room list: `/rooms/`
3. Room detail: open one published demo room from `/rooms/`
4. Viewing registration form: `/rooms/<published_id>/register/`
5. Viewing registration success page: `/rooms/<published_id>/register/success/`
6. Login page: `/login/`

### Owner

Log in as `owner_test`.

1. Owner dashboard: `/owner/dashboard/`
2. Rooms: `/owner/rooms/`
3. Listings: `/owner/listings/`
4. Tenants: `/owner/tenants/`
5. Contracts: `/owner/contracts/`
6. Invoices: `/owner/invoices/`
7. Invoice detail or payment recording page if available
8. Repairs: `/owner/repairs/`
9. Viewing registrations: `/owner/viewing-registrations/`

### Tenant

Log in as `tenant_test`.

1. Tenant dashboard: `/tenant/dashboard/`
2. Profile: `/tenant/profile/`
3. Contracts: `/tenant/contracts/`
4. Invoices: `/tenant/invoices/`
5. Payments: `/tenant/payments/`
6. Repairs: `/tenant/repairs/`
7. Notifications: `/tenant/notifications/`

### Other

1. 404 page: open an obviously invalid route such as `/not-found-demo/`
2. Reports protected behavior: open `/reports/` as anonymous if you want to show staff-only protection
3. Admin login: `/admin/` only if the presentation needs to mention Django Admin/Jazzmin
4. Legacy isolation: `/legacy/login/` only if the presentation needs to mention old HOSTELLO isolation

## Video Demo Outline

Target length: 3 to 5 minutes.

| Time | Segment | What To Show |
| --- | --- | --- |
| 0:00-0:30 | Intro and project purpose | Landing page, short product explanation |
| 0:30-1:15 | Public room browsing | Room list, room detail, viewing registration form |
| 1:15-2:30 | Owner dashboard and management | Owner dashboard, rooms, invoices, payment, repairs, viewing registrations |
| 2:30-3:30 | Tenant portal | Tenant dashboard, contract/invoices/payments/repairs/notifications |
| 3:30-4:15 | Demo data, security, privacy | Explain fake demo data, role scoping, protected reports/admin |
| 4:15-5:00 | Conclusion and limitations | Local demo readiness, remaining production work |

Keep transitions short. The safest flow is:

```text
/ -> /rooms/ -> room detail -> viewing registration form -> /login/ -> owner dashboard -> owner invoices/payment -> tenant dashboard -> tenant invoices/payments -> conclusion
```

## Vietnamese Narration Script

### 0:00-0:30 - Gioi thieu

Xin chao thay co va cac ban. Day la RentEase, mot he thong quan ly nha tro duoc xay dung bang Django. Muc tieu cua he thong la ho tro chu tro quan ly phong, khach thue, hop dong, hoa don, thanh toan, yeu cau sua chua, tin dang phong va lich xem phong.

### 0:30-1:15 - Trang cong khai

O phan cong khai, nguoi xem co the vao danh sach phong dang cho thue. Trang chi hien thi thong tin an toan cho khach tham quan, khong hien thi du lieu rieng nhu hop dong, hoa don hay thong tin noi bo cua chu tro. Neu quan tam mot phong, khach co the mo chi tiet phong va gui dang ky xem phong.

### 1:15-2:30 - Cong thong tin chu tro

Sau khi dang nhap bang tai khoan chu tro, he thong chuyen den dashboard rieng cua chu tro. Dashboard tong hop so phong, hop dong, hoa don, thanh toan, sua chua va lich xem phong. Cac trang quan ly deu duoc gioi han theo chu tro hien tai, nen chu tro chi nhin thay du lieu cua minh.

O day co the xem danh sach phong, tin dang, khach thue da lien ket, hop dong, hoa don va lich su thanh toan. Viec ghi nhan thanh toan duoc thuc hien tu chi tiet hoa don de tranh sua truc tiep cac truong tinh tien quan trong.

### 2:30-3:30 - Cong thong tin khach thue

Voi tai khoan khach thue, he thong hien thi dashboard rieng cho khach. Khach thue co the xem thong tin ca nhan, hop dong, hoa don, lich su thanh toan, yeu cau sua chua va thong bao cua minh. Cac trang nay khong hien thi du lieu cua khach thue khac, khong hien thi thong tin nhay cam nhu can cuoc cong dan hay truong quan tri noi bo.

### 3:30-4:15 - Du lieu demo va bao mat

Du lieu trong ban demo la du lieu gia lap, duoc tao bang lenh seed rieng cho demo. He thong tach ro vai tro cong khai, chu tro, khach thue va nhan vien quan tri. Trang bao cao va admin duoc bao ve, cac route legacy cu khong con mo o muc root.

### 4:15-5:00 - Ket luan

Hien tai RentEase da san sang cho demo cuc bo va trinh bay mon hoc. Cac phan can lam tiep neu dua len san pham that gom cau hinh production, co so du lieu production, static/media/email/logging, quy trinh tai khoan va cai tien chi tiet nghiep vu tinh tien dien nuoc.

## Manual Visual QA Checklist

Before recording, quickly confirm:

- [ ] no broken layout on desktop
- [ ] no horizontal overflow on desktop
- [ ] no raw Django template tags such as `{% block %}` or `{% url %}`
- [ ] no citizen ID values
- [ ] no citizen ID images/files
- [ ] no auth/password/permission fields
- [ ] no payment collector internals
- [ ] no owner private notes on public or tenant pages
- [ ] buttons are visible and readable
- [ ] tables are readable
- [ ] forms have clear labels
- [ ] demo data exists on public, owner, and tenant pages
- [ ] reports remain staff-only
- [ ] `/api/requests/` and `/fees/` remain unavailable at root

## Known Limitations To Mention Honestly

- RentEase is local-demo ready, not production-ready.
- Screenshots and video are captured manually.
- Production database and production settings are not configured yet.
- Deployment, static/media, email, logging, and CI are future work.
- Owner-facing utility/billing detail workflows can be improved later.
- Account onboarding and lifecycle are still incomplete for real production.

## Final Recommendation

For course presentation, record the public flow first, then owner management, then tenant self-service, and end by explaining privacy and production limitations.

Recommended next manual action:

```text
Run the local server, capture screenshots, then record the 3 to 5 minute demo video.
```

Optional later phase:

```text
Phase 18B: Final Submission Package Review
```
