@echo off
:default_dir
if not exist ..\studio echo Default directory not found! & goto :enter_dir
cd ..\studio
goto :cmd_interface

:enter_dir
echo:
echo Auto-setup failed.
echo Ensure the bat tools folder is located in the git-repo folder containing the studio folder.
set /P directory= "Please enter the directory of your studio folder:"
if exist %directory% goto :set_dir
echo NO SUCH DIRECTORY
goto :enter_dir

:set_dir
cd %directory%
goto :cmd_interface

:cmd_interface
echo:
echo     -~-~-Tool Interface-~-~-
echo Enter "help" for more information.
set /P command= Cmd: 
echo:
echo ___________________________________________________________________
if /I "%command%" EQU "help" goto :help
if /I "%command%" EQU "wd" echo %CD%
if /I "%command%" EQU "quit" exit
if /I "%command%" EQU "switch" call "%~dp0\tools\Branch_Switch.bat"
if /I "%command%" EQU "delete prefs" call "%~dp0\tools\Delete_Prefs.bat"
if /I "%command%" EQU "chaff" call "%~dp0\tools\doublechaff.bat"
if /I "%command%" EQU "chaff single" call "%~dp0\tools\chaff.bat"
if /I "%command%" EQU "create" call "%~dp0\tools\Create_Branch.bat"
if /I "%command%" EQU "status" call "%~dp0\tools\status.bat"
if /I "%command%" EQU "delete branch" call "%~dp0\tools\Delete_branch.bat"
echo:
echo ___________________________________________________________________

goto :cmd_interface

:help
echo:
echo Commands:
echo chaff         ~ Removes chaff from studio code. Runs twice by default.
echo chaff single  ~ Removes chaff from studio code. Single run variant.
echo create        ~ Run branch creation tool.
echo delete branch ~ Delete branch locally and remotely. (BE CAREFUL!)
echo delete prefs  ~ Delete Silhouette Studio preferences.
echo help          ~ Displays tool interface keywords.
echo quit          ~ Quit tool interface.
echo status        ~ Displays studio and shared_code git statuses.
echo switch        ~ Run branch switching tool.
echo wd            ~ Display current working directory
echo:
echo ___________________________________________________________________      
goto :cmd_interface