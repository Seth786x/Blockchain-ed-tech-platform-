<template>
  <div class="edit-course">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-8">
          <div class="card">
            <div class="card-header d-flex justify-content-between align-items-center">
              <h3>Edit Course</h3>
              <button class="btn btn-outline-danger btn-sm" @click="deleteCourse" v-if="course._id">
                <i class="fas fa-trash me-2"></i>Delete Course
              </button>
            </div>
            <div class="card-body">
              <div v-if="loading" class="text-center py-4">
                <div class="spinner-border" role="status">
                  <span class="visually-hidden">Loading...</span>
                </div>
              </div>

              <form v-else @submit.prevent="submitCourse">
                <div class="mb-3">
                  <label class="form-label">Course Title</label>
                  <input 
                    type="text" 
                    class="form-control" 
                    v-model="course.title" 
                    required
                    placeholder="Enter course title"
                  >
                </div>

                <div class="mb-3">
                  <label class="form-label">Description</label>
                  <textarea 
                    class="form-control" 
                    v-model="course.description" 
                    rows="4" 
                    required
                    placeholder="Enter course description"
                  ></textarea>
                </div>

                <div class="row">
                  <div class="col-md-6">
                    <div class="mb-3">
                      <label class="form-label">Category</label>
                      <select class="form-select" v-model="course.category" required>
                        <option value="">Select category</option>
                        <option value="computer_hardware">Computer Hardware</option>
                        <option value="networking">Networking</option>
                        <option value="programming">Programming</option>
                        <option value="cybersecurity">Cybersecurity</option>
                        <option value="data_science">Data Science</option>
                      </select>
                    </div>
                  </div>
                  <div class="col-md-6">
                    <div class="mb-3">
                      <label class="form-label">Difficulty Level</label>
                      <select class="form-select" v-model="course.level" required>
                        <option value="">Select level</option>
                        <option value="beginner">Beginner</option>
                        <option value="intermediate">Intermediate</option>
                        <option value="advanced">Advanced</option>
                      </select>
                    </div>
                  </div>
                </div>

                <div class="row">
                  <div class="col-md-6">
                    <div class="mb-3">
                      <label class="form-label">Duration (hours)</label>
                      <input 
                        type="number" 
                        class="form-control" 
                        v-model="course.duration_hours" 
                        min="1"
                        required
                        placeholder="Enter duration in hours"
                      >
                    </div>
                  </div>
                  <div class="col-md-6">
                    <div class="mb-3">
                      <label class="form-label">Hardware Component</label>
                      <select class="form-select" v-model="course.hardware_component">
                        <option value="">Select component (optional)</option>
                        <option value="cpu">CPU</option>
                        <option value="gpu">GPU</option>
                        <option value="motherboard">Motherboard</option>
                        <option value="ram">RAM</option>
                        <option value="storage">Storage</option>
                        <option value="power_supply">Power Supply</option>
                        <option value="cooling">Cooling</option>
                        <option value="network_card">Network Card</option>
                      </select>
                    </div>
                  </div>
                </div>

                <div class="mb-3">
                  <label class="form-label">Prerequisites</label>
                  <textarea 
                    class="form-control" 
                    v-model="course.prerequisites" 
                    rows="2"
                    placeholder="Enter any prerequisites for this course"
                  ></textarea>
                </div>

                <div class="mb-3">
                  <label class="form-label">Learning Objectives</label>
                  <textarea 
                    class="form-control" 
                    v-model="course.learning_objectives" 
                    rows="3"
                    placeholder="Enter what students will learn"
                  ></textarea>
                </div>

                <div class="mb-3">
                  <div class="form-check">
                    <input 
                      class="form-check-input" 
                      type="checkbox" 
                      v-model="course.is_published"
                      id="publishCourse"
                    >
                    <label class="form-check-label" for="publishCourse">
                      Course is published
                    </label>
                  </div>
                </div>

                <div class="d-flex justify-content-between">
                  <button type="button" class="btn btn-secondary" @click="goBack">
                    Cancel
                  </button>
                  <button type="submit" class="btn btn-primary" :disabled="isSubmitting">
                    <span v-if="isSubmitting" class="spinner-border spinner-border-sm me-2"></span>
                    {{ isSubmitting ? 'Updating...' : 'Update Course' }}
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { coursesAPI } from '../../services/api'

export default {
  name: 'EditCourse',
  data() {
    return {
      course: {
        _id: '',
        title: '',
        description: '',
        category: '',
        level: '',
        duration_hours: null,
        hardware_component: '',
        prerequisites: '',
        learning_objectives: '',
        is_published: false
      },
      loading: true,
      isSubmitting: false
    }
  },
  async mounted() {
    await this.loadCourse()
  },
  methods: {
    async loadCourse() {
      try {
        const courseId = this.$route.params.id
        const response = await coursesAPI.getCourse(courseId)
        this.course = { ...response.data }
      } catch (error) {
        console.error('Error loading course:', error)
        alert('Error loading course data.')
        this.$router.push('/courses')
      } finally {
        this.loading = false
      }
    },
    async submitCourse() {
      this.isSubmitting = true
      try {
        const response = await coursesAPI.updateCourse(this.course._id, this.course)
        console.log('Course updated:', response.data)
        
        // Redirect to course detail
        this.$router.push(`/courses/${this.course._id}`)
        
        // Show success message
        alert('Course updated successfully!')
      } catch (error) {
        console.error('Error updating course:', error)
        alert('Error updating course. Please try again.')
      } finally {
        this.isSubmitting = false
      }
    },
    async deleteCourse() {
      if (confirm('Are you sure you want to delete this course? This action cannot be undone.')) {
        try {
          await coursesAPI.deleteCourse(this.course._id)
          alert('Course deleted successfully!')
          this.$router.push('/courses')
        } catch (error) {
          console.error('Error deleting course:', error)
          alert('Error deleting course. Please try again.')
        }
      }
    },
    goBack() {
      this.$router.go(-1)
    }
  }
}
</script>

<style scoped>
.edit-course {
  padding: 20px 0;
}

.card {
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
}

.form-label {
  font-weight: 600;
  color: #333;
}

.form-control:focus,
.form-select:focus {
  border-color: #0d6efd;
  box-shadow: 0 0 0 0.2rem rgba(13, 110, 253, 0.25);
}

.btn-primary {
  background-color: #0d6efd;
  border-color: #0d6efd;
}

.btn-primary:hover {
  background-color: #0b5ed7;
  border-color: #0a58ca;
}

.spinner-border-sm {
  width: 1rem;
  height: 1rem;
}

.btn-outline-danger:hover {
  background-color: #dc3545;
  border-color: #dc3545;
}
</style>
