<template>
  <div class="courses-container">
    <!-- Header -->
    <div class="py-5" style="background: linear-gradient(135deg, #000000 0%, #667eea 100%); color: white;">
      <div class="container">
        <div class="row align-items-center">
          <div class="col-md-8">
            <div class="page-header">
              <h1 class="display-5 fw-bold mb-3">
                <i class="fas fa-microchip me-3"></i>
                Hardware Learning Courses ⚡
              </h1>
            </div>
            <p class="lead mb-0">Master computer hardware with hands-on courses and blockchain-verified certificates 🎓</p>
          </div>
          <div class="col-md-4 text-end">
            <div v-if="authStore.isInstructor || authStore.isAdmin">
              <router-link to="/courses/create" class="btn btn-light btn-lg">
                <i class="fas fa-plus me-2"></i>Create Course
              </router-link>
            </div>
            <div class="position-relative mt-3">
              <span style="font-size: 3rem; opacity: 0.2;">🔧</span>
              <span style="font-size: 2rem; opacity: 0.3; margin-left: 20px;">💻</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="container py-5">
      <!-- Filters -->
      <div class="row mb-4">
        <div class="col-12">
          <div class="card">
            <div class="card-body">
              <h5 class="card-title mb-3">
                <i class="fas fa-filter me-2 text-secondary"></i>
                Filter Courses 🔍
              </h5>
              <div class="row align-items-end">
                <div class="col-md-3 mb-3">
                  <label class="form-label">Hardware Component</label>
                  <select v-model="filters.component" class="form-select" @change="applyFilters">
                    <option value="">All Components</option>
                    <option value="cpu">CPU 🧠</option>
                    <option value="gpu">GPU 🎮</option>
                    <option value="ram">RAM ⚡</option>
                    <option value="motherboard">Motherboard 🔌</option>
                    <option value="storage">Storage 💽</option>
                    <option value="power_supply">Power Supply 🔋</option>
                    <option value="cooling">Cooling ❄️</option>
                    <option value="case">Case 📦</option>
                  </select>
                </div>
                <div class="col-md-3 mb-3">
                  <label class="form-label">Difficulty Level</label>
                  <select v-model="filters.level" class="form-select" @change="applyFilters">
                    <option value="">All Levels</option>
                    <option value="beginner">Beginner 🌱</option>
                    <option value="intermediate">Intermediate</option>
                    <option value="advanced">Advanced</option>
                  </select>
                </div>
                <div class="col-md-3 mb-3">
                  <label class="form-label">Price Range</label>
                  <select v-model="filters.price" class="form-select" @change="applyFilters">
                    <option value="">All Prices</option>
                    <option value="free">Free</option>
                    <option value="paid">Paid</option>
                  </select>
                </div>
                <div class="col-md-3 mb-3">
                  <button @click="clearFilters" class="btn btn-outline-secondary w-100">
                    <i class="fas fa-times me-2"></i>Clear Filters
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="coursesStore.loading" class="text-center py-5">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
        <p class="mt-3">Loading courses...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="coursesStore.error" class="alert alert-danger" role="alert">
        <i class="fas fa-exclamation-triangle me-2"></i>
        {{ coursesStore.error }}
        <button @click="loadCourses" class="btn btn-sm btn-outline-danger ms-3">
          <i class="fas fa-redo me-1"></i>Retry
        </button>
      </div>

      <!-- Courses Grid -->
      <div v-else>
        <!-- Results Count -->
        <div class="d-flex justify-content-between align-items-center mb-4">
          <h4 class="mb-0">
            {{ filteredCourses.length }} Course{{ filteredCourses.length !== 1 ? 's' : '' }} Found
          </h4>
          <div class="d-flex gap-2">
            <button 
              @click="viewMode = 'grid'" 
              class="btn btn-outline-primary"
              :class="{ active: viewMode === 'grid' }"
            >
              <i class="fas fa-th"></i>
            </button>
            <button 
              @click="viewMode = 'list'" 
              class="btn btn-outline-primary"
              :class="{ active: viewMode === 'list' }"
            >
              <i class="fas fa-list"></i>
            </button>
          </div>
        </div>

        <!-- No Courses Found -->
        <div v-if="filteredCourses.length === 0" class="text-center py-5">
          <i class="fas fa-search text-muted" style="font-size: 4rem;"></i>
          <h4 class="mt-3 text-muted">No courses found</h4>
          <p class="text-muted">Try adjusting your filters or check back later for new courses.</p>
          <button @click="clearFilters" class="btn btn-primary">
            <i class="fas fa-times me-2"></i>Clear Filters
          </button>
        </div>

        <!-- Grid View -->
        <div v-else-if="viewMode === 'grid'" class="row">
          <div 
            v-for="course in filteredCourses" 
            :key="course.id" 
            class="col-lg-4 col-md-6 mb-4"
          >
            <div class="card course-card h-100 border-0 shadow-sm">
              <!-- Course Image -->
              <div class="course-image position-relative" style="height: 200px; overflow: hidden;">
                <img 
                  v-if="course.thumbnail_url" 
                  :src="`http://localhost:8000${course.thumbnail_url}`" 
                  :alt="course.title"
                  class="w-100 h-100"
                  style="object-fit: cover;"
                />
                <div 
                  v-else 
                  class="bg-light d-flex align-items-center justify-content-center h-100"
                >
                  <i :class="getComponentIcon(course.title, course.category)" class="text-primary" style="font-size: 3rem;"></i>
                </div>
                
                <!-- Course Overlay -->
                <div class="position-absolute top-0 start-0 w-100 h-100 d-flex justify-content-between p-2">
                  <div class="d-flex flex-column gap-1">
                    <span class="badge bg-primary">{{ course.difficulty || course.level }}</span>
                    <span class="badge bg-secondary">{{ course.category }}</span>
                  </div>
                  <div class="d-flex flex-column align-items-end">
                    <span class="badge bg-success">
                      {{ course.price === 0 ? 'Free' : `${course.price} ETH` }}
                    </span>
                  </div>
                </div>
              </div>

              <!-- Course Content -->
              <div class="card-body d-flex flex-column">
                <h5 class="card-title fw-bold">{{ course.title }}</h5>
                <p class="card-text text-muted flex-grow-1">{{ course.description }}</p>
                
                <div class="course-meta mb-3">
                  <div class="d-flex justify-content-between align-items-center mb-2">
                    <small class="text-muted">
                      <i class="fas fa-book me-1"></i>{{ course.modules?.length || 0 }} modules
                    </small>
                    <small class="text-muted">
                      <i class="fas fa-clock me-1"></i>{{ course.duration }}
                    </small>
                  </div>
                  <div class="d-flex justify-content-between align-items-center">
                    <small class="text-muted">
                      <i class="fas fa-user me-1"></i>{{ course.instructor }}
                    </small>
                    <small class="text-muted">
                      <i class="fas fa-star me-1"></i>{{ course.rating || 4.8 }}
                    </small>
                  </div>
                </div>

                <!-- Action Buttons -->
                <div class="d-grid gap-2">
                  <router-link 
                    :to="`/courses/${course._id}`" 
                    class="btn btn-outline-primary"
                  >
                    <i class="fas fa-eye me-2"></i>View Details
                  </router-link>
                  
                  <button 
                    v-if="!coursesStore.isEnrolled(course._id)"
                    @click="enrollInCourse(course._id)"
                    class="btn btn-primary"
                    :disabled="enrollingCourse === course._id"
                  >
                    <span v-if="enrollingCourse === course._id" class="spinner-border spinner-border-sm me-2"></span>
                    <i v-else class="fas fa-graduation-cap me-2"></i>
                    {{ enrollingCourse === course._id ? 'Enrolling...' : 'Enroll Now' }}
                  </button>
                  
                  <router-link 
                    v-else
                    :to="`/courses/${course._id}`" 
                    class="btn btn-success"
                  >
                    <i class="fas fa-play me-2"></i>Continue Learning
                  </router-link>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- List View -->
        <div v-else class="row">
          <div class="col-12">
            <div v-for="course in filteredCourses" :key="course.id" class="card mb-3 border-0 shadow-sm">
              <div class="card-body">
                <div class="row align-items-center">
                  <div class="col-md-2 text-center">
                    <div class="course-icon-large">
                      <i :class="getComponentIcon(course.component)" class="text-primary"></i>
                    </div>
                  </div>
                  <div class="col-md-6">
                    <h5 class="card-title fw-bold mb-2">{{ course.title }}</h5>
                    <p class="card-text text-muted mb-2">{{ course.description }}</p>
                    <div class="d-flex gap-2">
                      <span class="badge bg-primary">{{ course.level }}</span>
                      <span class="badge bg-secondary">{{ course.component }}</span>
                      <span class="badge bg-info">{{ course.modules?.length || 0 }} modules</span>
                    </div>
                  </div>
                  <div class="col-md-2 text-center">
                    <div class="course-price">
                      <span class="h5 text-success fw-bold">
                        {{ course.price === 0 ? 'Free' : `${course.price} ETH` }}
                      </span>
                    </div>
                  </div>
                  <div class="col-md-2 text-end">
                    <div class="d-grid gap-2">
                      <router-link 
                        :to="`/courses/${course.id}`" 
                        class="btn btn-outline-primary btn-sm"
                      >
                        <i class="fas fa-eye me-1"></i>View
                      </router-link>
                      
                      <button 
                        v-if="!coursesStore.isEnrolled(course.id)"
                        @click="enrollInCourse(course.id)"
                        class="btn btn-primary btn-sm"
                        :disabled="enrollingCourse === course.id"
                      >
                        <span v-if="enrollingCourse === course.id" class="spinner-border spinner-border-sm me-1"></span>
                        <i v-else class="fas fa-graduation-cap me-1"></i>
                        {{ enrollingCourse === course.id ? 'Enrolling...' : 'Enroll' }}
                      </button>
                      
                      <router-link 
                        v-else
                        :to="`/courses/${course.id}`" 
                        class="btn btn-success btn-sm"
                      >
                        <i class="fas fa-play me-1"></i>Continue
                      </router-link>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useCoursesStore } from '../stores/courses'

export default {
  name: 'Courses',
  setup() {
    const authStore = useAuthStore()
    const coursesStore = useCoursesStore()

    // State
    const viewMode = ref('grid')
    const enrollingCourse = ref(null)
    const filters = reactive({
      component: '',
      level: '',
      price: ''
    })

    // Computed
    const filteredCourses = computed(() => {
      let courses = coursesStore.publishedCourses

      if (filters.component) {
        // Filter by component name in title, description, or category
        courses = courses.filter(course => {
          const searchText = `${course.title} ${course.description} ${course.category}`.toLowerCase()
          const componentName = filters.component.replace('_', ' ').toLowerCase()
          return searchText.includes(componentName) || 
                 searchText.includes(componentName.replace('power supply', 'psu')) ||
                 searchText.includes(componentName.replace('cpu', 'processor'))
        })
      }

      if (filters.level) {
        courses = courses.filter(course => course.difficulty === filters.level)
      }

      if (filters.price === 'free') {
        courses = courses.filter(course => course.price === 0)
      } else if (filters.price === 'paid') {
        courses = courses.filter(course => course.price > 0)
      }

      return courses
    })

    // Methods
    const getComponentIcon = (courseTitle, courseCategory) => {
      const text = `${courseTitle} ${courseCategory}`.toLowerCase()
      
      if (text.includes('cpu') || text.includes('processor')) return 'fas fa-microchip'
      if (text.includes('gpu') || text.includes('graphics')) return 'fas fa-tv'
      if (text.includes('ram') || text.includes('memory')) return 'fas fa-memory'
      if (text.includes('motherboard') || text.includes('mobo')) return 'fas fa-server'
      if (text.includes('storage') || text.includes('ssd') || text.includes('hdd')) return 'fas fa-hdd'
      if (text.includes('power') || text.includes('psu')) return 'fas fa-bolt'
      if (text.includes('cooling') || text.includes('fan')) return 'fas fa-snowflake'
      if (text.includes('case') || text.includes('chassis')) return 'fas fa-box'
      return 'fas fa-cog'
    }

    const applyFilters = () => {
      // Filters are applied automatically through computed property
    }

    const clearFilters = () => {
      filters.component = ''
      filters.level = ''
      filters.price = ''
    }

    const loadCourses = async () => {
      try {
        await coursesStore.fetchCourses()
      } catch (error) {
        console.error('Failed to load courses:', error)
      }
    }

    const enrollInCourse = async (courseId) => {
      if (!authStore.isAuthenticated) {
        // Redirect to login
        return
      }

      enrollingCourse.value = courseId
      try {
        await coursesStore.enrollInCourse(courseId)
        // Show success message
        alert('Successfully enrolled in course!')
      } catch (error) {
        console.error('Enrollment failed:', error)
        alert('Failed to enroll in course. Please try again.')
      } finally {
        enrollingCourse.value = null
      }
    }

    // Lifecycle
    onMounted(() => {
      loadCourses()
    })

    return {
      viewMode,
      enrollingCourse,
      filters,
      filteredCourses,
      authStore,
      coursesStore,
      getComponentIcon,
      applyFilters,
      clearFilters,
      loadCourses,
      enrollInCourse
    }
  }
}
</script>

<style scoped>
.courses-container {
  min-height: 100vh;
  background-color: #f8f9fa;
}

.course-card {
  border-radius: 15px;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  overflow: hidden;
}

.course-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1) !important;
}

.course-image {
  position: relative;
  height: 200px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
}

.course-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.3);
  display: flex;
  align-items: flex-start;
  justify-content: flex-end;
  padding: 1rem;
}

.course-badges {
  display: flex;
  gap: 0.5rem;
}

.course-thumbnail {
  font-size: 3rem;
  color: white;
}

.course-icon-large {
  font-size: 2.5rem;
}

.course-price {
  font-size: 1.1rem;
}

.btn {
  border-radius: 10px;
  font-weight: 500;
}

.btn-sm {
  border-radius: 8px;
}

.badge {
  font-size: 0.75rem;
}

.form-select, .form-control {
  border-radius: 10px;
}

.card {
  border-radius: 15px;
}
</style>
