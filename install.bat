@echo off
REM Jekyll installation script
REM Installs Ruby dependencies using Bundler

echo Installing Jekyll and dependencies...
echo.

REM Check if Ruby is installed
ruby --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Ruby is not installed!
    echo.
    echo Please install Ruby first:
    echo   1. Download Ruby+Devkit from https://rubyinstaller.org/downloads/
    echo   2. Run the installer and check "Add Ruby executables to your PATH"
    echo   3. Restart this terminal after installation
    echo   4. See INSTALL_RUBY.md for detailed instructions
    echo.
    pause
    exit /b 1
)

REM Check if Bundler is installed
bundle --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Bundler is not installed. Installing Bundler...
    echo.
    gem install bundler
    if %ERRORLEVEL% NEQ 0 (
        echo.
        echo Failed to install Bundler. Please install it manually:
        echo   gem install bundler
        echo.
        pause
        exit /b 1
    )
)

echo Installing gems from Gemfile...
echo.
bundle install

if %ERRORLEVEL% EQU 0 (
    echo.
    echo Installation completed successfully!
    echo.
    echo You can now use:
    echo   serve.bat    - Start local development server
    echo   build.bat    - Build the site
    exit /b 0
) else (
    echo.
    echo Installation failed with error code %ERRORLEVEL%
    echo.
    echo If you see SSL certificate errors, try:
    echo   gem update --system
    echo.
    echo If you see "Failed to build native extension", make sure you:
    echo   1. Installed Ruby+Devkit (not just Ruby)
    echo   2. Ran 'ridk install' and selected option 3
    echo.
    pause
    exit /b %ERRORLEVEL%
)

