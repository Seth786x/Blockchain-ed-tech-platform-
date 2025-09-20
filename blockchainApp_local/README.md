# EdTech Hardware Learning Platform

A blockchain-based educational platform focused on computer hardware learning with transparent donation and resource allocation system.

## 🎯 Project Overview

This full-stack application combines:
- **Educational Content**: Computer hardware courses (CPU, GPU, RAM, etc.)
- **Blockchain Transparency**: Smart contracts for donation tracking
- **Resource Allocation**: Fair distribution of funds to schools
- **Impact Measurement**: Real-time tracking of educational outcomes

## 🏗️ Architecture

### Frontend (Vue.js)
- **Framework**: Vue 3 + Vite
- **State Management**: Pinia
- **UI Framework**: Bootstrap 5
- **Web3 Integration**: Ethers.js + Web3.js
- **Wallet Support**: MetaMask

### Backend (Python FastAPI)
- **Framework**: FastAPI
- **Database**: MongoDB
- **Authentication**: JWT tokens
- **File Storage**: IPFS
- **Blockchain**: Web3.py integration

### Smart Contracts (Solidity)
- **Framework**: Hardhat
- **Language**: Solidity ^0.8.19
- **Standards**: OpenZeppelin
- **Networks**: Ethereum, Sepolia testnet

## 📁 Project Structure

```
blockchainApp_local/
├── frontend/                 # Vue.js frontend
│   ├── src/
│   │   ├── views/           # Page components
│   │   ├── stores/          # Pinia state management
│   │   └── App.vue          # Main app component
│   ├── package.json
│   └── vite.config.js
├── backend/                  # FastAPI backend
│   ├── routes/              # API routes
│   ├── models.py            # Database models
│   ├── main.py              # FastAPI app
│   └── requirements.txt
└── smart-contracts/          # Solidity contracts
    ├── contracts/
    │   └── EdTechDonation.sol
    ├── scripts/
    │   └── deploy.js
    └── hardhat.config.js
```

## 🚀 Installation & Setup

### Prerequisites
- Node.js (v16+)
- Python (3.8+)
- MongoDB
- MetaMask browser extension

### 1. Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Install Frontend Dependencies

```bash
cd frontend
npm install
```

### 3. Install Smart Contract Dependencies

```bash
cd smart-contracts
npm install
```

### 4. Configure Environment

Copy `.env.example` to `.env` in the backend directory and fill in your values:

```bash
cp backend/.env.example backend/.env
```

### 5. Start MongoDB

Ensure MongoDB is running on `mongodb://localhost:27017`

## 🏃‍♂️ Running the Application

### 1. Start Backend Server

```bash
cd backend
python main.py
```
Backend will run on: http://localhost:8000

### 2. Start Frontend Development Server

```bash
cd frontend
npm run dev
```
Frontend will run on: http://localhost:5173

### 3. Deploy Smart Contracts (Local)

```bash
cd smart-contracts
npx hardhat node                    # Terminal 1: Start local blockchain
npx hardhat run scripts/deploy.js   # Terminal 2: Deploy contracts
```

## 🔧 Key Features

### For Students
- 📚 Hardware courses (CPU, GPU, RAM, etc.)
- 🏆 Blockchain-verified certificates
- 📊 Progress tracking
- 💡 Interactive learning modules

### For Donors
- 💰 Transparent ETH donations
- 📈 Real-time impact tracking
- 🏫 Choose specific schools to support
- 🔍 Blockchain transaction verification

### For Schools
- 📝 Resource request submission
- 💻 Hardware equipment allocation
- 📊 Impact reporting
- 🔐 Secure fund withdrawal

### For Administrators
- ✅ School verification
- 📋 Resource allocation management
- 📊 Platform analytics
- 🛡️ Smart contract administration

## 🔗 API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `GET /api/auth/me` - Get current user

### Courses
- `GET /api/courses` - List courses
- `POST /api/courses` - Create course
- `GET /api/courses/{id}` - Get course details

### Donations
- `GET /api/donations` - List donations
- `POST /api/donations` - Record donation
- `GET /api/donations/stats` - Donation statistics

### Resources
- `GET /api/resources/schools` - List schools
- `POST /api/resources/requests` - Create resource request
- `PUT /api/resources/requests/{id}/allocate` - Allocate resources

## 🧪 Smart Contract Functions

### EdTechDonation.sol

#### Public Functions
- `donate(string purpose)` - Make a donation
- `getSchoolBalance(uint256 schoolId)` - Check school balance
- `getStats()` - Get platform statistics

#### Owner Functions
- `registerSchool(address wallet, string name, string contact)` - Register school
- `verifySchool(uint256 schoolId)` - Verify school
- `allocateFunds(uint256 donationId, uint256 schoolId, string purpose)` - Allocate donation

#### School Functions
- `withdrawFunds(uint256 allocationId)` - Withdraw allocated funds

## 📊 Database Schema

### MongoDB Collections

#### Users
```javascript
{
  _id: ObjectId,
  email: String,
  username: String,
  full_name: String,
  role: "student" | "instructor" | "school" | "donor" | "admin",
  wallet_address: String,
  created_at: Date
}
```

#### Courses
```javascript
{
  _id: ObjectId,
  title: String,
  description: String,
  component: "cpu" | "gpu" | "ram" | "motherboard" | "storage",
  level: "beginner" | "intermediate" | "advanced",
  instructor_id: String,
  modules: Array,
  created_at: Date
}
```

#### Donations
```javascript
{
  _id: ObjectId,
  donor_id: String,
  amount_eth: Number,
  transaction_hash: String,
  purpose: String,
  status: "pending" | "confirmed" | "allocated",
  created_at: Date
}
```

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
```

### Smart Contract Tests
```bash
cd smart-contracts
npx hardhat test
```

### Frontend Tests
```bash
cd frontend
npm run test
```

## 🚀 Deployment

### Production Environment

1. **Backend**: Deploy to cloud provider (AWS, GCP, Heroku)
2. **Frontend**: Build and deploy to CDN
3. **Smart Contracts**: Deploy to Ethereum mainnet
4. **Database**: Use MongoDB Atlas or cloud MongoDB

### Environment Variables

Set these in production:
- `MONGODB_URL` - Production MongoDB connection
- `SECRET_KEY` - JWT secret
- `ETHEREUM_RPC_URL` - Mainnet RPC endpoint
- `PRIVATE_KEY` - Deployment wallet private key

## 📈 Research Paper Potential

This project provides rich data for research papers on:

1. **"Blockchain-Based Transparency in Educational Funding"**
   - Donation tracking and allocation efficiency
   - Trust building in educational philanthropy

2. **"Impact Measurement in Decentralized Education Systems"**
   - Student outcome tracking
   - Resource allocation effectiveness

3. **"Computer Hardware Education Through Blockchain Technology"**
   - Learning outcome analysis
   - Certification verification systems

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License.

## 📞 Support

For questions or support:
- Email: support@edtechhardware.com
- GitHub Issues: [Create an issue](https://github.com/your-repo/issues)

---

**Built with ❤️ for transparent education funding and computer hardware learning.**
