@echo off
setlocal

:: Получаем путь к директории, где находится этот .bat файл
set "script_dir=%~dp0"

:: Переходим в директорию скрипта
cd /d "%script_dir%"

:: Здесь вы можете добавить команды, которые хотите выполнить в этой директории
git checkout alexandr

endlocal