@echo off
cd /d %~dp0backend
call .\venv\Scripts\activate
set PYTHONIOENCODING=utf-8
python manage.py runserver
pause
