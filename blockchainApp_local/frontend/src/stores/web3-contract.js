import { defineStore } from 'pinia'
import Web3 from 'web3'

// Smart Contract ABI (simplified for donation function)
const CONTRACT_ABI = [
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
    "inputs": [
      { "internalType": "uint256", "name": "courseId", "type": "uint256" }
    ],
    "name": "purchaseCourse",
    "outputs": [],
    "stateMutability": "payable",
    "type": "function"
  },
  {
    "inputs": [
      { "internalType": "uint256", "name": "courseId", "type": "uint256" },
      { "internalType": "address", "name": "user", "type": "address" }
    ],
    "name": "hasPurchased",
    "outputs": [ { "internalType": "bool", "name": "", "type": "bool" } ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "coursePrice",
    "outputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "anonymous": false,
    "inputs": [
      { "indexed": true, "internalType": "address", "name": "buyer", "type": "address" },
      { "indexed": true, "internalType": "uint256", "name": "courseId", "type": "uint256" },
      { "indexed": false, "internalType": "uint256", "name": "amount", "type": "uint256" }
    ],
    "name": "CoursePurchased",
    "type": "event"
  }
]

export const useWeb3ContractStore = defineStore('web3Contract', {
  state: () => ({
    web3: null,
    contract: null,
    account: null,
    isConnected: false,
    networkId: null,
    balance: '0',
    isCorrectNetwork: false,
    contractAddress: null,
    contractStats: null,
    lastTransaction: null
  }),

  getters: {
    shortAddress: (state) => {
      if (!state.account) return ''
      return `${state.account.slice(0, 6)}...${state.account.slice(-4)}`
    },
    
    formattedBalance: (state) => {
      if (!state.balance) return '0'
      return parseFloat(state.balance).toFixed(4)
    },
    
    networkName: (state) => {
      switch (state.networkId) {
        case 11155111: return 'Sepolia Testnet'
        case 1: return 'Ethereum Mainnet'
        case 1337: return 'Local Hardhat'
        default: return `Network ${state.networkId}`
      }
    }
  },

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
          
          // Get balance
          await this.updateBalance()
          
          // Initialize contract if we have the address
          await this.initializeContract()
          
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
        await this.initializeContract()
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
            await this.initializeContract()
          } catch (addError) {
            throw new Error('Failed to add Sepolia network')
          }
        } else {
          throw new Error('Failed to switch to Sepolia network')
        }
      }
    },

    async initializeContract() {
      if (!this.web3 || !this.isCorrectNetwork) return
      
      // For demo purposes, we'll use a hardcoded contract address
      // In production, this should be loaded from environment or deployment
      this.contractAddress = '0x5FbDB2315678afecb367f032d93F642f64180aa3' // Replace with actual deployed address
      
      if (this.contractAddress) {
        this.contract = new this.web3.eth.Contract(CONTRACT_ABI, this.contractAddress)
        await this.loadContractStats()
      }
    },

    async sendDonation(amount, purpose = "EdTech Donation") {
      if (!this.isConnected) {
        throw new Error('Wallet not connected')
      }

      if (!this.isCorrectNetwork) {
        await this.switchToSepolia()
      }

      if (!this.contract) {
        throw new Error('Smart contract not initialized')
      }

      try {
        const amountWei = this.web3.utils.toWei(amount.toString(), 'ether')
        
        console.log('Sending donation to smart contract:', {
          amount: amount,
          amountWei: amountWei,
          purpose: purpose,
          contractAddress: this.contractAddress
        })

        const result = await this.contract.methods.donate(purpose).send({
          from: this.account,
          value: amountWei,
          gas: 200000
        })

        this.lastTransaction = result
        await this.updateBalance()
        await this.loadContractStats()
        
        return result
      } catch (error) {
        console.error('Error sending donation:', error)
        throw error
      }
    },

    async loadContractStats() {
      if (!this.contract) return
      
      try {
        const stats = await this.contract.methods.getStats().call()
        this.contractStats = {
          totalDonationsCount: stats.totalDonationsCount,
          totalDonationsAmount: this.web3.utils.fromWei(stats.totalDonationsAmount, 'ether'),
          totalAllocatedAmount: this.web3.utils.fromWei(stats.totalAllocatedAmount, 'ether'),
          totalWithdrawnAmount: this.web3.utils.fromWei(stats.totalWithdrawnAmount, 'ether'),
          contractBalance: this.web3.utils.fromWei(stats.contractBalance, 'ether')
        }
      } catch (error) {
        console.error('Error loading contract stats:', error)
      }
    },

    async getDonation(donationId) {
      if (!this.contract) return null
      
      try {
        const donation = await this.contract.methods.getDonation(donationId).call()
        return {
          id: donation.id,
          donor: donation.donor,
          amount: this.web3.utils.fromWei(donation.amount, 'ether'),
          purpose: donation.purpose,
          status: donation.status,
          timestamp: new Date(donation.timestamp * 1000)
        }
      } catch (error) {
        console.error('Error getting donation:', error)
        return null
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

    async purchaseCourse(courseId) {
      if (!this.isConnected) throw new Error('Wallet not connected')
      if (!this.contract) throw new Error('Smart contract not initialized')
      const priceWei = await this.contract.methods.coursePrice().call()
      return await this.contract.methods.purchaseCourse(courseId).send({
        from: this.account,
        value: priceWei,
        gas: 200000
      })
    },
    async hasPurchased(courseId) {
      if (!this.isConnected) return false
      if (!this.contract) return false
      return await this.contract.methods.hasPurchased(courseId, this.account).call()
    },
    async getCoursePrice() {
      if (!this.contract) return '0'
      const priceWei = await this.contract.methods.coursePrice().call()
      return this.web3.utils.fromWei(priceWei, 'ether')
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
      window.location.reload()
    },

    disconnectWallet() {
      this.web3 = null
      this.contract = null
      this.account = null
      this.isConnected = false
      this.networkId = null
      this.balance = '0'
      this.isCorrectNetwork = false
      this.contractStats = null
      this.lastTransaction = null
    },

    async checkConnection() {
      if (typeof window.ethereum !== 'undefined') {
        try {
          const accounts = await window.ethereum.request({ method: 'eth_accounts' })
          if (accounts.length > 0) {
            await this.connectWallet()
          }
        } catch (error) {
          console.error('Error checking connection:', error)
        }
      }
    }
  }
}) 