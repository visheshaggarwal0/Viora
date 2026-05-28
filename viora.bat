@echo off
rem Viora Global CLI Launcher
rem Temporarily shift working directory into engine/ so python resolves imports natively.
pushd C:\Users\aggar\Documents\Viora\engine
C:\Users\aggar\Documents\Viora\.venv\Scripts\python.exe cli.py %*
popd
