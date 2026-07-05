# RentEase - Hệ Thống Quản Lý Nhà Trọ Thông Minh

RentEase là ứng dụng web quản lý nhà trọ và phòng cho thuê, phát triển từ dự án HOSTELLO cũ. Hệ thống hỗ trợ chủ trọ quản lý cơ sở, phòng, khách thuê, hợp đồng, hóa đơn, thanh toán, yêu cầu sửa chữa, tin đăng phòng trống và lịch xem phòng; đồng thời cung cấp cổng tự phục vụ riêng cho khách thuê, báo cáo dành cho nhân viên và Django Admin.

Dự án sử dụng mô hình **monorepo** với Django backend, Django Templates và static assets trong cùng repository. RentEase **không sử dụng React/Vite** và không cần chạy một frontend server riêng.

> **Trạng thái:** phù hợp cho demo local và tiếp tục hoàn thiện trước production. Không sử dụng dữ liệu cá nhân thật, tài liệu định danh thật hoặc thông tin ngân hàng thật trong môi trường demo.

## Kiến Trúc Dự Án

```text
RentEase/
|-- backend/                         # Django backend và các ứng dụng nghiệp vụ
|   |-- hostello_backend/            # Cấu hình Django chính; giữ nguyên module path
|   |-- accounts/                    # Người dùng, hồ sơ chủ trọ và phân vai
|   |-- properties/                  # Cơ sở cho thuê và phòng
|   |-- tenants/                     # Khách thuê và người ở cùng
|   |-- contracts/                   # Hợp đồng thuê
|   |-- billing/                     # Giá, hóa đơn, dòng tiền, PayOS/VietQR
|   |-- maintenance/                 # Sửa chữa, bảo trì và thông báo
|   |-- listings/                    # Tin đăng công khai và đăng ký xem phòng
|   |-- governance/                  # Tài liệu riêng tư và nền tảng audit
|   |-- portal/                      # Cổng Chủ trọ/Khách thuê và dữ liệu demo
|   |-- reports/                     # Báo cáo chỉ dành cho staff
|   |-- manage.py
|   `-- requirements.txt
|-- frontend/
|   |-- templates/                   # Django Templates
|   `-- static/                      # CSS, JavaScript, ảnh và admin assets
|-- docs/                            # Tài liệu sản phẩm, kiến trúc, bảo mật và demo
|-- docker-compose.yml               # PostgreSQL 15 cho môi trường local
|-- AGENTS.md                        # Quy tắc làm việc an toàn trong repository
`-- README.md
```

Các ứng dụng HOSTELLO cũ (`students`, `attendance`, `fees`, `requests`, `notices`) vẫn được giữ trong source để tương thích lịch sử nhưng không phải bề mặt sản phẩm RentEase chính.

## Yêu Cầu Hệ Thống

- **Python:** 3.12+
- **Django:** 5.2.6
- **Database khuyến nghị:** PostgreSQL 15 qua Docker
- **Database fallback:** SQLite khi không cấu hình `DATABASE_URL`
- **Docker Desktop + Docker Compose:** dùng cho PostgreSQL local
- **Frontend:** trình duyệt hiện đại; không cần Node.js/npm
- **Hệ điều hành hướng dẫn chính:** Windows PowerShell

## Hướng Dẫn Khởi Động Nhanh

### 1. Khởi động PostgreSQL

Tại thư mục gốc repository:

```powershell
docker-compose up -d
docker-compose ps
```

PostgreSQL chạy tại `localhost:5432`. Dữ liệu được lưu trong Docker named volume `rentease_pgdata`, không nằm trong Git và không tự động được chia sẻ sang máy khác.

### 2. Tạo môi trường Python

```powershell
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Cấu hình environment

```powershell
Copy-Item .env.example .env
```

Mở `backend/.env` và cấu hình tối thiểu:

```dotenv
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=postgres://<user>:<password>@localhost:5432/rentease_db
```

Không commit `.env`, mật khẩu database, PayOS keys hoặc Django `SECRET_KEY` lên Git.

### 4. Kiểm tra và migrate database

```powershell
.\venv\Scripts\python.exe manage.py check
.\venv\Scripts\python.exe manage.py makemigrations --check --dry-run
.\venv\Scripts\python.exe manage.py migrate
```

### 5. Tạo tài khoản quản trị

```powershell
.\venv\Scripts\python.exe manage.py createsuperuser --username admin
```

Lệnh sẽ yêu cầu bạn tự nhập email và mật khẩu. Không dùng mật khẩu demo cho production.

### 6. Chạy server

```powershell
.\venv\Scripts\python.exe manage.py runserver
```

Mở trình duyệt tại `http://127.0.0.1:8000/`.

## Tài Khoản Demo và Cách Thiết Lập

Repository chỉ công khai **tên tài khoản demo**, không lưu mật khẩu đang hoạt động.

| Tài khoản | Vai trò | Chuẩn bị trên database local |
|---|---|---|
| `admin` | Superuser | Tạo bằng `createsuperuser` hoặc đặt lại mật khẩu local. |
| `owner_test` | Chủ trọ | Tạo user loại `OWNER`, sau đó tạo `UserProfile` liên kết. |
| `tenant_test` | Khách thuê | Tạo user loại `TENANT`, sau đó tạo `Tenant` liên kết. |

Sau khi tài khoản đã tồn tại, đặt mật khẩu riêng trên từng máy:

```powershell
.\venv\Scripts\python.exe manage.py changepassword admin
.\venv\Scripts\python.exe manage.py changepassword owner_test
.\venv\Scripts\python.exe manage.py changepassword tenant_test
```

Bạn có thể tạo `owner_test`, `tenant_test` và các profile liên kết tại `/admin/`. Chỉ dùng dữ liệu giả trong demo.

### Tạo dữ liệu demo

Xem trước mà không ghi database:

```powershell
.\venv\Scripts\python.exe manage.py seed_rentease_demo_data --dry-run --owner-username owner_test --tenant-username tenant_test
```

Tạo hoặc cập nhật Property, phòng, tin đăng, hợp đồng, hóa đơn, thanh toán, sửa chữa, thông báo và lịch xem phòng:

```powershell
.\venv\Scripts\python.exe manage.py seed_rentease_demo_data --owner-username owner_test --tenant-username tenant_test
```

Lệnh seed yêu cầu hai tài khoản demo và profile tương ứng đã tồn tại. Không chạy seed trên production hoặc database có dữ liệu giá trị.

## Cách Sử Dụng Theo Vai Trò

### Khách truy cập (Visitor)

1. Mở `/` để xem trang giới thiệu.
2. Mở `/rooms/` để xem các phòng đang được công khai.
3. Chọn phòng để xem giá, diện tích, sức chứa, ngày có thể vào ở và vị trí công khai an toàn.
4. Gửi biểu mẫu đăng ký xem phòng mà không cần tài khoản.

Khách truy cập không được xem địa chỉ chính xác, dữ liệu hợp đồng, hóa đơn, CCCD hoặc hồ sơ riêng tư.

### Chủ trọ (Owner)

1. Đăng nhập bằng tài khoản có vai trò `OWNER`.
2. Sử dụng dashboard tại `/owner/dashboard/`.
3. Quản lý cơ sở cho thuê, phòng, tin đăng, khách thuê và hợp đồng thuộc quyền sở hữu.
4. Lập/cập nhật hóa đơn, ghi nhận thanh toán và theo dõi công nợ.
5. Xử lý yêu cầu sửa chữa và đăng ký xem phòng.

Mọi truy vấn Owner phải được giới hạn theo hồ sơ chủ trọ hiện tại; Owner không được xem dữ liệu của chủ trọ khác.

### Khách thuê (Tenant)

1. Đăng nhập bằng tài khoản có vai trò `TENANT`.
2. Sử dụng dashboard tại `/tenant/dashboard/`.
3. Xem hồ sơ, hợp đồng, hóa đơn, lịch sử thanh toán và thông báo của chính mình.
4. Gửi yêu cầu sửa chữa an toàn cho phòng đang thuê.
5. Nếu PayOS đã được cấu hình, mở hóa đơn chưa thanh toán và chọn **Thanh toán VietQR**.

Tenant không được xem dữ liệu của khách thuê khác hoặc thông tin nội bộ của người thu tiền.

### Admin và Staff

1. Đăng nhập tại `/admin/`.
2. Quản trị dữ liệu toàn hệ thống theo quyền Django được cấp.
3. Staff hợp lệ có thể xem báo cáo tại `/reports/`.
4. Dữ liệu định danh nhạy cảm không xuất hiện trong danh sách/tìm kiếm admin; non-superuser staff chỉ được đọc các trường nhạy cảm trong trang chi tiết được kiểm soát.

## Tính Năng Chính

- Quản lý tài khoản và phân vai Visitor/Owner/Tenant/Admin/Staff
- Quản lý nhiều cơ sở cho thuê và phòng theo từng chủ trọ
- Quản lý khách thuê, người ở cùng và hợp đồng
- Cấu hình giá thuê, điện, nước, dịch vụ và dòng hóa đơn
- Tính tổng hóa đơn, công nợ, trạng thái thanh toán và chống trả vượt số tiền còn lại
- Ghi nhận thanh toán thủ công và lịch sử thanh toán
- Tích hợp PayOS/VietQR bằng payment intent và webhook có chữ ký
- Quản lý yêu cầu sửa chữa, vòng đời bảo trì và thông báo
- Tin đăng phòng công khai và đăng ký xem phòng
- Dashboard riêng cho Owner và Tenant
- Báo cáo nội bộ dành cho Staff
- Django Admin được tùy biến bằng Jazzmin
- Bảo vệ dữ liệu theo chủ trọ/khách thuê và giới hạn dữ liệu định danh

## Thanh Toán PayOS/VietQR

RentEase không lưu tên đăng nhập, mật khẩu, PIN hoặc OTP ngân hàng. Chủ tài khoản tự liên kết ngân hàng với payOS qua luồng chính thức.

Để bật thanh toán thật, thêm vào `backend/.env`:

```dotenv
PAYOS_CLIENT_ID=
PAYOS_API_KEY=
PAYOS_CHECKSUM_KEY=
```

Webhook hiện được tiếp nhận tại:

```text
/api/billing/webhooks/payos/
```

Khi test từ localhost, cần một HTTPS URL công khai hoặc môi trường deploy thử nghiệm để payOS gửi webhook. Return URL chỉ dùng để điều hướng giao diện; việc ghi nhận thanh toán phải dựa trên webhook hợp lệ.

## URL Quan Trọng

| URL | Mục đích |
|---|---|
| `/` | Trang công khai RentEase |
| `/rooms/` | Danh sách phòng công khai |
| `/login/` | Đăng nhập Owner/Tenant |
| `/owner/dashboard/` | Dashboard Chủ trọ |
| `/owner/properties/` | Quản lý cơ sở cho thuê |
| `/owner/rooms/` | Quản lý phòng |
| `/owner/tenants/` | Quản lý khách thuê |
| `/owner/contracts/` | Quản lý hợp đồng |
| `/owner/invoices/` | Quản lý hóa đơn và thanh toán |
| `/tenant/dashboard/` | Dashboard Khách thuê |
| `/tenant/invoices/` | Hóa đơn và VietQR của khách thuê |
| `/tenant/payments/` | Lịch sử thanh toán khách thuê |
| `/tenant/repairs/` | Yêu cầu sửa chữa khách thuê |
| `/admin/` | Django Admin/Jazzmin |
| `/reports/` | Báo cáo dành cho Staff |
| `/api/billing/webhooks/payos/` | Webhook PayOS |

## Công Nghệ Sử Dụng

### Backend

- **Python 3.12+**: ngôn ngữ backend
- **Django 5.2.6**: web framework, ORM, forms, authentication, sessions và permissions
- **Django REST Framework 3.16.1**: endpoint webhook/API giới hạn; RentEase không phải hệ thống API-first đầy đủ
- **django-jazzmin 3.0.1**: giao diện Django Admin
- **django-cors-headers 4.8.0**: nền tảng cấu hình CORS
- **dj-database-url 3.1.2**: đọc `DATABASE_URL`
- **psycopg2-binary 2.9.10**: kết nối PostgreSQL
- **python-decouple 3.8**: đọc biến môi trường
- **WhiteNoise 6.12.0**: phục vụ static files khi deploy
- **Pillow 11.3.0**: xử lý trường ảnh/uploads
- **Requests**: HTTP client được PayOS adapter sử dụng; cần được pin trong dependencies trước khi clean deployment

### Frontend

- **Django Templates**: server-side rendering
- **HTML5, CSS3 và JavaScript thuần**
- **Bootstrap Icons**: icon giao diện
- **RentEase Design System/DreamPOS direction**: CSS tùy biến cho public, Owner, Tenant, Reports và Admin

### Database, Hạ Tầng và Tích Hợp

- **PostgreSQL 15 Alpine** chạy qua Docker Compose
- **SQLite** làm fallback local khi không có `DATABASE_URL`
- **Docker named volumes** để giữ dữ liệu PostgreSQL qua lần restart
- **PayOS/VietQR** cho payment link, QR và webhook xác nhận thanh toán
- **HMAC-SHA256** để kiểm tra chữ ký request/webhook PayOS
- **Gmail SMTP hoặc SMTP tương thích** cho email khi được cấu hình

### Các Công Nghệ Không Sử Dụng

- Không có React, Vite, Redux Toolkit hoặc React Router
- Không cần Node.js/npm cho frontend hiện tại
- Không dùng JWT/SimpleJWT; đăng nhập hiện dùng Django session authentication
- Không có Swagger/OpenAPI UI công khai
- Không có Celery/Redis hoặc hàng đợi background job
- Không có Kubernetes
- Stripe chỉ là placeholder cũ trong `.env.example`, không phải cổng thanh toán đang hoạt động

## Dữ Liệu PostgreSQL và Docker

Database PostgreSQL được lưu trong Docker named volume, không nằm trong repository. Mỗi máy clone dự án sẽ có volume riêng và cần chạy migrations/seed riêng.

```powershell
docker volume ls
docker-compose ps
```

`docker-compose down` dừng container nhưng giữ dữ liệu. `docker-compose down -v` xóa volume và toàn bộ dữ liệu, vì vậy chỉ dùng khi chắc chắn muốn tạo lại database.

Không commit `.env`, database dump, SQLite database, media uploads, logs hoặc Docker volume.

## Hướng Dẫn Phát Triển và Kiểm Thử

Chạy các lệnh từ `backend/` bằng virtual environment chính thức:

```powershell
.\venv\Scripts\python.exe manage.py check
.\venv\Scripts\python.exe manage.py makemigrations --check --dry-run
.\venv\Scripts\python.exe manage.py test
```

Nguyên tắc quan trọng:

1. Không tạo migration hoặc đổi schema nếu chưa có kế hoạch được duyệt.
2. Không thay đổi authentication, permissions, billing, settings hoặc PayOS một cách trực tiếp.
3. Luôn kiểm tra đúng/sai vai trò và cô lập dữ liệu Owner/Tenant.
4. Không đưa CCCD, tài liệu định danh, credential hoặc dữ liệu thật vào source/test/demo.
5. Không chỉnh/xóa các ứng dụng legacy nếu chưa có kế hoạch dependency và dữ liệu riêng.

## Trạng Thái Dự Án

- **Phiên bản:** 1.0.0
- **Cập nhật:** July 2026
- **Nhánh chuẩn:** `complete-product`
- **Database local hiện hỗ trợ:** PostgreSQL qua Docker, SQLite fallback
- **Trạng thái:** local-demo ready; chưa production-ready
- **Kiểm thử gần nhất:** 83 Django tests đạt trên PostgreSQL local
- **PayOS:** mã tích hợp đã có; cần cấu hình keys và webhook HTTPS để test giao dịch thật

## Tài Liệu Liên Quan

- [`docs/README.md`](docs/README.md)
- [`docs/demo/README.md`](docs/demo/README.md)
- [`docs/agent/RENTEASE_CURRENT_STATE.md`](docs/agent/RENTEASE_CURRENT_STATE.md)
- [`docs/agent/NEXT_ACTION.md`](docs/agent/NEXT_ACTION.md)
- [`docs/agent/RENTEASE_PRODUCT_CONTEXT.md`](docs/agent/RENTEASE_PRODUCT_CONTEXT.md)
- [`docs/agent/RENTEASE_SECURITY_RULES.md`](docs/agent/RENTEASE_SECURITY_RULES.md)
- [`docs/architecture/PROJECT_STRUCTURE_MAP.md`](docs/architecture/PROJECT_STRUCTURE_MAP.md)
- [`docs/architecture/LEGACY_BOUNDARIES.md`](docs/architecture/LEGACY_BOUNDARIES.md)
- [`docs/ui/RENTEASE_PROFESSIONAL_DESIGN_SYSTEM.md`](docs/ui/RENTEASE_PROFESSIONAL_DESIGN_SYSTEM.md)

## Liên Lạc và Hỗ Trợ

Nếu gặp lỗi khi chạy dự án:

1. Kiểm tra `docker-compose ps` và kết nối PostgreSQL.
2. Chạy `manage.py check` và migration dry-run.
3. Đọc `docs/demo/README.md` cho luồng demo.
4. Tạo issue kèm thông báo lỗi đã loại bỏ password, API key, database URL và dữ liệu định danh.

---

**Phiên bản:** 1.0.0 | **Ngày cập nhật:** July 2026
