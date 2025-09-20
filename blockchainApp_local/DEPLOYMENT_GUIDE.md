# 🚀 Real Blockchain Deployment Guide

## **Quick Setup for Real Blockchain Donations**

### **1. Deploy Smart Contract to Sepolia Testnet**

```bash
# Navigate to smart contracts directory
cd smart-contracts

# Install dependencies
npm install

# Compile contracts
npx hardhat compile

# Deploy to Sepolia (make sure you have Sepolia ETH)
npx hardhat run scripts/deploy.js --network sepolia
```

**After deployment, you'll get a contract address like:**
```
✅ EdTechDonation deployed to: 0x1234567890abcdef...
```

### **2. Update Frontend Contract Address**

Edit `frontend/src/stores/web3-contract.js` and replace the hardcoded address:

```javascript
// Replace this line:
this.contractAddress = '0x5FbDB2315678afecb367f032d93F642f64180aa3'

// With your actual deployed address:
this.contractAddress = '0x1234567890abcdef...' // Your deployed address
```

### **3. Get Sepolia Test ETH**

Visit these faucets to get free test ETH:
- https://sepoliafaucet.com/
- https://www.infura.io/faucet/sepolia

### **4. Test Real Blockchain Donations**

1. Start your frontend: `npm run dev`
2. Go to `/donations/blockchain`
3. Connect MetaMask (make sure you're on Sepolia)
4. Send a real donation to the smart contract!

## **What's Different Now**

### **✅ Real Smart Contract Integration**
- Donations go to your deployed smart contract
- Each donation gets a unique ID on the blockchain
- All transactions are verifiable on Etherscan
- Smart contract tracks total donations and balances

### **✅ Real-Time Blockchain Data**
- Contract statistics update in real-time
- Transaction hashes are recorded
- Donation history is stored on-chain
- Transparent and immutable records

### **✅ Professional Features**
- Proper error handling
- Gas estimation
- Network validation
- Transaction confirmation

## **For Production**

### **1. Deploy to Ethereum Mainnet**
```bash
npx hardhat run scripts/deploy.js --network mainnet
```

### **2. Update Environment Variables**
```env
ETHEREUM_RPC_URL=https://mainnet.infura.io/v3/YOUR_PROJECT_ID
PRIVATE_KEY=your_mainnet_private_key
```

### **3. Verify Contract on Etherscan**
The deployment script will automatically verify your contract.

## **Troubleshooting**

### **"Contract not initialized" Error**
- Make sure you've updated the contract address in the frontend
- Check that you're on the correct network (Sepolia)

### **"Insufficient funds" Error**
- Get more Sepolia test ETH from the faucets
- Check your wallet balance

### **"Transaction failed" Error**
- Increase gas limit if needed
- Check network connection
- Ensure MetaMask is connected

## **Next Steps**

1. **Deploy the smart contract** using the guide above
2. **Update the contract address** in the frontend
3. **Test with real donations** on Sepolia
4. **Integrate with backend** to sync blockchain data
5. **Deploy to mainnet** for production use

Your blockchain integration is now ready for real use! 🎉 