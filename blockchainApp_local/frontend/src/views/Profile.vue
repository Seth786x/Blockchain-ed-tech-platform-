<template>
  <div class="profile">
    <div class="container">
      <div class="row">
        <div class="col-md-8">
          <div class="card">
            <div class="card-header">
              <h3>My Profile</h3>
            </div>
            <div class="card-body">
              <form @submit.prevent="updateProfile">
                <div class="row">
                  <div class="col-md-6">
                    <div class="mb-3">
                      <label class="form-label">Full Name</label>
                      <input 
                        type="text" 
                        class="form-control" 
                        v-model="profile.full_name" 
                        required
                      >
                    </div>
                  </div>
                  <div class="col-md-6">
                    <div class="mb-3">
                      <label class="form-label">Email</label>
                      <input 
                        type="email" 
                        class="form-control" 
                        v-model="profile.email" 
                        readonly
                      >
                    </div>
                  </div>
                </div>

                <div class="mb-3">
                  <label class="form-label">Role</label>
                  <input 
                    type="text" 
                    class="form-control" 
                    :value="profile.role" 
                    readonly
                  >
                </div>

                <div class="mb-3">
                  <label class="form-label">Bio</label>
                  <textarea 
                    class="form-control" 
                    v-model="profile.bio" 
                    rows="3"
                    placeholder="Tell us about yourself..."
                  ></textarea>
                </div>

                <button type="submit" class="btn btn-primary" :disabled="isUpdating">
                  <span v-if="isUpdating" class="spinner-border spinner-border-sm me-2"></span>
                  {{ isUpdating ? 'Updating...' : 'Update Profile' }}
                </button>
              </form>
            </div>
          </div>
        </div>

        <div class="col-md-4">
          <div class="card">
            <div class="card-header">
              <h5>Account Info</h5>
            </div>
            <div class="card-body">
              <div class="mb-3">
                <strong>Member Since:</strong>
                <br>{{ formatDate(profile.created_at) }}
              </div>
              <div class="mb-3">
                <strong>Last Login:</strong>
                <br>{{ formatDate(profile.last_login) }}
              </div>
              <div class="mb-3">
                <strong>Status:</strong>
                <br>
                <span class="badge bg-success" v-if="profile.is_active">Active</span>
                <span class="badge bg-danger" v-else>Inactive</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { authService } from '../services/auth'

export default {
  name: 'Profile',
  data() {
    return {
      profile: {
        full_name: '',
        email: '',
        role: '',
        bio: '',
        created_at: '',
        last_login: '',
        is_active: true
      },
      isUpdating: false
    }
  },
  async mounted() {
    await this.loadProfile()
  },
  methods: {
    async loadProfile() {
      try {
        const user = authService.getUser()
        if (user) {
          this.profile = {
            ...user,
            bio: user.bio || '',
            created_at: user.created_at || new Date().toISOString(),
            last_login: user.last_login || new Date().toISOString()
          }
        }
      } catch (error) {
        console.error('Error loading profile:', error)
      }
    },
    async updateProfile() {
      this.isUpdating = true
      try {
        // Mock update
        setTimeout(() => {
          alert('Profile updated successfully!')
          this.isUpdating = false
        }, 1000)
      } catch (error) {
        console.error('Error updating profile:', error)
        alert('Error updating profile. Please try again.')
        this.isUpdating = false
      }
    },
    formatDate(dateString) {
      if (!dateString) return 'Unknown'
      return new Date(dateString).toLocaleDateString()
    }
  }
}
</script>

<style scoped>
.profile {
  padding: 20px 0;
}

.card {
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
}
</style>
