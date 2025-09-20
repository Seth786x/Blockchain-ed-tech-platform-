<template>
  <div class="login-container">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-6 col-lg-4">
          <div class="card shadow-lg border-0">
            <div class="card-body p-5">
              <!-- Header -->
              <div class="text-center mb-4">
                <h2 class="fw-bold text-primary">
                  <i class="fas fa-microchip me-2"></i>
                  EdTech Hardware
                </h2>
                <p class="text-muted">Sign in to your account</p>
              </div>

              <!-- Login Form -->
              <form @submit.prevent="handleLogin" class="needs-validation" novalidate>
                <!-- Email Field -->
                <div class="mb-3">
                  <label for="email" class="form-label">Email Address</label>
                  <div class="input-group">
                    <span class="input-group-text">
                      <i class="fas fa-envelope"></i>
                    </span>
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
                </div>

                <!-- Password Field -->
                <div class="mb-4">
                  <label for="password" class="form-label">Password</label>
                  <div class="input-group">
                    <span class="input-group-text">
                      <i class="fas fa-lock"></i>
                    </span>
                    <input
                      :type="showPassword ? 'text' : 'password'"
                      class="form-control"
                      id="password"
                      v-model="form.password"
                      :class="{ 'is-invalid': errors.password }"
                      placeholder="Enter your password"
                      required
                    />
                    <button
                      type="button"
                      class="btn btn-outline-secondary"
                      @click="showPassword = !showPassword"
                    >
                      <i :class="showPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
                    </button>
                    <div class="invalid-feedback" v-if="errors.password">
                      {{ errors.password }}
                    </div>
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
                    <i v-else class="fas fa-sign-in-alt me-2"></i>
                    {{ authStore.loading ? 'Signing In...' : 'Sign In' }}
                  </button>
                </div>

                <!-- Demo Accounts -->
                <div class="mb-3">
                  <small class="text-muted">Demo Accounts:</small>
                  <div class="mt-2">
                    <button
                      type="button"
                      class="btn btn-sm btn-outline-secondary me-2 mb-1"
                      @click="fillDemoAccount('student')"
                    >
                      Student
                    </button>
                    <button
                      type="button"
                      class="btn btn-sm btn-outline-secondary me-2 mb-1"
                      @click="fillDemoAccount('instructor')"
                    >
                      Instructor
                    </button>
                    <button
                      type="button"
                      class="btn btn-sm btn-outline-secondary me-2 mb-1"
                      @click="fillDemoAccount('admin')"
                    >
                      Admin
                    </button>
                    <button
                      type="button"
                      class="btn btn-sm btn-outline-secondary me-2 mb-1"
                      @click="fillDemoAccount('donor')"
                    >
                      Donor
                    </button>
                  </div>
                </div>

                <!-- Links -->
                <div class="text-center">
                  <p class="mb-0">
                    Don't have an account?
                    <router-link to="/register" class="text-decoration-none">
                      Sign up here
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
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

export default {
  name: 'Login',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()

    // Form data
    const form = reactive({
      email: '',
      password: ''
    })

    // Form state
    const showPassword = ref(false)
    const errors = reactive({})

    // Demo accounts
    const demoAccounts = {
      student: { email: 'student@edtech.com', password: 'student123' },
      instructor: { email: 'instructor@edtech.com', password: 'instructor123' },
      admin: { email: 'admin@edtech.com', password: 'admin123' },
      donor: { email: 'donor@edtech.com', password: 'donor123' }
    }

    // Fill demo account
    const fillDemoAccount = (role) => {
      const account = demoAccounts[role]
      form.email = account.email
      form.password = account.password
    }

    // Validate form
    const validateForm = () => {
      errors.email = ''
      errors.password = ''

      if (!form.email) {
        errors.email = 'Email is required'
      } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) {
        errors.email = 'Please enter a valid email address'
      }

      if (!form.password) {
        errors.password = 'Password is required'
      } else if (form.password.length < 6) {
        errors.password = 'Password must be at least 6 characters'
      }

      return !errors.email && !errors.password
    }

    // Handle login
    const handleLogin = async () => {
      if (!validateForm()) {
        return
      }

      try {
        await authStore.login({
          email: form.email,
          password: form.password
        })

        // Redirect based on user role
        const user = authStore.user
        if (user) {
          switch (user.role) {
            case 'admin':
              router.push('/admin/dashboard')
              break
            case 'instructor':
              router.push('/instructor/dashboard')
              break
            case 'student':
              router.push('/dashboard')
              break
            case 'donor':
              router.push('/donor/dashboard')
              break
            case 'school':
              router.push('/school/dashboard')
              break
            default:
              router.push('/dashboard')
          }
        }
      } catch (error) {
        console.error('Login error:', error)
        // Error is handled by the store
      }
    }

    return {
      form,
      errors,
      showPassword,
      authStore,
      fillDemoAccount,
      handleLogin
    }
  }
}
</script>

<style scoped>
.login-container {
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

.input-group-text {
  background: #f8f9fa;
  border: 1px solid #dee2e6;
  color: #6c757d;
}

.form-control {
  border: 1px solid #dee2e6;
  border-radius: 0 10px 10px 0;
  transition: all 0.3s ease;
}

.form-control:focus {
  border-color: #667eea;
  box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25);
}

.input-group .form-control {
  border-radius: 0 10px 10px 0;
}

.input-group .input-group-text {
  border-radius: 10px 0 0 10px;
}

.btn-outline-secondary {
  border-radius: 0 10px 10px 0;
}

.alert {
  border-radius: 10px;
  border: none;
}

.btn-sm {
  border-radius: 8px;
  font-size: 0.8rem;
}
</style>
