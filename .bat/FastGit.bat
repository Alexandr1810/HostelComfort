@echo off
chcp 65001 > nul
cls

:menu
echo.
echo  =========== Fast Git ===========
echo.
echo  1. Сделать быстрый коммит       
echo  2. Сделать обычный коммит       
echo  3. Переключиться на другую ветку
echo  4. Выход                        
echo.
set /p choice="Выберите действие (1-4): "

if "%choice%"=="1" goto fast_commit
if "%choice%"=="2" goto commit
if "%choice%"=="3" goto checkout
if "%choice%"=="4" goto quit

echo Ты написал что-то кроме предложенных вариантов
pause
goto menu

:fast_commit
setlocal
set "script_dir=%~dp0"
cd /d "%script_dir%"
for /f "delims=" %%b in ('git rev-parse --abbrev-ref HEAD') do set "current_branch=%%b"
git add .
git commit -m "fast commit"
git push origin %current_branch%
endlocal
goto menu

:commit
setlocal
set "script_dir=%~dp0"
cd /d "%script_dir%"
set /p user_input="Комментарий: "
for /f "delims=" %%b in ('git rev-parse --abbrev-ref HEAD') do set "current_branch=%%b"
git add .
git commit -m "%user_input%"
git push origin %current_branch%
endlocal
goto menu

:checkout
setlocal
set "script_dir=%~dp0"
cd /d "%script_dir%"
git branch
set /p branch_name="Введи название ветки: "
git checkout %branch_name%
endlocal
goto menu

:quit
exit