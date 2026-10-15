@echo off
cd /d "%~dp0"
echo ============================================================
echo Starting Streamlit Legacy Dashboard (app.py)...
echo Opening http://localhost:8501 in your default browser...
echo ============================================================
start "" "http://localhost:8501"
"%~dp0.venv\Scripts\python.exe" -m streamlit run app.py
pause
