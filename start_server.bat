@echo off
setlocal
chcp 65001

:: Получаем путь к директории, где находится этот .bat файл
set "script_dir=%~dp0"

:: Переходим в директорию скрипта
cd /d "%script_dir%"
cd..
cd myenv\Scripts\activate.bat
cd..
cd..
cd..
cd myproject
python manage.py runserver


endlocal