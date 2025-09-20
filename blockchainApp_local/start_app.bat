@echo off
echo 🚀 Starting EdTech Blockchain App...
echo.

echo 📋 Checking prerequisites...

REM Check if Node.js is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js is not installed. Please install Node.js first.
    pause
    exit /b 1
)

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed. Please install Python first.
    pause
    exit /b 1
)

echo ✅ Prerequisites check passed!
echo.

echo 🔧 Starting Backend Server...
cd backend
if not exist venv (
    echo Creating Python virtual environment...
    python -m venv venv
)

call venv\Scripts\activate.bat
pip install -r requirements.txt >nul 2>&1

echo Backend starting on http://localhost:8000
start cmd /k "python main.py"

cd ..

echo 🌐 Starting Frontend...
cd frontend

if not exist node_modules (
    echo Installing npm dependencies...
    npm install
)

echo Frontend starting on http://localhost:5173
start cmd /k "npm run dev"

cd ..

timeout /t 3 >nul

echo.
echo 🎉 EdTech Blockchain App is starting!
echo.
echo 📱 Frontend: http://localhost:5173
echo 🔧 Backend: http://localhost:8000
echo 📚 API Docs: http://localhost:8000/docs
echo 🦊 MetaMask Test: file:///X:/Folder C/Project1/blockchainApp_local/metamask_test.html
echo.
echo 💡 Tips:
echo   - Make sure MetaMask is installed
echo   - Switch to Sepolia testnet
echo   - Get test ETH from https://sepoliafaucet.com/
echo.

REM Open the MetaMask test page
start "" "metamask_test.html"

pause
