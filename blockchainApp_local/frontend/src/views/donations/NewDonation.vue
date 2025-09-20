<template>
  <div class="new-donation">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-8">
          <div class="card">
            <div class="card-header">
              <h3>Make a Donation</h3>
              <p class="mb-0 text-muted">Support computer hardware education with blockchain transparency</p>
            </div>
            <div class="card-body">
              <form @submit.prevent="submitDonation">
                <div class="mb-4">
                  <label class="form-label">Select School</label>
                  <select class="form-select" v-model="donation.school_id" required>
                    <option value="">Choose a school to support</option>
                    <option v-for="school in schools" :key="school._id" :value="school._id">
                      {{ school.name }} - {{ school.address }}
                    </option>
                  </select>
                </div>

                <div class="mb-4">
                  <label class="form-label">Donation Amount (ETH)</label>
                  <div class="input-group">
                    <input 
                      type="number" 
                      class="form-control" 
                      v-model="donation.amount" 
                      step="0.001"
                      min="0.001"
                      required
                      placeholder="0.000"
                    >
                    <span class="input-group-text">ETH</span>
                  </div>
                  <div class="form-text">
                    Approximately ${{ (donation.amount * ethToUsd).toFixed(2) }} USD
                  </div>
                </div>

                <div class="mb-4">
                  <label class="form-label">Your Information</label>
                  <div class="row">
                    <div class="col-md-6">
                      <input 
                        type="text" 
                        class="form-control mb-3" 
                        v-model="donation.donor_name" 
                        placeholder="Full Name"
                        required
                      >
                    </div>
                    <div class="col-md-6">
                      <input 
                        type="email" 
                        class="form-control mb-3" 
                        v-model="donation.donor_email" 
                        placeholder="Email Address"
                        required
                      >
                    </div>
                  </div>
                </div>

                <div class="mb-4">
                  <label class="form-label">Message (Optional)</label>
                  <textarea 
                    class="form-control" 
                    v-model="donation.message" 
                    rows="3"
                    placeholder="Leave a message for the school..."
                  ></textarea>
                </div>

                <div class="mb-4">
                  <div class="card bg-light">
                    <div class="card-body">
                      <h6><i class="fas fa-shield-alt me-2"></i>Blockchain Transparency</h6>
                      <p class="mb-0 small text-muted">
                        Your donation will be recorded on the Ethereum blockchain for complete transparency. 
                        You'll receive a transaction hash as proof of your contribution.
                      </p>
                    </div>
                  </div>
                </div>

                <div class="d-flex justify-content-between">
                  <button type="button" class="btn btn-secondary" @click="goBack">
                    Cancel
                  </button>
                  <button type="submit" class="btn btn-primary" :disabled="isSubmitting">
                    <span v-if="isSubmitting" class="spinner-border spinner-border-sm me-2"></span>
                    <i v-else class="fas fa-heart me-2"></i>
                    {{ isSubmitting ? 'Processing...' : 'Donate Now' }}
                  </button>
                </div>
              </form>
            </div>
          </div>

          <!-- Recent Donations -->
          <div class="card mt-4">
            <div class="card-header">
              <h5>Recent Donations</h5>
            </div>
            <div class="card-body">
              <div v-if="recentDonations.length === 0" class="text-center text-muted py-3">
                <i class="fas fa-heart fa-2x mb-2 opacity-25"></i>
                <p>No recent donations</p>
              </div>
              <div v-else>
                <div v-for="recent in recentDonations" :key="recent.id" class="d-flex justify-content-between align-items-center mb-2">
                  <div>
                    <strong>{{ recent.donor_name }}</strong> donated <span class="badge bg-success">{{ recent.amount }} ETH</span>
                    <br>
                    <small class="text-muted">to {{ recent.school_name }} • {{ recent.date }}</small>
                  </div>
                  <i class="fas fa-check-circle text-success"></i>
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
import { donationService } from '../../services/donations'
import { schoolService } from '../../services/schools'

export default {
  name: 'NewDonation',
  data() {
    return {
      donation: {
        school_id: '',
        amount: '',
        donor_name: '',
        donor_email: '',
        message: ''
      },
      schools: [],
      recentDonations: [],
      isSubmitting: false,
      ethToUsd: 2000 // Mock ETH to USD rate
    }
  },
  async mounted() {
    await this.loadSchools()
    await this.loadRecentDonations()
  },
  methods: {
    async loadSchools() {
      try {
        const response = await schoolService.getAllSchools()
        this.schools = response.data.filter(school => school.verification_status === 'verified')
      } catch (error) {
        console.error('Error loading schools:', error)
      }
    },
    async loadRecentDonations() {
      try {
        const response = await donationService.getAllDonations()
        this.recentDonations = response.data.slice(0, 5).map(d => ({
          ...d,
          date: new Date(d.created_at).toLocaleDateString()
        }))
      } catch (error) {
        console.error('Error loading recent donations:', error)
      }
    },
    async submitDonation() {
      this.isSubmitting = true
      try {
        const response = await donationService.createDonation(this.donation)
        console.log('Donation created:', response.data)
        
        // Show success message
        alert(`Thank you for your donation of ${this.donation.amount} ETH! Your transaction will be processed on the blockchain.`)
        
        // Redirect to donations page
        this.$router.push('/donations')
      } catch (error) {
        console.error('Error creating donation:', error)
        alert('Error processing donation. Please try again.')
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
.new-donation {
  padding: 20px 0;
}

.card {
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
}

.form-label {
  font-weight: 600;
  color: #333;
}

.form-control:focus,
.form-select:focus {
  border-color: #0d6efd;
  box-shadow: 0 0 0 0.2rem rgba(13, 110, 253, 0.25);
}

.btn-primary {
  background-color: #0d6efd;
  border-color: #0d6efd;
}

.btn-primary:hover {
  background-color: #0b5ed7;
  border-color: #0a58ca;
}

.spinner-border-sm {
  width: 1rem;
  height: 1rem;
}

.bg-light {
  background-color: #f8f9fa !important;
}
</style>
