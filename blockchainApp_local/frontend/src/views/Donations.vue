<template>
  <div class="donations-container">
    <!-- Header -->
    <div class="bg-primary text-white py-5">
      <div class="container">
        <div class="row align-items-center">
          <div class="col-md-8">
            <h1 class="display-5 fw-bold mb-3">
              <i class="fas fa-hand-holding-heart me-3"></i>
              Transparent Donations
            </h1>
            <p class="lead mb-0">Support education through blockchain-verified donations and track your impact</p>
          </div>
          <div class="col-md-4 text-end">
            <div class="btn-group">
              <router-link to="/donations/blockchain" class="btn btn-warning btn-lg me-2">
                <i class="fab fa-ethereum me-2"></i>Real Blockchain Demo
              </router-link>
              <div v-if="authStore.isDonor || authStore.isAdmin">
                <router-link to="/donations/new" class="btn btn-light btn-lg">
                  <i class="fas fa-plus me-2"></i>Make Donation
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="container py-5">
      <!-- Blockchain Statistics Cards -->
      <div class="row mb-5">
        <div class="col-md-3 mb-3" v-for="stat in blockchainStats" :key="stat.title">
          <div class="card border-0 shadow-sm text-center h-100">
            <div class="card-body">
              <div class="mb-3">
                <i :class="stat.icon" class="text-primary" style="font-size: 2.5rem;"></i>
              </div>
              <h3 class="fw-bold mb-1">{{ stat.value }}</h3>
              <p class="text-muted mb-0">{{ stat.title }}</p>
              <small v-if="stat.subtitle" class="text-success">{{ stat.subtitle }}</small>
            </div>
          </div>
        </div>
      </div>

      <!-- Smart Contract Status -->
      <div v-if="web3Store.contractStats" class="row mb-5">
        <div class="col-12">
          <div class="card border-0 shadow-sm">
            <div class="card-header bg-success text-white">
              <h5 class="mb-0">
                <i class="fab fa-ethereum me-2"></i>
                Smart Contract Statistics (Live from Blockchain)
              </h5>
            </div>
            <div class="card-body">
              <div class="row text-center">
                <div class="col-md-2">
                  <div class="small text-muted">Total Donations</div>
                  <div class="h4 fw-bold text-primary">{{ web3Store.contractStats.totalDonationsCount }}</div>
                </div>
                <div class="col-md-2">
                  <div class="small text-muted">Total Amount</div>
                  <div class="h4 fw-bold text-success">{{ web3Store.contractStats.totalDonationsAmount }} ETH</div>
                </div>
                <div class="col-md-2">
                  <div class="small text-muted">Contract Balance</div>
                  <div class="h4 fw-bold text-info">{{ web3Store.contractStats.contractBalance }} ETH</div>
                </div>
                <div class="col-md-2">
                  <div class="small text-muted">Allocated</div>
                  <div class="h4 fw-bold text-warning">{{ web3Store.contractStats.totalAllocatedAmount }} ETH</div>
                </div>
                <div class="col-md-2">
                  <div class="small text-muted">Withdrawn</div>
                  <div class="h4 fw-bold text-danger">{{ web3Store.contractStats.totalWithdrawnAmount }} ETH</div>
                </div>
                <div class="col-md-2">
                  <div class="small text-muted">Contract Address</div>
                  <div class="font-monospace small">{{ web3Store.contractAddress?.slice(0, 10) }}...</div>
                  <a :href="`https://sepolia.etherscan.io/address/${web3Store.contractAddress}`" 
                     target="_blank" 
                     class="btn btn-sm btn-outline-primary mt-1">
                    View on Etherscan
                  </a>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Donation Leaderboard -->
      <div class="row mb-5">
        <div class="col-md-6">
          <div class="card border-0 shadow-sm">
            <div class="card-header bg-white border-0">
              <h5 class="mb-0">
                <i class="fas fa-trophy me-2 text-warning"></i>
                Top Donors
              </h5>
            </div>
            <div class="card-body">
              <div v-if="leaderboard.length === 0" class="text-center py-4">
                <i class="fas fa-users text-muted" style="font-size: 3rem;"></i>
                <p class="mt-3 text-muted">No donations yet. Be the first to make a difference!</p>
                <router-link to="/donations/blockchain" class="btn btn-primary">
                  <i class="fab fa-ethereum me-2"></i>Make First Donation
                </router-link>
              </div>
              <div v-else>
                <div v-for="(donor, index) in leaderboard" :key="donor._id" class="d-flex align-items-center mb-3">
                  <div class="me-3">
                    <span class="badge bg-warning text-dark">{{ index + 1 }}</span>
                  </div>
                  <div class="flex-grow-1">
                    <h6 class="mb-1">{{ donor.donor_name }}</h6>
                    <small class="text-muted">{{ donor.donation_count }} donations</small>
                  </div>
                  <div class="text-end">
                    <div class="fw-bold text-success">{{ donor.total_eth }} ETH</div>
                    <small class="text-muted">${{ donor.total_usd?.toFixed(2) }}</small>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="col-md-6">
          <div class="card border-0 shadow-sm">
            <div class="card-header bg-white border-0">
              <h5 class="mb-0">
                <i class="fas fa-chart-line me-2 text-info"></i>
                Recent Donations
              </h5>
            </div>
            <div class="card-body">
              <div v-if="recentDonations.length === 0" class="text-center py-4">
                <i class="fas fa-heart text-muted" style="font-size: 3rem;"></i>
                <p class="mt-3 text-muted">No recent donations</p>
                <router-link to="/donations/blockchain" class="btn btn-primary">
                  <i class="fab fa-ethereum me-2"></i>Make First Donation
                </router-link>
              </div>
              <div v-else>
                <div v-for="donation in recentDonations" :key="donation.id" class="d-flex align-items-center mb-3">
                  <div class="me-3">
                    <i class="fas fa-heart text-danger"></i>
                  </div>
                  <div class="flex-grow-1">
                    <h6 class="mb-1">{{ donation.amount_eth }} ETH</h6>
                    <small class="text-muted">{{ donation.purpose }}</small>
                  </div>
                  <div class="text-end">
                    <div class="small text-muted">{{ formatDate(donation.created_at) }}</div>
                    <a v-if="donation.transaction_hash" 
                       :href="`https://sepolia.etherscan.io/tx/${donation.transaction_hash}`" 
                       target="_blank" 
                       class="btn btn-sm btn-outline-primary">
                      View on Etherscan
                    </a>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Impact Section -->
      <div class="row mb-5">
        <div class="col-12">
          <div class="card border-0 shadow-sm">
            <div class="card-header bg-info text-white">
              <h5 class="mb-0">
                <i class="fas fa-chart-pie me-2"></i>
                Donation Impact
              </h5>
            </div>
            <div class="card-body">
              <div class="row">
                <div class="col-md-4 text-center">
                  <div class="mb-3">
                    <i class="fas fa-laptop text-primary" style="font-size: 3rem;"></i>
                  </div>
                  <h4 class="fw-bold">Hardware Equipment</h4>
                  <p class="text-muted">Computers, tablets, and educational devices for schools</p>
                </div>
                <div class="col-md-4 text-center">
                  <div class="mb-3">
                    <i class="fas fa-graduation-cap text-success" style="font-size: 3rem;"></i>
                  </div>
                  <h4 class="fw-bold">Educational Resources</h4>
                  <p class="text-muted">Software licenses, learning materials, and online courses</p>
                </div>
                <div class="col-md-4 text-center">
                  <div class="mb-3">
                    <i class="fas fa-users text-warning" style="font-size: 3rem;"></i>
                  </div>
                  <h4 class="fw-bold">Student Support</h4>
                  <p class="text-muted">Scholarships, mentoring programs, and career guidance</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Call to Action -->
      <div class="row">
        <div class="col-12 text-center">
          <div class="card border-0 shadow-sm bg-gradient-primary text-white">
            <div class="card-body py-5">
              <h2 class="fw-bold mb-3">Ready to Make a Difference?</h2>
              <p class="lead mb-4">Join our community of donors and help bridge the digital divide in education</p>
              <div class="d-flex justify-content-center gap-3">
                <router-link to="/donations/blockchain" class="btn btn-warning btn-lg">
                  <i class="fab fa-ethereum me-2"></i>Send Blockchain Donation
                </router-link>
                <router-link to="/schools" class="btn btn-light btn-lg">
                  <i class="fas fa-school me-2"></i>View Schools
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useAuthStore } from '../stores/auth'
import { useWeb3ContractStore } from '@/stores/web3-contract'
import { donationsAPI } from '@/services/api'

export default {
  name: 'Donations',
  setup() {
    const authStore = useAuthStore()
    const web3Store = useWeb3ContractStore()
    return { authStore, web3Store }
  },
  data() {
    return {
      stats: [
        { title: 'Total Donations', value: '0', icon: 'fas fa-hand-holding-heart', subtitle: 'On Blockchain' },
        { title: 'Total Amount', value: '0 ETH', icon: 'fas fa-coins', subtitle: 'Transparent' },
        { title: 'Schools Supported', value: '0', icon: 'fas fa-school', subtitle: 'Verified' },
        { title: 'Students Impacted', value: '0', icon: 'fas fa-users', subtitle: 'Growing' }
      ],
      leaderboard: [],
      recentDonations: [],
      loading: false
    }
  },
  computed: {
    blockchainStats() {
      if (this.web3Store.contractStats) {
        return [
          { 
            title: 'Total Donations', 
            value: this.web3Store.contractStats.totalDonationsCount, 
            icon: 'fas fa-hand-holding-heart', 
            subtitle: 'On Blockchain' 
          },
          { 
            title: 'Total Amount', 
            value: `${this.web3Store.contractStats.totalDonationsAmount} ETH`, 
            icon: 'fas fa-coins', 
            subtitle: 'Transparent' 
          },
          { 
            title: 'Contract Balance', 
            value: `${this.web3Store.contractStats.contractBalance} ETH`, 
            icon: 'fas fa-wallet', 
            subtitle: 'Available' 
          },
          { 
            title: 'Allocated Funds', 
            value: `${this.web3Store.contractStats.totalAllocatedAmount} ETH`, 
            icon: 'fas fa-chart-line', 
            subtitle: 'To Schools' 
          }
        ]
      }
      return this.stats
    }
  },
  async mounted() {
    await this.loadData()
    await this.web3Store.checkConnection()
  },
  methods: {
    async loadData() {
      this.loading = true
      try {
        // Load backend data
        const [donationsResponse, leaderboardResponse] = await Promise.all([
          donationsAPI.getDonations({ limit: 10 }),
          donationsAPI.getDonations({ endpoint: 'leaderboard' })
        ])
        
        this.recentDonations = donationsResponse.data || []
        this.leaderboard = leaderboardResponse.data || []
        
        // Update stats from backend
        this.updateStats()
      } catch (error) {
        console.error('Error loading donation data:', error)
      } finally {
        this.loading = false
      }
    },
    
    updateStats() {
      // Update stats based on blockchain and backend data
      if (this.web3Store.contractStats) {
        this.stats[0].value = this.web3Store.contractStats.totalDonationsCount
        this.stats[1].value = `${this.web3Store.contractStats.totalDonationsAmount} ETH`
      }
    },
    
    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString()
    }
  }
}
</script>

<style scoped>
.donations-container {
  min-height: 100vh;
  background-color: #f8f9fa;
}

.bg-gradient-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.card {
  border-radius: 15px;
  transition: transform 0.2s ease;
}

.card:hover {
  transform: translateY(-2px);
}

.badge {
  font-size: 0.75rem;
}

.btn {
  border-radius: 10px;
  font-weight: 500;
}

.btn-lg {
  border-radius: 12px;
}
</style>
