@echo off
setlocal
chcp 65001

:: Получаем путь к директории, где находится этот .bat файл
set "script_dir=%~dp0"

:: Переходим в директорию скрипта
cd /d "%script_dir%"

:: Здесь вы можете добавить команды, которые хотите выполнить в этой директории
for /f "delims=" %%b in ('git rev-parse --abbrev-ref HEAD') do set "current_branch=%%b"
git push origin %current_branch%

endlocal