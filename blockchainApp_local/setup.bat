@echo off
echo 🚀 Setting up EdTech Hardware Learning Platform...
echo =================================================

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js is not installed. Please install Node.js first.
    pause
    exit /b 1
)

REM Check if Python is installed
py --version >nul 2>&1
if errorlevel 1 (
    python --version >nul 2>&1
    if errorlevel 1 (
        echo ❌ Python is not installed. Please install Python first.
        pause
        exit /b 1
    )
)

echo 📦 Installing dependencies...

REM Install backend dependencies
echo 🐍 Setting up Python backend...
cd backend
py -m pip install -r requirements.txt
if errorlevel 1 (
    python -m pip install -r requirements.txt
)
cd ..

REM Install frontend dependencies
echo 🎨 Setting up Vue.js frontend...
cd frontend
npm install
cd ..

REM Install smart contract dependencies
echo ⛓️  Setting up Hardhat smart contracts...
cd smart-contracts
npm install
cd ..

REM Create environment file
echo ⚙️  Setting up environment configuration...
if not exist backend\.env (
    copy backend\.env.example backend\.env
    echo 📝 Please edit backend\.env with your configuration
)

echo.
echo ✅ Setup complete!
echo.
echo 🏃‍♂️ To start development:
echo ================================
echo.
echo 1. Start MongoDB (if not running):
echo    net start MongoDB
echo.
echo 2. Start backend server:
echo    cd backend
echo    py main.py
echo    Backend: http://localhost:8000
echo.
echo 3. Start frontend (new command prompt):
echo    cd frontend
echo    npm run dev
echo    Frontend: http://localhost:5173
echo.
echo 4. Start local blockchain (new command prompt):
echo    cd smart-contracts
echo    npx hardhat node
echo.
echo 5. Deploy smart contracts (new command prompt):
echo    cd smart-contracts
echo    npx hardhat run scripts/deploy.js --network localhost
echo.
echo 📚 Documentation: See README.md for detailed instructions
echo 🔧 API Docs: http://localhost:8000/docs (after starting backend)
echo.
echo Happy coding! 🎉
pause
