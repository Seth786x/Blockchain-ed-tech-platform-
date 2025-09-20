# 🚀 Manual Startup Guide

## Terminal 1 - Backend (Python FastAPI)
```bash
cd backend
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt
python main.py
```
**Result**: Backend runs at http://localhost:8000

## Terminal 2 - Frontend (Vue.js + Vite)
```bash
cd frontend
npm install
npm run dev
```
**Result**: Frontend runs at http://localhost:5173

## What Each Part Does:

### 🖥️ **Backend (Port 8000)**
- **FastAPI server** with REST API
- **User authentication** (JWT tokens)
- **Database integration** (MongoDB)
- **Blockchain event listener** (monitors donations)
- **API documentation** at http://localhost:8000/docs

### 🌐 **Frontend (Port 5173)**
- **Vue.js application** with user interface
- **MetaMask integration** for wallet connection
- **Course browsing and purchasing**
- **Donation interface**
- **User dashboard and profiles**

## 🔗 **How They Work Together:**

1. **Frontend** → Makes API calls to **Backend** (http://localhost:8000)
2. **Backend** → Stores data in **MongoDB**
3. **Frontend** → Connects to **MetaMask** for blockchain transactions
4. **Backend** → Listens for blockchain events and syncs to database

## 🧪 **Testing URLs:**

- **Main App**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **MetaMask Test**: file:///path/to/metamask_test.html
- **Micro-Transaction Test**: file:///path/to/micro_test.html

## ⚡ **Quick Status Check:**

After starting both servers, you should see:
- ✅ Backend: "Server running on http://0.0.0.0:8000"
- ✅ Frontend: "Local: http://localhost:5173/"
- ✅ Both should show "ready" status
