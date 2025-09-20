<template>
  <div class="certificates">
    <div class="container">
      <div class="row">
        <div class="col-md-12">
          <h2>My Certificates</h2>
          <p class="text-muted mb-4">View and download your course completion certificates</p>

          <div v-if="loading" class="text-center py-5">
            <div class="spinner-border" role="status">
              <span class="visually-hidden">Loading...</span>
            </div>
          </div>

          <div v-else>
            <div v-if="certificates.length === 0" class="text-center py-5">
              <i class="fas fa-certificate fa-3x mb-3 text-muted"></i>
              <h4>No Certificates Yet</h4>
              <p class="text-muted">Complete courses to earn certificates</p>
              <router-link to="/courses" class="btn btn-primary">Browse Courses</router-link>
            </div>

            <div v-else class="row">
              <div v-for="certificate in certificates" :key="certificate.id" class="col-md-6 col-lg-4 mb-4">
                <div class="card certificate-card">
                  <div class="card-body text-center">
                    <div class="certificate-icon mb-3">
                      <i class="fas fa-medal text-warning fa-3x"></i>
                    </div>
                    <h5 class="card-title">{{ certificate.course_title }}</h5>
                    <p class="text-muted small">{{ certificate.completion_date }}</p>
                    <div class="certificate-actions">
                      <button class="btn btn-primary btn-sm me-2" @click="viewCertificate(certificate)">
                        <i class="fas fa-eye me-1"></i>View
                      </button>
                      <button class="btn btn-outline-secondary btn-sm" @click="downloadCertificate(certificate)">
                        <i class="fas fa-download me-1"></i>Download
                      </button>
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
  name: 'Certificates',
  data() {
    return {
      loading: true,
      certificates: []
    }
  },
  async mounted() {
    await this.loadCertificates()
  },
  methods: {
    async loadCertificates() {
      try {
        // Mock certificates data
        setTimeout(() => {
          this.certificates = [
            {
              id: 1,
              course_title: 'Introduction to Computer Hardware',
              completion_date: '2024-03-15',
              certificate_url: '#'
            }
          ]
          this.loading = false
        }, 1000)
      } catch (error) {
        console.error('Error loading certificates:', error)
        this.loading = false
      }
    },
    viewCertificate(certificate) {
      alert(`Viewing certificate for: ${certificate.course_title}`)
    },
    downloadCertificate(certificate) {
      alert(`Downloading certificate for: ${certificate.course_title}`)
    }
  }
}
</script>

<style scoped>
.certificates {
  padding: 20px 0;
}

.certificate-card {
  transition: transform 0.2s;
  border: none;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.certificate-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 20px rgba(0,0,0,0.15);
}

.certificate-icon {
  margin-bottom: 15px;
}
</style>
+