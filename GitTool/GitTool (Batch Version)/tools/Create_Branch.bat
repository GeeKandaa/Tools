@echo off

:dir_chosen
echo:
set /P source_branch="Source Branch: "
set /P new_branch="New Branch: "
echo ___________________________________________________________________
goto :choice1

:choice1
echo:
call "%~dp0\status.bat"
echo ___________________________________________________________________
echo:
echo -~-~-Preparing to switch shared_code from %source_branch% to %new_branch%-~-~-
echo    Are you sure you want to continue[Y/N]? Press [R] to reset head.
set /P continue= "Cmd:"
if /I "%continue%" EQU "Y" goto :shared_True
if /I "%continue%" EQU "N" goto :shared_False
if /I "%continue%" EQU "R" goto :reset_head
echo ___________________________________________________________________
goto :choice1

:reset_head
echo ___________________________________________________________________
if exist ..\studio cd shared_code
git reset head --h
if not exist ..\studio cd ..
git reset head --h
goto :choice1

:shared_True
echo:
if exist ..\studio cd shared_code
git checkout %source_branch%
if %ERRORLEVEL% NEQ 0 call :ERROR 0
echo ~~~~   ~~~~   ~~~~   ~~~~   ~~~~   ~~~~   ~~~~   ~~~~
git fetch
if %ERRORLEVEL% NEQ 0 call :ERROR 1
echo ~~~~   ~~~~   ~~~~   ~~~~   ~~~~   ~~~~   ~~~~   ~~~~
git pull origin %source_branch%
if %ERRORLEVEL% NEQ 0 call :ERROR 2
echo ~~~~   ~~~~   ~~~~   ~~~~   ~~~~   ~~~~   ~~~~   ~~~~
git checkout -b %new_branch%
if %ERRORLEVEL% NEQ 0 call :ERROR 3
echo ~~~~   ~~~~   ~~~~   ~~~~   ~~~~   ~~~~   ~~~~   ~~~~
git push origin %new_branch%
if %ERRORLEVEL% NEQ 0 call :ERROR 4
echo ~~~~   ~~~~   ~~~~   ~~~~   ~~~~   ~~~~   ~~~~   ~~~~
git branch -u origin/%new_branch%
if %ERRORLEVEL% NEQ 0 call :ERROR 5
echo ___________________________________________________________________
goto :shared_Done

:shared_False
echo:
echo shared_code not switched to new branch!
echo Preparing to switch studio to new branch anyway..
echo ___________________________________________________________________
goto :shared_Done

:shared_Done
echo:
call "%~dp0\status.bat"
echo ___________________________________________________________________
echo:
echo -~-~-Preparing to switch studio from %source_branch% to %new_branch%-~-~-
echo Are you sure you want to continue[Y/N]?
set /P continue= "Cmd:"
if /I "%continue%" EQU "Y" goto :studio_True
if /I "%continue%" EQU "N" goto :studio_False
echo ___________________________________________________________________
goto :shared_Done

:studio_True
if not exist ..\studio cd ..
echo:
git checkout %source_branch%
IF %ERRORLEVEL% NEQ 0 call :ERROR 0
echo ~~~~   ~~~~   ~~~~   ~~~~   ~~~~   ~~~~   ~~~~   ~~~~
git fetch
IF %ERRORLEVEL% NEQ 0 call :ERROR 1
echo ~~~~   ~~~~   ~~~~   ~~~~   ~~~~   ~~~~   ~~~~   ~~~~
git pull origin %source_branch%
IF %ERRORLEVEL% NEQ 0 call :ERROR 2
echo ~~~~   ~~~~   ~~~~   ~~~~   ~~~~   ~~~~   ~~~~   ~~~~
git checkout -b %new_branch%
IF %ERRORLEVEL% NEQ 0 call :ERROR 3
echo ~~~~   ~~~~   ~~~~   ~~~~   ~~~~   ~~~~   ~~~~   ~~~~
git push origin %new_branch%
IF %ERRORLEVEL% NEQ 0 call :ERROR 4
echo ~~~~   ~~~~   ~~~~   ~~~~   ~~~~   ~~~~   ~~~~   ~~~~
git branch -u origin/%new_branch%
IF %ERRORLEVEL% NEQ 0 call :ERROR 5
echo ___________________________________________________________________
goto :studio_Done

:studio_False
echo:
echo Studio not switched to new branch!
echo ___________________________________________________________________
goto :studio_Done

:ERROR
echo ___________________________________________________________________
echo Git has encountered an error:
if %~1 EQU 0 echo Error in checkout. Are you sure the source branch exists?
if %~1 EQU 1 echo Error in fetch.
if %~1 EQU 2 echo Error in pull.
if %~1 EQU 3 echo Error in new branch creation. Are you sure the new branch doesn't already exist?
if %~1 EQU 4 echo Error in pushing new branch.
if %~1 EQU 5 echo Error in adding new branch tracking.
Echo:
echo ___________________________________________________________________
Echo Process error. 
Echo Branch may have been created but not set up properly, please check and ammend accordingly.
echo ___________________________________________________________________
echo = -~-~-PROCESS ERROR. TOOL WILL CLOSE-~-~-
echo ___________________________________________________________________

:studio_Done
echo:
set /p end = "~                   ENTER TO CONTINUE                     ~"
echo ___________________________________________________________________
