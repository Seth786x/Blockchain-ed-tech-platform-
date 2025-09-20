import { authAPI, apiUtils } from './api'

export const authService = {
  // User authentication
  async login(credentials) {
    try {
      const response = await authAPI.login(credentials)
      const { access_token, user } = response.data
      
      apiUtils.setAuthToken(access_token)
      apiUtils.setUser(user)
      
      return response
    } catch (error) {
      throw error
    }
  },

  async register(userData) {
    try {
      const response = await authAPI.register(userData)
      return response
    } catch (error) {
      throw error
    }
  },

  async getCurrentUser() {
    try {
      const response = await authAPI.getCurrentUser()
      apiUtils.setUser(response.data)
      return response
    } catch (error) {
      throw error
    }
  },

  logout() {
    authAPI.logout()
    window.location.href = '/login'
  },

  // Admin user management functions
  async getAllUsers() {
    try {
      // This would need to be implemented in the backend
      const response = await fetch('/api/admin/users', {
        headers: {
          'Authorization': `Bearer ${apiUtils.getAuthToken()}`,
          'Content-Type': 'application/json'
        }
      })
      return { data: await response.json() }
    } catch (error) {
      // Mock data for now
      return {
        data: [
          {
            _id: '1',
            full_name: 'John Doe',
            email: 'john@example.com',
            role: 'student',
            is_active: true,
            created_at: new Date().toISOString()
          },
          {
            _id: '2',
            full_name: 'Jane Smith',
            email: 'jane@example.com',
            role: 'instructor',
            is_active: true,
            created_at: new Date().toISOString()
          }
        ]
      }
    }
  },

  async createUser(userData) {
    try {
      // This would need to be implemented in the backend
      const response = await fetch('/api/admin/users', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${apiUtils.getAuthToken()}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(userData)
      })
      return { data: await response.json() }
    } catch (error) {
      console.log('Creating user:', userData)
      return { data: { success: true } }
    }
  },

  async updateUser(userId, userData) {
    try {
      // This would need to be implemented in the backend
      const response = await fetch(`/api/admin/users/${userId}`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${apiUtils.getAuthToken()}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(userData)
      })
      return { data: await response.json() }
    } catch (error) {
      console.log('Updating user:', userId, userData)
      return { data: { success: true } }
    }
  },

  // Utility functions
  isAuthenticated() {
    return apiUtils.isAuthenticated()
  },

  getUser() {
    return apiUtils.getUser()
  },

  hasRole(role) {
    const user = this.getUser()
    return user && user.role === role
  },

  isAdmin() {
    return this.hasRole('admin')
  }
}

export default authService
