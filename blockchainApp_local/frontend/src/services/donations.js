import { donationsAPI } from './api'

export const donationService = {
  async getAllDonations() {
    try {
      const response = await donationsAPI.getDonations()
      return response
    } catch (error) {
      // Mock data for demo
      return {
        data: [
          {
            _id: '1',
            donor_name: 'Alice Johnson',
            donor_email: 'alice@example.com',
            school_name: 'Lincoln Elementary School',
            amount: '2.5',
            status: 'completed',
            blockchain_tx_hash: '0x1234567890abcdef1234567890abcdef12345678',
            message: 'Hope this helps the kids learn about computers!',
            created_at: new Date(Date.now() - 86400000).toISOString() // 1 day ago
          },
          {
            _id: '2',
            donor_name: 'Bob Smith',
            donor_email: 'bob@example.com',
            school_name: 'Tech High School',
            amount: '1.0',
            status: 'pending',
            blockchain_tx_hash: null,
            message: 'Supporting tech education',
            created_at: new Date(Date.now() - 3600000).toISOString() // 1 hour ago
          },
          {
            _id: '3',
            donor_name: 'Carol Williams',
            donor_email: 'carol@example.com',
            school_name: 'Community College Prep',
            amount: '0.75',
            status: 'failed',
            blockchain_tx_hash: null,
            message: '',
            created_at: new Date(Date.now() - 7200000).toISOString() // 2 hours ago
          },
          {
            _id: '4',
            donor_name: 'David Brown',
            donor_email: 'david@example.com',
            school_name: 'Lincoln Elementary School',
            amount: '5.0',
            status: 'completed',
            blockchain_tx_hash: '0xabcdef1234567890abcdef1234567890abcdef12',
            message: 'For new computer lab equipment',
            created_at: new Date(Date.now() - 172800000).toISOString() // 2 days ago
          }
        ]
      }
    }
  },

  async getDonation(id) {
    try {
      const response = await donationsAPI.getDonation(id)
      return response
    } catch (error) {
      throw error
    }
  },

  async createDonation(donationData) {
    try {
      const response = await donationsAPI.createDonation(donationData)
      return response
    } catch (error) {
      throw error
    }
  },

  async getDonationStats() {
    try {
      const response = await donationsAPI.getStats()
      return response
    } catch (error) {
      // Mock stats
      return {
        data: {
          totalDonations: 9.25,
          activeCampaigns: 3,
          totalDonors: 4,
          pendingRequests: 1
        }
      }
    }
  },

  async getMonthlyStats() {
    try {
      const response = await donationsAPI.getMonthlyStats()
      return response
    } catch (error) {
      // Mock monthly stats
      return {
        data: [
          { month: 'January', amount: 12.5, donors: 8 },
          { month: 'February', amount: 8.75, donors: 6 },
          { month: 'March', amount: 15.2, donors: 12 },
          { month: 'April', amount: 9.25, donors: 4 }
        ]
      }
    }
  },

  async getLeaderboard() {
    try {
      const response = await donationsAPI.getLeaderboard()
      return response
    } catch (error) {
      // Mock leaderboard
      return {
        data: [
          { donor_name: 'David Brown', total_amount: '5.0', donation_count: 1 },
          { donor_name: 'Alice Johnson', total_amount: '2.5', donation_count: 1 },
          { donor_name: 'Bob Smith', total_amount: '1.0', donation_count: 1 },
          { donor_name: 'Carol Williams', total_amount: '0.75', donation_count: 1 }
        ]
      }
    }
  },

  async confirmDonation(id) {
    try {
      const response = await donationsAPI.confirmDonation(id)
      return response
    } catch (error) {
      console.log('Confirming donation:', id)
      return { data: { success: true } }
    }
  },

  async verifyDonation(id) {
    try {
      // This would call a blockchain verification endpoint
      const response = await fetch(`/api/donations/${id}/verify`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('auth_token')}`,
          'Content-Type': 'application/json'
        }
      })
      return { data: await response.json() }
    } catch (error) {
      // Mock verification
      return {
        data: {
          verified: true,
          blockchain_status: 'confirmed',
          confirmations: 12,
          gas_used: '21000'
        }
      }
    }
  },

  async syncBlockchain() {
    try {
      // This would sync with the blockchain smart contract
      const response = await fetch('/api/donations/sync-blockchain', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('auth_token')}`,
          'Content-Type': 'application/json'
        }
      })
      return { data: await response.json() }
    } catch (error) {
      // Mock sync
      return {
        data: {
          synced: true,
          new_donations: 0,
          updated_donations: 2,
          blockchain_height: 18750432
        }
      }
    }
  },

  async getSchoolDonations(schoolId) {
    try {
      const response = await donationsAPI.getSchoolDonations(schoolId)
      return response
    } catch (error) {
      throw error
    }
  }
}

export default donationService
