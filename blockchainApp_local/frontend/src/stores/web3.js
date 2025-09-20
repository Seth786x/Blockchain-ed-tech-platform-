import { defineStore } from 'pinia'
import Web3 from 'web3'

// Import contract ABI (you'll need to generate this from your smart contract)
const DONATION_CONTRACT_ABI = [
  {
    "inputs": [],
    "stateMutability": "nonpayable",
    "type": "constructor"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "owner",
        "type": "address"
      }
    ],
    "name": "OwnableInvalidOwner",
    "type": "error"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "account",
        "type": "address"
      }
    ],
    "name": "OwnableUnauthorizedAccount",
    "type": "error"
  },
  {
    "inputs": [],
    "name": "ReentrancyGuardReentrantCall",
    "type": "error"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "internalType": "address",
        "name": "buyer",
        "type": "address"
      },
      {
        "indexed": true,
        "internalType": "uint256",
        "name": "courseId",
        "type": "uint256"
      },
      {
        "indexed": false,
        "internalType": "uint256",
        "name": "amount",
        "type": "uint256"
      }
    ],
    "name": "CoursePurchased",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "internalType": "uint256",
        "name": "donationId",
        "type": "uint256"
      },
      {
        "indexed": true,
        "internalType": "address",
        "name": "donor",
        "type": "address"
      },
      {
        "indexed": false,
        "internalType": "uint256",
        "name": "amount",
        "type": "uint256"
      },
      {
        "indexed": false,
        "internalType": "string",
        "name": "purpose",
        "type": "string"
      }
    ],
    "name": "DonationReceived",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "internalType": "uint256",
        "name": "allocationId",
        "type": "uint256"
      },
      {
        "indexed": true,
        "internalType": "uint256",
        "name": "schoolId",
        "type": "uint256"
      },
      {
        "indexed": false,
        "internalType": "uint256",
        "name": "amount",
        "type": "uint256"
      },
      {
        "indexed": false,
        "internalType": "string",
        "name": "purpose",
        "type": "string"
      }
    ],
    "name": "FundsAllocated",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "internalType": "uint256",
        "name": "schoolId",
        "type": "uint256"
      },
      {
        "indexed": false,
        "internalType": "uint256",
        "name": "amount",
        "type": "uint256"
      },
      {
        "indexed": true,
        "internalType": "address",
        "name": "recipient",
        "type": "address"
      }
    ],
    "name": "FundsWithdrawn",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "internalType": "address",
        "name": "previousOwner",
        "type": "address"
      },
      {
        "indexed": true,
        "internalType": "address",
        "name": "newOwner",
        "type": "address"
      }
    ],
    "name": "OwnershipTransferred",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "internalType": "uint256",
        "name": "schoolId",
        "type": "uint256"
      },
      {
        "indexed": true,
        "internalType": "address",
        "name": "schoolWallet",
        "type": "address"
      },
      {
        "indexed": false,
        "internalType": "string",
        "name": "name",
        "type": "string"
      }
    ],
    "name": "SchoolRegistered",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "internalType": "uint256",
        "name": "schoolId",
        "type": "uint256"
      },
      {
        "indexed": true,
        "internalType": "address",
        "name": "verifier",
        "type": "address"
      }
    ],
    "name": "SchoolVerified",
    "type": "event"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "donationId",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "schoolId",
        "type": "uint256"
      },
      {
        "internalType": "string",
        "name": "purpose",
        "type": "string"
      }
    ],
    "name": "allocateFunds",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "",
        "type": "uint256"
      }
    ],
    "name": "allocations",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "id",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "schoolId",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "donationId",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "amount",
        "type": "uint256"
      },
      {
        "internalType": "string",
        "name": "purpose",
        "type": "string"
      },
      {
        "internalType": "uint256",
        "name": "timestamp",
        "type": "uint256"
      },
      {
        "internalType": "bool",
        "name": "withdrawn",
        "type": "bool"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "coursePrice",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "",
        "type": "uint256"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "",
        "type": "uint256"
      },
      {
        "internalType": "address",
        "name": "",
        "type": "address"
      }
    ],
    "name": "coursePurchases",
    "outputs": [
      {
        "internalType": "bool",
        "name": "",
        "type": "bool"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "string",
        "name": "purpose",
        "type": "string"
      }
    ],
    "name": "donate",
    "outputs": [],
    "stateMutability": "payable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "",
        "type": "uint256"
      }
    ],
    "name": "donations",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "id",
        "type": "uint256"
      },
      {
        "internalType": "address",
        "name": "donor",
        "type": "address"
      },
      {
        "internalType": "uint256",
        "name": "amount",
        "type": "uint256"
      },
      {
        "internalType": "string",
        "name": "purpose",
        "type": "string"
      },
      {
        "internalType": "enum EdTechDonation.DonationStatus",
        "name": "status",
        "type": "uint8"
      },
      {
        "internalType": "uint256",
        "name": "timestamp",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "allocatedToSchool",
        "type": "uint256"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "emergencyWithdraw",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "getContractBalance",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "",
        "type": "uint256"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "donationId",
        "type": "uint256"
      }
    ],
    "name": "getDonation",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "id",
        "type": "uint256"
      },
      {
        "internalType": "address",
        "name": "donor",
        "type": "address"
      },
      {
        "internalType": "uint256",
        "name": "amount",
        "type": "uint256"
      },
      {
        "internalType": "string",
        "name": "purpose",
        "type": "string"
      },
      {
        "internalType": "enum EdTechDonation.DonationStatus",
        "name": "status",
        "type": "uint8"
      },
      {
        "internalType": "uint256",
        "name": "timestamp",
        "type": "uint256"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "getDonationCount",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "",
        "type": "uint256"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "schoolId",
        "type": "uint256"
      }
    ],
    "name": "getSchoolAllocations",
    "outputs": [
      {
        "internalType": "uint256[]",
        "name": "",
        "type": "uint256[]"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "schoolId",
        "type": "uint256"
      }
    ],
    "name": "getSchoolBalance",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "",
        "type": "uint256"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "getStats",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "totalDonationsCount",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "totalDonationsAmount",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "totalAllocatedAmount",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "totalWithdrawnAmount",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "contractBalance",
        "type": "uint256"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "getTotalAllocations",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "",
        "type": "uint256"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "getTotalDonations",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "",
        "type": "uint256"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "getTotalSchools",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "",
        "type": "uint256"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "courseId",
        "type": "uint256"
      },
      {
        "internalType": "address",
        "name": "user",
        "type": "address"
      }
    ],
    "name": "hasPurchased",
    "outputs": [
      {
        "internalType": "bool",
        "name": "",
        "type": "bool"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "owner",
    "outputs": [
      {
        "internalType": "address",
        "name": "",
        "type": "address"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "courseId",
        "type": "uint256"
      }
    ],
    "name": "purchaseCourse",
    "outputs": [],
    "stateMutability": "payable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "schoolWallet",
        "type": "address"
      },
      {
        "internalType": "string",
        "name": "name",
        "type": "string"
      },
      {
        "internalType": "string",
        "name": "contactInfo",
        "type": "string"
      }
    ],
    "name": "registerSchool",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "renounceOwnership",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "",
        "type": "uint256"
      }
    ],
    "name": "schoolAllocations",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "",
        "type": "uint256"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "",
        "type": "address"
      }
    ],
    "name": "schoolByWallet",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "",
        "type": "uint256"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "",
        "type": "uint256"
      }
    ],
    "name": "schools",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "id",
        "type": "uint256"
      },
      {
        "internalType": "address",
        "name": "walletAddress",
        "type": "address"
      },
      {
        "internalType": "string",
        "name": "name",
        "type": "string"
      },
      {
        "internalType": "string",
        "name": "contactInfo",
        "type": "string"
      },
      {
        "internalType": "enum EdTechDonation.SchoolStatus",
        "name": "status",
        "type": "uint8"
      },
      {
        "internalType": "uint256",
        "name": "totalReceived",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "totalWithdrawn",
        "type": "uint256"
      },
      {
        "internalType": "uint256",
        "name": "registrationTimestamp",
        "type": "uint256"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "newPriceWei",
        "type": "uint256"
      }
    ],
    "name": "setCoursePrice",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "totalAllocated",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "",
        "type": "uint256"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "totalDonations",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "",
        "type": "uint256"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "totalWithdrawn",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "",
        "type": "uint256"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "newOwner",
        "type": "address"
      }
    ],
    "name": "transferOwnership",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "schoolId",
        "type": "uint256"
      }
    ],
    "name": "verifySchool",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "allocationId",
        "type": "uint256"
      }
    ],
    "name": "withdrawFunds",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  }
]

export const useWeb3Store = defineStore('web3', {
  state: () => ({
    web3: null,
    account: null,
    isConnected: false,
    networkId: null,
    balance: '0',
    isCorrectNetwork: false,
    donationContract: null,
    contractAddress: '0xA83dE1A13494B6B5bAaF6C7A30eC22acE666e0C0' // Your deployed contract address
  }),

  actions: {
    async connectWallet() {
      try {
        if (typeof window.ethereum !== 'undefined') {
          // Request account access
          await window.ethereum.request({ method: 'eth_requestAccounts' })
          
          // Initialize Web3
          this.web3 = new Web3(window.ethereum)
          
          // Get account
          const accounts = await this.web3.eth.getAccounts()
          this.account = accounts[0]
          
          // Get network ID
          this.networkId = await this.web3.eth.net.getId()
          this.isCorrectNetwork = this.networkId === 11155111 // Sepolia chain ID
          
          // Initialize contract
          if (this.isCorrectNetwork && DONATION_CONTRACT_ABI.length > 0) {
            this.donationContract = new this.web3.eth.Contract(DONATION_CONTRACT_ABI, this.contractAddress)
          }
          
          // Get balance
          await this.updateBalance()
          
          this.isConnected = true
          
          // Listen for account changes
          window.ethereum.on('accountsChanged', this.handleAccountsChanged)
          window.ethereum.on('chainChanged', this.handleChainChanged)
          
          return this.account
        } else {
          throw new Error('MetaMask is not installed')
        }
      } catch (error) {
        console.error('Error connecting wallet:', error)
        throw error
      }
    },

    async switchToSepolia() {
      if (!window.ethereum) {
        throw new Error('MetaMask is not installed')
      }

      try {
        await window.ethereum.request({
          method: 'wallet_switchEthereumChain',
          params: [{ chainId: '0xAA36A7' }], // Sepolia chain ID in hex
        })
        this.isCorrectNetwork = true
        await this.updateBalance()
      } catch (switchError) {
        // If the chain has not been added to MetaMask
        if (switchError.code === 4902) {
          try {
            await window.ethereum.request({
              method: 'wallet_addEthereumChain',
              params: [
                {
                  chainId: '0xAA36A7',
                  chainName: 'Sepolia Test Network',
                  nativeCurrency: {
                    name: 'Sepolia ETH',
                    symbol: 'SEP',
                    decimals: 18,
                  },
                  rpcUrls: ['https://sepolia.infura.io/v3/d13137512ce84238b1838bd9e3e4d78c'],
                  blockExplorerUrls: ['https://sepolia.etherscan.io'],
                },
              ],
            })
            this.isCorrectNetwork = true
            await this.updateBalance()
          } catch (addError) {
            throw new Error('Failed to add Sepolia network')
          }
        } else {
          throw new Error('Failed to switch to Sepolia network')
        }
      }
    },

    async sendDonation(amount, purpose = "EdTech Donation") {
      if (!this.isConnected) {
        throw new Error('Wallet not connected')
      }

      if (!this.isCorrectNetwork) {
        await this.switchToSepolia()
      }

      if (!this.donationContract) {
        throw new Error('Donation contract not initialized')
      }

      try {
        const amountWei = this.web3.utils.toWei(amount.toString(), 'ether')
        
        // Call the donate function on the smart contract
        const result = await this.donationContract.methods.donate(purpose).send({
          from: this.account,
          value: amountWei,
          gas: 100000 // Estimate gas properly in production
        })

        await this.updateBalance()
        return result
      } catch (error) {
        console.error('Error sending donation:', error)
        throw error
      }
    },

    async updateBalance() {
      if (this.web3 && this.account) {
        try {
          const balanceWei = await this.web3.eth.getBalance(this.account)
          this.balance = this.web3.utils.fromWei(balanceWei, 'ether')
        } catch (error) {
          console.error('Error updating balance:', error)
        }
      }
    },

    async sendTransaction(to, amount) {
      if (!this.isConnected) {
        throw new Error('Wallet not connected')
      }

      try {
        const amountWei = this.web3.utils.toWei(amount.toString(), 'ether')
        
        const transaction = {
          from: this.account,
          to: to,
          value: amountWei,
          gas: 21000
        }

        const result = await this.web3.eth.sendTransaction(transaction)
        await this.updateBalance()
        
        return result
      } catch (error) {
        console.error('Error sending transaction:', error)
        throw error
      }
    },

    async callContract(contractAddress, abi, methodName, params = []) {
      if (!this.isConnected) {
        throw new Error('Wallet not connected')
      }

      try {
        const contract = new this.web3.eth.Contract(abi, contractAddress)
        const result = await contract.methods[methodName](...params).call({
          from: this.account
        })
        
        return result
      } catch (error) {
        console.error('Error calling contract:', error)
        throw error
      }
    },

    async sendContractTransaction(contractAddress, abi, methodName, params = [], value = 0) {
      if (!this.isConnected) {
        throw new Error('Wallet not connected')
      }

      try {
        const contract = new this.web3.eth.Contract(abi, contractAddress)
        const method = contract.methods[methodName](...params)
        
        const gas = await method.estimateGas({ from: this.account, value })
        
        const result = await method.send({
          from: this.account,
          gas: Math.floor(gas * 1.1), // Add 10% buffer
          value
        })

        await this.updateBalance()
        return result
      } catch (error) {
        console.error('Error sending contract transaction:', error)
        throw error
      }
    },

    handleAccountsChanged(accounts) {
      if (accounts.length === 0) {
        this.disconnectWallet()
      } else {
        this.account = accounts[0]
        this.updateBalance()
      }
    },

    handleChainChanged(chainId) {
      this.networkId = parseInt(chainId, 16)
      this.isCorrectNetwork = this.networkId === 11155111
      this.updateBalance()
    },

    disconnectWallet() {
      this.web3 = null
      this.account = null
      this.isConnected = false
      this.networkId = null
      this.balance = '0'
      this.isCorrectNetwork = false
      
      if (window.ethereum) {
        window.ethereum.removeListener('accountsChanged', this.handleAccountsChanged)
        window.ethereum.removeListener('chainChanged', this.handleChainChanged)
      }
    },

    async checkConnection() {
      if (typeof window.ethereum !== 'undefined') {
        try {
          const accounts = await window.ethereum.request({ method: 'eth_accounts' })
          if (accounts.length > 0) {
            await this.connectWallet()
          }
        } catch (error) {
          console.error('Error checking wallet connection:', error)
        }
      }
    }
  },

  getters: {
    shortAddress: (state) => {
      if (!state.account) return ''
      return `${state.account.slice(0, 6)}...${state.account.slice(-4)}`
    },
    
    formattedBalance: (state) => {
      return parseFloat(state.balance).toFixed(4)
    },

    networkName: (state) => {
      switch (state.networkId) {
        case 1: return 'Ethereum Mainnet'
        case 11155111: return 'Sepolia Testnet'
        case 1337: return 'Local Network'
        default: return 'Unknown Network'
      }
    }
  }
})
