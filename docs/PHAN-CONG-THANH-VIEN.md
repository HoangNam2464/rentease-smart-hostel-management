# PhÃ¢n CÃ´ng ThÃ nh ViÃªn RentEase

## Vai TrÃ² ThÃ nh ViÃªn

ThÃ nh viÃªn há»— trá»£ nÃªn táº­p trung vÃ o cÃ¡c viá»‡c an toÃ n cho demo:

- kiá»ƒm thá»­ UI
- chá»¥p mÃ n hÃ¬nh
- ghi chÃº lá»—i giao diá»‡n
- cáº­p nháº­t tÃ i liá»‡u hÆ°á»›ng dáº«n
- nháº­p dá»¯ liá»‡u demo giáº£ trong admin náº¿u Ä‘Æ°á»£c phÃ¢n cÃ´ng

## Task CÃ³ Thá»ƒ LÃ m

- Má»Ÿ `/`, `/rooms/`, `/login/`, owner portal, tenant portal vÃ  ghi láº¡i lá»—i hiá»ƒn thá»‹.
- Kiá»ƒm tra trang cÃ³ chá»¯ tiáº¿ng Viá»‡t rÃµ rÃ ng hay khÃ´ng.
- Kiá»ƒm tra báº£ng cÃ³ bá»‹ trÃ n ngang quÃ¡ má»©c hay khÃ´ng.
- Kiá»ƒm tra nÃºt/link cÃ³ dá»… hiá»ƒu hay khÃ´ng.
- Chá»¥p screenshot theo `docs/demo/SCREENSHOT_CHECKLIST.md`.
- LÃ m theo `docs/demo/LOCAL_SETUP_AND_DEMO_DATA.md` Ä‘á»ƒ cháº¡y local demo.

## File CÃ³ Thá»ƒ Sá»­a Khi ÄÆ°á»£c Giao

- `docs/`
- `README.md`
- file checklist/demo script
- template RentEase active náº¿u Ä‘Æ°á»£c giao rÃµ:
  - `frontend/templates/home.html`
  - `frontend/templates/listings/`
  - `frontend/templates/portal/`
- CSS chÃ­nh náº¿u Ä‘Æ°á»£c giao rÃµ:
  - `frontend/static/css/rentease-design.css`

## File KhÃ´ng ÄÆ°á»£c Sá»­a Náº¿u ChÆ°a Há»i HoÃ ng Nam

- `models.py`
- migration files
- `settings.py`
- `urls.py`
- billing logic
- authentication/permission logic
- legacy HOSTELLO apps:
  - `students`
  - `attendance`
  - `fees`
  - `requests`
  - `notices`
- legacy HOSTELLO templates:
  - `templates/dashboard.html`
  - `templates/index.html`
  - `templates/login.html`
  - `templates/admin/`
- database files:
  - `db.sqlite3`
  - backup JSON files
- `.env`
- `venv`

## CÃ¡ch Test UI

1. Cháº¡y server local.
2. Má»Ÿ trang public:
   - `/`
   - `/rooms/`
   - `/login/`
3. ÄÄƒng nháº­p owner vÃ  kiá»ƒm tra:
   - `/owner/dashboard/`
   - `/owner/rooms/`
   - `/owner/invoices/`
   - `/owner/repairs/`
4. ÄÄƒng nháº­p tenant vÃ  kiá»ƒm tra:
   - `/tenant/dashboard/`
   - `/tenant/invoices/`
   - `/tenant/repairs/`
5. Ghi láº¡i:
   - URL
   - lá»—i nhÃ¬n tháº¥y
   - áº£nh chá»¥p mÃ n hÃ¬nh náº¿u cÃ³
   - bÆ°á»›c Ä‘á»ƒ láº·p láº¡i lá»—i

## CÃ¡ch BÃ¡o CÃ¡o Khi HoÃ n ThÃ nh

Gá»­i cho HoÃ ng Nam:

- task Ä‘Ã£ lÃ m
- file Ä‘Ã£ sá»­a
- trang Ä‘Ã£ test
- lá»—i cÃ²n láº¡i
- áº£nh chá»¥p náº¿u cÃ³
- cÃ³ Ä‘á»¥ng database hay khÃ´ng

## Khi NÃ o Pháº£i Há»i HoÃ ng Nam TrÆ°á»›c

Há»i trÆ°á»›c khi:

- sá»­a model hoáº·c migration
- sá»­a quyá»n Ä‘Äƒng nháº­p/phÃ¢n quyá»n
- sá»­a billing logic
- xÃ³a file/app cÅ©
- commit database
- thÃªm áº£nh tá»« internet
- dÃ¹ng dá»¯ liá»‡u cÃ¡ nhÃ¢n tháº­t
- Ä‘á»•i cáº¥u trÃºc URL
