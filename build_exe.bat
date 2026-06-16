@echo off
cd /d "%~dp0"
python -m pip install -r requirements.txt
pyinstaller --onefile --name PCSwitchService app.py
echo.
echo EXE created in the dist folder.
pause
