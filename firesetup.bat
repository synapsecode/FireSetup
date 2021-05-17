@echo off
set "script_path=%~dp0"
set "script_path=%script_path%firesetup.py"
python %script_path% %~dp0 "%CD%" %*