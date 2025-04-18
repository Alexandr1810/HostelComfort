@echo off
setlocal

:: Получаем путь к директории, где находится этот .bat файл
set "script_dir=%~dp0"

:: Выводим путь для проверки
echo Путь к директории скрипта: %script_dir%

:: Переходим в директорию скрипта
cd /d "%script_dir%"

:: Здесь вы можете добавить команды, которые хотите выполнить в этой директории
git checkout ilya
git add .
git commit -m "fast commit (ilya)"
git push origin ilya

endlocal