<template>
  <div>
    <!-- Hero Section -->
    <section class="hero-section py-5" style="background: linear-gradient(135deg, #000000 0%, #667eea 100%); color: white;">
      <div class="container">
        <div class="row align-items-center">
          <div class="col-lg-6">
            <div class="page-header">
              <h1 class="display-4 fw-bold mb-4">
                Learn Computer Hardware with Transparent Impact ⚡
              </h1>
            </div>
            <p class="lead mb-4">
              Master CPU, GPU, RAM, and more through blockchain-verified courses. 
              Your donations directly fund hardware equipment for schools worldwide. 🌍
            </p>
            <div class="d-flex gap-3">
              <router-link to="/courses" class="btn btn-light btn-lg">
                <i class="fas fa-play me-2"></i>Start Learning
              </router-link>
              <router-link to="/donations" class="btn btn-outline-light btn-lg">
                <i class="fas fa-heart me-2"></i>Donate Now
              </router-link>
            </div>
          </div>
          <div class="col-lg-6">
            <div class="text-center position-relative">
              <i class="fas fa-microchip display-1 text-white-50 floating-doodle"></i>
              <div class="position-absolute" style="top: 20px; right: 20px; font-size: 2rem; opacity: 0.3;">🔧</div>
              <div class="position-absolute" style="bottom: 20px; left: 20px; font-size: 1.5rem; opacity: 0.4;">⚙️</div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Stats Section -->
    <section class="py-5">
      <div class="container">
        <div class="section-divider">
          <span>Our Impact</span>
        </div>
        <div class="row text-center">
          <div class="col-md-3 mb-4">
            <div class="card stats-card h-100">
              <div class="card-body">
                <i class="fas fa-graduation-cap text-secondary fs-1 mb-3"></i>
                <h3 class="fw-bold">{{ stats.totalStudents }}</h3>
                <p class="text-muted">Students Enrolled 🎓</p>
              </div>
            </div>
          </div>
          <div class="col-md-3 mb-4">
            <div class="card stats-card h-100">
              <div class="card-body">
                <i class="fab fa-ethereum text-secondary fs-1 mb-3"></i>
                <h3 class="fw-bold">{{ stats.totalDonations }} ETH</h3>
                <p class="text-muted">Total Donations 💎</p>
              </div>
            </div>
          </div>
          <div class="col-md-3 mb-4">
            <div class="card stats-card h-100">
              <div class="card-body">
                <i class="fas fa-school text-secondary fs-1 mb-3"></i>
                <h3 class="fw-bold">{{ stats.schoolsHelped }}</h3>
                <p class="text-muted">Schools Helped 🏫</p>
              </div>
            </div>
          </div>
          <div class="col-md-3 mb-4">
            <div class="card stats-card h-100">
              <div class="card-body">
                <i class="fas fa-laptop text-secondary fs-1 mb-3"></i>
                <h3 class="fw-bold">{{ stats.equipmentDistributed }}</h3>
                <p class="text-muted">Equipment Distributed 💻</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Featured Courses -->
    <section class="py-5" style="background: linear-gradient(135deg, #f8fafc 0%, #ffffff 100%);">
      <div class="container">
        <div class="text-center mb-5">
          <div class="page-header">
            <h2 class="fw-bold">Featured Hardware Courses ⚡</h2>
          </div>
          <p class="lead text-muted">Master computer hardware with hands-on learning 🛠️</p>
        </div>
        
        <div class="row">
          <div class="col-lg-4 mb-4" v-for="course in featuredCourses" :key="course._id">
            <div class="card course-card h-100">
              <div class="card-img-top position-relative" style="height: 200px; overflow: hidden;">
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
                  <i class="fas fa-microchip text-primary" style="font-size: 3rem;"></i>
                </div>
              </div>
              <div class="card-body">
                <div class="d-flex justify-content-between align-items-start mb-2">
                  <span class="badge bg-primary">{{ course.difficulty || 'General' }}</span>
                  <span class="text-muted small">{{ course.duration }}</span>
                </div>
                <h5 class="card-title">{{ course.title }}</h5>
                <p class="card-text text-muted">{{ course.description.substring(0, 100) }}...</p>
                <div class="mb-2">
                  <small class="text-muted">{{ course.category }}</small>
                </div>
                <div class="d-flex justify-content-between align-items-center">
                  <span class="fw-bold text-success">
                    {{ course.price === 0 ? 'Free' : `${course.price} ETH` }}
                  </span>
                  <button 
                    class="btn btn-primary btn-sm"
                    @click="goToCourse(course._id)"
                  >
                    <i class="fas fa-play me-1"></i>Start Course
                  </button>
                </div>
                <div class="mt-2">
                  <small class="text-muted">{{ course.modules?.length || 0 }} modules</small>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="text-center mt-4">
          <router-link to="/courses" class="btn btn-outline-primary btn-lg">
            View All Courses
          </router-link>
        </div>
      </div>
    </section>

    <!-- How It Works -->
    <section class="py-5 bg-light">
      <div class="container">
        <div class="text-center mb-5">
          <h2 class="fw-bold">How It Works</h2>
          <p class="lead text-muted">Transparent education funding through blockchain</p>
        </div>
        
        <div class="row">
          <div class="col-lg-3 mb-4 text-center">
            <div class="bg-primary text-white rounded-circle d-inline-flex align-items-center justify-content-center mb-3" style="width: 80px; height: 80px;">
              <span class="fs-2 fw-bold">1</span>
            </div>
            <h5>Learn Hardware</h5>
            <p class="text-muted">Take courses on CPU, GPU, RAM, and other components</p>
          </div>
          <div class="col-lg-3 mb-4 text-center">
            <div class="bg-primary text-white rounded-circle d-inline-flex align-items-center justify-content-center mb-3" style="width: 80px; height: 80px;">
              <span class="fs-2 fw-bold">2</span>
            </div>
            <h5>Donate Funds</h5>
            <p class="text-muted">Contribute ETH to fund hardware equipment for schools</p>
          </div>
          <div class="col-lg-3 mb-4 text-center">
            <div class="bg-primary text-white rounded-circle d-inline-flex align-items-center justify-content-center mb-3" style="width: 80px; height: 80px;">
              <span class="fs-2 fw-bold">3</span>
            </div>
            <h5>Transparent Allocation</h5>
            <p class="text-muted">Smart contracts ensure funds reach verified schools</p>
          </div>
          <div class="col-lg-3 mb-4 text-center">
            <div class="bg-primary text-white rounded-circle d-inline-flex align-items-center justify-content-center mb-3" style="width: 80px; height: 80px;">
              <span class="fs-2 fw-bold">4</span>
            </div>
            <h5>Track Impact</h5>
            <p class="text-muted">See exactly how your donations help students learn</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Call to Action -->
    <section class="py-5 bg-primary text-white">
      <div class="container text-center">
        <h2 class="fw-bold mb-4">Ready to Make an Impact?</h2>
        <p class="lead mb-4">Join thousands of learners and donors making computer hardware education accessible worldwide.</p>
        <div class="d-flex justify-content-center gap-3">
          <router-link to="/register" class="btn btn-light btn-lg">
            <i class="fas fa-user-plus me-2"></i>Get Started
          </router-link>
          <router-link to="/donations" class="btn btn-outline-light btn-lg">
            <i class="fas fa-heart me-2"></i>Make a Donation
          </router-link>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

export default {
  name: 'Home',
  setup() {
    const router = useRouter()
    
    const stats = ref({
      totalStudents: 12847,
      totalDonations: 156.7,
      schoolsHelped: 89,
      equipmentDistributed: 342
    })

    const featuredCourses = ref([])
    const loading = ref(false)
    const error = ref(null)

    const fetchFeaturedCourses = async () => {
      try {
        loading.value = true
        error.value = null
        
        const response = await fetch('http://localhost:8000/api/courses/featured')
        if (!response.ok) {
          throw new Error('Failed to fetch featured courses')
        }
        
        const courses = await response.json()
        featuredCourses.value = courses
        
      } catch (err) {
        console.error('Error fetching featured courses:', err)
        error.value = err.message
        // Fallback to sample courses if API fails
        featuredCourses.value = [
          {
            _id: 'sample1',
            title: 'CPU Fundamentals',
            description: 'Learn how processors work, from basics to advanced concepts',
            difficulty: 'Beginner',
            duration: '4 hours',
            price: 0,
            category: 'Core Hardware',
            modules: [{}, {}, {}]
          }
        ]
      } finally {
        loading.value = false
      }
    }

    const goToCourse = (courseId) => {
      router.push(`/courses/${courseId}`)
    }

    onMounted(() => {
      fetchFeaturedCourses()
    })

    return {
      stats,
      featuredCourses,
      loading,
      error,
      goToCourse
    }
  }
}
</script>

<style scoped>
.hero-section {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.card {
  transition: transform 0.2s;
}

.card:hover {
  transform: translateY(-5px);
}
</style>
