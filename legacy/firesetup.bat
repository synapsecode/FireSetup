@echo off
rem ~dp0 is the path that points to the directory of this batch file
set "script_path=%~dp0" 
rem Append the batchfile directory path with the firesetup script
set "script_path=%script_path%firesetup.py"
rem Calls the FireSetup Python Script
python %script_path% %~dp0 "%CD%" %*