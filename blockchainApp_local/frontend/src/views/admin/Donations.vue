<template>
  <div class="admin-donations">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2>Donation Management</h2>
      <div>
        <button class="btn btn-success me-2" @click="syncBlockchain">
          <i class="fas fa-sync me-2"></i>Sync Blockchain
        </button>
        <button class="btn btn-primary" @click="exportReport">
          <i class="fas fa-download me-2"></i>Export Report
        </button>
      </div>
    </div>

    <!-- Stats Cards -->
    <div class="row mb-4">
      <div class="col-md-3">
        <div class="card bg-primary text-white">
          <div class="card-body">
            <h5>Total Donations</h5>
            <h3>{{ stats.totalDonations.toFixed(4) }} ETH</h3>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card bg-success text-white">
          <div class="card-body">
            <h5>Active Campaigns</h5>
            <h3>{{ stats.activeCampaigns }}</h3>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card bg-info text-white">
          <div class="card-body">
            <h5>Total Donors</h5>
            <h3>{{ stats.totalDonors }}</h3>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card bg-warning text-white">
          <div class="card-body">
            <h5>Pending Requests</h5>
            <h3>{{ stats.pendingRequests }}</h3>
          </div>
        </div>
      </div>
    </div>

    <!-- Donations Table -->
    <div class="card">
      <div class="card-header d-flex justify-content-between align-items-center">
        <h5 class="mb-0">All Donations</h5>
        <div class="d-flex gap-2">
          <select class="form-select form-select-sm" v-model="filterStatus" style="width: auto;">
            <option value="">All Status</option>
            <option value="completed">Completed</option>
            <option value="pending">Pending</option>
            <option value="failed">Failed</option>
          </select>
          <input type="text" class="form-control form-control-sm" placeholder="Search..." v-model="searchTerm" style="width: 200px;">
        </div>
      </div>
      <div class="card-body">
        <div class="table-responsive">
          <table class="table table-striped">
            <thead>
              <tr>
                <th>Donor</th>
                <th>School</th>
                <th>Amount (ETH)</th>
                <th>Blockchain TX</th>
                <th>Status</th>
                <th>Date</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="donation in filteredDonations" :key="donation._id">
                <td>
                  <div>{{ donation.donor_name }}</div>
                  <small class="text-muted">{{ donation.donor_email }}</small>
                </td>
                <td>{{ donation.school_name }}</td>
                <td>
                  <strong>{{ donation.amount }}</strong>
                  <div class="text-muted small">${{ (donation.amount * ethToUsd).toFixed(2) }}</div>
                </td>
                <td>
                  <span v-if="donation.blockchain_tx_hash" class="font-monospace">
                    {{ donation.blockchain_tx_hash.substring(0, 10) }}...
                  </span>
                  <span v-else class="text-muted">-</span>
                </td>
                <td>
                  <span class="badge" :class="getStatusBadgeClass(donation.status)">
                    {{ donation.status }}
                  </span>
                </td>
                <td>{{ formatDate(donation.created_at) }}</td>
                <td>
                  <button class="btn btn-sm btn-outline-primary me-2" @click="viewDetails(donation)">
                    <i class="fas fa-eye"></i>
                  </button>
                  <button class="btn btn-sm btn-outline-info" @click="verifyOnBlockchain(donation)">
                    <i class="fas fa-chain"></i>
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Donation Details Modal -->
    <div class="modal fade" :class="{ show: showDetailsModal }" style="display: block;" v-if="showDetailsModal">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Donation Details</h5>
            <button type="button" class="btn-close" @click="closeDetailsModal"></button>
          </div>
          <div class="modal-body" v-if="selectedDonation">
            <div class="row">
              <div class="col-md-6">
                <h6>Donor Information</h6>
                <p><strong>Name:</strong> {{ selectedDonation.donor_name }}</p>
                <p><strong>Email:</strong> {{ selectedDonation.donor_email }}</p>
                <p><strong>Message:</strong> {{ selectedDonation.message || 'No message' }}</p>
              </div>
              <div class="col-md-6">
                <h6>Transaction Details</h6>
                <p><strong>Amount:</strong> {{ selectedDonation.amount }} ETH</p>
                <p><strong>Status:</strong> {{ selectedDonation.status }}</p>
                <p><strong>Date:</strong> {{ formatDate(selectedDonation.created_at) }}</p>
                <p><strong>Blockchain TX:</strong> 
                  <span v-if="selectedDonation.blockchain_tx_hash" class="font-monospace">
                    {{ selectedDonation.blockchain_tx_hash }}
                  </span>
                  <span v-else>Not available</span>
                </p>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closeDetailsModal">Close</button>
          </div>
        </div>
      </div>
    </div>
    <div class="modal-backdrop fade show" v-if="showDetailsModal"></div>
  </div>
</template>

<script>
import { donationService } from '../../services/donations'

export default {
  name: 'AdminDonations',
  data() {
    return {
      donations: [],
      stats: {
        totalDonations: 0,
        activeCampaigns: 0,
        totalDonors: 0,
        pendingRequests: 0
      },
      showDetailsModal: false,
      selectedDonation: null,
      filterStatus: '',
      searchTerm: '',
      ethToUsd: 2000 // Mock ETH to USD rate
    }
  },
  computed: {
    filteredDonations() {
      let filtered = this.donations
      
      if (this.filterStatus) {
        filtered = filtered.filter(d => d.status === this.filterStatus)
      }
      
      if (this.searchTerm) {
        const term = this.searchTerm.toLowerCase()
        filtered = filtered.filter(d => 
          d.donor_name.toLowerCase().includes(term) ||
          d.donor_email.toLowerCase().includes(term) ||
          d.school_name.toLowerCase().includes(term)
        )
      }
      
      return filtered
    }
  },
  async mounted() {
    await this.loadDonations()
    await this.loadStats()
  },
  methods: {
    async loadDonations() {
      try {
        const response = await donationService.getAllDonations()
        this.donations = response.data
      } catch (error) {
        console.error('Error loading donations:', error)
      }
    },
    async loadStats() {
      try {
        const response = await donationService.getDonationStats()
        this.stats = response.data
      } catch (error) {
        console.error('Error loading stats:', error)
        // Calculate basic stats from donations if API fails
        this.calculateStatsFromDonations()
      }
    },
    calculateStatsFromDonations() {
      this.stats.totalDonations = this.donations.reduce((sum, d) => sum + parseFloat(d.amount), 0)
      this.stats.totalDonors = new Set(this.donations.map(d => d.donor_email)).size
      this.stats.pendingRequests = this.donations.filter(d => d.status === 'pending').length
    },
    getStatusBadgeClass(status) {
      const classes = {
        completed: 'bg-success',
        pending: 'bg-warning',
        failed: 'bg-danger'
      }
      return classes[status] || 'bg-secondary'
    },
    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString()
    },
    viewDetails(donation) {
      this.selectedDonation = donation
      this.showDetailsModal = true
    },
    closeDetailsModal() {
      this.showDetailsModal = false
      this.selectedDonation = null
    },
    async verifyOnBlockchain(donation) {
      try {
        const response = await donationService.verifyDonation(donation._id)
        console.log('Blockchain verification:', response.data)
        alert('Blockchain verification completed. Check console for details.')
      } catch (error) {
        console.error('Error verifying on blockchain:', error)
        alert('Error verifying donation on blockchain.')
      }
    },
    async syncBlockchain() {
      try {
        const response = await donationService.syncBlockchain()
        console.log('Blockchain sync:', response.data)
        await this.loadDonations()
        await this.loadStats()
        alert('Blockchain sync completed successfully!')
      } catch (error) {
        console.error('Error syncing blockchain:', error)
        alert('Error syncing with blockchain.')
      }
    },
    exportReport() {
      const csv = this.generateCSV()
      const blob = new Blob([csv], { type: 'text/csv' })
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `donations_report_${new Date().toISOString().split('T')[0]}.csv`
      a.click()
      window.URL.revokeObjectURL(url)
    },
    generateCSV() {
      const headers = ['Donor Name', 'Donor Email', 'School', 'Amount (ETH)', 'Status', 'Date', 'Blockchain TX']
      const rows = this.donations.map(d => [
        d.donor_name,
        d.donor_email,
        d.school_name,
        d.amount,
        d.status,
        this.formatDate(d.created_at),
        d.blockchain_tx_hash || ''
      ])
      
      return [headers, ...rows].map(row => row.join(',')).join('\n')
    }
  }
}
</script>

<style scoped>
.admin-donations {
  padding: 20px;
}

.modal {
  background-color: rgba(0, 0, 0, 0.5);
}

.table th {
  font-weight: 600;
}

.badge {
  font-size: 0.75rem;
}

.card {
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
}

.font-monospace {
  font-family: 'Courier New', monospace;
  font-size: 0.875rem;
}
</style>
