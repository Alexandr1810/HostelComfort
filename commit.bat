@echo off
setlocal
chcp 65001

:: Получаем путь к директории, где находится этот .bat файл
set "script_dir=%~dp0"

:: Переходим в директорию скрипта
cd /d "%script_dir%"

:: Здесь вы можете добавить команды, которые хотите выполнить в этой директории
username=$(git config user.name)
set /p user_input="Комментарий: "
for /f "delims=" %%b in ('git rev-parse --abbrev-ref HEAD') do set "current_branch=%%b"
git add .
git commit -m "%user_input% (%username%)"
git push origin %current_branch%

endlocal