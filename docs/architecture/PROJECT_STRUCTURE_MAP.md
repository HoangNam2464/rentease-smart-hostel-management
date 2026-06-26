# RentEase Project Structure Map

## Má»¥c ÄÃ­ch

TÃ i liá»‡u nÃ y mÃ´ táº£ cáº¥u trÃºc hiá»‡n táº¡i cá»§a RentEase sau khi Ä‘á»•i tÃªn thÆ° má»¥c Django ngoÃ i tá»« `backend/` thÃ nh `backend/` vÃ  chuyá»ƒn templates/static sang `frontend/`.

Phase nÃ y chá»‰ Ä‘á»•i cáº¥u trÃºc thÆ° má»¥c ngoÃ i vÃ  vá»‹ trÃ­ frontend assets. KhÃ´ng Ä‘á»•i business logic, khÃ´ng Ä‘á»•i models, khÃ´ng táº¡o migrations, khÃ´ng Ä‘á»•i URL names, khÃ´ng Ä‘á»•i permissions vÃ  khÃ´ng Ä‘á»•i owner-scoped querysets.

## Cáº¥u TrÃºc Hiá»‡n Táº¡i

```text
HOSTELLO-Automated_Smart_Hostel_Management_System_using_Django-main/
â”œâ”€â”€ AGENTS.md
â”œâ”€â”€ README.md
â”œâ”€â”€ docs/
â”œâ”€â”€ assets/
â”œâ”€â”€ backend/
â”‚   â”œâ”€â”€ manage.py
â”‚   â”œâ”€â”€ requirements.txt
â”‚   â”œâ”€â”€ db.sqlite3                  # local database, khÃ´ng nÃªn commit
â”‚   â”œâ”€â”€ media/                      # local uploaded/demo media
â”‚   â”œâ”€â”€ backend/           # inner Django config package, giá»¯ nguyÃªn tÃªn
â”‚   â”œâ”€â”€ accounts/
â”‚   â”œâ”€â”€ properties/
â”‚   â”œâ”€â”€ tenants/
â”‚   â”œâ”€â”€ contracts/
â”‚   â”œâ”€â”€ billing/
â”‚   â”œâ”€â”€ maintenance/
â”‚   â”œâ”€â”€ listings/
â”‚   â”œâ”€â”€ portal/
â”‚   â”œâ”€â”€ reports/
â”‚   â”œâ”€â”€ students/
â”‚   â”œâ”€â”€ attendance/
â”‚   â”œâ”€â”€ fees/
â”‚   â”œâ”€â”€ requests/
â”‚   â””â”€â”€ notices/
â”œâ”€â”€ frontend/
â”‚   â”œâ”€â”€ templates/
â”‚   â””â”€â”€ static/
â””â”€â”€ venv/                           # local virtual environment, khÃ´ng nÃªn commit
```

## Manage.py VÃ  Settings Module

- `manage.py` hiá»‡n náº±m táº¡i: `backend/manage.py`
- Django settings module váº«n lÃ : `hostello_backend.settings`
- File settings hiá»‡n táº¡i: `backend/hostello_backend/settings.py`
- Root URLConf váº«n lÃ : `hostello_backend.urls`
- File URL chÃ­nh: `backend/hostello_backend/urls.py`

Äiá»ƒm quan trá»ng: chá»‰ Ä‘á»•i tÃªn thÆ° má»¥c ngoÃ i. Package cáº¥u hÃ¬nh Django bÃªn trong váº«n lÃ  `hostello_backend`, khÃ´ng Ä‘á»•i thÃ nh `backend`.

## Current Backend Files/Folders

### Django config

```text
backend/hostello_backend/
â”œâ”€â”€ settings.py
â”œâ”€â”€ urls.py
â”œâ”€â”€ wsgi.py
â””â”€â”€ asgi.py
```

### Active RentEase apps

```text
backend/accounts/
backend/properties/
backend/tenants/
backend/contracts/
backend/billing/
backend/maintenance/
backend/listings/
backend/portal/
backend/reports/
```

### Legacy HOSTELLO apps

```text
backend/students/
backend/attendance/
backend/fees/
backend/requests/
backend/notices/
```

CÃ¡c app legacy váº«n cÃ²n trong `INSTALLED_APPS` Ä‘á»ƒ giá»¯ tÆ°Æ¡ng thÃ­ch/lá»‹ch sá»­. KhÃ´ng xÃ³a náº¿u chÆ°a cÃ³ dependency audit riÃªng.

## Current Frontend Template Files/Folders

Django hiá»‡n Ä‘á»c template chÃ­nh tá»«:

```text
frontend/templates/
```

`settings.py` dÃ¹ng:

```python
REPO_ROOT / "frontend" / "templates"
```

CÃ¡c nhÃ³m template chÃ­nh:

```text
frontend/templates/home.html
frontend/templates/404.html
frontend/templates/500.html
frontend/templates/portal/
frontend/templates/listings/
frontend/templates/admin/
frontend/templates/payments/
frontend/templates/base/
frontend/templates/reports/
```

Reports templates Ä‘Ã£ Ä‘Æ°á»£c chuyá»ƒn ra frontend vÃ  váº«n resolve theo cÃ¹ng relative path:

```text
frontend/templates/reports/
```

Legacy templates váº«n cÃ²n nhÆ°ng Ä‘Ã£ náº±m trong frontend:

```text
frontend/templates/index.html
frontend/templates/login.html
frontend/templates/dashboard.html
frontend/templates/admin/
frontend/templates/payments/success.html
```

KhÃ´ng dÃ¹ng cÃ¡c file legacy nÃ y cho RentEase UI má»›i náº¿u chÆ°a Ä‘Æ°á»£c duyá»‡t.

## Current Static Files/Folders

Django hiá»‡n Ä‘á»c static source tá»«:

```text
frontend/static/
```

`settings.py` dÃ¹ng:

```python
REPO_ROOT / "frontend" / "static"
```

CÃ¡c file static chÃ­nh:

```text
frontend/static/css/rentease-design.css
frontend/static/css/rentease-layout.css
frontend/static/admin/css/custom_admin.css
frontend/static/css/styles.css
frontend/static/css/student-dashboard.css
frontend/static/js/script.js
frontend/static/js/student-dashboard.js
frontend/static/rentease/
frontend/static/vendor/
```

RentEase UI hiá»‡n chá»§ yáº¿u dÃ¹ng:

```text
frontend/static/css/rentease-design.css
frontend/static/css/rentease-layout.css
frontend/static/admin/css/custom_admin.css
```

Legacy/static cÅ© cáº§n cáº©n tháº­n:

```text
frontend/static/css/styles.css
frontend/static/css/student-dashboard.css
frontend/static/js/script.js
frontend/static/js/student-dashboard.js
assets/
```

## Current Database/Model Files

CÃ¡c model chÃ­nh:

```text
backend/accounts/models.py
backend/properties/models.py
backend/tenants/models.py
backend/contracts/models.py
backend/billing/models.py
backend/maintenance/models.py
backend/listings/models.py
```

Legacy model files:

```text
backend/students/models.py
backend/attendance/models.py
backend/fees/models.py
backend/requests/models.py
backend/notices/models.py
```

Database local hiá»‡n táº¡i:

```text
backend/db.sqlite3
```

KhÃ´ng commit database local.

## Current Media/Upload Folders

Media config hiá»‡n táº¡i:

```python
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
```

ThÆ° má»¥c media hiá»‡n táº¡i:

```text
backend/media/
```

Ná»™i dung media cÃ³ thá»ƒ gá»“m áº£nh/demo upload tá»« dá»± Ã¡n cÅ© vÃ  local data. KhÃ´ng nÃªn commit media tháº­t hoáº·c dá»¯ liá»‡u cÃ³ thÃ´ng tin cÃ¡ nhÃ¢n.

## Current Documentation Folders

```text
docs/agent/
docs/architecture/
docs/demo/
docs/security/
docs/spqm/
docs/ui/
```

## Possibly Unused Or Unclear Files

CÃ¡c má»¥c cáº§n audit riÃªng trÆ°á»›c khi xÃ³a/di chuyá»ƒn:

```text
assets/
run_backend.bat
run_frontend.bat
Working.py
backup_phase2.json
backup_phase3.json
backup_phase4.json
backup_phase5.json
backend/phase8b2_wip.patch
frontend/static/css/styles.css
frontend/static/js/script.js
```

KhÃ´ng xÃ³a cÃ¡c file nÃ y trong phase hiá»‡n táº¡i. Má»™t sá»‘ cÃ³ thá»ƒ lÃ  di sáº£n HOSTELLO hoáº·c cÃ´ng cá»¥ local.

## Completed Folder Reorganization

ÄÃ£ thá»±c hiá»‡n:

- Äá»•i tÃªn thÆ° má»¥c Django ngoÃ i `backend/` thÃ nh `backend/`.
- Giá»¯ nguyÃªn inner Django config package `backend/hostello_backend/`.
- Di chuyá»ƒn `backend/templates/` sang `frontend/templates/`.
- Di chuyá»ƒn `backend/static/` sang `frontend/static/`.
- Di chuyá»ƒn reports app templates sang `frontend/templates/reports/` vÃ  giá»¯ nguyÃªn template relative paths nhÆ° `reports/dashboard.html`.
- Giá»¯ nguyÃªn relative paths bÃªn trong template/static.
- KhÃ´ng Ä‘á»•i tÃªn template files.
- KhÃ´ng Ä‘á»•i tÃªn CSS/JS files.
- KhÃ´ng di chuyá»ƒn Django apps.
- KhÃ´ng Ä‘á»•i models hoáº·c migrations.

## Files Safe To Move Later

CÃ³ thá»ƒ di chuyá»ƒn/tá»• chá»©c láº¡i dáº§n trong cÃ¡c phase nhá»:

- `frontend/templates/listings/` thÃ nh nhÃ³m public rÃµ hÆ¡n.
- `frontend/templates/portal/` thÃ nh nhÃ³m owner/tenant rÃµ hÆ¡n.
- `frontend/templates/home.html`, `404.html`, `500.html` vÃ o nhÃ³m public/base náº¿u cáº­p nháº­t render path.
- Reports templates Ä‘Ã£ Ä‘Æ°á»£c chuyá»ƒn sang `frontend/templates/reports/`.
- `frontend/static/css/rentease-design.css` vÃ o `frontend/static/rentease/css/`.
- `frontend/static/css/rentease-layout.css` vÃ o `frontend/static/rentease/css/`.

Má»—i nhÃ³m di chuyá»ƒn pháº£i cháº¡y route smoke test ngay sau Ä‘Ã³.

## Files That Should Not Be Moved Yet

KhÃ´ng nÃªn di chuyá»ƒn trong cÃ¡c phase tiáº¿p theo náº¿u chÆ°a cÃ³ plan riÃªng:

- `backend/manage.py`
- `backend/hostello_backend/settings.py`
- `backend/hostello_backend/urls.py`
- Django app folders nhÆ° `accounts`, `properties`, `tenants`, `contracts`, `billing`, `maintenance`, `listings`, `portal`, `reports`
- Migration folders
- Model files
- Legacy apps
- Media upload folder
- Database local

LÃ½ do: cÃ¡c file nÃ y liÃªn quan trá»±c tiáº¿p Ä‘áº¿n import path, app label, migration history, admin registration vÃ  URL routing.

## Risks When Moving Django Apps

Di chuyá»ƒn app Django cÃ³ thá»ƒ gÃ¢y lá»—i:

- `INSTALLED_APPS` sai path
- `AppConfig.name` sai
- migration dependency bá»‹ lá»‡ch
- admin registration khÃ´ng load
- import trong views/forms/services lá»—i
- content type/app label thay Ä‘á»•i ngoÃ i Ã½ muá»‘n
- dá»¯ liá»‡u cÅ© khÃ´ng khá»›p app label má»›i

VÃ¬ váº­y khÃ´ng di chuyá»ƒn app vÃ o `backend/apps/` náº¿u chÆ°a cÃ³ phase riÃªng vÃ  káº¿ hoáº¡ch rollback.

## Risks When Moving Templates

Di chuyá»ƒn template cÃ³ thá»ƒ gÃ¢y lá»—i:

- `render(request, "...")` khÃ´ng tÃ¬m tháº¥y template
- `{% extends %}` trá» sai path
- `{% include %}` trá» sai path
- template cÃ¹ng tÃªn bá»‹ Æ°u tiÃªn khÃ¡c do `APP_DIRS=True`
- route váº«n cháº¡y nhÆ°ng render sai shell public/owner/tenant

Náº¿u di chuyá»ƒn template tiáº¿p, cáº§n di chuyá»ƒn theo tá»«ng nhÃ³m nhá» vÃ  kiá»ƒm tra route ngay.

## Risks When Moving Static Files

Di chuyá»ƒn static cÃ³ thá»ƒ gÃ¢y lá»—i:

- `{% static %}` trá» sai file
- admin custom CSS khÃ´ng load
- public/owner/tenant layout máº¥t style
- file legacy vÃ  RentEase bá»‹ trá»™n
- `collectstatic` hoáº·c `STATICFILES_DIRS` bá»‹ sai

KhÃ´ng xÃ³a static cÅ© cho Ä‘áº¿n khi má»i reference Ä‘Ã£ Ä‘Æ°á»£c cáº­p nháº­t vÃ  kiá»ƒm tra.

## Recommended Next Phases

### Phase A: Route Smoke Test After Folder Rename

1. Cháº¡y Django check.
2. Cháº¡y migration dry-run.
3. Kiá»ƒm tra public routes: `/`, `/rooms/`, room detail, viewing registration.
4. Kiá»ƒm tra auth routes: `/login/`, `/dashboard/`.
5. Kiá»ƒm tra owner routes.
6. Kiá»ƒm tra tenant routes.
7. Kiá»ƒm tra `/admin/`.
8. Kiá»ƒm tra `/reports/`.

### Phase B: Commit Folder Rename

Commit riÃªng pháº§n rename/move náº¿u checks pass.

### Phase C: Move Public Templates Gradually

Chá»‰ sau khi Phase A/B sáº¡ch, má»›i cÃ¢n nháº¯c tá»• chá»©c láº¡i template public theo nhÃ³m má»›i.

### Phase D: Move Owner/Tenant Templates Gradually

Di chuyá»ƒn owner/tenant templates theo tá»«ng nhÃ³m nhá» vÃ  cáº­p nháº­t `render()` náº¿u Ä‘á»•i path.

### Phase E: Organize Static Files Gradually

Di chuyá»ƒn CSS/JS vÃ o `frontend/static/rentease/` theo nhÃ³m nhá», cáº­p nháº­t `{% static %}` vÃ  kiá»ƒm tra tá»«ng route.
