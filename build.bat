@echo off
REM Build script for Pelican blog on Windows
REM This script activates the virtual environment and runs the build script

setlocal

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo Error: Failed to create virtual environment
        exit /b 1
    )
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo Error: Failed to activate virtual environment
    exit /b 1
)

REM Check if requirements are installed
python -c "import pelican" 2>nul
if errorlevel 1 (
    echo Installing requirements...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo Error: Failed to install requirements
        exit /b 1
    )
)

REM Run the build script with all arguments passed through
python build.py %*

endlocal

