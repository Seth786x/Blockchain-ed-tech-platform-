import { defineStore } from 'pinia'
import Web3 from 'web3'

export const useWeb3Store = defineStore('web3', {
  state: () => ({
    web3: null,
    account: null,
    isConnected: false,
    networkId: null,
    balance: '0',
    isCorrectNetwork: false,
    targetAddress: '0xA83dE1A13494B6B5bAaF6C7A30eC22acE666e0C0' // Your address for testing
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
                  rpcUrls: ['https://sepolia.infura.io/v3/9aa3d95b3bc440fa88ea12eaa4456161'],
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

      try {
        const amountWei = this.web3.utils.toWei(amount.toString(), 'ether')
        
        const transaction = {
          from: this.account,
          to: this.targetAddress, // Your address for testing
          value: amountWei,
          gas: 21000
        }

        console.log('Sending donation transaction:', transaction)
        const result = await this.web3.eth.sendTransaction(transaction)
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
