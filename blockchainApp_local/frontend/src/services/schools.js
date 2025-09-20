import { resourcesAPI } from './api'

export const schoolService = {
  async getAllSchools() {
    try {
      const response = await resourcesAPI.getSchools()
      return response
    } catch (error) {
      // Mock data for demo
      return {
        data: [
          {
            _id: '1',
            name: 'Lincoln Elementary School',
            address: '123 Main St, Springfield, IL 62701',
            contact_email: 'contact@lincoln.edu',
            contact_phone: '(555) 123-4567',
            website: 'https://lincoln.edu',
            description: 'A public elementary school serving grades K-5',
            verification_status: 'verified',
            is_active: true,
            created_at: new Date().toISOString()
          },
          {
            _id: '2',
            name: 'Tech High School',
            address: '456 Oak Ave, Springfield, IL 62702',
            contact_email: 'admin@techigh.edu',
            contact_phone: '(555) 234-5678',
            website: 'https://techigh.edu',
            description: 'A technology-focused high school',
            verification_status: 'pending',
            is_active: true,
            created_at: new Date().toISOString()
          },
          {
            _id: '3',
            name: 'Community College Prep',
            address: '789 Pine St, Springfield, IL 62703',
            contact_email: 'info@ccprep.edu',
            contact_phone: '(555) 345-6789',
            description: 'Preparing students for community college',
            verification_status: 'rejected',
            is_active: false,
            created_at: new Date().toISOString()
          }
        ]
      }
    }
  },

  async getSchool(id) {
    try {
      const response = await resourcesAPI.getSchool(id)
      return response
    } catch (error) {
      throw error
    }
  },

  async createSchool(schoolData) {
    try {
      const response = await resourcesAPI.registerSchool(schoolData)
      return response
    } catch (error) {
      console.log('Creating school:', schoolData)
      return { data: { success: true, _id: Date.now().toString() } }
    }
  },

  async updateSchool(id, schoolData) {
    try {
      // This would need to be implemented in the backend
      const response = await fetch(`/api/resources/schools/${id}`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('auth_token')}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(schoolData)
      })
      return { data: await response.json() }
    } catch (error) {
      console.log('Updating school:', id, schoolData)
      return { data: { success: true } }
    }
  },

  async verifySchool(id) {
    try {
      const response = await resourcesAPI.verifySchool(id)
      return response
    } catch (error) {
      console.log('Verifying school:', id)
      return { data: { success: true } }
    }
  },

  async getSchoolRequests(schoolId) {
    try {
      const response = await resourcesAPI.getSchoolRequests(schoolId)
      return response
    } catch (error) {
      throw error
    }
  },

  async getSchoolStats() {
    try {
      const response = await resourcesAPI.getSchoolStats()
      return response
    } catch (error) {
      // Mock stats
      return {
        data: {
          total_schools: 3,
          verified_schools: 1,
          pending_schools: 1,
          rejected_schools: 1
        }
      }
    }
  }
}

export default schoolService
