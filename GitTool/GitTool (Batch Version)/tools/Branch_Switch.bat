@echo off
echo ___________________________________________________________________
:dir_chosen
echo:
set /P new_branch="Switch to Branch: "
goto :choice1

:choice1
echo:
echo ___________________________________________________________________
call "%~dp0\status.bat"
echo ___________________________________________________________________
echo:
echo           -~-~-Preparing to switch to %new_branch%-~-~-
echo    Are you sure you want to continue[Y/N]? Press [R] to reset head.
set /P continue="Cmd:"
if /I "%continue%" EQU "Y" goto :switch_True
if /I "%continue%" EQU "N" goto :switch_Done
if /I "%continue%" EQU "R" goto :reset_head
goto :choice1

:reset_head
echo ___________________________________________________________________
if exist ..\studio cd shared_code
git reset head --h
if not exist ..\studio cd ..
git reset head --h
goto :choice1

:switch_True
echo:
echo ___________________________________________________________________
echo:
if exist ..\studio cd shared_code
git checkout %new_branch%
if %ERRORLEVEL% NEQ 0 call :ERROR 0
echo:
echo ~~~~   ~~~~   ~~~~   ~~~~   ~~~~   ~~~~   ~~~~   ~~~~
git fetch
if %ERRORLEVEL% NEQ 0 call :ERROR 1
echo:
echo ___________________________________________________________________
echo:
if not exist ..\studio cd ..
git checkout %new_branch%
IF %ERRORLEVEL% NEQ 0 call :ERROR 0
echo:
echo ~~~~   ~~~~   ~~~~   ~~~~   ~~~~   ~~~~   ~~~~   ~~~~
git fetch
IF %ERRORLEVEL% NEQ 0 call :ERROR 1
goto :switch_Done

:ERROR
echo:
echo ___________________________________________________________________
echo -~-~-Git has encountered an error-~-~-
if %~1 EQU 0 echo Error in checkout. Are you sure the source branch exists?
if %~1 EQU 1 echo Error in fetch.
Echo:
Echo Process error. 
Echo Error has occured, please try again or manually switch branch.
echo:
echo ___________________________________________________________________
set /P end = PROCESS ERROR. TOOL WILL CLOSE

:switch_Done
echo:
echo ___________________________________________________________________
echo:
echo -~-~-Studio and Shared_Code switched to %new_branch%-~-~-
set /p end = "~                   ENTER TO CONTINUE                     ~"