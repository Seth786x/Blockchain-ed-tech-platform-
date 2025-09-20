<template>
  <div class="blockchain-donation">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-8">
          <div class="card shadow-lg">
            <div class="card-header bg-primary text-white">
              <h3 class="mb-0">
                <i class="fab fa-ethereum me-2"></i>
                Real Smart Contract Donation
              </h3>
              <p class="mb-0">Send real ETH to our smart contract on Sepolia testnet</p>
            </div>
            <div class="card-body">
              <!-- Wallet Connection Status -->
              <div v-if="!web3Store.isConnected" class="text-center mb-4">
                <i class="fab fa-ethereum fa-4x text-primary mb-3"></i>
                <h5>Connect Your Wallet</h5>
                <p class="text-muted">Connect MetaMask to send real blockchain donations to our smart contract</p>
                <button @click="connectWallet" class="btn btn-primary btn-lg">
                  <i class="fab fa-ethereum me-2"></i>Connect MetaMask
                </button>
              </div>

              <!-- Network Warning -->
              <div v-else-if="!web3Store.isCorrectNetwork" class="alert alert-warning">
                <h6><i class="fas fa-exclamation-triangle me-2"></i>Wrong Network</h6>
                <p class="mb-2">You need to be on Sepolia testnet to send donations to our smart contract.</p>
                <button @click="switchNetwork" class="btn btn-warning">
                  Switch to Sepolia
                </button>
              </div>

              <!-- Connected Wallet Info -->
              <div v-else>
                <div class="row mb-4">
                  <div class="col-md-6">
                    <div class="card bg-light">
                      <div class="card-body text-center">
                        <h6>Connected Wallet</h6>
                        <p class="mb-0 font-monospace">{{ web3Store.shortAddress }}</p>
                        <small class="text-muted">{{ web3Store.networkName }}</small>
                      </div>
                    </div>
                  </div>
                  <div class="col-md-6">
                    <div class="card bg-light">
                      <div class="card-body text-center">
                        <h6>Your Balance</h6>
                        <p class="mb-0">{{ web3Store.formattedBalance }} ETH</p>
                        <small class="text-muted">≈ ${{ (parseFloat(web3Store.balance) * 2000).toFixed(2) }}</small>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Smart Contract Info -->
                <div v-if="web3Store.contractStats" class="row mb-4">
                  <div class="col-12">
                    <div class="card bg-success text-white">
                      <div class="card-body">
                        <h6><i class="fas fa-chart-bar me-2"></i>Smart Contract Statistics</h6>
                        <div class="row text-center">
                          <div class="col-md-3">
                            <div class="small">Total Donations</div>
                            <div class="fw-bold">{{ web3Store.contractStats.totalDonationsCount }}</div>
                          </div>
                          <div class="col-md-3">
                            <div class="small">Total Amount</div>
                            <div class="fw-bold">{{ web3Store.contractStats.totalDonationsAmount }} ETH</div>
                          </div>
                          <div class="col-md-3">
                            <div class="small">Contract Balance</div>
                            <div class="fw-bold">{{ web3Store.contractStats.contractBalance }} ETH</div>
                          </div>
                          <div class="col-md-3">
                            <div class="small">Contract Address</div>
                            <div class="fw-bold font-monospace small">{{ web3Store.contractAddress?.slice(0, 10) }}...</div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Donation Form -->
                <form @submit.prevent="sendDonation">
                  <div class="mb-4">
                    <label class="form-label">Donation Amount (ETH)</label>
                    <div class="input-group">
                      <input 
                        type="number" 
                        class="form-control" 
                        v-model="donationAmount" 
                        step="0.001"
                        min="0.001"
                        max="1"
                        required
                        placeholder="0.001"
                      >
                      <span class="input-group-text">ETH</span>
                    </div>
                    <div class="form-text">
                      Approximately ${{ (donationAmount * 2000).toFixed(2) }} USD
                      (Minimum: 0.001 ETH for testing)
                    </div>
                  </div>

                  <div class="mb-4">
                    <label class="form-label">Message (Optional)</label>
                    <textarea 
                      class="form-control" 
                      v-model="donationMessage" 
                      rows="3"
                      placeholder="Leave a message with your donation..."
                    ></textarea>
                  </div>

                  <div class="mb-4">
                    <div class="card bg-info text-white">
                      <div class="card-body">
                        <h6><i class="fas fa-info-circle me-2"></i>About This Smart Contract Donation</h6>
                        <ul class="mb-0 small">
                          <li>This sends <strong>real ETH</strong> to our smart contract on Sepolia testnet</li>
                          <li>Your donation is recorded on the blockchain with a unique ID</li>
                          <li>You'll get a real transaction hash that's verifiable on Etherscan</li>
                          <li>The smart contract tracks all donations transparently</li>
                          <li>Contract address: <code>{{ web3Store.contractAddress }}</code></li>
                        </ul>
                      </div>
                    </div>
                  </div>

                  <div class="d-flex justify-content-between">
                    <button type="button" class="btn btn-secondary" @click="goBack">
                      Cancel
                    </button>
                    <button type="submit" class="btn btn-primary btn-lg" :disabled="isSubmitting || donationAmount <= 0">
                      <span v-if="isSubmitting" class="spinner-border spinner-border-sm me-2"></span>
                      <i v-else class="fab fa-ethereum me-2"></i>
                      {{ isSubmitting ? 'Sending to Smart Contract...' : `Send ${donationAmount} ETH` }}
                    </button>
                  </div>
                </form>

                <!-- Transaction Result -->
                <div v-if="lastTransaction" class="mt-4">
                  <div class="alert alert-success">
                    <h6><i class="fas fa-check-circle me-2"></i>Smart Contract Transaction Successful!</h6>
                    <p class="mb-2">Your donation has been recorded on the blockchain:</p>
                    <div class="d-flex justify-content-between align-items-center">
                      <code class="small">{{ lastTransaction.transactionHash }}</code>
                      <a :href="`https://sepolia.etherscan.io/tx/${lastTransaction.transactionHash}`" 
                         target="_blank" 
                         class="btn btn-sm btn-outline-success">
                        View on Etherscan
                      </a>
                    </div>
                    <div class="mt-2">
                      <small class="text-muted">
                        Block: {{ lastTransaction.blockNumber }} | 
                        Gas Used: {{ lastTransaction.gasUsed }}
                      </small>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Get Test ETH Section -->
              <div class="mt-4 pt-4 border-top">
                <h6>Need Sepolia Test ETH?</h6>
                <p class="text-muted small">Get free test ETH from these faucets:</p>
                <div class="row">
                  <div class="col-md-6">
                    <a href="https://sepoliafaucet.com/" target="_blank" class="btn btn-outline-primary btn-sm w-100 mb-2">
                      Sepolia Faucet #1
                    </a>
                  </div>
                  <div class="col-md-6">
                    <a href="https://www.infura.io/faucet/sepolia" target="_blank" class="btn btn-outline-primary btn-sm w-100 mb-2">
                      Infura Sepolia Faucet
                    </a>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useWeb3ContractStore } from '@/stores/web3-contract'

export default {
  name: 'BlockchainDonation',
  setup() {
    const web3Store = useWeb3ContractStore()
    return { web3Store }
  },
  data() {
    return {
      donationAmount: 0.001,
      donationMessage: '',
      isSubmitting: false,
      lastTransaction: null
    }
  },
  async mounted() {
    // Check if already connected
    await this.web3Store.checkConnection()
  },
  methods: {
    async connectWallet() {
      try {
        await this.web3Store.connectWallet()
        if (!this.web3Store.isCorrectNetwork) {
          await this.switchNetwork()
        }
      } catch (error) {
        alert(`Error connecting wallet: ${error.message}`)
      }
    },

    async switchNetwork() {
      try {
        await this.web3Store.switchToSepolia()
      } catch (error) {
        alert(`Error switching network: ${error.message}`)
      }
    },

    async sendDonation() {
      this.isSubmitting = true
      this.lastTransaction = null

      try {
        console.log(`Sending ${this.donationAmount} ETH to smart contract...`)
        
        const result = await this.web3Store.sendDonation(
          this.donationAmount, 
          this.donationMessage || "EdTech Platform Donation"
        )

        console.log('Smart contract transaction successful:', result)
        this.lastTransaction = result

        // Show success message
        alert(`🎉 Smart Contract Donation Successful!\n\nAmount: ${this.donationAmount} ETH\nTransaction: ${result.transactionHash}\n\nView on Etherscan: https://sepolia.etherscan.io/tx/${result.transactionHash}`)

        // Reset form
        this.donationAmount = 0.001
        this.donationMessage = ''

      } catch (error) {
        console.error('Smart contract transaction failed:', error)
        alert(`Transaction failed: ${error.message}`)
      } finally {
        this.isSubmitting = false
      }
    },

    goBack() {
      this.$router.go(-1)
    }
  }
}
</script>

<style scoped>
.blockchain-donation {
  padding: 20px 0;
  min-height: 80vh;
}

.card {
  border-radius: 15px;
}

.card-header {
  border-radius: 15px 15px 0 0;
}

.form-control:focus {
  border-color: #0d6efd;
  box-shadow: 0 0 0 0.2rem rgba(13, 110, 253, 0.25);
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
}

.btn-primary:hover {
  background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%);
}

code {
  background-color: #f8f9fa;
  padding: 0.2rem 0.4rem;
  border-radius: 0.25rem;
  font-size: 0.875em;
}

.font-monospace {
  font-family: 'Courier New', monospace;
}

.bg-info {
  background-color: #0dcaf0 !important;
}

.alert-success {
  border-left: 4px solid #198754;
}

.spinner-border-sm {
  width: 1rem;
  height: 1rem;
}
</style>
