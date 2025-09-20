# EdTech Blockchain App - Testing Guide

## 🚀 Quick Start Testing

### 1. **Start the Backend Server**
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
Expected: Server starts at http://localhost:8000

### 2. **Start the Frontend**
```bash
cd frontend
npm install
npm run dev
```
Expected: Frontend starts at http://localhost:5173

### 3. **Test MetaMask Connection**

#### Prerequisites:
- Install MetaMask browser extension
- Switch to Sepolia test network
- Get test ETH from: https://sepoliafaucet.com/

#### Testing Steps:
1. Open http://localhost:5173
2. Look for "Connect Wallet" button
3. Click it - MetaMask should popup
4. Approve connection
5. Check if your address appears in the UI

### 4. **Test Smart Contract Interaction**

#### First, you need the Contract ABI:
1. Go to `smart-contracts/artifacts/contracts/EdTechDonation.sol/`
2. Copy the ABI from `EdTechDonation.json`
3. Add it to `frontend/src/stores/web3.js`

## 🔧 **Fix Missing Contract ABI**

Your Web3 store needs the actual contract ABI. Here's how to get it:

### Option 1: Copy from Artifacts (if contract is compiled)
```javascript
// Replace the empty array in web3.js with the actual ABI
const DONATION_CONTRACT_ABI = [
  // Paste the ABI from artifacts/contracts/EdTechDonation.sol/EdTechDonation.json
]
```

### Option 2: Redeploy Contract and Get Fresh ABI
```bash
cd smart-contracts
npm install
npx hardhat compile
npx hardhat run scripts/deploy.js --network sepolia
```

## 🧪 **Current Testing Capabilities**

### ✅ **What Works Now:**
1. **MetaMask Connection**: Can connect and detect wallet
2. **Network Detection**: Checks if on Sepolia testnet
3. **Balance Display**: Shows ETH balance
4. **User Registration**: Can create accounts via API
5. **Authentication**: JWT-based login system

### ⚠️ **What Needs Setup:**
1. **Contract ABI**: Empty array needs real ABI
2. **Contract Deployment**: May need fresh deployment
3. **Environment Variables**: Update with real values

### ❌ **What Won't Work Yet:**
1. **Smart Contract Calls**: Without ABI, can't interact with contract
2. **Donation Transactions**: Needs contract ABI
3. **Course Purchases**: Needs contract deployment
4. **Event Listening**: Backend needs contract address

## 🎯 **Immediate Next Steps**

### Priority 1: Get Contract Working
1. Compile smart contracts
2. Deploy to Sepolia testnet  
3. Update contract address in .env
4. Copy ABI to frontend

### Priority 2: Test Basic Flow
1. Connect MetaMask
2. Register user account
3. Make test donation
4. Verify transaction appears

### Priority 3: Test Advanced Features
1. School registration
2. Fund allocation
3. Course purchases
4. Event monitoring

## 🐛 **Common Issues & Solutions**

### MetaMask Not Connecting:
- Check if MetaMask is installed
- Make sure you're on Sepolia network
- Clear browser cache
- Check browser console for errors

### Backend Errors:
- Check MongoDB is running
- Verify environment variables
- Check port 8000 is available

### Contract Errors:
- Verify contract is deployed
- Check contract address is correct
- Ensure ABI matches deployed contract

## 📱 **Mobile Testing**
- Use MetaMask mobile app
- Access via mobile browser
- Test responsive design

## 🔐 **Security Testing**
- Test with different wallet addresses
- Try invalid inputs
- Test rate limiting
- Check error handling
