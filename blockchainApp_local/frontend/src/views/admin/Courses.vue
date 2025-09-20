<template>
  <div class="admin-courses">
    <div class="container">
      <div class="row">
        <div class="col-12">
          <div class="d-flex justify-content-between align-items-center mb-4">
            <h2>Course Management</h2>
            <div>
              <router-link to="/courses/create" class="btn btn-primary me-2">
                <i class="fas fa-plus me-2"></i>Create Course
              </router-link>
              <button @click="syncBlockchainPrice" class="btn btn-outline-info" :disabled="syncing">
                <span v-if="syncing" class="spinner-border spinner-border-sm me-2"></span>
                <i v-else class="fab fa-ethereum me-2"></i>
                {{ syncing ? 'Syncing...' : 'Sync Blockchain Price' }}
              </button>
            </div>
          </div>

          <!-- Blockchain Price Management -->
          <div class="card mb-4">
            <div class="card-header">
              <h5><i class="fab fa-ethereum me-2"></i>Blockchain Course Price</h5>
            </div>
            <div class="card-body">
              <div class="row align-items-center">
                <div class="col-md-4">
                  <div class="form-group">
                    <label class="form-label">Current Price (ETH)</label>
                    <div class="input-group">
                      <span class="input-group-text"><i class="fab fa-ethereum"></i></span>
                      <input 
                        type="number" 
                        class="form-control" 
                        v-model="newPrice"
                        step="0.000001"
                        min="0"
                        :disabled="updatingPrice"
                      >
                    </div>
                  </div>
                </div>
                <div class="col-md-4">
                  <div class="form-group">
                    <label class="form-label">Current Blockchain Price</label>
                    <div class="alert alert-info mb-0">
                      <strong>{{ currentBlockchainPrice }} ETH</strong>
                    </div>
                  </div>
                </div>
                <div class="col-md-4">
                  <div class="form-group">
                    <label class="form-label">&nbsp;</label>
                    <div>
                      <button 
                        @click="updateBlockchainPrice" 
                        class="btn btn-warning"
                        :disabled="updatingPrice || !newPrice"
                      >
                        <span v-if="updatingPrice" class="spinner-border spinner-border-sm me-2"></span>
                        <i v-else class="fas fa-sync me-2"></i>
                        {{ updatingPrice ? 'Updating...' : 'Update Price' }}
                      </button>
                    </div>
                  </div>
                </div>
              </div>
              <div v-if="priceUpdateError" class="alert alert-danger mt-3">{{ priceUpdateError }}</div>
              <div v-if="priceUpdateSuccess" class="alert alert-success mt-3">{{ priceUpdateSuccess }}</div>
            </div>
          </div>

          <!-- Courses Table -->
          <div class="card">
            <div class="card-header">
              <h5>All Courses</h5>
            </div>
            <div class="card-body">
              <div class="table-responsive">
                <table class="table table-striped">
                  <thead>
                    <tr>
                      <th>Course</th>
                      <th>Category</th>
                      <th>Difficulty</th>
                      <th>Database Price</th>
                      <th>Published</th>
                      <th>Students</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="course in courses" :key="course._id">
                      <td>
                        <div>
                          <strong>{{ course.title }}</strong>
                          <br>
                          <small class="text-muted">{{ course.description.substring(0, 100) }}...</small>
                        </div>
                      </td>
                      <td>
                        <span class="badge bg-secondary">{{ course.category }}</span>
                      </td>
                      <td>
                        <span 
                          class="badge"
                          :class="{
                            'bg-success': course.difficulty === 'beginner',
                            'bg-warning': course.difficulty === 'intermediate', 
                            'bg-danger': course.difficulty === 'advanced'
                          }"
                        >
                          {{ course.difficulty }}
                        </span>
                      </td>
                      <td>
                        <div class="input-group input-group-sm" style="width: 120px;">
                          <span class="input-group-text">$</span>
                          <input 
                            type="number" 
                            class="form-control" 
                            v-model="course.price"
                            step="0.01"
                            min="0"
                            @change="updateCoursePrice(course)"
                          >
                        </div>
                      </td>
                      <td>
                        <div class="form-check form-switch">
                          <input 
                            class="form-check-input" 
                            type="checkbox" 
                            v-model="course.is_published"
                            @change="togglePublished(course)"
                          >
                        </div>
                      </td>
                      <td>{{ course.enrolled_count || 0 }}</td>
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
                            @click="deleteCourse(course)" 
                            class="btn btn-outline-danger"
                            title="Delete Course"
                          >
                            <i class="fas fa-trash"></i>
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
import { useWeb3ContractStore } from '@/stores/web3-contract'

export default {
  name: 'AdminCourses',
  data() {
    return {
      courses: [],
      loading: true,
      currentBlockchainPrice: '0.000005',
      newPrice: '0.000005',
      updatingPrice: false,
      syncing: false,
      priceUpdateError: '',
      priceUpdateSuccess: ''
    }
  },
  computed: {
    web3Store() {
      return useWeb3ContractStore()
    }
  },
  async mounted() {
    await this.loadCourses()
    await this.loadBlockchainPrice()
  },
  methods: {
    async loadCourses() {
      try {
        const response = await coursesAPI.getCourses()
        this.courses = response.data
      } catch (error) {
        console.error('Error loading courses:', error)
      } finally {
        this.loading = false
      }
    },
    async loadBlockchainPrice() {
      try {
        await this.web3Store.checkConnection()
        this.currentBlockchainPrice = await this.web3Store.getCoursePrice()
        this.newPrice = this.currentBlockchainPrice
      } catch (error) {
        console.error('Error loading blockchain price:', error)
      }
    },
    async updateBlockchainPrice() {
      this.updatingPrice = true
      this.priceUpdateError = ''
      this.priceUpdateSuccess = ''
      
      try {
        await this.web3Store.connectWallet()
        
        // Convert ETH to Wei
        const priceWei = this.web3Store.web3.utils.toWei(this.newPrice.toString(), 'ether')
        
        // Call smart contract to update price (only contract owner can do this)
        await this.web3Store.contract.methods.setCoursePrice(priceWei).send({
          from: this.web3Store.account,
          gas: 100000
        })
        
        this.currentBlockchainPrice = this.newPrice
        this.priceUpdateSuccess = 'Course price updated successfully on blockchain!'
        
        setTimeout(() => {
          this.priceUpdateSuccess = ''
        }, 5000)
        
      } catch (error) {
        console.error('Error updating blockchain price:', error)
        this.priceUpdateError = error.message || 'Failed to update blockchain price. Make sure you are the contract owner.'
      } finally {
        this.updatingPrice = false
      }
    },
    async syncBlockchainPrice() {
      this.syncing = true
      try {
        await this.loadBlockchainPrice()
      } catch (error) {
        console.error('Error syncing price:', error)
      } finally {
        this.syncing = false
      }
    },
    async updateCoursePrice(course) {
      try {
        await coursesAPI.updateCourse(course._id, {
          ...course,
          price: parseFloat(course.price)
        })
        console.log('Course price updated')
      } catch (error) {
        console.error('Error updating course price:', error)
      }
    },
    async togglePublished(course) {
      try {
        await coursesAPI.updateCourse(course._id, {
          ...course,
          is_published: course.is_published
        })
        console.log('Course publication status updated')
      } catch (error) {
        console.error('Error updating course status:', error)
        // Revert on error
        course.is_published = !course.is_published
      }
    },
    async deleteCourse(course) {
      if (confirm(`Are you sure you want to delete "${course.title}"?`)) {
        try {
          await coursesAPI.deleteCourse(course._id)
          this.courses = this.courses.filter(c => c._id !== course._id)
        } catch (error) {
          console.error('Error deleting course:', error)
          alert('Failed to delete course')
        }
      }
    }
  }
}
</script>

<style scoped>
.admin-courses {
  padding: 20px 0;
}

.card {
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
}

.table th {
  border-top: none;
  font-weight: 600;
}

.btn-group-sm > .btn {
  padding: 0.25rem 0.5rem;
}

.form-check-input:checked {
  background-color: #28a745;
  border-color: #28a745;
}

.input-group-sm .input-group-text {
  padding: 0.25rem 0.5rem;
  font-size: 0.875rem;
}

.badge {
  font-size: 0.75rem;
}

.alert {
  border-radius: 0.5rem;
}
</style>
