<template>
  <div class="dashboard-container">
    <!-- Header -->
    <div class="bg-primary text-white py-4">
      <div class="container">
        <div class="row align-items-center">
          <div class="col-md-8">
            <h1 class="h3 mb-0">
              <i class="fas fa-tachometer-alt me-2"></i>
              Welcome back, {{ authStore.fullName }}!
            </h1>
            <p class="mb-0 text-white-50">{{ getRoleDescription() }}</p>
          </div>
          <div class="col-md-4 text-end">
            <div class="d-flex align-items-center justify-content-end">
              <span class="badge bg-light text-dark me-2">{{ authStore.user?.role }}</span>
              <button @click="logout" class="btn btn-outline-light btn-sm">
                <i class="fas fa-sign-out-alt me-1"></i>Logout
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="container py-4">
      <!-- Loading State -->
      <div v-if="loading" class="text-center py-5">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
        <p class="mt-3">Loading your dashboard...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="alert alert-danger" role="alert">
        <i class="fas fa-exclamation-triangle me-2"></i>
        {{ error }}
        <button @click="loadDashboard" class="btn btn-sm btn-outline-danger ms-3">
          <i class="fas fa-redo me-1"></i>Retry
        </button>
      </div>

      <!-- Dashboard Content -->
      <div v-else>
        <!-- Stats Cards -->
        <div class="row mb-4">
          <div class="col-md-3 mb-3" v-for="stat in stats" :key="stat.title">
            <div class="card border-0 shadow-sm h-100">
              <div class="card-body text-center">
                <div class="mb-3">
                  <i :class="stat.icon" class="text-primary" style="font-size: 2rem;"></i>
                </div>
                <h3 class="fw-bold mb-1">{{ stat.value }}</h3>
                <p class="text-muted mb-0">{{ stat.title }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Role-specific Content -->
        <div class="row">
          <!-- Student Dashboard -->
          <div v-if="authStore.isStudent" class="col-12">
            <div class="row">
              <!-- Enrolled Courses -->
              <div class="col-md-8 mb-4">
                <div class="card border-0 shadow-sm">
                  <div class="card-header bg-white border-0">
                    <h5 class="mb-0">
                      <i class="fas fa-graduation-cap me-2 text-primary"></i>
                      My Courses
                    </h5>
                  </div>
                  <div class="card-body">
                    <div v-if="enrolledCourses.length === 0" class="text-center py-4">
                      <i class="fas fa-book-open text-muted" style="font-size: 3rem;"></i>
                      <p class="mt-3 text-muted">You haven't enrolled in any courses yet.</p>
                      <router-link to="/courses" class="btn btn-primary">
                        <i class="fas fa-search me-2"></i>Browse Courses
                      </router-link>
                    </div>
                    <div v-else>
                      <div v-for="enrollment in enrolledCourses" :key="enrollment.id" class="mb-3">
                        <div class="d-flex align-items-center p-3 border rounded">
                          <div class="flex-grow-1">
                            <h6 class="mb-1">{{ enrollment.course?.title }}</h6>
                            <p class="text-muted mb-2">{{ enrollment.course?.description }}</p>
                            <div class="progress mb-2" style="height: 8px;">
                              <div 
                                class="progress-bar bg-primary" 
                                :style="{ width: enrollment.progress_percentage + '%' }"
                              ></div>
                            </div>
                            <small class="text-muted">
                              {{ enrollment.progress_percentage }}% Complete
                            </small>
                          </div>
                          <div class="ms-3">
                            <router-link 
                              :to="`/courses/${enrollment.course_id}`" 
                              class="btn btn-outline-primary btn-sm"
                            >
                              Continue
                            </router-link>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Quick Actions -->
              <div class="col-md-4 mb-4">
                <div class="card border-0 shadow-sm">
                  <div class="card-header bg-white border-0">
                    <h5 class="mb-0">
                      <i class="fas fa-bolt me-2 text-primary"></i>
                      Quick Actions
                    </h5>
                  </div>
                  <div class="card-body">
                    <div class="d-grid gap-2">
                      <router-link to="/courses" class="btn btn-outline-primary">
                        <i class="fas fa-search me-2"></i>Browse Courses
                      </router-link>
                      <router-link to="/certificates" class="btn btn-outline-success">
                        <i class="fas fa-certificate me-2"></i>My Certificates
                      </router-link>
                      <router-link to="/progress" class="btn btn-outline-info">
                        <i class="fas fa-chart-line me-2"></i>Progress Report
                      </router-link>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Instructor Dashboard -->
          <div v-if="authStore.isInstructor" class="col-12">
            <div class="row">
              <!-- My Courses -->
              <div class="col-md-8 mb-4">
                <div class="card border-0 shadow-sm">
                  <div class="card-header bg-white border-0 d-flex justify-content-between align-items-center">
                    <h5 class="mb-0">
                      <i class="fas fa-chalkboard-teacher me-2 text-primary"></i>
                      My Courses
                    </h5>
                    <router-link to="/courses/create" class="btn btn-primary btn-sm">
                      <i class="fas fa-plus me-2"></i>Create Course
                    </router-link>
                  </div>
                  <div class="card-body">
                    <div v-if="instructorCourses.length === 0" class="text-center py-4">
                      <i class="fas fa-chalkboard text-muted" style="font-size: 3rem;"></i>
                      <p class="mt-3 text-muted">You haven't created any courses yet.</p>
                      <router-link to="/courses/create" class="btn btn-primary">
                        <i class="fas fa-plus me-2"></i>Create Your First Course
                      </router-link>
                    </div>
                    <div v-else>
                      <div v-for="course in instructorCourses" :key="course.id" class="mb-3">
                        <div class="d-flex align-items-center p-3 border rounded">
                          <div class="flex-grow-1">
                            <h6 class="mb-1">{{ course.title }}</h6>
                            <p class="text-muted mb-2">{{ course.description }}</p>
                            <div class="d-flex gap-2">
                              <span class="badge bg-primary">{{ course.level }}</span>
                              <span class="badge bg-secondary">{{ course.component }}</span>
                              <span class="badge" :class="course.is_published ? 'bg-success' : 'bg-warning'">
                                {{ course.is_published ? 'Published' : 'Draft' }}
                              </span>
                            </div>
                          </div>
                          <div class="ms-3">
                            <router-link 
                              :to="`/courses/${course.id}/edit`" 
                              class="btn btn-outline-primary btn-sm me-2"
                            >
                              Edit
                            </router-link>
                            <router-link 
                              :to="`/courses/${course.id}`" 
                              class="btn btn-outline-info btn-sm"
                            >
                              View
                            </router-link>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Instructor Stats -->
              <div class="col-md-4 mb-4">
                <div class="card border-0 shadow-sm">
                  <div class="card-header bg-white border-0">
                    <h5 class="mb-0">
                      <i class="fas fa-chart-bar me-2 text-primary"></i>
                      Teaching Stats
                    </h5>
                  </div>
                  <div class="card-body">
                    <div class="text-center mb-3">
                      <h3 class="fw-bold text-primary">{{ instructorCourses.length }}</h3>
                      <p class="text-muted mb-0">Total Courses</p>
                    </div>
                    <div class="d-grid gap-2">
                      <router-link to="/courses/create" class="btn btn-primary">
                        <i class="fas fa-plus me-2"></i>Create New Course
                      </router-link>
                      <router-link to="/analytics" class="btn btn-outline-primary">
                        <i class="fas fa-chart-line me-2"></i>View Analytics
                      </router-link>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Admin Dashboard -->
          <div v-if="authStore.isAdmin" class="col-12">
            <div class="row">
              <!-- Platform Overview -->
              <div class="col-md-8 mb-4">
                <div class="card border-0 shadow-sm">
                  <div class="card-header bg-white border-0">
                    <h5 class="mb-0">
                      <i class="fas fa-cogs me-2 text-primary"></i>
                      Platform Management
                    </h5>
                  </div>
                  <div class="card-body">
                    <div class="row">
                      <div class="col-md-6 mb-3">
                        <div class="card bg-light border-0">
                          <div class="card-body text-center">
                            <i class="fas fa-users text-primary mb-2" style="font-size: 2rem;"></i>
                            <h5>User Management</h5>
                            <router-link to="/admin/users" class="btn btn-primary btn-sm">
                              Manage Users
                            </router-link>
                          </div>
                        </div>
                      </div>
                      <div class="col-md-6 mb-3">
                        <div class="card bg-light border-0">
                          <div class="card-body text-center">
                            <i class="fas fa-school text-primary mb-2" style="font-size: 2rem;"></i>
                            <h5>School Verification</h5>
                            <router-link to="/admin/schools" class="btn btn-primary btn-sm">
                              Verify Schools
                            </router-link>
                          </div>
                        </div>
                      </div>
                      <div class="col-md-6 mb-3">
                        <div class="card bg-light border-0">
                          <div class="card-body text-center">
                            <i class="fas fa-hand-holding-usd text-primary mb-2" style="font-size: 2rem;"></i>
                            <h5>Donation Management</h5>
                            <router-link to="/admin/donations" class="btn btn-primary btn-sm">
                              Manage Donations
                            </router-link>
                          </div>
                        </div>
                      </div>
                      <div class="col-md-6 mb-3">
                        <div class="card bg-light border-0">
                          <div class="card-body text-center">
                            <i class="fas fa-chart-pie text-primary mb-2" style="font-size: 2rem;"></i>
                            <h5>Analytics</h5>
                            <router-link to="/admin/analytics" class="btn btn-primary btn-sm">
                              View Analytics
                            </router-link>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Admin Quick Actions -->
              <div class="col-md-4 mb-4">
                <div class="card border-0 shadow-sm">
                  <div class="card-header bg-white border-0">
                    <h5 class="mb-0">
                      <i class="fas fa-tools me-2 text-primary"></i>
                      Quick Actions
                    </h5>
                  </div>
                  <div class="card-body">
                    <div class="d-grid gap-2">
                      <router-link to="/admin/users" class="btn btn-outline-primary">
                        <i class="fas fa-users me-2"></i>Manage Users
                      </router-link>
                      <router-link to="/admin/schools" class="btn btn-outline-success">
                        <i class="fas fa-school me-2"></i>Verify Schools
                      </router-link>
                      <router-link to="/admin/donations" class="btn btn-outline-warning">
                        <i class="fas fa-hand-holding-usd me-2"></i>Donations
                      </router-link>
                      <router-link to="/admin/analytics" class="btn btn-outline-info">
                        <i class="fas fa-chart-bar me-2"></i>Analytics
                      </router-link>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Donor Dashboard -->
          <div v-if="authStore.isDonor" class="col-12">
            <div class="row">
              <!-- My Donations -->
              <div class="col-md-8 mb-4">
                <div class="card border-0 shadow-sm">
                  <div class="card-header bg-white border-0 d-flex justify-content-between align-items-center">
                    <h5 class="mb-0">
                      <i class="fas fa-hand-holding-heart me-2 text-primary"></i>
                      My Donations
                    </h5>
                    <router-link to="/donations/new" class="btn btn-primary btn-sm">
                      <i class="fas fa-plus me-2"></i>Make Donation
                    </router-link>
                  </div>
                  <div class="card-body">
                    <div v-if="donations.length === 0" class="text-center py-4">
                      <i class="fas fa-heart text-muted" style="font-size: 3rem;"></i>
                      <p class="mt-3 text-muted">You haven't made any donations yet.</p>
                      <router-link to="/donations/new" class="btn btn-primary">
                        <i class="fas fa-heart me-2"></i>Make Your First Donation
                      </router-link>
                    </div>
                    <div v-else>
                      <div v-for="donation in donations" :key="donation.id" class="mb-3">
                        <div class="d-flex align-items-center p-3 border rounded">
                          <div class="flex-grow-1">
                            <h6 class="mb-1">{{ donation.amount_eth }} ETH</h6>
                            <p class="text-muted mb-2">{{ donation.purpose }}</p>
                            <div class="d-flex gap-2">
                              <span class="badge" :class="getStatusBadgeClass(donation.status)">
                                {{ donation.status }}
                              </span>
                              <small class="text-muted">{{ formatDate(donation.created_at) }}</small>
                            </div>
                          </div>
                          <div class="ms-3">
                            <span class="text-success fw-bold">${{ donation.amount_usd }}</span>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Donor Stats -->
              <div class="col-md-4 mb-4">
                <div class="card border-0 shadow-sm">
                  <div class="card-header bg-white border-0">
                    <h5 class="mb-0">
                      <i class="fas fa-chart-pie me-2 text-primary"></i>
                      Impact Summary
                    </h5>
                  </div>
                  <div class="card-body">
                    <div class="text-center mb-3">
                      <h3 class="fw-bold text-success">${{ totalDonated }}</h3>
                      <p class="text-muted mb-0">Total Donated</p>
                    </div>
                    <div class="d-grid gap-2">
                      <router-link to="/donations/new" class="btn btn-primary">
                        <i class="fas fa-heart me-2"></i>Make Donation
                      </router-link>
                      <router-link to="/impact" class="btn btn-outline-primary">
                        <i class="fas fa-chart-line me-2"></i>View Impact
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
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useCoursesStore } from '../stores/courses'
import { donationsAPI } from '../services/api'

export default {
  name: 'Dashboard',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    const coursesStore = useCoursesStore()

    // State
    const loading = ref(true)
    const error = ref(null)
    const enrolledCourses = ref([])
    const instructorCourses = ref([])
    const donations = ref([])

    // Computed
    const stats = computed(() => {
      if (authStore.isStudent) {
        return [
          {
            title: 'Enrolled Courses',
            value: enrolledCourses.value.length,
            icon: 'fas fa-graduation-cap'
          },
          {
            title: 'Completed Modules',
            value: enrolledCourses.value.reduce((total, enrollment) => 
              total + enrollment.completed_modules.length, 0),
            icon: 'fas fa-check-circle'
          },
          {
            title: 'Average Progress',
            value: enrolledCourses.value.length > 0 
              ? Math.round(enrolledCourses.value.reduce((total, enrollment) => 
                  total + enrollment.progress_percentage, 0) / enrolledCourses.value.length) + '%'
              : '0%',
            icon: 'fas fa-chart-line'
          },
          {
            title: 'Certificates',
            value: enrolledCourses.value.filter(e => e.progress_percentage === 100).length,
            icon: 'fas fa-certificate'
          }
        ]
      } else if (authStore.isInstructor) {
        return [
          {
            title: 'Total Courses',
            value: instructorCourses.value.length,
            icon: 'fas fa-chalkboard'
          },
          {
            title: 'Published',
            value: instructorCourses.value.filter(c => c.is_published).length,
            icon: 'fas fa-check'
          },
          {
            title: 'Drafts',
            value: instructorCourses.value.filter(c => !c.is_published).length,
            icon: 'fas fa-edit'
          },
          {
            title: 'Total Students',
            value: '0', // TODO: Get from backend
            icon: 'fas fa-users'
          }
        ]
      } else if (authStore.isAdmin) {
        return [
          {
            title: 'Total Users',
            value: '0', // TODO: Get from backend
            icon: 'fas fa-users'
          },
          {
            title: 'Total Courses',
            value: '0', // TODO: Get from backend
            icon: 'fas fa-book'
          },
          {
            title: 'Total Donations',
            value: '0', // TODO: Get from backend
            icon: 'fas fa-hand-holding-usd'
          },
          {
            title: 'Schools',
            value: '0', // TODO: Get from backend
            icon: 'fas fa-school'
          }
        ]
      } else if (authStore.isDonor) {
        return [
          {
            title: 'Total Donations',
            value: donations.value.length,
            icon: 'fas fa-heart'
          },
          {
            title: 'Total Amount',
            value: `$${totalDonated.value}`,
            icon: 'fas fa-dollar-sign'
          },
          {
            title: 'Schools Helped',
            value: '0', // TODO: Get from backend
            icon: 'fas fa-school'
          },
          {
            title: 'Impact Score',
            value: '100', // TODO: Calculate
            icon: 'fas fa-star'
          }
        ]
      }
      return []
    })

    const totalDonated = computed(() => {
      return donations.value.reduce((total, donation) => total + donation.amount_usd, 0).toFixed(2)
    })

    // Methods
    const getRoleDescription = () => {
      switch (authStore.user?.role) {
        case 'student': return 'Track your learning progress and explore new courses'
        case 'instructor': return 'Manage your courses and help students learn'
        case 'admin': return 'Manage the platform and ensure smooth operations'
        case 'donor': return 'Make a difference in education through donations'
        case 'school': return 'Request resources and track allocations'
        default: return 'Welcome to the EdTech Hardware Learning Platform'
      }
    }

    const getStatusBadgeClass = (status) => {
      switch (status) {
        case 'confirmed': return 'bg-success'
        case 'pending': return 'bg-warning'
        case 'allocated': return 'bg-info'
        case 'completed': return 'bg-primary'
        default: return 'bg-secondary'
      }
    }

    const formatDate = (dateString) => {
      return new Date(dateString).toLocaleDateString()
    }

    const logout = () => {
      authStore.logout()
      router.push('/login')
    }

    const loadDashboard = async () => {
      loading.value = true
      error.value = null

      try {
        if (authStore.isStudent) {
          await coursesStore.fetchEnrolledCourses()
          enrolledCourses.value = coursesStore.enrolledCourses
        } else if (authStore.isInstructor) {
          await coursesStore.fetchCourses({ instructor_id: authStore.user.id })
          instructorCourses.value = coursesStore.courses
        } else if (authStore.isDonor) {
          const response = await donationsAPI.getDonations()
          donations.value = response.data
        }
      } catch (err) {
        error.value = 'Failed to load dashboard data'
        console.error('Dashboard loading error:', err)
      } finally {
        loading.value = false
      }
    }

    // Lifecycle
    onMounted(() => {
      loadDashboard()
    })

    return {
      loading,
      error,
      enrolledCourses,
      instructorCourses,
      donations,
      stats,
      totalDonated,
      authStore,
      getRoleDescription,
      getStatusBadgeClass,
      formatDate,
      logout,
      loadDashboard
    }
  }
}
</script>

<style scoped>
.dashboard-container {
  min-height: 100vh;
  background-color: #f8f9fa;
}

.card {
  border-radius: 15px;
  transition: transform 0.2s ease;
}

.card:hover {
  transform: translateY(-2px);
}

.progress {
  border-radius: 10px;
}

.progress-bar {
  border-radius: 10px;
}

.badge {
  font-size: 0.75rem;
}

.btn {
  border-radius: 10px;
  font-weight: 500;
}

.btn-sm {
  border-radius: 8px;
}
</style>
