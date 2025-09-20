<template>
  <div id="app">
    <!-- Decorative doodle elements -->
    <div class="doodle-corner top-right floating-doodle"></div>
    <div class="doodle-corner bottom-left floating-doodle"></div>
    
    <!-- Navigation -->
    <nav v-if="authStore.isAuthenticated" class="navbar navbar-expand-lg">
      <div class="container">
        <router-link class="navbar-brand fw-bold" to="/">
          <i class="fas fa-microchip me-2"></i>
          EdTech Hardware
        </router-link>

        <button 
          class="navbar-toggler" 
          type="button" 
          data-bs-toggle="collapse" 
          data-bs-target="#navbarNav"
        >
          <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav me-auto">
            <li class="nav-item">
              <router-link class="nav-link" to="/dashboard">
                <i class="fas fa-tachometer-alt me-1"></i>Dashboard
              </router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/courses">
                <i class="fas fa-graduation-cap me-1"></i>Courses
              </router-link>
            </li>
            
            <!-- Admin Menu -->
            <li v-if="authStore.isAdmin" class="nav-item dropdown">
              <a 
                class="nav-link dropdown-toggle" 
                href="#" 
                role="button" 
                data-bs-toggle="dropdown"
              >
                <i class="fas fa-cogs me-1"></i>Admin
              </a>
              <ul class="dropdown-menu">
                <li>
                  <router-link class="dropdown-item" to="/admin/courses">
                    <i class="fas fa-book me-2"></i>Manage Courses
                  </router-link>
                </li>
                <li>
                  <router-link class="dropdown-item" to="/admin/users">
                    <i class="fas fa-users me-2"></i>Manage Users
                  </router-link>
                </li>
                <li>
                  <router-link class="dropdown-item" to="/admin/schools">
                    <i class="fas fa-school me-2"></i>Manage Schools
                  </router-link>
                </li>
                <li>
                  <router-link class="dropdown-item" to="/admin/donations">
                    <i class="fas fa-donate me-2"></i>Manage Donations
                  </router-link>
                </li>
              </ul>
            </li>
            
            <!-- Instructor Menu -->
            <li v-if="authStore.isInstructor" class="nav-item">
              <router-link class="nav-link" to="/instructor/dashboard">
                <i class="fas fa-chalkboard-teacher me-1"></i>Teaching
              </router-link>
            </li>
            
            <li class="nav-item">
              <router-link class="nav-link" to="/donations">
                <i class="fas fa-hand-holding-heart me-1"></i>Donations
              </router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/schools">
                <i class="fas fa-school me-1"></i>Schools
              </router-link>
            </li>
          </ul>

          <!-- User Menu -->
          <ul class="navbar-nav">
            <li class="nav-item dropdown">
              <a 
                class="nav-link dropdown-toggle d-flex align-items-center" 
                href="#" 
                role="button" 
                data-bs-toggle="dropdown"
              >
                <i class="fas fa-user-circle me-2"></i>
                {{ authStore.fullName }}
                <span class="badge bg-light text-dark ms-2">{{ authStore.user?.role }}</span>
              </a>
              <ul class="dropdown-menu dropdown-menu-end">
                <li>
                  <router-link class="dropdown-item" to="/profile">
                    <i class="fas fa-user me-2"></i>Profile
                  </router-link>
                </li>
                <li>
                  <router-link class="dropdown-item" to="/settings">
                    <i class="fas fa-cog me-2"></i>Settings
                  </router-link>
                </li>
                <li><hr class="dropdown-divider"></li>
                <li>
                  <a class="dropdown-item text-danger" href="#" @click.prevent="logout">
                    <i class="fas fa-sign-out-alt me-2"></i>Logout
                  </a>
                </li>
              </ul>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <main>
      <router-view />
    </main>

    <!-- Footer -->
    <footer v-if="authStore.isAuthenticated" class="bg-dark text-white py-4 mt-5">
      <div class="container">
        <div class="row">
          <div class="col-md-6">
            <h5>
              <i class="fas fa-microchip me-2"></i>
              EdTech Hardware Learning Platform
            </h5>
            <p class="text-muted">
              Empowering education through blockchain technology and transparent resource allocation.
            </p>
          </div>
          <div class="col-md-3">
            <h6>Quick Links</h6>
            <ul class="list-unstyled">
              <li><router-link to="/courses" class="text-muted text-decoration-none">Courses</router-link></li>
              <li><router-link to="/donations" class="text-muted text-decoration-none">Donations</router-link></li>
              <li><router-link to="/schools" class="text-muted text-decoration-none">Schools</router-link></li>
            </ul>
          </div>
          <div class="col-md-3">
            <h6>Support</h6>
            <ul class="list-unstyled">
              <li><a href="#" class="text-muted text-decoration-none">Help Center</a></li>
              <li><a href="#" class="text-muted text-decoration-none">Contact Us</a></li>
              <li><a href="#" class="text-muted text-decoration-none">Privacy Policy</a></li>
            </ul>
          </div>
        </div>
        <hr class="my-4">
        <div class="row align-items-center">
          <div class="col-md-6">
            <p class="mb-0 text-muted">
              © 2024 EdTech Hardware. All rights reserved.
            </p>
          </div>
          <div class="col-md-6 text-end">
            <div class="d-flex gap-3 justify-content-end">
              <a href="#" class="text-muted">
                <i class="fab fa-twitter"></i>
              </a>
              <a href="#" class="text-muted">
                <i class="fab fa-linkedin"></i>
              </a>
              <a href="#" class="text-muted">
                <i class="fab fa-github"></i>
              </a>
            </div>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>

<script>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from './stores/auth'

export default {
  name: 'App',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()

    const logout = () => {
      authStore.logout()
      router.push('/login')
    }

    onMounted(async () => {
      // Initialize authentication state
      await authStore.initAuth()
    })

    return {
      authStore,
      logout
    }
  }
}
</script>

<style>
/* Global Styles */
* {
  box-sizing: border-box;
}

body {
  margin: 0;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  line-height: 1.6;
  color: #333;
}

#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

main {
  flex: 1;
}

/* Bootstrap Overrides */
.navbar {
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.navbar-brand {
  font-size: 1.5rem;
}

.nav-link {
  font-weight: 500;
  transition: color 0.2s ease;
}

.nav-link:hover {
  color: rgba(255, 255, 255, 0.8) !important;
}

.dropdown-menu {
  border: none;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  border-radius: 10px;
}

.dropdown-item {
  padding: 0.75rem 1rem;
  transition: background-color 0.2s ease;
}

.dropdown-item:hover {
  background-color: #f8f9fa;
}

/* Custom Scrollbar */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
}

::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}

/* Utility Classes */
.text-primary {
  color: #667eea !important;
}

.bg-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
}

.btn-primary:hover {
  background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%);
  transform: translateY(-1px);
}

/* Animation Classes */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

.slide-enter-active, .slide-leave-active {
  transition: transform 0.3s ease;
}

.slide-enter-from {
  transform: translateX(-100%);
}

.slide-leave-to {
  transform: translateX(100%);
}

/* Responsive Design */
@media (max-width: 768px) {
  .navbar-brand {
    font-size: 1.25rem;
  }
  
  .container {
    padding-left: 15px;
    padding-right: 15px;
  }
}

/* Loading States */
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.9);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

/* Card Enhancements */
.card {
  border: none;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.2s ease;
}

.card:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}

/* Button Enhancements */
.btn {
  border-radius: 8px;
  font-weight: 500;
  transition: all 0.2s ease;
}

.btn:hover {
  transform: translateY(-1px);
}

/* Form Enhancements */
.form-control, .form-select {
  border-radius: 8px;
  border: 1px solid #dee2e6;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.form-control:focus, .form-select:focus {
  border-color: #667eea;
  box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25);
}

/* Alert Enhancements */
.alert {
  border: none;
  border-radius: 10px;
}

/* Badge Enhancements */
.badge {
  font-weight: 500;
  border-radius: 6px;
}
</style>