<template>
  <div class="register-container">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-8 col-lg-6">
          <div class="card shadow-lg border-0">
            <div class="card-body p-5">
              <!-- Header -->
              <div class="text-center mb-4">
                <h2 class="fw-bold text-primary">
                  <i class="fas fa-user-plus me-2"></i>
                  Create Account
                </h2>
                <p class="text-muted">Join the EdTech Hardware Learning Platform</p>
              </div>

              <!-- Registration Form -->
              <form @submit.prevent="handleRegister" class="needs-validation" novalidate>
                <div class="row">
                  <!-- Full Name -->
                  <div class="col-md-6 mb-3">
                    <label for="fullName" class="form-label">Full Name</label>
                    <input
                      type="text"
                      class="form-control"
                      id="fullName"
                      v-model="form.full_name"
                      :class="{ 'is-invalid': errors.full_name }"
                      placeholder="Enter your full name"
                      required
                    />
                    <div class="invalid-feedback" v-if="errors.full_name">
                      {{ errors.full_name }}
                    </div>
                  </div>

                  <!-- Username -->
                  <div class="col-md-6 mb-3">
                    <label for="username" class="form-label">Username</label>
                    <input
                      type="text"
                      class="form-control"
                      id="username"
                      v-model="form.username"
                      :class="{ 'is-invalid': errors.username }"
                      placeholder="Choose a username"
                      required
                    />
                    <div class="invalid-feedback" v-if="errors.username">
                      {{ errors.username }}
                    </div>
                  </div>
                </div>

                <!-- Email -->
                <div class="mb-3">
                  <label for="email" class="form-label">Email Address</label>
                  <input
                    type="email"
                    class="form-control"
                    id="email"
                    v-model="form.email"
                    :class="{ 'is-invalid': errors.email }"
                    placeholder="Enter your email"
                    required
                  />
                  <div class="invalid-feedback" v-if="errors.email">
                    {{ errors.email }}
                  </div>
                </div>

                <!-- Role Selection -->
                <div class="mb-3">
                  <label for="role" class="form-label">Account Type</label>
                  <select
                    class="form-select"
                    id="role"
                    v-model="form.role"
                    :class="{ 'is-invalid': errors.role }"
                    required
                  >
                    <option value="">Select your role</option>
                    <option value="student">Student - Learn hardware</option>
                    <option value="instructor">Instructor - Create courses</option>
                    <option value="donor">Donor - Support education</option>
                    <option value="school">School - Request resources</option>
                  </select>
                  <div class="invalid-feedback" v-if="errors.role">
                    {{ errors.role }}
                  </div>
                </div>

                <!-- Wallet Address -->
                <div class="mb-3">
                  <label for="walletAddress" class="form-label">
                    Wallet Address (Optional)
                    <i class="fas fa-info-circle text-muted ms-1" 
                       title="Your Ethereum wallet address for blockchain transactions"></i>
                  </label>
                  <input
                    type="text"
                    class="form-control"
                    id="walletAddress"
                    v-model="form.wallet_address"
                    :class="{ 'is-invalid': errors.wallet_address }"
                    placeholder="0x..."
                  />
                  <div class="invalid-feedback" v-if="errors.wallet_address">
                    {{ errors.wallet_address }}
                  </div>
                  <small class="form-text text-muted">
                    You can add this later for blockchain features
                  </small>
                </div>

                <div class="row">
                  <!-- Password -->
                  <div class="col-md-6 mb-3">
                    <label for="password" class="form-label">Password</label>
                    <div class="input-group">
                      <input
                        :type="showPassword ? 'text' : 'password'"
                        class="form-control"
                        id="password"
                        v-model="form.password"
                        :class="{ 'is-invalid': errors.password }"
                        placeholder="Create a password"
                        required
                      />
                      <button
                        type="button"
                        class="btn btn-outline-secondary"
                        @click="showPassword = !showPassword"
                      >
                        <i :class="showPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
                      </button>
                    </div>
                    <div class="invalid-feedback" v-if="errors.password">
                      {{ errors.password }}
                    </div>
                  </div>

                  <!-- Confirm Password -->
                  <div class="col-md-6 mb-3">
                    <label for="confirmPassword" class="form-label">Confirm Password</label>
                    <div class="input-group">
                      <input
                        :type="showConfirmPassword ? 'text' : 'password'"
                        class="form-control"
                        id="confirmPassword"
                        v-model="confirmPassword"
                        :class="{ 'is-invalid': errors.confirmPassword }"
                        placeholder="Confirm your password"
                        required
                      />
                      <button
                        type="button"
                        class="btn btn-outline-secondary"
                        @click="showConfirmPassword = !showConfirmPassword"
                      >
                        <i :class="showConfirmPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
                      </button>
                    </div>
                    <div class="invalid-feedback" v-if="errors.confirmPassword">
                      {{ errors.confirmPassword }}
                    </div>
                  </div>
                </div>

                <!-- Password Strength -->
                <div class="mb-3" v-if="form.password">
                  <small class="form-text">
                    Password strength:
                    <span :class="passwordStrengthClass">{{ passwordStrength }}</span>
                  </small>
                  <div class="progress mt-1" style="height: 4px;">
                    <div 
                      class="progress-bar" 
                      :class="passwordStrengthClass"
                      :style="{ width: passwordStrengthPercentage + '%' }"
                    ></div>
                  </div>
                </div>

                <!-- Error Alert -->
                <div v-if="authStore.error" class="alert alert-danger alert-dismissible fade show" role="alert">
                  <i class="fas fa-exclamation-triangle me-2"></i>
                  {{ authStore.error }}
                  <button type="button" class="btn-close" @click="authStore.clearError()"></button>
                </div>

                <!-- Submit Button -->
                <div class="d-grid mb-3">
                  <button
                    type="submit"
                    class="btn btn-primary btn-lg"
                    :disabled="authStore.loading"
                  >
                    <span v-if="authStore.loading" class="spinner-border spinner-border-sm me-2"></span>
                    <i v-else class="fas fa-user-plus me-2"></i>
                    {{ authStore.loading ? 'Creating Account...' : 'Create Account' }}
                  </button>
                </div>

                <!-- Links -->
                <div class="text-center">
                  <p class="mb-0">
                    Already have an account?
                    <router-link to="/login" class="text-decoration-none">
                      Sign in here
                    </router-link>
                  </p>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

export default {
  name: 'Register',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()

    // Form data
    const form = reactive({
      full_name: '',
      username: '',
      email: '',
      role: '',
      wallet_address: '',
      password: ''
    })

    // Form state
    const confirmPassword = ref('')
    const showPassword = ref(false)
    const showConfirmPassword = ref(false)
    const errors = reactive({})

    // Password strength
    const passwordStrength = computed(() => {
      const password = form.password
      if (!password) return ''
      
      let score = 0
      if (password.length >= 8) score++
      if (/[a-z]/.test(password)) score++
      if (/[A-Z]/.test(password)) score++
      if (/[0-9]/.test(password)) score++
      if (/[^A-Za-z0-9]/.test(password)) score++

      if (score < 2) return 'Weak'
      if (score < 4) return 'Fair'
      if (score < 5) return 'Good'
      return 'Strong'
    })

    const passwordStrengthClass = computed(() => {
      const strength = passwordStrength.value
      switch (strength) {
        case 'Weak': return 'text-danger'
        case 'Fair': return 'text-warning'
        case 'Good': return 'text-info'
        case 'Strong': return 'text-success'
        default: return 'text-muted'
      }
    })

    const passwordStrengthPercentage = computed(() => {
      const password = form.password
      if (!password) return 0
      
      let score = 0
      if (password.length >= 8) score++
      if (/[a-z]/.test(password)) score++
      if (/[A-Z]/.test(password)) score++
      if (/[0-9]/.test(password)) score++
      if (/[^A-Za-z0-9]/.test(password)) score++

      return (score / 5) * 100
    })

    // Validate form
    const validateForm = () => {
      errors.full_name = ''
      errors.username = ''
      errors.email = ''
      errors.role = ''
      errors.password = ''
      errors.confirmPassword = ''
      errors.wallet_address = ''

      if (!form.full_name.trim()) {
        errors.full_name = 'Full name is required'
      }

      if (!form.username.trim()) {
        errors.username = 'Username is required'
      } else if (form.username.length < 3) {
        errors.username = 'Username must be at least 3 characters'
      }

      if (!form.email) {
        errors.email = 'Email is required'
      } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) {
        errors.email = 'Please enter a valid email address'
      }

      if (!form.role) {
        errors.role = 'Please select a role'
      }

      if (!form.password) {
        errors.password = 'Password is required'
      } else if (form.password.length < 6) {
        errors.password = 'Password must be at least 6 characters'
      }

      if (!confirmPassword.value) {
        errors.confirmPassword = 'Please confirm your password'
      } else if (form.password !== confirmPassword.value) {
        errors.confirmPassword = 'Passwords do not match'
      }

      if (form.wallet_address && !/^0x[a-fA-F0-9]{40}$/.test(form.wallet_address)) {
        errors.wallet_address = 'Please enter a valid Ethereum address'
      }

      return !Object.values(errors).some(error => error)
    }

    // Handle registration
    const handleRegister = async () => {
      if (!validateForm()) {
        return
      }

      try {
        await authStore.register(form)
        
        // Show success message and redirect to login
        alert('Account created successfully! Please sign in.')
        router.push('/login')
      } catch (error) {
        console.error('Registration error:', error)
        // Error is handled by the store
      }
    }

    return {
      form,
      confirmPassword,
      errors,
      showPassword,
      showConfirmPassword,
      authStore,
      passwordStrength,
      passwordStrengthClass,
      passwordStrengthPercentage,
      handleRegister
    }
  }
}
</script>

<style scoped>
.register-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  padding: 2rem 0;
}

.card {
  border-radius: 15px;
  backdrop-filter: blur(10px);
  background: rgba(255, 255, 255, 0.95);
}

.card-body {
  border-radius: 15px;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  border-radius: 10px;
  font-weight: 600;
  transition: all 0.3s ease;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
}

.form-control, .form-select {
  border: 1px solid #dee2e6;
  border-radius: 10px;
  transition: all 0.3s ease;
}

.form-control:focus, .form-select:focus {
  border-color: #667eea;
  box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25);
}

.input-group .form-control {
  border-radius: 10px 0 0 10px;
}

.input-group .btn-outline-secondary {
  border-radius: 0 10px 10px 0;
}

.alert {
  border-radius: 10px;
  border: none;
}

.progress {
  border-radius: 10px;
}

.progress-bar {
  border-radius: 10px;
}
</style>
