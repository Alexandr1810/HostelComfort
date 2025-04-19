@echo off
chcp 65001 > nul
cls

:menu
echo.
echo ============= Fast Git ==============
echo.=                                   =
echo = 1. Сделать быстрый коммит         =
echo = 2. Сделать обычный коммит         =
echo = 3. Переключиться на другую ветку  =
echo = 4. Создать новую ветку            =
echo = 5. Удалить определённую ветку     =
echo = 6. Выполнить слияние(merge) веток =
echo = 7. Выход                          =
echo =====================================
echo.
set /p choice="Выберите действие (1-7): "

if "%choice%"=="1" goto fast_commit
if "%choice%"=="2" goto commit
if "%choice%"=="3" goto checkout
if "%choice%"=="4" goto create_new_branch
if "%choice%"=="5" goto delete_branch
if "%choice%"=="6" goto merge
if "%choice%"=="7" goto quit

echo Ты написал что-то кроме предложенных вариантов
pause
goto menu

:fast_commit
	setlocal
	set "script_dir=%~dp0"
	for /f "delims=" %%i in ('git config user.name') do set "username=%%i"
	cd /d "%script_dir%"
	username=$(git config user.name)
	for /f "delims=" %%b in ('git rev-parse --abbrev-ref HEAD') do set "current_branch=%%b"
	git add .
	git commit -m "fast commit (%username%)"
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
	git commit -m "%user_input% (%username%)"
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

:create_new_branch
	setlocal
	set "script_dir=%~dp0"
	cd /d "%script_dir%"
	set /p branch_name1="Введи название ветки которую возьмёте за основу новой: "
	set /p branch_name="Введи название создаваемой ветки: "
	if "%branch_name%"=="" (
    echo Ошибка: имя ветки не может быть пустым!
    goto create_new_branch
	)
	
	git checkout %branch_name1%
	git branch %branch_name%
	git push origin %branch_name%
	echo Ветка "%branch_name%" создана
	endlocal
	goto menu

:merge
	setlocal
	set "script_dir=%~dp0"
	cd /d "%script_dir%"
	git branch
	set /p branch_name1="Введи название ветки в которую нужно внести изменения: "
	set /p branch_name2="Введи название ветки из которой нужно взять изменения: "
	git checkout %branch_name1%
	set /p user_input="Комментарий: "
	if "%user_input%"=="" (
		git merge -m "Fast merge" %branch_name2%
		git push origin %branch_name1%
		goto menu
	)
	git merge -m "%user_input%" %branch_name2%
	git push origin %branch_name1%
	goto menu

:quit
	