@echo off
REM Navigate to your project directory
cd /d "C:\Users\YourUser\path\to\tempFileDeleter"

REM Activate the venv and run your main script
call .venv\Scripts\activate
python -m src.main %*
