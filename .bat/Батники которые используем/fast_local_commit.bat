@echo off
setlocal

:: Получаем путь к директории, где находится этот .bat файл
set "script_dir=%~dp0"

:: Получаем имя пользователя Git
for /f "delims=" %%i in ('git config user.name') do set "username=%%i"

:: Переходим в директорию скрипта
cd /d "%script_dir%"

:: Здесь вы можете добавить команды, которые хотите выполнить в этой директории
username=$(git config user.name)
for /f "delims=" %%b in ('git rev-parse --abbrev-ref HEAD') do set "current_branch=%%b"
git add .
git commit -m "fast commit (%username%)"

endlocal