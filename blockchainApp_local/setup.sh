#!/bin/bash

# EdTech Hardware Learning Platform - Setup Script
# This script sets up the entire development environment

echo "🚀 Setting up EdTech Hardware Learning Platform..."
echo "================================================="

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js first."
    exit 1
fi

# Check if Python is installed
if ! command -v python &> /dev/null && ! command -v py &> /dev/null; then
    echo "❌ Python is not installed. Please install Python first."
    exit 1
fi

# Check if MongoDB is running
if ! pgrep mongod > /dev/null; then
    echo "⚠️  MongoDB is not running. Please start MongoDB service."
    echo "   Windows: net start MongoDB"
    echo "   macOS: brew services start mongodb-community"
    echo "   Linux: sudo systemctl start mongod"
fi

echo "📦 Installing dependencies..."

# Install backend dependencies
echo "🐍 Setting up Python backend..."
cd backend
if command -v py &> /dev/null; then
    py -m pip install -r requirements.txt
else
    pip install -r requirements.txt
fi
cd ..

# Install frontend dependencies
echo "🎨 Setting up Vue.js frontend..."
cd frontend
npm install
cd ..

# Install smart contract dependencies
echo "⛓️  Setting up Hardhat smart contracts..."
cd smart-contracts
npm install
cd ..

# Create environment file
echo "⚙️  Setting up environment configuration..."
if [ ! -f backend/.env ]; then
    cp backend/.env.example backend/.env
    echo "📝 Please edit backend/.env with your configuration"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "🏃‍♂️ To start development:"
echo "================================"
echo ""
echo "1. Start MongoDB (if not running):"
echo "   Windows: net start MongoDB"
echo "   macOS: brew services start mongodb-community"
echo "   Linux: sudo systemctl start mongod"
echo ""
echo "2. Start backend server:"
echo "   cd backend"
if command -v py &> /dev/null; then
    echo "   py main.py"
else
    echo "   python main.py"
fi
echo "   Backend: http://localhost:8000"
echo ""
echo "3. Start frontend (new terminal):"
echo "   cd frontend"
echo "   npm run dev"
echo "   Frontend: http://localhost:5173"
echo ""
echo "4. Start local blockchain (new terminal):"
echo "   cd smart-contracts"
echo "   npx hardhat node"
echo ""
echo "5. Deploy smart contracts (new terminal):"
echo "   cd smart-contracts"
echo "   npx hardhat run scripts/deploy.js --network localhost"
echo ""
echo "📚 Documentation: See README.md for detailed instructions"
echo "🔧 API Docs: http://localhost:8000/docs (after starting backend)"
echo ""
echo "Happy coding! 🎉"
