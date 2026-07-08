# RentEase - Há»‡ Thá»‘ng Quáº£n LÃ½ NhÃ  Trá» ThÃ´ng Minh

RentEase lÃ  á»©ng dá»¥ng web quáº£n lÃ½ nhÃ  trá» vÃ  phÃ²ng cho thuÃª, phÃ¡t triá»ƒn tá»« dá»± Ã¡n HOSTELLO cÅ©. Há»‡ thá»‘ng há»— trá»£ chá»§ trá» quáº£n lÃ½ cÆ¡ sá»Ÿ, phÃ²ng, khÃ¡ch thuÃª, há»£p Ä‘á»“ng, hÃ³a Ä‘Æ¡n, thanh toÃ¡n, yÃªu cáº§u sá»­a chá»¯a, tin Ä‘Äƒng phÃ²ng trá»‘ng vÃ  lá»‹ch xem phÃ²ng; Ä‘á»“ng thá»i cung cáº¥p cá»•ng tá»± phá»¥c vá»¥ riÃªng cho khÃ¡ch thuÃª, bÃ¡o cÃ¡o dÃ nh cho nhÃ¢n viÃªn vÃ  Django Admin.

Dá»± Ã¡n sá»­ dá»¥ng mÃ´ hÃ¬nh **monorepo** vá»›i Django backend, Django Templates vÃ  static assets trong cÃ¹ng repository. RentEase **khÃ´ng sá»­ dá»¥ng React/Vite** vÃ  khÃ´ng cáº§n cháº¡y má»™t frontend server riÃªng.

> **Tráº¡ng thÃ¡i:** phÃ¹ há»£p cho demo local vÃ  tiáº¿p tá»¥c hoÃ n thiá»‡n trÆ°á»›c production. KhÃ´ng sá»­ dá»¥ng dá»¯ liá»‡u cÃ¡ nhÃ¢n tháº­t, tÃ i liá»‡u Ä‘á»‹nh danh tháº­t hoáº·c thÃ´ng tin ngÃ¢n hÃ ng tháº­t trong mÃ´i trÆ°á»ng demo.

## Kiáº¿n TrÃºc Dá»± Ãn

```text
RentEase/
|-- backend/                         # Django backend vÃ  cÃ¡c á»©ng dá»¥ng nghiá»‡p vá»¥
|   |-- hostello_backend/            # Cáº¥u hÃ¬nh Django chÃ­nh; giá»¯ nguyÃªn module path
|   |-- accounts/                    # NgÆ°á»i dÃ¹ng, há»“ sÆ¡ chá»§ trá» vÃ  phÃ¢n vai
|   |-- properties/                  # CÆ¡ sá»Ÿ cho thuÃª vÃ  phÃ²ng
|   |-- tenants/                     # KhÃ¡ch thuÃª vÃ  ngÆ°á»i á»Ÿ cÃ¹ng
|   |-- contracts/                   # Há»£p Ä‘á»“ng thuÃª
|   |-- billing/                     # GiÃ¡, hÃ³a Ä‘Æ¡n, dÃ²ng tiá»n, PayOS/VietQR
|   |-- maintenance/                 # Sá»­a chá»¯a, báº£o trÃ¬ vÃ  thÃ´ng bÃ¡o
|   |-- listings/                    # Tin Ä‘Äƒng cÃ´ng khai vÃ  Ä‘Äƒng kÃ½ xem phÃ²ng
|   |-- governance/                  # TÃ i liá»‡u riÃªng tÆ° vÃ  ná»n táº£ng audit
|   |-- portal/                      # Cá»•ng Chá»§ trá»/KhÃ¡ch thuÃª vÃ  dá»¯ liá»‡u demo
|   |-- reports/                     # BÃ¡o cÃ¡o chá»‰ dÃ nh cho staff
|   |-- manage.py
|   `-- requirements.txt
|-- frontend/
|   |-- templates/                   # Django Templates
|   `-- static/                      # CSS, JavaScript, áº£nh vÃ  admin assets
|-- docs/                            # TÃ i liá»‡u sáº£n pháº©m, kiáº¿n trÃºc, báº£o máº­t vÃ  demo
|-- docker-compose.yml               # PostgreSQL 15 cho mÃ´i trÆ°á»ng local
|-- AGENTS.md                        # Quy táº¯c lÃ m viá»‡c an toÃ n trong repository
`-- README.md
```

CÃ¡c á»©ng dá»¥ng HOSTELLO cÅ© (`students`, `attendance`, `fees`, `requests`, `notices`) váº«n Ä‘Æ°á»£c giá»¯ trong source Ä‘á»ƒ tÆ°Æ¡ng thÃ­ch lá»‹ch sá»­ nhÆ°ng khÃ´ng pháº£i bá» máº·t sáº£n pháº©m RentEase chÃ­nh.

## YÃªu Cáº§u Há»‡ Thá»‘ng

- **Python:** 3.12+
- **Django:** 5.2.6
- **Database khuyáº¿n nghá»‹:** PostgreSQL 15 qua Docker
- **Database fallback:** SQLite khi khÃ´ng cáº¥u hÃ¬nh `DATABASE_URL`
- **Docker Desktop + Docker Compose:** dÃ¹ng cho PostgreSQL local
- **Frontend:** trÃ¬nh duyá»‡t hiá»‡n Ä‘áº¡i; khÃ´ng cáº§n Node.js/npm
- **Há»‡ Ä‘iá»u hÃ nh hÆ°á»›ng dáº«n chÃ­nh:** Windows PowerShell

## HÆ°á»›ng Dáº«n Khá»Ÿi Äá»™ng Nhanh

### 1. Khá»Ÿi Ä‘á»™ng PostgreSQL

Táº¡i thÆ° má»¥c gá»‘c repository:

```powershell
docker-compose up -d
docker-compose ps
```

PostgreSQL cháº¡y táº¡i `localhost:5432`. Dá»¯ liá»‡u Ä‘Æ°á»£c lÆ°u trong Docker named volume `rentease-management-postgres-data`, khÃ´ng náº±m trong Git vÃ  khÃ´ng tá»± Ä‘á»™ng Ä‘Æ°á»£c chia sáº» sang mÃ¡y khÃ¡c.

### 2. Táº¡o mÃ´i trÆ°á»ng Python

```powershell
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Cáº¥u hÃ¬nh environment

```powershell
Copy-Item .env.example .env
```

Má»Ÿ `backend/.env` vÃ  cáº¥u hÃ¬nh tá»‘i thiá»ƒu:

```dotenv
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=postgres://<user>:<password>@localhost:5432/rentease_db
```

KhÃ´ng commit `.env`, máº­t kháº©u database, PayOS keys hoáº·c Django `SECRET_KEY` lÃªn Git.

### 4. Kiá»ƒm tra vÃ  migrate database

```powershell
.\venv\Scripts\python.exe manage.py check
.\venv\Scripts\python.exe manage.py makemigrations --check --dry-run
.\venv\Scripts\python.exe manage.py migrate
```

### 5. Táº¡o tÃ i khoáº£n quáº£n trá»‹

```powershell
.\venv\Scripts\python.exe manage.py createsuperuser --username admin
```

Lá»‡nh sáº½ yÃªu cáº§u báº¡n tá»± nháº­p email vÃ  máº­t kháº©u. KhÃ´ng dÃ¹ng máº­t kháº©u demo cho production.

### 6. Cháº¡y server

```powershell
.\venv\Scripts\python.exe manage.py runserver
```

Má»Ÿ trÃ¬nh duyá»‡t táº¡i `http://127.0.0.1:8000/`.

## TÃ i Khoáº£n Demo vÃ  CÃ¡ch Thiáº¿t Láº­p

Repository chá»‰ cÃ´ng khai **tÃªn tÃ i khoáº£n demo**, khÃ´ng lÆ°u máº­t kháº©u Ä‘ang hoáº¡t Ä‘á»™ng.

| TÃ i khoáº£n | Vai trÃ² | Chuáº©n bá»‹ trÃªn database local |
|---|---|---|
| `admin` | Superuser | Táº¡o báº±ng `createsuperuser` hoáº·c Ä‘áº·t láº¡i máº­t kháº©u local. |
| `owner_test` | Chá»§ trá» | Táº¡o user loáº¡i `OWNER`, sau Ä‘Ã³ táº¡o `UserProfile` liÃªn káº¿t. |
| `tenant_test` | KhÃ¡ch thuÃª | Táº¡o user loáº¡i `TENANT`, sau Ä‘Ã³ táº¡o `Tenant` liÃªn káº¿t. |

Sau khi tÃ i khoáº£n Ä‘Ã£ tá»“n táº¡i, Ä‘áº·t máº­t kháº©u riÃªng trÃªn tá»«ng mÃ¡y:

```powershell
.\venv\Scripts\python.exe manage.py changepassword admin
.\venv\Scripts\python.exe manage.py changepassword owner_test
.\venv\Scripts\python.exe manage.py changepassword tenant_test
```

Báº¡n cÃ³ thá»ƒ táº¡o `owner_test`, `tenant_test` vÃ  cÃ¡c profile liÃªn káº¿t táº¡i `/admin/`. Chá»‰ dÃ¹ng dá»¯ liá»‡u giáº£ trong demo.

### Táº¡o dá»¯ liá»‡u demo

Xem trÆ°á»›c mÃ  khÃ´ng ghi database:

```powershell
.\venv\Scripts\python.exe manage.py seed_rentease_demo_data --dry-run --owner-username owner_test --tenant-username tenant_test
```

Táº¡o hoáº·c cáº­p nháº­t Property, phÃ²ng, tin Ä‘Äƒng, há»£p Ä‘á»“ng, hÃ³a Ä‘Æ¡n, thanh toÃ¡n, sá»­a chá»¯a, thÃ´ng bÃ¡o vÃ  lá»‹ch xem phÃ²ng:

```powershell
.\venv\Scripts\python.exe manage.py seed_rentease_demo_data --owner-username owner_test --tenant-username tenant_test
```

Lá»‡nh seed yÃªu cáº§u hai tÃ i khoáº£n demo vÃ  profile tÆ°Æ¡ng á»©ng Ä‘Ã£ tá»“n táº¡i. KhÃ´ng cháº¡y seed trÃªn production hoáº·c database cÃ³ dá»¯ liá»‡u giÃ¡ trá»‹.

## CÃ¡ch Sá»­ Dá»¥ng Theo Vai TrÃ²

### KhÃ¡ch truy cáº­p (Visitor)

1. Má»Ÿ `/` Ä‘á»ƒ xem trang giá»›i thiá»‡u.
2. Má»Ÿ `/rooms/` Ä‘á»ƒ xem cÃ¡c phÃ²ng Ä‘ang Ä‘Æ°á»£c cÃ´ng khai.
3. Chá»n phÃ²ng Ä‘á»ƒ xem giÃ¡, diá»‡n tÃ­ch, sá»©c chá»©a, ngÃ y cÃ³ thá»ƒ vÃ o á»Ÿ vÃ  vá»‹ trÃ­ cÃ´ng khai an toÃ n.
4. Gá»­i biá»ƒu máº«u Ä‘Äƒng kÃ½ xem phÃ²ng mÃ  khÃ´ng cáº§n tÃ i khoáº£n.

KhÃ¡ch truy cáº­p khÃ´ng Ä‘Æ°á»£c xem Ä‘á»‹a chá»‰ chÃ­nh xÃ¡c, dá»¯ liá»‡u há»£p Ä‘á»“ng, hÃ³a Ä‘Æ¡n, CCCD hoáº·c há»“ sÆ¡ riÃªng tÆ°.

### Chá»§ trá» (Owner)

1. ÄÄƒng nháº­p báº±ng tÃ i khoáº£n cÃ³ vai trÃ² `OWNER`.
2. Sá»­ dá»¥ng dashboard táº¡i `/owner/dashboard/`.
3. Quáº£n lÃ½ cÆ¡ sá»Ÿ cho thuÃª, phÃ²ng, tin Ä‘Äƒng, khÃ¡ch thuÃª vÃ  há»£p Ä‘á»“ng thuá»™c quyá»n sá»Ÿ há»¯u.
4. Láº­p/cáº­p nháº­t hÃ³a Ä‘Æ¡n, ghi nháº­n thanh toÃ¡n vÃ  theo dÃµi cÃ´ng ná»£.
5. Xá»­ lÃ½ yÃªu cáº§u sá»­a chá»¯a vÃ  Ä‘Äƒng kÃ½ xem phÃ²ng.

Má»i truy váº¥n Owner pháº£i Ä‘Æ°á»£c giá»›i háº¡n theo há»“ sÆ¡ chá»§ trá» hiá»‡n táº¡i; Owner khÃ´ng Ä‘Æ°á»£c xem dá»¯ liá»‡u cá»§a chá»§ trá» khÃ¡c.

### KhÃ¡ch thuÃª (Tenant)

1. ÄÄƒng nháº­p báº±ng tÃ i khoáº£n cÃ³ vai trÃ² `TENANT`.
2. Sá»­ dá»¥ng dashboard táº¡i `/tenant/dashboard/`.
3. Xem há»“ sÆ¡, há»£p Ä‘á»“ng, hÃ³a Ä‘Æ¡n, lá»‹ch sá»­ thanh toÃ¡n vÃ  thÃ´ng bÃ¡o cá»§a chÃ­nh mÃ¬nh.
4. Gá»­i yÃªu cáº§u sá»­a chá»¯a an toÃ n cho phÃ²ng Ä‘ang thuÃª.
5. Náº¿u PayOS Ä‘Ã£ Ä‘Æ°á»£c cáº¥u hÃ¬nh, má»Ÿ hÃ³a Ä‘Æ¡n chÆ°a thanh toÃ¡n vÃ  chá»n **Thanh toÃ¡n VietQR**.

Tenant khÃ´ng Ä‘Æ°á»£c xem dá»¯ liá»‡u cá»§a khÃ¡ch thuÃª khÃ¡c hoáº·c thÃ´ng tin ná»™i bá»™ cá»§a ngÆ°á»i thu tiá»n.

### Admin vÃ  Staff

1. ÄÄƒng nháº­p táº¡i `/admin/`.
2. Quáº£n trá»‹ dá»¯ liá»‡u toÃ n há»‡ thá»‘ng theo quyá»n Django Ä‘Æ°á»£c cáº¥p.
3. Staff há»£p lá»‡ cÃ³ thá»ƒ xem bÃ¡o cÃ¡o táº¡i `/reports/`.
4. Dá»¯ liá»‡u Ä‘á»‹nh danh nháº¡y cáº£m khÃ´ng xuáº¥t hiá»‡n trong danh sÃ¡ch/tÃ¬m kiáº¿m admin; non-superuser staff chá»‰ Ä‘Æ°á»£c Ä‘á»c cÃ¡c trÆ°á»ng nháº¡y cáº£m trong trang chi tiáº¿t Ä‘Æ°á»£c kiá»ƒm soÃ¡t.

## TÃ­nh NÄƒng ChÃ­nh

- Quáº£n lÃ½ tÃ i khoáº£n vÃ  phÃ¢n vai Visitor/Owner/Tenant/Admin/Staff
- Quáº£n lÃ½ nhiá»u cÆ¡ sá»Ÿ cho thuÃª vÃ  phÃ²ng theo tá»«ng chá»§ trá»
- Quáº£n lÃ½ khÃ¡ch thuÃª, ngÆ°á»i á»Ÿ cÃ¹ng vÃ  há»£p Ä‘á»“ng
- Cáº¥u hÃ¬nh giÃ¡ thuÃª, Ä‘iá»‡n, nÆ°á»›c, dá»‹ch vá»¥ vÃ  dÃ²ng hÃ³a Ä‘Æ¡n
- TÃ­nh tá»•ng hÃ³a Ä‘Æ¡n, cÃ´ng ná»£, tráº¡ng thÃ¡i thanh toÃ¡n vÃ  chá»‘ng tráº£ vÆ°á»£t sá»‘ tiá»n cÃ²n láº¡i
- Ghi nháº­n thanh toÃ¡n thá»§ cÃ´ng vÃ  lá»‹ch sá»­ thanh toÃ¡n
- TÃ­ch há»£p PayOS/VietQR báº±ng payment intent vÃ  webhook cÃ³ chá»¯ kÃ½
- Quáº£n lÃ½ yÃªu cáº§u sá»­a chá»¯a, vÃ²ng Ä‘á»i báº£o trÃ¬ vÃ  thÃ´ng bÃ¡o
- Tin Ä‘Äƒng phÃ²ng cÃ´ng khai vÃ  Ä‘Äƒng kÃ½ xem phÃ²ng
- Dashboard riÃªng cho Owner vÃ  Tenant
- BÃ¡o cÃ¡o ná»™i bá»™ dÃ nh cho Staff
- Django Admin Ä‘Æ°á»£c tÃ¹y biáº¿n báº±ng Jazzmin
- Báº£o vá»‡ dá»¯ liá»‡u theo chá»§ trá»/khÃ¡ch thuÃª vÃ  giá»›i háº¡n dá»¯ liá»‡u Ä‘á»‹nh danh

## Thanh ToÃ¡n PayOS/VietQR

RentEase khÃ´ng lÆ°u tÃªn Ä‘Äƒng nháº­p, máº­t kháº©u, PIN hoáº·c OTP ngÃ¢n hÃ ng. Chá»§ tÃ i khoáº£n tá»± liÃªn káº¿t ngÃ¢n hÃ ng vá»›i payOS qua luá»“ng chÃ­nh thá»©c.

Äá»ƒ báº­t thanh toÃ¡n tháº­t, thÃªm vÃ o `backend/.env`:

```dotenv
PAYOS_CLIENT_ID=
PAYOS_API_KEY=
PAYOS_CHECKSUM_KEY=
```

Webhook hiá»‡n Ä‘Æ°á»£c tiáº¿p nháº­n táº¡i:

```text
/api/billing/webhooks/payos/
```

Khi test tá»« localhost, cáº§n má»™t HTTPS URL cÃ´ng khai hoáº·c mÃ´i trÆ°á»ng deploy thá»­ nghiá»‡m Ä‘á»ƒ payOS gá»­i webhook. Return URL chá»‰ dÃ¹ng Ä‘á»ƒ Ä‘iá»u hÆ°á»›ng giao diá»‡n; viá»‡c ghi nháº­n thanh toÃ¡n pháº£i dá»±a trÃªn webhook há»£p lá»‡.

## URL Quan Trá»ng

| URL | Má»¥c Ä‘Ã­ch |
|---|---|
| `/` | Trang cÃ´ng khai RentEase |
| `/rooms/` | Danh sÃ¡ch phÃ²ng cÃ´ng khai |
| `/login/` | ÄÄƒng nháº­p Owner/Tenant |
| `/owner/dashboard/` | Dashboard Chá»§ trá» |
| `/owner/properties/` | Quáº£n lÃ½ cÆ¡ sá»Ÿ cho thuÃª |
| `/owner/rooms/` | Quáº£n lÃ½ phÃ²ng |
| `/owner/tenants/` | Quáº£n lÃ½ khÃ¡ch thuÃª |
| `/owner/contracts/` | Quáº£n lÃ½ há»£p Ä‘á»“ng |
| `/owner/invoices/` | Quáº£n lÃ½ hÃ³a Ä‘Æ¡n vÃ  thanh toÃ¡n |
| `/tenant/dashboard/` | Dashboard KhÃ¡ch thuÃª |
| `/tenant/invoices/` | HÃ³a Ä‘Æ¡n vÃ  VietQR cá»§a khÃ¡ch thuÃª |
| `/tenant/payments/` | Lá»‹ch sá»­ thanh toÃ¡n khÃ¡ch thuÃª |
| `/tenant/repairs/` | YÃªu cáº§u sá»­a chá»¯a khÃ¡ch thuÃª |
| `/admin/` | Django Admin/Jazzmin |
| `/reports/` | BÃ¡o cÃ¡o dÃ nh cho Staff |
| `/api/billing/webhooks/payos/` | Webhook PayOS |

## CÃ´ng Nghá»‡ Sá»­ Dá»¥ng

### Backend

- **Python 3.12+**: ngÃ´n ngá»¯ backend
- **Django 5.2.6**: web framework, ORM, forms, authentication, sessions vÃ  permissions
- **Django REST Framework 3.16.1**: endpoint webhook/API giá»›i háº¡n; RentEase khÃ´ng pháº£i há»‡ thá»‘ng API-first Ä‘áº§y Ä‘á»§
- **django-jazzmin 3.0.1**: giao diá»‡n Django Admin
- **django-cors-headers 4.8.0**: ná»n táº£ng cáº¥u hÃ¬nh CORS
- **dj-database-url 3.1.2**: Ä‘á»c `DATABASE_URL`
- **psycopg2-binary 2.9.10**: káº¿t ná»‘i PostgreSQL
- **python-decouple 3.8**: Ä‘á»c biáº¿n mÃ´i trÆ°á»ng
- **WhiteNoise 6.12.0**: phá»¥c vá»¥ static files khi deploy
- **Pillow 11.3.0**: xá»­ lÃ½ trÆ°á»ng áº£nh/uploads
- **Requests**: HTTP client Ä‘Æ°á»£c PayOS adapter sá»­ dá»¥ng; cáº§n Ä‘Æ°á»£c pin trong dependencies trÆ°á»›c khi clean deployment

### Frontend

- **Django Templates**: server-side rendering
- **HTML5, CSS3 vÃ  JavaScript thuáº§n**
- **Bootstrap Icons**: icon giao diá»‡n
- **RentEase Design System/DreamPOS direction**: CSS tÃ¹y biáº¿n cho public, Owner, Tenant, Reports vÃ  Admin

### Database, Háº¡ Táº§ng vÃ  TÃ­ch Há»£p

- **PostgreSQL 15 Alpine** cháº¡y qua Docker Compose
- **SQLite** lÃ m fallback local khi khÃ´ng cÃ³ `DATABASE_URL`
- **Docker named volumes** Ä‘á»ƒ giá»¯ dá»¯ liá»‡u PostgreSQL qua láº§n restart
- **PayOS/VietQR** cho payment link, QR vÃ  webhook xÃ¡c nháº­n thanh toÃ¡n
- **HMAC-SHA256** Ä‘á»ƒ kiá»ƒm tra chá»¯ kÃ½ request/webhook PayOS
- **Gmail SMTP hoáº·c SMTP tÆ°Æ¡ng thÃ­ch** cho email khi Ä‘Æ°á»£c cáº¥u hÃ¬nh

### CÃ¡c CÃ´ng Nghá»‡ KhÃ´ng Sá»­ Dá»¥ng

- KhÃ´ng cÃ³ React, Vite, Redux Toolkit hoáº·c React Router
- KhÃ´ng cáº§n Node.js/npm cho frontend hiá»‡n táº¡i
- KhÃ´ng dÃ¹ng JWT/SimpleJWT; Ä‘Äƒng nháº­p hiá»‡n dÃ¹ng Django session authentication
- KhÃ´ng cÃ³ Swagger/OpenAPI UI cÃ´ng khai
- KhÃ´ng cÃ³ Celery/Redis hoáº·c hÃ ng Ä‘á»£i background job
- KhÃ´ng cÃ³ Kubernetes
- Stripe chá»‰ lÃ  placeholder cÅ© trong `.env.example`, khÃ´ng pháº£i cá»•ng thanh toÃ¡n Ä‘ang hoáº¡t Ä‘á»™ng

## Dá»¯ Liá»‡u PostgreSQL vÃ  Docker

Database PostgreSQL Ä‘Æ°á»£c lÆ°u trong Docker named volume, khÃ´ng náº±m trong repository. Má»—i mÃ¡y clone dá»± Ã¡n sáº½ cÃ³ volume riÃªng vÃ  cáº§n cháº¡y migrations/seed riÃªng.

```powershell
docker volume ls
docker-compose ps
```

`docker-compose down` dá»«ng container nhÆ°ng giá»¯ dá»¯ liá»‡u. `docker-compose down -v` xÃ³a volume vÃ  toÃ n bá»™ dá»¯ liá»‡u, vÃ¬ váº­y chá»‰ dÃ¹ng khi cháº¯c cháº¯n muá»‘n táº¡o láº¡i database.

KhÃ´ng commit `.env`, database dump, SQLite database, media uploads, logs hoáº·c Docker volume.

## HÆ°á»›ng Dáº«n PhÃ¡t Triá»ƒn vÃ  Kiá»ƒm Thá»­

Cháº¡y cÃ¡c lá»‡nh tá»« `backend/` báº±ng virtual environment chÃ­nh thá»©c:

```powershell
.\venv\Scripts\python.exe manage.py check
.\venv\Scripts\python.exe manage.py makemigrations --check --dry-run
.\venv\Scripts\python.exe manage.py test
```

NguyÃªn táº¯c quan trá»ng:

1. KhÃ´ng táº¡o migration hoáº·c Ä‘á»•i schema náº¿u chÆ°a cÃ³ káº¿ hoáº¡ch Ä‘Æ°á»£c duyá»‡t.
2. KhÃ´ng thay Ä‘á»•i authentication, permissions, billing, settings hoáº·c PayOS má»™t cÃ¡ch trá»±c tiáº¿p.
3. LuÃ´n kiá»ƒm tra Ä‘Ãºng/sai vai trÃ² vÃ  cÃ´ láº­p dá»¯ liá»‡u Owner/Tenant.
4. KhÃ´ng Ä‘Æ°a CCCD, tÃ i liá»‡u Ä‘á»‹nh danh, credential hoáº·c dá»¯ liá»‡u tháº­t vÃ o source/test/demo.
5. KhÃ´ng chá»‰nh/xÃ³a cÃ¡c á»©ng dá»¥ng legacy náº¿u chÆ°a cÃ³ káº¿ hoáº¡ch dependency vÃ  dá»¯ liá»‡u riÃªng.

## Tráº¡ng ThÃ¡i Dá»± Ãn

- **PhiÃªn báº£n:** 1.0.0
- **Cáº­p nháº­t:** July 2026
- **NhÃ¡nh chuáº©n:** `complete-product`
- **Database local hiá»‡n há»— trá»£:** PostgreSQL qua Docker, SQLite fallback
- **Tráº¡ng thÃ¡i:** local-demo ready; chÆ°a production-ready
- **Kiá»ƒm thá»­ gáº§n nháº¥t:** 83 Django tests Ä‘áº¡t trÃªn PostgreSQL local
- **PayOS:** mÃ£ tÃ­ch há»£p Ä‘Ã£ cÃ³; cáº§n cáº¥u hÃ¬nh keys vÃ  webhook HTTPS Ä‘á»ƒ test giao dá»‹ch tháº­t

## TÃ i Liá»‡u LiÃªn Quan

- [`docs/README.md`](docs/README.md)
- [`docs/DEMO.md`](docs/DEMO.md)
- [`docs/STATE.md`](docs/STATE.md)
- [`docs/NEXT.md`](docs/NEXT.md)
- [`docs/DEMO.md`](docs/DEMO.md)
- [`docs/SECURITY.md`](docs/SECURITY.md)
- [`docs/STRUCTURE.md`](docs/STRUCTURE.md)
- [`docs/LEGACY.md`](docs/LEGACY.md)
- [`docs/DESIGN.md`](docs/DESIGN.md)

## LiÃªn Láº¡c vÃ  Há»— Trá»£

Náº¿u gáº·p lá»—i khi cháº¡y dá»± Ã¡n:

1. Kiá»ƒm tra `docker-compose ps` vÃ  káº¿t ná»‘i PostgreSQL.
2. Cháº¡y `manage.py check` vÃ  migration dry-run.
3. Äá»c `docs/PRODUCT.md` cho luá»“ng demo.
4. Táº¡o issue kÃ¨m thÃ´ng bÃ¡o lá»—i Ä‘Ã£ loáº¡i bá» password, API key, database URL vÃ  dá»¯ liá»‡u Ä‘á»‹nh danh.

---

**PhiÃªn báº£n:** 1.0.0 | **NgÃ y cáº­p nháº­t:** July 2026
