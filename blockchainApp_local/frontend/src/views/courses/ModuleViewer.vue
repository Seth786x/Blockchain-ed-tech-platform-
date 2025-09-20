<template>
  <div class="module-viewer">
    <div class="container py-4">
      <!-- Loading State -->
      <div v-if="loading" class="text-center py-5">
        <div class="spinner-border" role="status">
          <span class="visually-hidden">Loading module...</span>
        </div>
      </div>

      <!-- Module Content -->
      <div v-else-if="module && course" class="row">
        <div class="col-lg-9">
          <!-- Module Header -->
          <div class="module-header mb-4">
            <nav aria-label="breadcrumb">
              <ol class="breadcrumb">
                <li class="breadcrumb-item">
                  <router-link to="/courses">Courses</router-link>
                </li>
                <li class="breadcrumb-item">
                  <router-link :to="`/courses/${course._id}`">{{ course.title }}</router-link>
                </li>
                <li class="breadcrumb-item active" aria-current="page">
                  {{ module.title }}
                </li>
              </ol>
            </nav>

            <div class="d-flex justify-content-between align-items-start mb-3">
              <div>
                <h1>{{ module.title }}</h1>
                <p class="lead text-muted">{{ module.description }}</p>
              </div>
              <div class="text-end">
                <div class="badge bg-primary mb-2">
                  <i class="fas fa-clock me-1"></i>
                  {{ module.duration_minutes || 30 }} minutes
                </div>
              </div>
            </div>
          </div>

          <!-- Module Content -->
          <div class="module-content">
            <div class="card">
              <div class="card-body">
                <div v-if="module.content" class="content-area">
                  <!-- Render markdown-style content -->
                  <div v-html="formatModuleContent(module.content)" class="module-text"></div>
                </div>
                <div v-else class="text-center text-muted py-5">
                  <i class="fas fa-file-alt fa-3x mb-3 opacity-25"></i>
                  <p>No content available for this module yet.</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Module Navigation -->
          <div class="module-navigation mt-4">
            <div class="row">
              <div class="col-6">
                <button 
                  v-if="previousModule" 
                  @click="navigateToModule(previousModule._id)"
                  class="btn btn-outline-primary"
                >
                  <i class="fas fa-chevron-left me-2"></i>
                  Previous: {{ previousModule.title }}
                </button>
              </div>
              <div class="col-6 text-end">
                <button 
                  v-if="nextModule" 
                  @click="navigateToModule(nextModule._id)"
                  class="btn btn-primary"
                >
                  Next: {{ nextModule.title }}
                  <i class="fas fa-chevron-right ms-2"></i>
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Sidebar -->
        <div class="col-lg-3">
          <div class="card">
            <div class="card-header">
              <h6><i class="fas fa-list me-2"></i>Course Modules</h6>
            </div>
            <div class="card-body p-0">
              <div class="list-group list-group-flush">
                <div 
                  v-for="(mod, index) in course.modules" 
                  :key="mod._id || index"
                  class="list-group-item list-group-item-action d-flex justify-content-between align-items-center"
                  :class="{ 'active': mod._id === moduleId || index == moduleIndex }"
                  @click="navigateToModuleByIndex(index)"
                  style="cursor: pointer;"
                >
                  <div>
                    <div class="fw-bold small">{{ mod.title }}</div>
                    <small class="text-muted">{{ mod.duration_minutes || 30 }} min</small>
                  </div>
                  <div>
                    <i v-if="mod._id === moduleId || index == moduleIndex" class="fas fa-play-circle text-primary"></i>
                    <span v-else class="badge bg-light text-dark">{{ index + 1 }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Course Info -->
          <div class="card mt-3">
            <div class="card-header">
              <h6><i class="fas fa-info-circle me-2"></i>Course Info</h6>
            </div>
            <div class="card-body">
              <div class="small">
                <div class="mb-2">
                  <strong>Progress:</strong> {{ currentProgress }}% complete
                </div>
                <div class="mb-2">
                  <strong>Level:</strong> {{ course.level }}
                </div>
                <div class="mb-2">
                  <strong>Category:</strong> {{ course.category }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Error State -->
      <div v-else class="text-center py-5">
        <h3>Module not found</h3>
        <p class="text-muted">The requested module could not be found.</p>
        <router-link to="/courses" class="btn btn-primary">
          <i class="fas fa-arrow-left me-2"></i>Back to Courses
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import { onMounted, ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { coursesAPI } from '../../services/api.js'

export default {
  name: 'ModuleViewer',
  setup() {
    const route = useRoute()
    const router = useRouter()
    const loading = ref(true)
    const course = ref(null)
    const module = ref(null)

    const courseId = computed(() => route.params.courseId)
    const moduleId = computed(() => route.params.moduleId)
    const moduleIndex = computed(() => parseInt(route.params.moduleIndex))

    const previousModule = computed(() => {
      if (!course.value || !course.value.modules) return null
      const currentIndex = getCurrentModuleIndex()
      if (currentIndex > 0) {
        return course.value.modules[currentIndex - 1]
      }
      return null
    })

    const nextModule = computed(() => {
      if (!course.value || !course.value.modules) return null
      const currentIndex = getCurrentModuleIndex()
      if (currentIndex < course.value.modules.length - 1) {
        return course.value.modules[currentIndex + 1]
      }
      return null
    })

    const currentProgress = computed(() => {
      if (!course.value || !course.value.modules) return 0
      const currentIndex = getCurrentModuleIndex()
      return Math.round(((currentIndex + 1) / course.value.modules.length) * 100)
    })

    const getCurrentModuleIndex = () => {
      if (!course.value || !course.value.modules) return 0
      
      // If we have a moduleIndex in route, use that
      if (!isNaN(moduleIndex.value)) {
        return moduleIndex.value
      }
      
      // Otherwise find by moduleId
      return course.value.modules.findIndex(mod => 
        mod._id === moduleId.value
      )
    }

    const formatModuleContent = (content) => {
      if (!content) return ''
      
      // Convert markdown-style formatting to HTML
      let formatted = content
        // Headers
        .replace(/^### (.+)$/gm, '<h3>$1</h3>')
        .replace(/^## (.+)$/gm, '<h2>$1</h2>')
        .replace(/^# (.+)$/gm, '<h1>$1</h1>')
        // Bold
        .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
        // Italic
        .replace(/\*(.+?)\*/g, '<em>$1</em>')
        // Code blocks
        .replace(/```[\s\S]*?```/g, '<pre class="bg-light p-3 rounded"><code>$&</code></pre>')
        // Inline code
        .replace(/`(.+?)`/g, '<code class="bg-light px-1 rounded">$1</code>')
        // Line breaks
        .replace(/\n\n/g, '</p><p>')
        // Lists (basic)
        .replace(/^- (.+)$/gm, '<li>$1</li>')
      
      // Wrap in paragraphs
      if (!formatted.includes('<h1>') && !formatted.includes('<h2>')) {
        formatted = '<p>' + formatted + '</p>'
      }
      
      // Fix list wrapping
      formatted = formatted.replace(/(<li>.*<\/li>)/gs, '<ul>$1</ul>')
      
      return formatted
    }

    const fetchCourseAndModule = async () => {
      try {
        loading.value = true
        
        // Fetch course data using the configured API service
        const courseResponse = await coursesAPI.getCourse(courseId.value)
        course.value = courseResponse.data
        
        // Find the specific module
        if (course.value && course.value.modules) {
          let moduleData = null
          
          if (!isNaN(moduleIndex.value)) {
            // Get module by index
            moduleData = course.value.modules[moduleIndex.value]
          } else if (moduleId.value) {
            // Get module by ID
            moduleData = course.value.modules.find(mod => mod._id === moduleId.value)
          }
          
          if (moduleData) {
            module.value = moduleData
          }
        }
      } catch (error) {
        console.error('Error fetching course/module:', error)
      } finally {
        loading.value = false
      }
    }

    const navigateToModule = (modId) => {
      router.push(`/courses/${courseId.value}/module/${modId}`)
    }

    const navigateToModuleByIndex = (index) => {
      router.push(`/courses/${courseId.value}/module/${index}`)
    }

    onMounted(() => {
      fetchCourseAndModule()
    })

    // Watch for route changes
    const unwatchRoute = router.afterEach(() => {
      if (route.name === 'ModuleViewer') {
        fetchCourseAndModule()
      }
    })

    return {
      loading,
      course,
      module,
      moduleId,
      moduleIndex,
      previousModule,
      nextModule,
      currentProgress,
      formatModuleContent,
      navigateToModule,
      navigateToModuleByIndex
    }
  }
}
</script>

<style scoped>
.module-content {
  min-height: 600px;
}

.module-text {
  line-height: 1.7;
  font-size: 1.1rem;
}

.module-text h1 {
  color: #2c3e50;
  border-bottom: 2px solid #3498db;
  padding-bottom: 0.5rem;
  margin-bottom: 1.5rem;
}

.module-text h2 {
  color: #34495e;
  margin-top: 2rem;
  margin-bottom: 1rem;
}

.module-text h3 {
  color: #7f8c8d;
  margin-top: 1.5rem;
  margin-bottom: 0.75rem;
}

.module-text p {
  margin-bottom: 1rem;
  text-align: justify;
}

.module-text ul {
  margin-bottom: 1rem;
}

.module-text li {
  margin-bottom: 0.25rem;
}

.module-text code {
  font-size: 0.9em;
}

.module-text pre {
  overflow-x: auto;
  max-width: 100%;
}

.list-group-item.active {
  background-color: #007bff !important;
  border-color: #007bff !important;
}

.module-navigation .btn {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>
