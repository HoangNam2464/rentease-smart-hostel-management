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
cd backend
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

### 0:00-0:30 - Giới thiệu

Xin chào thầy cô và các bạn. Đây là RentEase, một hệ thống quản lý nhà trọ được xây dựng bằng Django. Mục tiêu của hệ thống là hỗ trợ chủ trọ quản lý phòng, khách thuê, hợp đồng, hóa đơn, thanh toán, yêu cầu sửa chữa, tin đăng phòng và lịch xem phòng.

### 0:30-1:15 - Trang công khai

Ở phần công khai, người xem có thể vào danh sách phòng đang cho thuê. Trang chỉ hiển thị thông tin an toàn cho khách tham quan, không hiển thị dữ liệu riêng như hợp đồng, hóa đơn hay thông tin nội bộ của chủ trọ. Nếu quan tâm một phòng, khách có thể mở chi tiết phòng và gửi đăng ký xem phòng.

### 1:15-2:30 - Cổng thông tin chủ trọ

Sau khi đăng nhập bằng tài khoản chủ trọ, hệ thống chuyển đến dashboard riêng của chủ trọ. Dashboard tổng hợp số phòng, hợp đồng, hóa đơn, thanh toán, sửa chữa và lịch xem phòng. Các trang quản lý đều được giới hạn theo chủ trọ hiện tại, nên chủ trọ chỉ nhìn thấy dữ liệu của mình.

Ở đây có thể xem danh sách phòng, tin đăng, khách thuê đã liên kết, hợp đồng, hóa đơn và lịch sử thanh toán. Việc ghi nhận thanh toán được thực hiện từ chi tiết hóa đơn để tránh sửa trực tiếp các trường tính tiền quan trọng.

### 2:30-3:30 - Cổng thông tin khách thuê

Với tài khoản khách thuê, hệ thống hiển thị dashboard riêng cho khách. Khách thuê có thể xem thông tin cá nhân, hợp đồng, hóa đơn, lịch sử thanh toán, yêu cầu sửa chữa và thông báo của mình. Các trang này không hiển thị dữ liệu của khách thuê khác, không hiển thị thông tin nhạy cảm như căn cước công dân hay trường quản trị nội bộ.

### 3:30-4:15 - Du lieu demo va bao mat

Dữ liệu trong bản demo là dữ liệu giả lập, được tạo bằng lệnh seed riêng cho demo. Hệ thống tách rõ vai trò công khai, chủ trọ, khách thuê và nhân viên quản trị. Trang báo cáo và admin được bảo vệ, các route legacy cũ không còn mở ở mức root.

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
