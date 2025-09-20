import axios from 'axios'

// Create axios instance
const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('auth_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor to handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid
      localStorage.removeItem('auth_token')
      localStorage.removeItem('user')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// Authentication API
export const authAPI = {
  // Register new user
  register: (userData) => api.post('/auth/register', userData),
  
  // Login user
  login: (credentials) => api.post('/auth/login', credentials),
  
  // Get current user
  getCurrentUser: () => api.get('/auth/me'),
  
  // Logout (client-side)
  logout: () => {
    localStorage.removeItem('auth_token')
    localStorage.removeItem('user')
  }
}

// Courses API
export const coursesAPI = {
  // Get all courses
  getCourses: (params = {}) => api.get('/courses', { params }),
  
  // Get course by ID
  getCourse: (id) => api.get(`/courses/${id}`),
  
  // Create course (instructors/admins)
  createCourse: (courseData) => api.post('/courses', courseData),
  
  // Update course
  updateCourse: (id, courseData) => api.put(`/courses/${id}`, courseData),
  
  // Delete course
  deleteCourse: (id) => api.delete(`/courses/${id}`),
  
  // Enroll in course
  enrollInCourse: (id) => api.post(`/courses/${id}/enroll`),
  
  // Get course progress
  getCourseProgress: (id) => api.get(`/courses/${id}/progress`),
  
  // Complete module
  completeModule: (courseId, moduleId) => 
    api.post(`/courses/${courseId}/modules/${moduleId}/complete`),
  
  // Get enrolled courses
  getEnrolledCourses: () => api.get('/courses/enrolled')
}

// Donations API
export const donationsAPI = {
  // Get donations
  getDonations: (params = {}) => api.get('/donations', { params }),
  
  // Get donation by ID
  getDonation: (id) => api.get(`/donations/${id}`),
  
  // Create donation
  createDonation: (donationData) => api.post('/donations', donationData),
  
  // Get donation statistics
  getStats: () => api.get('/donations/stats/total'),
  
  // Get monthly stats
  getMonthlyStats: () => api.get('/donations/stats/monthly'),
  
  // Get donor leaderboard
  getLeaderboard: () => api.get('/donations/leaderboard'),
  
  // Confirm donation (admin)
  confirmDonation: (id) => api.post(`/donations/${id}/confirm`),
  
  // Allocate donation (admin)
  allocateDonation: (id, schoolId) => 
    api.post(`/donations/${id}/allocate`, { school_id: schoolId }),
  
  // Get school donations
  getSchoolDonations: (schoolId) => api.get(`/donations/schools/${schoolId}`)
}

// Resources/Schools API
export const resourcesAPI = {
  // Get schools
  getSchools: (params = {}) => api.get('/resources/schools', { params }),
  
  // Get school by ID
  getSchool: (id) => api.get(`/resources/schools/${id}`),
  
  // Register school
  registerSchool: (schoolData) => api.post('/resources/schools', schoolData),
  
  // Verify school (admin)
  verifySchool: (id) => api.put(`/resources/schools/${id}/verify`),
  
  // Get resource requests
  getResourceRequests: (params = {}) => api.get('/resources/requests', { params }),
  
  // Get resource request by ID
  getResourceRequest: (id) => api.get(`/resources/requests/${id}`),
  
  // Create resource request
  createResourceRequest: (requestData) => api.post('/resources/requests', requestData),
  
  // Approve resource request (admin)
  approveRequest: (id) => api.put(`/resources/requests/${id}/approve`),
  
  // Allocate resources (admin)
  allocateResources: (id, amount) => 
    api.put(`/resources/requests/${id}/allocate`, { allocation_amount: amount }),
  
  // Get school statistics
  getSchoolStats: () => api.get('/resources/stats/schools'),
  
  // Get request statistics
  getRequestStats: () => api.get('/resources/stats/requests'),
  
  // Get school requests
  getSchoolRequests: (schoolId) => api.get(`/resources/schools/${schoolId}/requests`)
}

// Utility functions
export const apiUtils = {
  // Set auth token
  setAuthToken: (token) => {
    localStorage.setItem('auth_token', token)
  },
  
  // Get auth token
  getAuthToken: () => {
    return localStorage.getItem('auth_token')
  },
  
  // Check if user is authenticated
  isAuthenticated: () => {
    return !!localStorage.getItem('auth_token')
  },
  
  // Get user from localStorage
  getUser: () => {
    const user = localStorage.getItem('user')
    return user ? JSON.parse(user) : null
  },
  
  // Set user in localStorage
  setUser: (user) => {
    localStorage.setItem('user', JSON.stringify(user))
  }
}

export default api 