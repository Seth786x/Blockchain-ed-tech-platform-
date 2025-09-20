<template>
  <div class="instructor-dashboard">
    <div class="container">
      <!-- Dashboard Header -->
      <div class="row mb-4">
        <div class="col-12">
          <h2>Instructor Dashboard</h2>
          <p class="text-muted">Manage your courses and track student progress</p>
        </div>
      </div>

      <!-- Stats Cards -->
      <div class="row mb-4">
        <div class="col-md-3">
          <div class="card bg-primary text-white">
            <div class="card-body">
              <div class="d-flex justify-content-between">
                <div>
                  <h4>{{ stats.totalCourses }}</h4>
                  <p class="mb-0">My Courses</p>
                </div>
                <div class="align-self-center">
                  <i class="fas fa-book fa-2x opacity-50"></i>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="col-md-3">
          <div class="card bg-success text-white">
            <div class="card-body">
              <div class="d-flex justify-content-between">
                <div>
                  <h4>{{ stats.totalStudents }}</h4>
                  <p class="mb-0">Total Students</p>
                </div>
                <div class="align-self-center">
                  <i class="fas fa-users fa-2x opacity-50"></i>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="col-md-3">
          <div class="card bg-info text-white">
            <div class="card-body">
              <div class="d-flex justify-content-between">
                <div>
                  <h4>{{ stats.publishedCourses }}</h4>
                  <p class="mb-0">Published</p>
                </div>
                <div class="align-self-center">
                  <i class="fas fa-globe fa-2x opacity-50"></i>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="col-md-3">
          <div class="card bg-warning text-white">
            <div class="card-body">
              <div class="d-flex justify-content-between">
                <div>
                  <h4>${{ stats.totalEarnings.toFixed(2) }}</h4>
                  <p class="mb-0">Earnings</p>
                </div>
                <div class="align-self-center">
                  <i class="fas fa-dollar-sign fa-2x opacity-50"></i>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Quick Actions -->
      <div class="row mb-4">
        <div class="col-12">
          <div class="card">
            <div class="card-header">
              <h5>Quick Actions</h5>
            </div>
            <div class="card-body">
              <div class="row">
                <div class="col-md-3 mb-3">
                  <router-link to="/courses/create" class="btn btn-primary w-100">
                    <i class="fas fa-plus me-2"></i>Create New Course
                  </router-link>
                </div>
                <div class="col-md-3 mb-3">
                  <button @click="viewAnalytics" class="btn btn-outline-info w-100">
                    <i class="fas fa-chart-bar me-2"></i>View Analytics
                  </button>
                </div>
                <div class="col-md-3 mb-3">
                  <button @click="manageStudents" class="btn btn-outline-success w-100">
                    <i class="fas fa-users me-2"></i>Manage Students
                  </button>
                </div>
                <div class="col-md-3 mb-3">
                  <button @click="reviewFeedback" class="btn btn-outline-warning w-100">
                    <i class="fas fa-comments me-2"></i>Student Feedback
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- My Courses -->
      <div class="row">
        <div class="col-12">
          <div class="card">
            <div class="card-header d-flex justify-content-between align-items-center">
              <h5>My Courses</h5>
              <div class="btn-group btn-group-sm">
                <button 
                  class="btn btn-outline-secondary"
                  :class="{ active: courseFilter === 'all' }"
                  @click="courseFilter = 'all'"
                >
                  All
                </button>
                <button 
                  class="btn btn-outline-secondary"
                  :class="{ active: courseFilter === 'published' }"
                  @click="courseFilter = 'published'"
                >
                  Published
                </button>
                <button 
                  class="btn btn-outline-secondary"
                  :class="{ active: courseFilter === 'draft' }"
                  @click="courseFilter = 'draft'"
                >
                  Drafts
                </button>
              </div>
            </div>
            <div class="card-body">
              <div v-if="filteredCourses.length === 0" class="text-center text-muted py-4">
                <i class="fas fa-book-open fa-3x mb-3 opacity-25"></i>
                <p>No courses found. Create your first course!</p>
                <router-link to="/courses/create" class="btn btn-primary">
                  <i class="fas fa-plus me-2"></i>Create Course
                </router-link>
              </div>
              <div v-else class="table-responsive">
                <table class="table table-hover">
                  <thead>
                    <tr>
                      <th>Course</th>
                      <th>Status</th>
                      <th>Students</th>
                      <th>Completion Rate</th>
                      <th>Earnings</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="course in filteredCourses" :key="course._id">
                      <td>
                        <div class="d-flex align-items-center">
                          <div class="course-thumbnail me-3">
                            <img 
                              v-if="course.thumbnail_url" 
                              :src="`http://localhost:8000${course.thumbnail_url}`" 
                              :alt="course.title"
                              class="rounded"
                              style="width: 50px; height: 50px; object-fit: cover;"
                            />
                            <div v-else class="bg-light rounded d-flex align-items-center justify-content-center" style="width: 50px; height: 50px;">
                              <i class="fas fa-book text-muted"></i>
                            </div>
                          </div>
                          <div>
                            <h6 class="mb-1">{{ course.title }}</h6>
                            <small class="text-muted">{{ course.category }}</small>
                          </div>
                        </div>
                      </td>
                      <td>
                        <span 
                          class="badge"
                          :class="course.is_published ? 'bg-success' : 'bg-secondary'"
                        >
                          {{ course.is_published ? 'Published' : 'Draft' }}
                        </span>
                      </td>
                      <td>{{ course.enrolled_count || 0 }}</td>
                      <td>
                        <div class="progress" style="height: 5px;">
                          <div 
                            class="progress-bar" 
                            :style="{ width: getCompletionRate(course) + '%' }"
                          ></div>
                        </div>
                        <small class="text-muted">{{ getCompletionRate(course) }}%</small>
                      </td>
                      <td>${{ ((course.enrolled_count || 0) * (course.price || 0)).toFixed(2) }}</td>
                      <td>
                        <div class="btn-group btn-group-sm">
                          <router-link 
                            :to="`/courses/${course._id}`" 
                            class="btn btn-outline-primary"
                            title="View Course"
                          >
                            <i class="fas fa-eye"></i>
                          </router-link>
                          <router-link 
                            :to="`/courses/${course._id}/edit`" 
                            class="btn btn-outline-secondary"
                            title="Edit Course"
                          >
                            <i class="fas fa-edit"></i>
                          </router-link>
                          <button 
                            @click="viewStudents(course)" 
                            class="btn btn-outline-info"
                            title="View Students"
                          >
                            <i class="fas fa-users"></i>
                          </button>
                          <button 
                            @click="togglePublish(course)" 
                            class="btn btn-outline-success"
                            :title="course.is_published ? 'Unpublish' : 'Publish'"
                          >
                            <i :class="course.is_published ? 'fas fa-eye-slash' : 'fas fa-globe'"></i>
                          </button>
                        </div>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { coursesAPI } from '../../services/api'
import { authService } from '../../services/auth'

export default {
  name: 'InstructorDashboard',
  data() {
    return {
      courses: [],
      courseFilter: 'all',
      stats: {
        totalCourses: 0,
        totalStudents: 0,
        publishedCourses: 0,
        totalEarnings: 0
      },
      loading: true
    }
  },
  computed: {
    filteredCourses() {
      if (this.courseFilter === 'all') return this.courses
      if (this.courseFilter === 'published') return this.courses.filter(c => c.is_published)
      if (this.courseFilter === 'draft') return this.courses.filter(c => !c.is_published)
      return this.courses
    }
  },
  async mounted() {
    await this.loadInstructorCourses()
    this.calculateStats()
  },
  methods: {
    async loadInstructorCourses() {
      try {
        // In a real app, this would filter by instructor ID
        const response = await coursesAPI.getCourses()
        this.courses = response.data
      } catch (error) {
        console.error('Error loading courses:', error)
      } finally {
        this.loading = false
      }
    },
    calculateStats() {
      this.stats.totalCourses = this.courses.length
      this.stats.publishedCourses = this.courses.filter(c => c.is_published).length
      this.stats.totalStudents = this.courses.reduce((sum, course) => sum + (course.enrolled_count || 0), 0)
      this.stats.totalEarnings = this.courses.reduce((sum, course) => sum + ((course.enrolled_count || 0) * (course.price || 0)), 0)
    },
    getCompletionRate(course) {
      // Mock completion rate calculation
      return Math.floor(Math.random() * 100)
    },
    async togglePublish(course) {
      try {
        const updatedCourse = {
          ...course,
          is_published: !course.is_published
        }
        await coursesAPI.updateCourse(course._id, updatedCourse)
        course.is_published = !course.is_published
        this.calculateStats()
      } catch (error) {
        console.error('Error updating course:', error)
        alert('Failed to update course status')
      }
    },
    viewStudents(course) {
      alert(`Student management for "${course.title}" coming soon!`)
    },
    viewAnalytics() {
      alert('Analytics dashboard coming soon!')
    },
    manageStudents() {
      alert('Student management coming soon!')
    },
    reviewFeedback() {
      alert('Feedback review coming soon!')
    }
  }
}
</script>

<style scoped>
.instructor-dashboard {
  padding: 20px 0;
  background-color: #f8f9fa;
  min-height: 100vh;
}

.card {
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
  border-radius: 0.5rem;
}

.stats-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
}

.opacity-50 {
  opacity: 0.5;
}

.table th {
  border-top: none;
  font-weight: 600;
  color: #495057;
}

.btn-group-sm > .btn {
  padding: 0.25rem 0.5rem;
}

.course-thumbnail img {
  border: 2px solid #dee2e6;
}

.progress {
  border-radius: 10px;
  background-color: #e9ecef;
}

.progress-bar {
  border-radius: 10px;
}

.badge {
  font-size: 0.75rem;
}

.btn-group .btn {
  border-radius: 0.375rem;
}

.btn-group .btn + .btn {
  margin-left: 0.25rem;
}
</style>
