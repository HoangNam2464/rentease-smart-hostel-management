# Phân Công Thành Viên RentEase

## Vai Trò Thành Viên

Thành viên hỗ trợ nên tập trung vào các việc an toàn cho demo:

- kiểm thử UI
- chụp màn hình
- ghi chú lỗi giao diện
- cập nhật tài liệu hướng dẫn
- nhập dữ liệu demo giả trong admin nếu được phân công

## Task Có Thể Làm

- Mở `/`, `/rooms/`, `/login/`, owner portal, tenant portal và ghi lại lỗi hiển thị.
- Kiểm tra trang có chữ tiếng Việt rõ ràng hay không.
- Kiểm tra bảng có bị tràn ngang quá mức hay không.
- Kiểm tra nút/link có dễ hiểu hay không.
- Chụp screenshot theo `docs/demo/SCREENSHOT_CHECKLIST.md`.
- Làm theo `docs/demo/LOCAL_SETUP_AND_DEMO_DATA.md` để chạy local demo.

## File Có Thể Sửa Khi Được Giao

- `docs/`
- `README.md`
- file checklist/demo script
- template RentEase active nếu được giao rõ:
  - `hostello_backend/templates/home.html`
  - `hostello_backend/templates/listings/`
  - `hostello_backend/templates/portal/`
- CSS chính nếu được giao rõ:
  - `hostello_backend/static/css/rentease-design.css`

## File Không Được Sửa Nếu Chưa Hỏi Hoàng Nam

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

## Cách Test UI

1. Chạy server local.
2. Mở trang public:
   - `/`
   - `/rooms/`
   - `/login/`
3. Đăng nhập owner và kiểm tra:
   - `/owner/dashboard/`
   - `/owner/rooms/`
   - `/owner/invoices/`
   - `/owner/repairs/`
4. Đăng nhập tenant và kiểm tra:
   - `/tenant/dashboard/`
   - `/tenant/invoices/`
   - `/tenant/repairs/`
5. Ghi lại:
   - URL
   - lỗi nhìn thấy
   - ảnh chụp màn hình nếu có
   - bước để lặp lại lỗi

## Cách Báo Cáo Khi Hoàn Thành

Gửi cho Hoàng Nam:

- task đã làm
- file đã sửa
- trang đã test
- lỗi còn lại
- ảnh chụp nếu có
- có đụng database hay không

## Khi Nào Phải Hỏi Hoàng Nam Trước

Hỏi trước khi:

- sửa model hoặc migration
- sửa quyền đăng nhập/phân quyền
- sửa billing logic
- xóa file/app cũ
- commit database
- thêm ảnh từ internet
- dùng dữ liệu cá nhân thật
- đổi cấu trúc URL
