<template>
  <div class="course-viewer">
    <div class="container-fluid">
      <div class="row">
        <!-- Course Navigation Sidebar -->
        <div class="col-lg-3 col-md-4">
          <div class="card sticky-top" style="top: 20px;">
            <div class="card-header">
              <h6>{{ course.title }}</h6>
              <div class="progress" style="height: 5px;">
                <div 
                  class="progress-bar" 
                  :style="{ width: progress + '%' }"
                ></div>
              </div>
              <small class="text-muted">{{ progress.toFixed(0) }}% Complete</small>
            </div>
            <div class="card-body p-0">
              <div class="list-group list-group-flush">
                <div 
                  v-for="(module, index) in course.modules" 
                  :key="module._id || index"
                  class="list-group-item list-group-item-action"
                  :class="{ 
                    'active': currentModuleIndex === index,
                    'completed': module.completed 
                  }"
                  @click="selectModule(index)"
                  style="cursor: pointer;"
                >
                  <div class="d-flex justify-content-between align-items-start">
                    <div>
                      <h6 class="mb-1">{{ module.title }}</h6>
                      <small class="text-muted">
                        <i class="fas fa-clock me-1"></i>
                        {{ module.duration_minutes || 30 }} min
                      </small>
                    </div>
                    <div>
                      <i 
                        v-if="module.completed" 
                        class="fas fa-check-circle text-success"
                      ></i>
                      <i 
                        v-else-if="currentModuleIndex === index" 
                        class="fas fa-play-circle text-primary"
                      ></i>
                      <i 
                        v-else 
                        class="far fa-circle text-muted"
                      ></i>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div class="card-footer">
              <router-link :to="`/courses/${$route.params.id}`" class="btn btn-outline-secondary btn-sm">
                <i class="fas fa-arrow-left me-1"></i>Back to Course
              </router-link>
            </div>
          </div>
        </div>

        <!-- Main Content Area -->
        <div class="col-lg-9 col-md-8">
          <div class="card">
            <div class="card-header d-flex justify-content-between align-items-center">
              <div>
                <h5>{{ currentModule.title }}</h5>
                <small class="text-muted">Module {{ currentModuleIndex + 1 }} of {{ course.modules.length }}</small>
              </div>
              <div class="btn-group">
                <button 
                  class="btn btn-outline-secondary btn-sm" 
                  @click="previousModule"
                  :disabled="currentModuleIndex === 0"
                >
                  <i class="fas fa-chevron-left"></i>
                </button>
                <button 
                  class="btn btn-outline-secondary btn-sm" 
                  @click="nextModule"
                  :disabled="currentModuleIndex === course.modules.length - 1"
                >
                  <i class="fas fa-chevron-right"></i>
                </button>
              </div>
            </div>
            <div class="card-body">
              <!-- Module Content -->
              <div class="module-content">
                <p class="lead">{{ currentModule.description }}</p>
                
                <!-- Render Markdown Content -->
                <div v-if="currentModule.content" class="content-area">
                  <div v-html="renderMarkdown(currentModule.content)"></div>
                </div>
                
                <div v-else class="text-center text-muted py-5">
                  <i class="fas fa-file-alt fa-3x mb-3 opacity-25"></i>
                  <p>Content is being prepared for this module.</p>
                </div>
              </div>
            </div>
            <div class="card-footer">
              <div class="d-flex justify-content-between align-items-center">
                <button 
                  v-if="!currentModule.completed"
                  @click="markCompleted"
                  class="btn btn-success"
                  :disabled="markingComplete"
                >
                  <span v-if="markingComplete" class="spinner-border spinner-border-sm me-2"></span>
                  <i v-else class="fas fa-check me-2"></i>
                  {{ markingComplete ? 'Marking Complete...' : 'Mark as Completed' }}
                </button>
                <span v-else class="badge bg-success">
                  <i class="fas fa-check me-1"></i>Completed
                </span>
                
                <div>
                  <button 
                    class="btn btn-outline-primary me-2" 
                    @click="previousModule"
                    :disabled="currentModuleIndex === 0"
                  >
                    <i class="fas fa-chevron-left me-1"></i>Previous
                  </button>
                  <button 
                    class="btn btn-primary" 
                    @click="nextModule"
                    :disabled="currentModuleIndex === course.modules.length - 1"
                  >
                    Next<i class="fas fa-chevron-right ms-1"></i>
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- Course Certificate -->
          <div v-if="progress === 100" class="card mt-4 border-success">
            <div class="card-body text-center">
              <h4 class="text-success mb-3">
                <i class="fas fa-trophy me-2"></i>Course Completed!
              </h4>
              <p class="mb-3">Congratulations! You have successfully completed this course.</p>
              <button class="btn btn-success btn-lg" @click="generateCertificate">
                <i class="fas fa-download me-2"></i>Download Certificate
              </button>
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
import { useWeb3ContractStore } from '@/stores/web3-contract'

export default {
  name: 'CourseViewer',
  data() {
    return {
      course: null,
      loading: true,
      currentModuleIndex: 0,
      markingComplete: false,
      isPurchased: false,
      enrollmentStatus: null
    }
  },
  computed: {
    currentModule() {
      return this.course?.modules?.[this.currentModuleIndex] || {}
    },
    progress() {
      if (!this.course?.modules?.length) return 0
      const completed = this.course.modules.filter(m => m.completed).length
      return (completed / this.course.modules.length) * 100
    },
    web3Store() {
      return useWeb3ContractStore()
    }
  },
  async mounted() {
    await this.loadCourse()
    await this.checkAccess()
  },
  methods: {
    async loadCourse() {
      try {
        const courseId = this.$route.params.id
        const response = await coursesAPI.getCourse(courseId)
        this.course = response.data
        
        // Initialize completion status (this should come from backend)
        this.course.modules = this.course.modules.map(module => ({
          ...module,
          completed: false // This should be fetched from user progress
        }))
      } catch (error) {
        console.error('Error loading course:', error)
        this.$router.push('/courses')
      } finally {
        this.loading = false
      }
    },
    async checkAccess() {
      try {
        // Check if user has purchased the course on blockchain
        await this.web3Store.checkConnection()
        this.isPurchased = await this.web3Store.hasPurchased(this.$route.params.id)
        
        if (!this.isPurchased) {
          alert('You need to purchase this course first!')
          this.$router.push(`/courses/${this.$route.params.id}`)
        }
      } catch (error) {
        console.error('Error checking access:', error)
      }
    },
    selectModule(index) {
      this.currentModuleIndex = index
    },
    nextModule() {
      if (this.currentModuleIndex < this.course.modules.length - 1) {
        this.currentModuleIndex++
      }
    },
    previousModule() {
      if (this.currentModuleIndex > 0) {
        this.currentModuleIndex--
      }
    },
    async markCompleted() {
      this.markingComplete = true
      try {
        // Mark module as completed
        this.course.modules[this.currentModuleIndex].completed = true
        
        // Here you would typically call an API to save progress
        // await coursesAPI.markModuleCompleted(this.course._id, this.currentModule._id)
        
        // Auto advance to next module if not the last one
        if (this.currentModuleIndex < this.course.modules.length - 1) {
          setTimeout(() => {
            this.nextModule()
          }, 1000)
        }
      } catch (error) {
        console.error('Error marking module complete:', error)
        alert('Failed to save progress. Please try again.')
      } finally {
        this.markingComplete = false
      }
    },
    renderMarkdown(content) {
      // Simple markdown rendering - you could use a library like marked.js
      if (!content) return ''
      
      return content
        .replace(/^# (.*$)/gim, '<h1>$1</h1>')
        .replace(/^## (.*$)/gim, '<h2>$1</h2>')
        .replace(/^### (.*$)/gim, '<h3>$1</h3>')
        .replace(/^\*\*(.*)\*\*/gim, '<strong>$1</strong>')
        .replace(/^\*(.*)\*/gim, '<em>$1</em>')
        .replace(/^\- (.*$)/gim, '<li>$1</li>')
        .replace(/\n/g, '<br>')
    },
    generateCertificate() {
      // Generate and download course completion certificate
      alert('Certificate generation feature coming soon!')
    }
  }
}
</script>

<style scoped>
.course-viewer {
  padding: 20px 0;
  min-height: 100vh;
  background-color: #f8f9fa;
}

.list-group-item.active {
  background-color: #0d6efd;
  border-color: #0d6efd;
}

.list-group-item.completed {
  background-color: #d4edda;
  border-color: #c3e6cb;
}

.list-group-item:hover {
  background-color: #f8f9fa;
}

.content-area {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
  line-height: 1.6;
  font-size: 16px;
}

.content-area h1 {
  font-size: 2rem;
  margin-bottom: 1rem;
  color: #2c3e50;
  border-bottom: 2px solid #3498db;
  padding-bottom: 0.5rem;
}

.content-area h2 {
  font-size: 1.5rem;
  margin-top: 2rem;
  margin-bottom: 1rem;
  color: #34495e;
}

.content-area h3 {
  font-size: 1.25rem;
  margin-top: 1.5rem;
  margin-bottom: 0.75rem;
  color: #34495e;
}

.content-area p {
  margin-bottom: 1rem;
}

.content-area li {
  margin-bottom: 0.5rem;
  list-style: none;
  position: relative;
  padding-left: 1.5rem;
}

.content-area li:before {
  content: "•";
  color: #3498db;
  font-weight: bold;
  position: absolute;
  left: 0;
}

.sticky-top {
  position: sticky !important;
}

.card {
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
}

.module-content {
  max-height: 70vh;
  overflow-y: auto;
}

.progress {
  border-radius: 10px;
}

.badge {
  font-size: 0.875rem;
}
</style>
