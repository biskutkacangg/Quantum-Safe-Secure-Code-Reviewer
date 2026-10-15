@echo off
cd /d "%~dp0"
echo ============================================================
echo Starting Design and Development of a Post-Quantum Cryptography-Based Secure Code Review Tool...
echo Opening http://localhost:8501 in your default browser...
echo ============================================================
start "" "http://localhost:8501"
"%~dp0.venv\Scripts\python.exe" -m streamlit run app.py
pause
