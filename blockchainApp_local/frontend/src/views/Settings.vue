<template>
  <div class="settings">
    <div class="container">
      <div class="row">
        <div class="col-md-8">
          <div class="card">
            <div class="card-header">
              <h3>Settings</h3>
            </div>
            <div class="card-body">
              <div class="mb-4">
                <h5>Notifications</h5>
                <div class="form-check">
                  <input 
                    class="form-check-input" 
                    type="checkbox" 
                    v-model="settings.emailNotifications"
                    id="emailNotifications"
                  >
                  <label class="form-check-label" for="emailNotifications">
                    Email notifications
                  </label>
                </div>
                <div class="form-check">
                  <input 
                    class="form-check-input" 
                    type="checkbox" 
                    v-model="settings.courseUpdates"
                    id="courseUpdates"
                  >
                  <label class="form-check-label" for="courseUpdates">
                    Course updates
                  </label>
                </div>
              </div>

              <div class="mb-4">
                <h5>Privacy</h5>
                <div class="form-check">
                  <input 
                    class="form-check-input" 
                    type="checkbox" 
                    v-model="settings.publicProfile"
                    id="publicProfile"
                  >
                  <label class="form-check-label" for="publicProfile">
                    Make profile public
                  </label>
                </div>
              </div>

              <div class="mb-4">
                <h5>Security</h5>
                <button class="btn btn-outline-primary mb-2" @click="changePassword">
                  Change Password
                </button>
                <br>
                <button class="btn btn-outline-warning" @click="enableTwoFactor">
                  Enable Two-Factor Authentication
                </button>
              </div>

              <button class="btn btn-primary" @click="saveSettings" :disabled="isSaving">
                <span v-if="isSaving" class="spinner-border spinner-border-sm me-2"></span>
                {{ isSaving ? 'Saving...' : 'Save Settings' }}
              </button>
            </div>
          </div>
        </div>

        <div class="col-md-4">
          <div class="card">
            <div class="card-header">
              <h5>Danger Zone</h5>
            </div>
            <div class="card-body">
              <p class="text-muted">Permanently delete your account and all data.</p>
              <button class="btn btn-danger" @click="deleteAccount">
                Delete Account
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Settings',
  data() {
    return {
      settings: {
        emailNotifications: true,
        courseUpdates: true,
        publicProfile: false
      },
      isSaving: false
    }
  },
  methods: {
    async saveSettings() {
      this.isSaving = true
      try {
        // Mock save
        setTimeout(() => {
          alert('Settings saved successfully!')
          this.isSaving = false
        }, 1000)
      } catch (error) {
        console.error('Error saving settings:', error)
        alert('Error saving settings. Please try again.')
        this.isSaving = false
      }
    },
    changePassword() {
      alert('Change password functionality coming soon!')
    },
    enableTwoFactor() {
      alert('Two-factor authentication setup coming soon!')
    },
    deleteAccount() {
      if (confirm('Are you sure you want to delete your account? This action cannot be undone.')) {
        alert('Account deletion functionality coming soon!')
      }
    }
  }
}
</script>

<style scoped>
.settings {
  padding: 20px 0;
}

.card {
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
}
</style>
