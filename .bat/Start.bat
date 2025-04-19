@echo off
chcp 65001 > nul
cls

net session >nul 2>&1
if %errorLevel% neq 0 (
    echo.
    echo [ОШИБКА] Запустите скрипт от имени администратора!
    echo.
    pause
    exit /b
)

goto download_python


::Готов
:download_python
	bitsadmin /transfer download-python /download /priority high https://www.python.org/ftp/python/3.13.3/python-3.13.3-amd64.exe %cd%\python-installer.exe
	python-installer.exe /quiet InstallAllUsers=1 PrependPath=1
	del /f python-*.exe
	py --version
	goto download_git

::Готов
:download_git
	set "git_url=https://github.com/git-for-windows/git/releases/download/v2.45.1.windows.1/Git-2.45.1-64-bit.exe"
	set "installer=git-installer.exe"
	bitsadmin /transfer download-git /download /priority high %git_url% %cd%\%installer%
	if not exist "%cd%\%installer%" (
	    echo.
	    echo [ОШИБКА] Не удалось скачать установщик!
	    echo - Доступ в интернет
	    echo - Антивирус,сожет блокировать
	    pause
	    exit /b
	)
	start /wait %installer% /VERYSILENT /NORESTART /COMPONENTS="icons,ext\reg\shellhere,assoc,assoc_sh"
	set "git_path=%ProgramFiles%\Git\cmd"
	setx PATH "%PATH%;%git_path%" >nul
	del /f /q %installer% >nul 2>&1

	"%git_path%\git.exe" --version >nul 2>&1
	if %errorLevel% equ 0 (
	    echo.
	    echo Успешно! Git установлен.
	    "%git_path%\git.exe" --version
	) else (
	    echo.
	    echo [ОШИБКА] Git не установлен! Проверьте:
	    echo - Доступ в интернет
	    echo - Антивирус,сожет блокировать
	)
	goto git_clone

:: Готов
	:git_clone
	cd /d "%script_dir%"
	git clone https://github.com/Alexandr1810/HostelComfort.git
	goto create_venv

:: Готов
:create_venv
	cd /d "%script_dir%"
	py -m venv myenv
	goto download_lib_to_venv

:: Готов
:download_lib_to_venv
	cd /d "%script_dir%"
	call myenv\Scripts\activate.bat
	pip install numpy
	pip freeze > requirements.txt
	goto other

:other
	cls
	echo.
	echo ====================================================================
	echo.
	echo Git----------------------------Скачен и установлена последняя версия
	echo Python----------------Скачен и установлена нужная версия для проекта
	echo Django----------------Скачен и установлена нужная версия для проекта
	echo Окружение----------------------------------------------------Создано
	echo Библиотеки для проекта----------------Установлены в окружение прокта
	echo Репозиторий------------------Клонирован и установлен в папку проекта
	echo.
	echo ====================================================================
	echo.
	echo Всё остальное вы найдёте в документации и файлах readme.md в проекте
	echo Этот файл можно будет удалить, он нужен только для установки проекта
	echo.

	pause
	exit