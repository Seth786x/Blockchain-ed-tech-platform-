<template>
  <div class="course-detail">
    <div class="container">
      <div v-if="loading" class="text-center py-5">
        <div class="spinner-border" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>

      <div v-else-if="course">
        <!-- Course Header -->
        <div class="row mb-4">
          <div class="col-md-8">
            <nav aria-label="breadcrumb">
              <ol class="breadcrumb">
                <li class="breadcrumb-item">
                  <router-link to="/courses">Courses</router-link>
                </li>
                <li class="breadcrumb-item active" aria-current="page">
                  {{ course.title }}
                </li>
              </ol>
            </nav>
            
            <h1>{{ course.title }}</h1>
            <p class="text-muted">{{ course.description }}</p>
            
            <div class="course-meta d-flex flex-wrap gap-3 mb-3">
              <span class="badge bg-primary">{{ course.category }}</span>
              <span class="badge bg-secondary">{{ course.level }}</span>
              <span class="badge bg-info">{{ course.duration_hours }} hours</span>
              <span v-if="course.hardware_component" class="badge bg-warning">
                {{ course.hardware_component }}
              </span>
            </div>
            
            <div class="instructor-info mb-3">
              <small class="text-muted">
                Instructor: <strong>{{ course.instructor_name || 'N/A' }}</strong>
              </small>
            </div>
          </div>
          
          <div class="col-md-4">
            <div class="card">
              <div class="card-body text-center">
                <!-- Blockchain Purchase Button -->
                <div v-if="!isPurchased">
                  <div class="mb-2">
                    <span class="badge bg-success">Price: {{ coursePriceEth }} ETH</span>
                  </div>
                  <button 
                    class="btn btn-warning btn-lg w-100 mb-3" 
                    @click="buyCourse"
                    :disabled="buying"
                  >
                    <span v-if="buying" class="spinner-border spinner-border-sm me-2"></span>
                    <i class="fab fa-ethereum me-2"></i>
                    {{ buying ? 'Processing...' : 'Buy Course with MetaMask' }}
                  </button>
                  <div v-if="web3Error" class="alert alert-danger small mt-2">{{ web3Error }}</div>
                </div>
                <div v-else>
                  <div class="alert alert-success">
                    <i class="fas fa-check-circle me-2"></i>
                    You have purchased this course (on blockchain)
                  </div>
                  <router-link :to="`/courses/${course._id}/learn`" class="btn btn-primary w-100">
                    <i class="fas fa-play me-2"></i>Start Learning
                  </router-link>
                </div>
                
                <!-- Edit buttons for instructors/admins -->
                <div v-if="canEdit" class="mt-3">
                  <router-link 
                    :to="`/courses/${course._id}/edit`" 
                    class="btn btn-outline-secondary btn-sm me-2"
                  >
                    <i class="fas fa-edit me-1"></i>Edit
                  </router-link>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Course Content -->
        <div class="row">
          <div class="col-md-8">
            <!-- Learning Objectives -->
            <div class="card mb-4">
              <div class="card-header">
                <h5><i class="fas fa-bullseye me-2"></i>Learning Objectives</h5>
              </div>
              <div class="card-body">
                <p>{{ course.learning_objectives || 'No learning objectives specified.' }}</p>
              </div>
            </div>

            <!-- Prerequisites -->
            <div class="card mb-4" v-if="course.prerequisites">
              <div class="card-header">
                <h5><i class="fas fa-list-check me-2"></i>Prerequisites</h5>
              </div>
              <div class="card-body">
                <p>{{ course.prerequisites }}</p>
              </div>
            </div>

            <!-- Course Modules -->
            <div class="card mb-4">
              <div class="card-header">
                <h5><i class="fas fa-book-open me-2"></i>Course Modules</h5>
              </div>
              <div class="card-body">
                <div v-if="course.modules && course.modules.length > 0">
                  <div 
                    v-for="(module, index) in course.modules" 
                    :key="module._id || index"
                    class="module-item p-3 mb-3 border rounded clickable-module"
                    @click="openModule(index)"
                    style="cursor: pointer;"
                  >
                    <div class="d-flex justify-content-between align-items-start">
                      <div class="flex-grow-1">
                        <div class="d-flex align-items-center mb-2">
                          <h6 class="mb-0 me-2">{{ module.title }}</h6>
                          <i class="fas fa-play-circle text-primary"></i>
                        </div>
                        <p class="text-muted mb-2">{{ module.description }}</p>
                        <small class="text-muted">
                          <i class="fas fa-clock me-1"></i>
                          {{ module.duration_minutes || 30 }} minutes
                        </small>
                      </div>
                      <div class="ms-3">
                        <span 
                          v-if="module.completed" 
                          class="badge bg-success"
                        >
                          <i class="fas fa-check me-1"></i>Completed
                        </span>
                        <span 
                          v-else-if="isEnrolled" 
                          class="badge bg-secondary"
                        >
                          Not Started
                        </span>
                        <div class="mt-2">
                          <button class="btn btn-sm btn-outline-primary">
                            <i class="fas fa-play me-1"></i>Start
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                <div v-else class="text-center text-muted py-4">
                  <i class="fas fa-book-open fa-3x mb-3 opacity-25"></i>
                  <p>No modules available yet. Check back later!</p>
                </div>
              </div>
            </div>
          </div>

          <div class="col-md-4">
            <!-- Course Stats -->
            <div class="card mb-4">
              <div class="card-header">
                <h6>Course Information</h6>
              </div>
              <div class="card-body">
                <div class="course-stat mb-2">
                  <strong>Duration:</strong> {{ course.duration_hours }} hours
                </div>
                <div class="course-stat mb-2">
                  <strong>Level:</strong> {{ course.level }}
                </div>
                <div class="course-stat mb-2">
                  <strong>Category:</strong> {{ course.category }}
                </div>
                <div class="course-stat mb-2" v-if="course.hardware_component">
                  <strong>Hardware Focus:</strong> {{ course.hardware_component }}
                </div>
                <div class="course-stat mb-2">
                  <strong>Enrolled Students:</strong> {{ course.enrolled_count || 0 }}
                </div>
                <div class="course-stat">
                  <strong>Created:</strong> {{ formatDate(course.created_at) }}
                </div>
              </div>
            </div>

            <!-- Related Courses -->
            <div class="card">
              <div class="card-header">
                <h6>Related Courses</h6>
              </div>
              <div class="card-body">
                <div class="text-center text-muted">
                  <small>Related courses coming soon...</small>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-else class="text-center py-5">
        <h3>Course not found</h3>
        <p class="text-muted">The course you're looking for doesn't exist.</p>
        <router-link to="/courses" class="btn btn-primary">
          Browse All Courses
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import { coursesAPI } from '../../services/api'
import { authService } from '../../services/auth'
import { useWeb3ContractStore } from '@/stores/web3-contract'

export default {
  name: 'CourseDetail',
  data() {
    return {
      course: null,
      loading: true,
      buying: false,
      isPurchased: false,
      coursePriceEth: '0.000005',
      web3Error: '',
      enrolling: false,
      isEnrolled: false,
      progress: 0
    }
  },
  computed: {
    canEdit() {
      const user = authService.getUser()
      return user && (user.role === 'admin' || user.role === 'instructor')
    },
    web3Store() {
      return useWeb3ContractStore()
    }
  },
  async mounted() {
    await this.loadCourse()
    if (this.course) {
      await this.fetchCoursePrice()
      await this.checkPurchaseStatus()
    }
  },
  methods: {
    async loadCourse() {
      try {
        const courseId = this.$route.params.id
        const response = await coursesAPI.getCourse(courseId)
        this.course = response.data
      } catch (error) {
        console.error('Error loading course:', error)
        this.course = null
      } finally {
        this.loading = false
      }
    },
    async fetchCoursePrice() {
      try {
        await this.web3Store.checkConnection()
        this.coursePriceEth = await this.web3Store.getCoursePrice()
      } catch (e) {
        this.coursePriceEth = '0.000005'
      }
    },
    async checkPurchaseStatus() {
      try {
        await this.web3Store.checkConnection()
        this.isPurchased = await this.web3Store.hasPurchased(this.$route.params.id)
      } catch (error) {
        this.isPurchased = false
      }
    },
    async buyCourse() {
      this.buying = true
      this.web3Error = ''
      try {
        await this.web3Store.connectWallet()
        await this.web3Store.purchaseCourse(this.$route.params.id)
        this.isPurchased = true
        alert('Course purchased successfully!')
      } catch (error) {
        this.web3Error = error.message || 'Blockchain transaction failed.'
      } finally {
        this.buying = false
      }
    },
    continueCourse() {
      // Navigate to course content or first module
      alert('Course content viewer coming soon!')
    },
    formatDate(dateString) {
      if (!dateString) return 'Unknown'
      return new Date(dateString).toLocaleDateString()
    },
    openModule(moduleIndex) {
      // Navigate to module viewer with course and module information
      this.$router.push(`/courses/${this.course._id}/module/${moduleIndex}`)
    }
  }
}
</script>

<style scoped>
.course-detail {
  padding: 20px 0;
}

.course-meta .badge {
  font-size: 0.875rem;
}

.module-item {
  background-color: #f8f9fa;
  transition: all 0.2s ease;
}

.module-item:hover {
  background-color: #e9ecef;
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.clickable-module {
  border: 2px solid #e9ecef !important;
  position: relative;
}

.clickable-module:hover {
  border-color: #007bff !important;
}

.clickable-module:hover .fa-play-circle {
  color: #007bff !important;
}

.course-stat {
  padding: 0.25rem 0;
  border-bottom: 1px solid #e9ecef;
}

.course-stat:last-child {
  border-bottom: none;
}

.progress {
  height: 8px;
}

.card {
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
}

.breadcrumb {
  background-color: transparent;
  padding: 0;
}

.spinner-border-sm {
  width: 1rem;
  height: 1rem;
}
</style>
