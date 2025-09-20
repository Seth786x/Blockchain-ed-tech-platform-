import { defineStore } from 'pinia'
import { useWeb3Store } from './web3'
import { coursesAPI } from '../services/api'

export const useCoursesStore = defineStore('courses', {
  state: () => ({
    courses: [],
    enrolledCourses: [],
    currentCourse: null,
    loading: false,
    error: null,
    filters: {
      component: null,
      level: null,
      limit: 20,
      skip: 0
    }
  }),

  getters: {
    // Get courses by component
    coursesByComponent: (state) => (component) => {
      return state.courses.filter(course => course.component === component)
    },

    // Get courses by level
    coursesByLevel: (state) => (level) => {
      return state.courses.filter(course => course.level === level)
    },

    // Get published courses
    publishedCourses: (state) => {
      return state.courses.filter(course => course.is_published)
    },

    // Get course by ID
    getCourseById: (state) => (id) => {
      return state.courses.find(course => course.id === id)
    },

    // Check if user is enrolled in course
    isEnrolled: (state) => (courseId) => {
      return state.enrolledCourses.some(enrollment => enrollment.course_id === courseId)
    },

    // Get enrollment for course
    getEnrollment: (state) => (courseId) => {
      return state.enrolledCourses.find(enrollment => enrollment.course_id === courseId)
    }
  },

  actions: {
    // Fetch all courses
    async fetchCourses(params = {}) {
      this.loading = true
      this.error = null
      
      try {
        const response = await coursesAPI.getCourses(params)
        this.courses = response.data
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to fetch courses'
        throw error
      } finally {
        this.loading = false
      }
    },

    // Fetch course by ID
    async fetchCourse(id) {
      this.loading = true
      this.error = null
      
      try {
        const response = await coursesAPI.getCourse(id)
        this.currentCourse = response.data
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to fetch course'
        throw error
      } finally {
        this.loading = false
      }
    },

    // Create new course
    async createCourse(courseData) {
      this.loading = true
      this.error = null
      
      try {
        const response = await coursesAPI.createCourse(courseData)
        this.courses.push(response.data)
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to create course'
        throw error
      } finally {
        this.loading = false
      }
    },

    // Update course
    async updateCourse(id, courseData) {
      this.loading = true
      this.error = null
      
      try {
        await coursesAPI.updateCourse(id, courseData)
        
        // Update course in state
        const index = this.courses.findIndex(course => course.id === id)
        if (index !== -1) {
          this.courses[index] = { ...this.courses[index], ...courseData }
        }
        
        return { success: true }
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to update course'
        throw error
      } finally {
        this.loading = false
      }
    },

    // Delete course
    async deleteCourse(id) {
      this.loading = true
      this.error = null
      
      try {
        await coursesAPI.deleteCourse(id)
        
        // Remove course from state
        this.courses = this.courses.filter(course => course.id !== id)
        
        return { success: true }
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to delete course'
        throw error
      } finally {
        this.loading = false
      }
    },

    // Enroll in course
    async enrollInCourse(courseId) {
      this.loading = true
      this.error = null
      
      try {
        await coursesAPI.enrollInCourse(courseId)
        
        // Add to enrolled courses
        const course = this.courses.find(c => c.id === courseId)
        if (course) {
          this.enrolledCourses.push({
            course_id: courseId,
            course: course,
            enrolled_at: new Date().toISOString(),
            status: 'active',
            progress_percentage: 0,
            completed_modules: []
          })
        }
        
        return { success: true }
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to enroll in course'
        throw error
      } finally {
        this.loading = false
      }
    },

    // Get course progress
    async fetchCourseProgress(courseId) {
      try {
        const response = await coursesAPI.getCourseProgress(courseId)
        return response.data
      } catch (error) {
        console.error('Failed to fetch course progress:', error)
        throw error
      }
    },

    // Complete module
    async completeModule(courseId, moduleId) {
      this.loading = true
      this.error = null
      
      try {
        const response = await coursesAPI.completeModule(courseId, moduleId)
        
        // Update enrollment progress
        const enrollment = this.enrolledCourses.find(e => e.course_id === courseId)
        if (enrollment) {
          enrollment.progress_percentage = response.data.progress_percentage
          if (!enrollment.completed_modules.includes(moduleId)) {
            enrollment.completed_modules.push(moduleId)
          }
        }
        
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to complete module'
        throw error
      } finally {
        this.loading = false
      }
    },

    // Fetch enrolled courses
    async fetchEnrolledCourses() {
      this.loading = true
      this.error = null
      
      try {
        const response = await coursesAPI.getEnrolledCourses()
        this.enrolledCourses = response.data
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to fetch enrolled courses'
        throw error
      } finally {
        this.loading = false
      }
    },

    // Set filters
    setFilters(filters) {
      this.filters = { ...this.filters, ...filters }
    },

    // Clear error
    clearError() {
      this.error = null
    },

    // Clear current course
    clearCurrentCourse() {
      this.currentCourse = null
    }
  }
}) 