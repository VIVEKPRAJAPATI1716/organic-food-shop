@echo off
chcp 65001 >nul
title Organic Food Shop - Easy Setup
color 0A

echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║     🛒 ORGANIC FOOD SHOP - EASY SETUP & RUN 🛒          ║
echo ╚══════════════════════════════════════════════════════════╝
echo.
echo This script will automatically:
echo   ✓ Install all required packages
echo   ✓ Setup database
echo   ✓ Create admin account
echo   ✓ Start the server
echo.
echo Press any key to continue...
pause >nul
echo.

echo [STEP 1/4] Installing Python packages...
echo ────────────────────────────────────────────────
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo.
    echo ❌ Error: Could not install packages
    echo Please check your internet connection and Python installation
    pause
    exit /b 1
)
echo ✓ Packages installed successfully!
echo.

echo [STEP 2/4] Setting up database...
echo ────────────────────────────────────────────────
python manage.py migrate --noinput
if errorlevel 1 (
    echo.
    echo ❌ Error: Database setup failed
    pause
    exit /b 1
)
echo ✓ Database ready!
echo.

echo [STEP 3/4] Creating admin account...
echo ────────────────────────────────────────────────
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@organicfood.com', 'admin')" 2>nul
if errorlevel 1 (
    echo ⚠ Admin user might already exist (this is OK)
) else (
    echo ✓ Admin account created!
    echo   Username: admin
    echo   Password: admin
)
echo.

echo [STEP 4/4] Creating static files directory...
echo ────────────────────────────────────────────────
if not exist static mkdir static >nul 2>&1
echo ✓ Static directory ready!
echo.

echo ╔══════════════════════════════════════════════════════════╗
echo ║              ✅ SETUP COMPLETE! ✅                        ║
echo ╚══════════════════════════════════════════════════════════╝
echo.
echo Starting server in 3 seconds...
timeout /t 3 /nobreak >nul

echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║              🚀 SERVER STARTING... 🚀                     ║
echo ╚══════════════════════════════════════════════════════════╝
echo.
echo 📍 Website:     http://127.0.0.1:8000/
echo 📍 Admin Panel: http://127.0.0.1:8000/admin/
echo.
echo 👤 Admin Login:
echo    Username: admin
echo    Password: admin
echo.
echo ⚠  Press Ctrl+C to stop the server
echo.
echo ────────────────────────────────────────────────────────────
echo.

python manage.py runserver

pause




