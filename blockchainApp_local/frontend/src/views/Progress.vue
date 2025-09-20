<template>
  <div class="progress-view">
    <div class="container">
      <div class="row">
        <div class="col-md-12">
          <h2>My Learning Progress</h2>
          <p class="text-muted mb-4">Track your progress across all enrolled courses</p>

          <div v-if="loading" class="text-center py-5">
            <div class="spinner-border" role="status">
              <span class="visually-hidden">Loading...</span>
            </div>
          </div>

          <div v-else>
            <div class="row mb-4">
              <div class="col-md-3">
                <div class="card text-center">
                  <div class="card-body">
                    <h3 class="text-primary">{{ stats.totalCourses }}</h3>
                    <small class="text-muted">Total Courses</small>
                  </div>
                </div>
              </div>
              <div class="col-md-3">
                <div class="card text-center">
                  <div class="card-body">
                    <h3 class="text-success">{{ stats.completedCourses }}</h3>
                    <small class="text-muted">Completed</small>
                  </div>
                </div>
              </div>
              <div class="col-md-3">
                <div class="card text-center">
                  <div class="card-body">
                    <h3 class="text-warning">{{ stats.inProgressCourses }}</h3>
                    <small class="text-muted">In Progress</small>
                  </div>
                </div>
              </div>
              <div class="col-md-3">
                <div class="card text-center">
                  <div class="card-body">
                    <h3 class="text-info">{{ stats.totalHours }}</h3>
                    <small class="text-muted">Total Hours</small>
                  </div>
                </div>
              </div>
            </div>

            <div class="card">
              <div class="card-header">
                <h5>Course Progress</h5>
              </div>
              <div class="card-body">
                <div v-if="courses.length === 0" class="text-center py-4">
                  <p class="text-muted">No enrolled courses yet</p>
                  <router-link to="/courses" class="btn btn-primary">Browse Courses</router-link>
                </div>
                <div v-else>
                  <div v-for="course in courses" :key="course.id" class="course-progress-item mb-4">
                    <div class="d-flex justify-content-between align-items-center mb-2">
                      <h6 class="mb-0">{{ course.title }}</h6>
                      <span class="badge bg-primary">{{ course.progress }}%</span>
                    </div>
                    <div class="progress mb-2" style="height: 8px;">
                      <div 
                        class="progress-bar" 
                        :style="{ width: course.progress + '%' }"
                        role="progressbar"
                      ></div>
                    </div>
                    <div class="d-flex justify-content-between text-muted small">
                      <span>{{ course.completedModules }}/{{ course.totalModules }} modules</span>
                      <span>{{ course.timeSpent }} hours spent</span>
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
export default {
  name: 'Progress',
  data() {
    return {
      loading: true,
      stats: {
        totalCourses: 0,
        completedCourses: 0,
        inProgressCourses: 0,
        totalHours: 0
      },
      courses: []
    }
  },
  async mounted() {
    await this.loadProgress()
  },
  methods: {
    async loadProgress() {
      try {
        // Mock progress data
        setTimeout(() => {
          this.stats = {
            totalCourses: 3,
            completedCourses: 1,
            inProgressCourses: 2,
            totalHours: 24
          }
          this.courses = [
            {
              id: 1,
              title: 'Introduction to Computer Hardware',
              progress: 100,
              completedModules: 8,
              totalModules: 8,
              timeSpent: 12
            },
            {
              id: 2,
              title: 'Advanced Networking Concepts',
              progress: 65,
              completedModules: 5,
              totalModules: 8,
              timeSpent: 8
            },
            {
              id: 3,
              title: 'Cybersecurity Fundamentals',
              progress: 30,
              completedModules: 2,
              totalModules: 7,
              timeSpent: 4
            }
          ]
          this.loading = false
        }, 1000)
      } catch (error) {
        console.error('Error loading progress:', error)
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.progress-view {
  padding: 20px 0;
}

.course-progress-item {
  padding: 15px;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  background: #f8f9fa;
}

.progress {
  border-radius: 4px;
}

.card {
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}
</style>
