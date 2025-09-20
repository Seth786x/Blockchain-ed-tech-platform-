<template>
  <div class="admin-schools">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2>School Management</h2>
      <button class="btn btn-primary" @click="showCreateModal = true">
        <i class="fas fa-plus me-2"></i>Add School
      </button>
    </div>

    <!-- Schools Table -->
    <div class="card">
      <div class="card-header">
        <h5 class="mb-0">All Schools</h5>
      </div>
      <div class="card-body">
        <div class="table-responsive">
          <table class="table table-striped">
            <thead>
              <tr>
                <th>Name</th>
                <th>Address</th>
                <th>Contact</th>
                <th>Status</th>
                <th>Verification</th>
                <th>Created</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="school in schools" :key="school._id">
                <td>{{ school.name }}</td>
                <td>{{ school.address }}</td>
                <td>
                  <div>{{ school.contact_email }}</div>
                  <small class="text-muted">{{ school.contact_phone }}</small>
                </td>
                <td>
                  <span class="badge" :class="school.is_active ? 'bg-success' : 'bg-danger'">
                    {{ school.is_active ? 'Active' : 'Inactive' }}
                  </span>
                </td>
                <td>
                  <span class="badge" :class="getVerificationBadgeClass(school.verification_status)">
                    {{ school.verification_status }}
                  </span>
                </td>
                <td>{{ formatDate(school.created_at) }}</td>
                <td>
                  <button class="btn btn-sm btn-outline-primary me-2" @click="editSchool(school)">
                    <i class="fas fa-edit"></i>
                  </button>
                  <button class="btn btn-sm btn-outline-warning me-2" @click="toggleVerification(school)">
                    <i class="fas fa-check"></i>
                  </button>
                  <button class="btn btn-sm btn-outline-danger" @click="toggleSchoolStatus(school)">
                    <i class="fas fa-ban"></i>
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Create/Edit School Modal -->
    <div class="modal fade" :class="{ show: showCreateModal }" style="display: block;" v-if="showCreateModal">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ editingSchool ? 'Edit School' : 'Create New School' }}</h5>
            <button type="button" class="btn-close" @click="closeModal"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="saveSchool">
              <div class="row">
                <div class="col-md-6">
                  <div class="mb-3">
                    <label class="form-label">School Name</label>
                    <input type="text" class="form-control" v-model="schoolForm.name" required>
                  </div>
                  <div class="mb-3">
                    <label class="form-label">Contact Email</label>
                    <input type="email" class="form-control" v-model="schoolForm.contact_email" required>
                  </div>
                  <div class="mb-3">
                    <label class="form-label">Contact Phone</label>
                    <input type="tel" class="form-control" v-model="schoolForm.contact_phone">
                  </div>
                </div>
                <div class="col-md-6">
                  <div class="mb-3">
                    <label class="form-label">Address</label>
                    <textarea class="form-control" v-model="schoolForm.address" rows="3" required></textarea>
                  </div>
                  <div class="mb-3">
                    <label class="form-label">Website</label>
                    <input type="url" class="form-control" v-model="schoolForm.website">
                  </div>
                </div>
              </div>
              <div class="mb-3">
                <label class="form-label">Description</label>
                <textarea class="form-control" v-model="schoolForm.description" rows="3"></textarea>
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closeModal">Cancel</button>
            <button type="button" class="btn btn-primary" @click="saveSchool">
              {{ editingSchool ? 'Update' : 'Create' }}
            </button>
          </div>
        </div>
      </div>
    </div>
    <div class="modal-backdrop fade show" v-if="showCreateModal"></div>
  </div>
</template>

<script>
import { schoolService } from '../../services/schools'

export default {
  name: 'AdminSchools',
  data() {
    return {
      schools: [],
      showCreateModal: false,
      editingSchool: null,
      schoolForm: {
        name: '',
        address: '',
        contact_email: '',
        contact_phone: '',
        website: '',
        description: ''
      }
    }
  },
  async mounted() {
    await this.loadSchools()
  },
  methods: {
    async loadSchools() {
      try {
        const response = await schoolService.getAllSchools()
        this.schools = response.data
      } catch (error) {
        console.error('Error loading schools:', error)
      }
    },
    getVerificationBadgeClass(status) {
      const classes = {
        verified: 'bg-success',
        pending: 'bg-warning',
        rejected: 'bg-danger'
      }
      return classes[status] || 'bg-secondary'
    },
    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString()
    },
    editSchool(school) {
      this.editingSchool = school
      this.schoolForm = {
        name: school.name,
        address: school.address,
        contact_email: school.contact_email,
        contact_phone: school.contact_phone || '',
        website: school.website || '',
        description: school.description || ''
      }
      this.showCreateModal = true
    },
    async toggleVerification(school) {
      const newStatus = school.verification_status === 'verified' ? 'pending' : 'verified'
      try {
        await schoolService.updateSchool(school._id, { verification_status: newStatus })
        await this.loadSchools()
      } catch (error) {
        console.error('Error updating verification status:', error)
      }
    },
    async toggleSchoolStatus(school) {
      try {
        await schoolService.updateSchool(school._id, { is_active: !school.is_active })
        await this.loadSchools()
      } catch (error) {
        console.error('Error updating school status:', error)
      }
    },
    async saveSchool() {
      try {
        if (this.editingSchool) {
          await schoolService.updateSchool(this.editingSchool._id, this.schoolForm)
        } else {
          await schoolService.createSchool(this.schoolForm)
        }
        await this.loadSchools()
        this.closeModal()
      } catch (error) {
        console.error('Error saving school:', error)
      }
    },
    closeModal() {
      this.showCreateModal = false
      this.editingSchool = null
      this.schoolForm = {
        name: '',
        address: '',
        contact_email: '',
        contact_phone: '',
        website: '',
        description: ''
      }
    }
  }
}
</script>

<style scoped>
.admin-schools {
  padding: 20px;
}

.modal {
  background-color: rgba(0, 0, 0, 0.5);
}

.table th {
  font-weight: 600;
}

.badge {
  font-size: 0.75rem;
}
</style>
