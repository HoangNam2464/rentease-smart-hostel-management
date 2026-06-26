# RentEase Project Structure Map

## Mục Đích

Tài liệu này ghi lại cấu trúc hiện tại của RentEase và đề xuất hướng tách dần thành cấu trúc dễ hiểu hơn theo kiểu:

```text
RentEase/
├── backend/
├── frontend/
└── docs/
```

Phase hiện tại chỉ kiểm kê và lập kế hoạch. Chưa di chuyển file, chưa đổi import, chưa đổi settings, chưa đổi template path, chưa đổi static path.

## Cấu Trúc Hiện Tại

```text
HOSTELLO-Automated_Smart_Hostel_Management_System_using_Django-main/
├── AGENTS.md
├── README.md
├── docs/
├── assets/
├── hostello_backend/
│   ├── manage.py
│   ├── requirements.txt
│   ├── db.sqlite3                  # local database, không nên commit
│   ├── media/                      # local uploaded/demo media
│   ├── static/
│   ├── templates/
│   ├── hostello_backend/
│   ├── accounts/
│   ├── properties/
│   ├── tenants/
│   ├── contracts/
│   ├── billing/
│   ├── maintenance/
│   ├── listings/
│   ├── portal/
│   ├── reports/
│   ├── students/
│   ├── attendance/
│   ├── fees/
│   ├── requests/
│   └── notices/
└── venv/                           # local virtual environment, không nên commit
```

## Manage.py Và Settings Module

- `manage.py` hiện nằm tại: `hostello_backend/manage.py`
- Django settings module hiện tại: `hostello_backend.settings`
- File settings hiện tại: `hostello_backend/hostello_backend/settings.py`
- Root URLConf hiện tại: `hostello_backend.urls`
- File URL chính: `hostello_backend/hostello_backend/urls.py`

## Current Backend Files/Folders

### Django config

```text
hostello_backend/hostello_backend/
├── settings.py
├── urls.py
├── wsgi.py
└── asgi.py
```

### Active RentEase apps

```text
hostello_backend/accounts/
hostello_backend/properties/
hostello_backend/tenants/
hostello_backend/contracts/
hostello_backend/billing/
hostello_backend/maintenance/
hostello_backend/listings/
hostello_backend/portal/
hostello_backend/reports/
```

### Legacy HOSTELLO apps

```text
hostello_backend/students/
hostello_backend/attendance/
hostello_backend/fees/
hostello_backend/requests/
hostello_backend/notices/
```

Các app legacy vẫn còn trong `INSTALLED_APPS` để giữ tương thích/lịch sử. Không xóa nếu chưa có dependency audit riêng.

## Current Frontend Template Files/Folders

### Global template directory

Django hiện dùng:

```python
TEMPLATES["DIRS"] = [BASE_DIR / "templates"]
```

Tức thư mục template chính là:

```text
hostello_backend/templates/
```

Các nhóm template chính:

```text
hostello_backend/templates/home.html
hostello_backend/templates/404.html
hostello_backend/templates/500.html
hostello_backend/templates/portal/
hostello_backend/templates/listings/
hostello_backend/templates/admin/
hostello_backend/templates/payments/
```

### App templates

Reports hiện có template nằm trong app:

```text
hostello_backend/reports/templates/reports/
```

Điều này đang hoạt động nhờ `APP_DIRS=True`.

### Legacy templates

Một số template HOSTELLO cũ vẫn còn:

```text
hostello_backend/templates/index.html
hostello_backend/templates/login.html
hostello_backend/templates/dashboard.html
hostello_backend/templates/admin/
hostello_backend/templates/payments/success.html
```

Không dùng các file này cho RentEase UI mới nếu chưa được duyệt.

## Current Static Files/Folders

Django hiện dùng:

```python
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
```

Thư mục static chính:

```text
hostello_backend/static/
```

Các file đang thấy:

```text
hostello_backend/static/css/rentease-design.css
hostello_backend/static/css/rentease-layout.css
hostello_backend/static/css/styles.css
hostello_backend/static/css/student-dashboard.css
hostello_backend/static/js/script.js
hostello_backend/static/js/student-dashboard.js
hostello_backend/static/admin/css/custom_admin.css
```

RentEase UI hiện chủ yếu dùng:

```text
hostello_backend/static/css/rentease-design.css
hostello_backend/static/css/rentease-layout.css
hostello_backend/static/admin/css/custom_admin.css
```

Legacy/static cũ cần cẩn thận:

```text
hostello_backend/static/css/styles.css
hostello_backend/static/css/student-dashboard.css
hostello_backend/static/js/script.js
hostello_backend/static/js/student-dashboard.js
assets/
```

## Current Database/Model Files

Các model chính:

```text
hostello_backend/accounts/models.py
hostello_backend/properties/models.py
hostello_backend/tenants/models.py
hostello_backend/contracts/models.py
hostello_backend/billing/models.py
hostello_backend/maintenance/models.py
hostello_backend/listings/models.py
```

Legacy model files:

```text
hostello_backend/students/models.py
hostello_backend/attendance/models.py
hostello_backend/fees/models.py
hostello_backend/requests/models.py
hostello_backend/notices/models.py
```

Database local hiện tại:

```text
hostello_backend/db.sqlite3
```

Không commit database local.

## Current Media/Upload Folders

Media config hiện tại:

```python
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
```

Thư mục media hiện tại:

```text
hostello_backend/media/
```

Nội dung media có thể gồm ảnh/demo upload từ dự án cũ và local data. Không nên commit media thật hoặc dữ liệu có thông tin cá nhân.

## Current Documentation Folders

```text
docs/agent/
docs/demo/
docs/security/
docs/spqm/
docs/ui/
```

Nên bổ sung và duy trì:

```text
docs/architecture/
```

## Possibly Unused Or Unclear Files

Các mục cần audit riêng trước khi xóa/di chuyển:

```text
assets/
run_backend.bat
run_frontend.bat
Working.py
backup_phase2.json
backup_phase3.json
backup_phase4.json
backup_phase5.json
hostello_backend/phase8b2_wip.patch
hostello_backend/static/css/styles.css
hostello_backend/static/js/script.js
```

Không xóa các file này trong phase hiện tại. Một số có thể là di sản HOSTELLO hoặc công cụ local.

## Recommended Future Backend/Frontend Structure

Định hướng dài hạn:

```text
RentEase/
├── backend/
│   ├── config/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── asgi.py
│   ├── apps/
│   │   ├── accounts/
│   │   ├── rooms/
│   │   ├── tenants/
│   │   ├── contracts/
│   │   ├── billing/
│   │   ├── repairs/
│   │   ├── reports/
│   │   └── portal/
│   ├── manage.py
│   └── requirements.txt
├── frontend/
│   ├── templates/
│   │   ├── base/
│   │   ├── portal/
│   │   │   ├── owner/
│   │   │   ├── tenant/
│   │   │   └── public/
│   │   └── reports/
│   └── static/
│       ├── rentease/
│       │   ├── css/
│       │   ├── js/
│       │   └── img/
│       └── vendor/
├── docs/
└── README.md
```

Không áp dụng toàn bộ cấu trúc này trong một bước.

## Files Safe To Move Later

Có thể di chuyển dần trong các phase nhỏ:

- Public templates trong `hostello_backend/templates/listings/`
- Portal templates trong `hostello_backend/templates/portal/`
- Global public templates như `home.html`, `404.html`, `500.html`
- Reports templates trong `hostello_backend/reports/templates/reports/`, nếu cập nhật đúng template discovery/render path
- RentEase CSS trong `hostello_backend/static/css/rentease-design.css`
- Portal layout CSS trong `hostello_backend/static/css/rentease-layout.css`

Mỗi nhóm di chuyển phải chạy route smoke test ngay sau đó.

## Files That Should Not Be Moved Yet

Không nên di chuyển trong các phase đầu:

- `hostello_backend/manage.py`
- `hostello_backend/hostello_backend/settings.py`
- `hostello_backend/hostello_backend/urls.py`
- Django app folders như `accounts`, `properties`, `tenants`, `contracts`, `billing`, `maintenance`, `listings`, `portal`, `reports`
- Migration folders
- Model files
- Legacy apps
- Media upload folder
- Database local

Lý do: các file này liên quan trực tiếp đến import path, app label, migration history, admin registration và URL routing.

## Risks When Moving Django Apps

Di chuyển app Django có thể gây lỗi:

- `INSTALLED_APPS` sai path
- `AppConfig.name` sai
- migration dependency bị lệch
- admin registration không load
- import trong views/forms/services lỗi
- content type/app label thay đổi ngoài ý muốn
- dữ liệu cũ không khớp app label mới

Vì vậy không di chuyển app vào `backend/apps/` nếu chưa có phase riêng và kế hoạch rollback.

## Risks When Moving Templates

Di chuyển template có thể gây lỗi:

- `render(request, "...")` không tìm thấy template
- `{% extends %}` trỏ sai path
- `{% include %}` trỏ sai path
- template cùng tên bị ưu tiên khác do `APP_DIRS=True`
- route vẫn chạy nhưng render sai shell public/owner/tenant

Nếu di chuyển template, cần di chuyển theo từng nhóm nhỏ và kiểm tra route ngay.

## Risks When Moving Static Files

Di chuyển static có thể gây lỗi:

- `{% static %}` trỏ sai file
- admin custom CSS không load
- public/owner/tenant layout mất style
- file legacy và RentEase bị trộn
- `collectstatic` hoặc `STATICFILES_DIRS` bị sai

Không xóa static cũ cho đến khi mọi reference đã được cập nhật và kiểm tra.

## Step-By-Step Migration Plan For Later Phases

## Phase 2 Frontend Folder Preparation

Phase 2 đã chuẩn bị thư mục `frontend/` ở root repository để làm nơi tổ chức Django templates và static assets trong các phase sau.

Thư mục mới:

```text
frontend/
├── templates/
│   ├── base/
│   ├── portal/
│   │   ├── owner/
│   │   ├── tenant/
│   │   └── public/
│   └── reports/
└── static/
    ├── rentease/
    │   ├── css/
    │   ├── js/
    │   └── img/
    └── vendor/
```

Ghi chú an toàn:

- Chưa di chuyển template nào.
- Chưa di chuyển static file nào.
- Đường dẫn template cũ `hostello_backend/templates/` vẫn hoạt động.
- App templates như `reports/templates/reports/` vẫn hoạt động qua `APP_DIRS=True`.
- Đường dẫn static cũ `hostello_backend/static/` vẫn hoạt động.
- `frontend/templates/` đã được thêm vào `TEMPLATES["DIRS"]` để Django có thể nhận template mới trong tương lai.
- `frontend/static/` đã được thêm vào `STATICFILES_DIRS` để Django có thể nhận static mới trong tương lai.
- Các thư mục rỗng có `.gitkeep` để Git theo dõi.

Phase này chỉ là bước chuẩn bị. Các phase sau mới xem xét di chuyển template/static theo từng nhóm nhỏ, sau khi review `render()`, `{% extends %}`, `{% include %}`, `{% static %}` và route smoke test.

### Phase 2: Prepare Frontend Folder

1. Tạo `frontend/templates/`.
2. Tạo `frontend/static/`.
3. Không di chuyển template/static ngay.
4. Chỉ thêm vào `TEMPLATES["DIRS"]` hoặc `STATICFILES_DIRS` nếu cần và an toàn.
5. Giữ đường dẫn cũ hoạt động.
6. Chạy `manage.py check`.
7. Chạy `makemigrations --check --dry-run`.

### Phase 3: Move Public Templates

1. Di chuyển public templates trước vì ít phụ thuộc owner/tenant hơn.
2. Cập nhật `TemplateView`, `render()`, `{% extends %}`, `{% include %}`.
3. Kiểm tra `/`, `/rooms/`, room detail, viewing registration form/success.

### Phase 4: Move Owner/Tenant Templates

1. Di chuyển owner templates theo nhóm nhỏ: dashboard, rooms, tenants, contracts, invoices, payments, repairs, viewing registrations.
2. Di chuyển tenant templates theo nhóm nhỏ: dashboard, profile, contracts, invoices, payments, repairs, notifications.
3. Kiểm tra owner/tenant role access và data scoping sau từng nhóm.

### Phase 5: Move Reports Templates

1. Di chuyển `reports/templates/reports/` nếu thật sự cần.
2. Đảm bảo staff-only access không đổi.
3. Kiểm tra `/reports/` và các report con.

### Phase 6: Organize Static Files

1. Tạo `frontend/static/rentease/css/`, `js/`, `img/`.
2. Copy trước, đổi reference sau, chưa xóa file cũ.
3. Cập nhật `{% static %}` theo từng nhóm.
4. Kiểm tra public/owner/tenant/reports/admin CSS.

### Phase 7: Backend Folder Migration

Chỉ thực hiện nếu được duyệt riêng. Đây là phase rủi ro cao.

Không di chuyển:

- Django apps
- `manage.py`
- config package
- migrations

cho đến khi có kế hoạch chi tiết về import path, app labels, migration compatibility và rollback.

## Current Recommendation

Hoàn tất Phase 1 bằng tài liệu trước. Phase tiếp theo an toàn nhất là Phase 2: tạo `frontend/templates/` và `frontend/static/` rỗng hoặc có file placeholder, sau đó thêm cấu hình template/static chỉ khi thật sự cần và kiểm tra kỹ.
