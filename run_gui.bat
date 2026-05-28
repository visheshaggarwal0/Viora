@echo off
rem Viora Global GUI Launcher

echo [Viora] Starting API Backend in background...
start "Viora API Backend" /D C:\Users\aggar\Documents\Viora\engine C:\Users\aggar\Documents\Viora\.venv\Scripts\python.exe api.py

echo [Viora] Starting React Interface in background...
start "Viora React Interface" /D C:\Users\aggar\Documents\Viora\interface cmd /c "npm run dev"

echo [Viora] GUI Startup initiated! 
echo Dashboard URL: http://localhost:5173
echo API Status: http://localhost:8000/status
pause
