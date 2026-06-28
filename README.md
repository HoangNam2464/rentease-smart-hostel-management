# RentEase - Hệ Thống Quản Lý Phòng Trọ Thông Minh

RentEase là một ứng dụng web Django dùng để quản lý nhà trọ/phòng trọ. Hệ thống hỗ trợ quản lý phòng, khách thuê, hợp đồng, hóa đơn, thanh toán, yêu cầu sửa chữa, bảo trì, tin đăng phòng trống, đăng ký xem phòng, báo cáo và vận hành qua Django Admin.

Dự án hiện dùng cấu trúc monorepo theo phong cách FoodieGo với `backend/`, `frontend/` và `docs/`. Khác với FoodieGo, RentEase không dùng React/Vite. Frontend của RentEase là Django Templates kết hợp HTML, CSS và JavaScript tĩnh.

## Project Architecture

```text
RentEase/
├── backend/                     # Django backend
│   ├── hostello_backend/        # Main Django config package
│   ├── accounts/                # User accounts and profiles
│   ├── properties/              # Properties and rooms
│   ├── tenants/                 # Tenant management
│   ├── contracts/               # Rental contracts
│   ├── billing/                 # Invoices and payments
│   ├── maintenance/             # Maintenance requests
│   ├── listings/                # Public room listings
│   ├── portal/                  # Owner/Tenant portal views
│   ├── reports/                 # Reports
│   ├── manage.py
│   └── requirements.txt
├── frontend/                    # Django Templates + static assets
│   ├── templates/
│   └── static/
├── docs/                        # Project documentation
└── README.md
```

Important:

- `backend/hostello_backend/` là package cấu hình Django chính, vẫn giữ module path `hostello_backend.settings`.
- `frontend/templates/` chứa Django templates.
- `frontend/static/` chứa CSS, JavaScript và static assets.
- Không có frontend React/Vite riêng.

## System Requirements

- Python 3.12+
- Django 5.2+
- SQLite cho local demo
- PostgreSQL-ready nếu triển khai production sau này
- Windows PowerShell commands được dùng trong README này
- Không cần Node.js/npm cho frontend hiện tại

## Quick Start

Mở terminal tại thư mục gốc repository, sau đó vào Django backend:

```powershell
cd backend
```

Nếu `backend/venv/` đã tồn tại:

```powershell
.\venv\Scripts\activate
```

Nếu cần tạo virtual environment mới:

```powershell
python -m venv venv
.\venv\Scripts\activate
```

Cài dependencies:

```powershell
pip install -r requirements.txt
```

Chạy kiểm tra Django:

```powershell
.\venv\Scripts\python.exe manage.py check
.\venv\Scripts\python.exe manage.py makemigrations --check --dry-run
```

Chạy migrations:

```powershell
.\venv\Scripts\python.exe manage.py migrate
```

Tạo superuser:

```powershell
.\venv\Scripts\python.exe manage.py createsuperuser
```

Chạy server:

```powershell
.\venv\Scripts\python.exe manage.py runserver
```

Mở trình duyệt:

```text
http://127.0.0.1:8000/
```

## Frontend Note

RentEase không có React/Vite frontend và không cần chạy `npm run dev`.

Frontend hiện tại được render bằng Django Templates:

- Templates: `frontend/templates/`
- Static assets: `frontend/static/`
- CSS/JS được phục vụ qua Django static files

## Main Features

- ✅ User/account management
- ✅ Owner dashboard
- ✅ Tenant dashboard
- ✅ Room management
- ✅ Tenant management
- ✅ Contract management
- ✅ Invoice management
- ✅ Payment recording
- ✅ Payment history
- ✅ Maintenance request management
- ✅ Public room listings
- ✅ Viewing registration
- ✅ Reports
- ✅ Django Admin/Jazzmin
- ✅ Role-based data access

## Main User Roles

| Role | Description |
|---|---|
| Visitor | Xem danh sách phòng công khai và đăng ký xem phòng. |
| Owner | Quản lý phòng, khách thuê, hợp đồng, hóa đơn, thanh toán, sửa chữa, tin đăng và báo cáo của chính mình. |
| Tenant | Xem thông tin thuê phòng, hợp đồng, hóa đơn, thanh toán, yêu cầu sửa chữa và thông báo của chính mình. |
| Admin/Staff | Quản trị hệ thống qua Django Admin/Jazzmin và xem báo cáo nội bộ. |

## Important URLs

| URL | Purpose |
|---|---|
| `/` | Public landing page |
| `/rooms/` | Public room listings |
| `/login/` | Portal login |
| `/admin/` | Django Admin/Jazzmin |
| `/reports/` | Staff reports |
| `/owner/dashboard/` | Owner dashboard |
| `/owner/rooms/` | Owner room management |
| `/owner/tenants/` | Owner tenant management |
| `/owner/contracts/` | Owner contract management |
| `/owner/invoices/` | Owner invoice management |
| `/tenant/dashboard/` | Tenant dashboard |
| `/tenant/invoices/` | Tenant invoices |
| `/tenant/payments/` | Tenant payment history |
| `/legacy/login/` | Legacy HOSTELLO login route, kept isolated |

## Technology Stack

### Backend

- Python
- Django
- Django ORM
- Django Forms
- Django Admin
- Jazzmin
- SQLite local demo
- PostgreSQL-ready

### Frontend

- Django Templates
- HTML5
- CSS3
- JavaScript
- Static files

### Documentation

- Markdown
- Mermaid
- Architecture docs
- Demo docs
- Security docs

## Development Guide

Recommended workflow:

1. Work on branch `complete-product`.
2. Run Django commands from `backend/`.
3. Use the official virtual environment at `backend/venv/`.
4. After changes, run:

```powershell
.\venv\Scripts\python.exe manage.py check
.\venv\Scripts\python.exe manage.py makemigrations --check --dry-run
```

5. Commit only after checks pass.
6. Do not push unless explicitly approved.

## Safety Notes

- Do not rename `backend/hostello_backend/` casually.
- Do not move apps into `backend/apps/` without a dedicated phase.
- Do not delete legacy apps yet: `students`, `attendance`, `fees`, `requests`, `notices`.
- Do not delete templates/static/media without dependency review.
- Do not use a root-level `venv/`.
- Official local virtual environment is `backend/venv/`.
- Do not create migrations unless explicitly required.
- Do not change database schema unless explicitly required.

## Project Status

Completed milestones:

- Backend/frontend restructure completed.
- Django templates moved to `frontend/templates/`.
- Static assets moved to `frontend/static/`.
- Reports templates moved to `frontend/templates/reports/`.
- Root `venv/` removed safely.
- Legacy dependency audit completed.
- Helper files archived.
- Django checks pass.
- No pending migrations detected.

Current status:

- Version: `1.0.0`
- Updated: June 2026
- Branch: `complete-product`
- Status: Local demo ready
- Production readiness: Not production-ready yet

## Related Documentation

- `docs/README.md`
- `docs/agent/RENTEASE_CURRENT_STATE.md`
- `docs/agent/NEXT_ACTION.md`
- `docs/agent/RENTEASE_PRODUCT_CONTEXT.md`
- `docs/architecture/PROJECT_STRUCTURE_MAP.md`
- `docs/architecture/LEGACY_BOUNDARIES.md`
- `docs/ui/RENTEASE_PROFESSIONAL_DESIGN_SYSTEM.md`
- `docs/demo/README.md`

Historical audits, plans, phase reports, and superseded rules are available through Git history and tags. See `docs/archive/README.md` only when historical evidence is required.

## Contact / Support

This is a student/project development repository. For setup or maintenance, start with:

1. `README.md`
2. `AGENTS.md`
3. `docs/agent/RENTEASE_CURRENT_STATE.md`
4. `docs/agent/NEXT_ACTION.md`

For agent-assisted work, the repo-local skill is `.agents/skills/rentease/SKILL.md`.

When in doubt, run Django checks before changing code:

```powershell
cd backend
.\venv\Scripts\python.exe manage.py check
.\venv\Scripts\python.exe manage.py makemigrations --check --dry-run
```
