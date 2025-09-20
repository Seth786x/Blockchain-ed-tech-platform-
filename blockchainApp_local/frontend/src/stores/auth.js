import { defineStore } from 'pinia'
import { authAPI, apiUtils } from '../services/api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: apiUtils.getUser(),
    token: apiUtils.getAuthToken(),
    isAuthenticated: apiUtils.isAuthenticated(),
    loading: false,
    error: null
  }),

  getters: {
    // Check if user is admin
    isAdmin: (state) => state.user?.role === 'admin',
    
    // Check if user is instructor
    isInstructor: (state) => state.user?.role === 'instructor',
    
    // Check if user is student
    isStudent: (state) => state.user?.role === 'student',
    
    // Check if user is donor
    isDonor: (state) => state.user?.role === 'donor',
    
    // Check if user is school
    isSchool: (state) => state.user?.role === 'school',
    
    // Get user's full name
    fullName: (state) => state.user?.full_name || 'User',
    
    // Get user's username
    username: (state) => state.user?.username || 'user'
  },

  actions: {
    // Login user
    async login(credentials) {
      this.loading = true
      this.error = null
      
      try {
        const response = await authAPI.login(credentials)
        const { access_token, user } = response.data
        
        // Store token and user data
        apiUtils.setAuthToken(access_token)
        apiUtils.setUser(user)
        
        // Update state
        this.token = access_token
        this.user = user
        this.isAuthenticated = true
        
        return { success: true, user }
      } catch (error) {
        this.error = error.response?.data?.detail || 'Login failed'
        throw error
      } finally {
        this.loading = false
      }
    },

    // Register user
    async register(userData) {
      this.loading = true
      this.error = null
      
      try {
        const response = await authAPI.register(userData)
        return { success: true, data: response.data }
      } catch (error) {
        this.error = error.response?.data?.detail || 'Registration failed'
        throw error
      } finally {
        this.loading = false
      }
    },

    // Logout user
    logout() {
      authAPI.logout()
      
      // Clear state
      this.user = null
      this.token = null
      this.isAuthenticated = false
      this.error = null
    },

    // Get current user from API
    async fetchCurrentUser() {
      try {
        const response = await authAPI.getCurrentUser()
        const user = response.data
        
        // Update user data
        apiUtils.setUser(user)
        this.user = user
        
        return user
      } catch (error) {
        console.error('Failed to fetch current user:', error)
        // If failed, logout user
        this.logout()
        throw error
      }
    },

    // Clear error
    clearError() {
      this.error = null
    },

    // Initialize auth state on app start
    async initAuth() {
      if (this.isAuthenticated && this.token) {
        try {
          await this.fetchCurrentUser()
        } catch (error) {
          // Token might be invalid, logout
          this.logout()
        }
      }
    }
  }
})
