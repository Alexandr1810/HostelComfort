@echo off
setlocal

:: Получаем путь к родительской директории
cd /d "%~dp0"
cd ..

:: Активируем окружение и запускаем новую cmd
call myenv\Scripts\activate.bat
cmd /k