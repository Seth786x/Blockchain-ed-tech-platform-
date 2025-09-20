<template>
  <div class="admin-users">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2>User Management</h2>
      <button class="btn btn-primary" @click="showCreateModal = true">
        <i class="fas fa-plus me-2"></i>Add User
      </button>
    </div>

    <!-- Users Table -->
    <div class="card">
      <div class="card-header">
        <h5 class="mb-0">All Users</h5>
      </div>
      <div class="card-body">
        <div class="table-responsive">
          <table class="table table-striped">
            <thead>
              <tr>
                <th>Name</th>
                <th>Email</th>
                <th>Role</th>
                <th>Status</th>
                <th>Created</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="user in users" :key="user._id">
                <td>{{ user.full_name }}</td>
                <td>{{ user.email }}</td>
                <td>
                  <span class="badge" :class="getRoleBadgeClass(user.role)">
                    {{ user.role }}
                  </span>
                </td>
                <td>
                  <span class="badge" :class="user.is_active ? 'bg-success' : 'bg-danger'">
                    {{ user.is_active ? 'Active' : 'Inactive' }}
                  </span>
                </td>
                <td>{{ formatDate(user.created_at) }}</td>
                <td>
                  <button class="btn btn-sm btn-outline-primary me-2" @click="editUser(user)">
                    <i class="fas fa-edit"></i>
                  </button>
                  <button class="btn btn-sm btn-outline-danger" @click="toggleUserStatus(user)">
                    <i class="fas fa-ban"></i>
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Create/Edit User Modal -->
    <div class="modal fade" :class="{ show: showCreateModal }" style="display: block;" v-if="showCreateModal">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ editingUser ? 'Edit User' : 'Create New User' }}</h5>
            <button type="button" class="btn-close" @click="closeModal"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="saveUser">
              <div class="mb-3">
                <label class="form-label">Full Name</label>
                <input type="text" class="form-control" v-model="userForm.full_name" required>
              </div>
              <div class="mb-3">
                <label class="form-label">Email</label>
                <input type="email" class="form-control" v-model="userForm.email" required>
              </div>
              <div class="mb-3">
                <label class="form-label">Role</label>
                <select class="form-select" v-model="userForm.role" required>
                  <option value="student">Student</option>
                  <option value="instructor">Instructor</option>
                  <option value="admin">Admin</option>
                  <option value="donor">Donor</option>
                  <option value="school_admin">School Admin</option>
                </select>
              </div>
              <div class="mb-3" v-if="!editingUser">
                <label class="form-label">Password</label>
                <input type="password" class="form-control" v-model="userForm.password" required>
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closeModal">Cancel</button>
            <button type="button" class="btn btn-primary" @click="saveUser">
              {{ editingUser ? 'Update' : 'Create' }}
            </button>
          </div>
        </div>
      </div>
    </div>
    <div class="modal-backdrop fade show" v-if="showCreateModal"></div>
  </div>
</template>

<script>
import { authService } from '../../services/auth'

export default {
  name: 'AdminUsers',
  data() {
    return {
      users: [],
      showCreateModal: false,
      editingUser: null,
      userForm: {
        full_name: '',
        email: '',
        role: 'student',
        password: ''
      }
    }
  },
  async mounted() {
    await this.loadUsers()
  },
  methods: {
    async loadUsers() {
      try {
        const response = await authService.getAllUsers()
        this.users = response.data
      } catch (error) {
        console.error('Error loading users:', error)
      }
    },
    getRoleBadgeClass(role) {
      const classes = {
        admin: 'bg-danger',
        instructor: 'bg-warning',
        student: 'bg-primary',
        donor: 'bg-success',
        school_admin: 'bg-info'
      }
      return classes[role] || 'bg-secondary'
    },
    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString()
    },
    editUser(user) {
      this.editingUser = user
      this.userForm = {
        full_name: user.full_name,
        email: user.email,
        role: user.role,
        password: ''
      }
      this.showCreateModal = true
    },
    async toggleUserStatus(user) {
      try {
        await authService.updateUser(user._id, { is_active: !user.is_active })
        await this.loadUsers()
      } catch (error) {
        console.error('Error updating user status:', error)
      }
    },
    async saveUser() {
      try {
        if (this.editingUser) {
          await authService.updateUser(this.editingUser._id, this.userForm)
        } else {
          await authService.createUser(this.userForm)
        }
        await this.loadUsers()
        this.closeModal()
      } catch (error) {
        console.error('Error saving user:', error)
      }
    },
    closeModal() {
      this.showCreateModal = false
      this.editingUser = null
      this.userForm = {
        full_name: '',
        email: '',
        role: 'student',
        password: ''
      }
    }
  }
}
</script>

<style scoped>
.admin-users {
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
