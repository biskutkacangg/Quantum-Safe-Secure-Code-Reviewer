@echo off
cd /d "%~dp0"
echo ============================================================
echo Starting Quantum-Safe Code Reviewer — Cyber SOC Web Server...
echo Opening http://localhost:8000 in your default browser...
echo ============================================================
start "" "http://localhost:8000"
"%~dp0.venv\Scripts\python.exe" server.py
pause
