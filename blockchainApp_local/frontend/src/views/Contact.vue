<template>
  <div class="contact">
    <div class="container">
      <div class="row">
        <div class="col-lg-8 mx-auto">
          <div class="text-center mb-5">
            <h1 class="page-title">Contact Us</h1>
            <p class="text-muted">
              Get in touch with our team for support or inquiries
            </p>
          </div>
          
          <div class="row">
            <div class="col-md-8">
              <div class="card">
                <div class="card-body">
                  <h5 class="card-title mb-4">Send us a message</h5>
                  
                  <form @submit.prevent="submitForm">
                    <div class="row">
                      <div class="col-md-6">
                        <div class="mb-3">
                          <label class="form-label">First Name *</label>
                          <input 
                            type="text" 
                            class="form-control" 
                            v-model="form.firstName"
                            required
                          >
                        </div>
                      </div>
                      <div class="col-md-6">
                        <div class="mb-3">
                          <label class="form-label">Last Name *</label>
                          <input 
                            type="text" 
                            class="form-control" 
                            v-model="form.lastName"
                            required
                          >
                        </div>
                      </div>
                    </div>
                    
                    <div class="mb-3">
                      <label class="form-label">Email *</label>
                      <input 
                        type="email" 
                        class="form-control" 
                        v-model="form.email"
                        required
                      >
                    </div>
                    
                    <div class="mb-3">
                      <label class="form-label">Subject *</label>
                      <select class="form-select" v-model="form.subject" required>
                        <option value="">Choose a subject</option>
                        <option value="general">General Inquiry</option>
                        <option value="support">Technical Support</option>
                        <option value="partnership">Partnership</option>
                        <option value="feedback">Feedback</option>
                      </select>
                    </div>
                    
                    <div class="mb-3">
                      <label class="form-label">Message *</label>
                      <textarea 
                        class="form-control" 
                        rows="5" 
                        v-model="form.message"
                        placeholder="Tell us how we can help..."
                        required
                      ></textarea>
                    </div>
                    
                    <button type="submit" class="btn btn-primary" :disabled="isSubmitting">
                      <i class="fas fa-paper-plane me-2"></i>
                      {{ isSubmitting ? 'Sending...' : 'Send Message' }}
                    </button>
                  </form>
                </div>
              </div>
            </div>
            
            <div class="col-md-4">
              <div class="card">
                <div class="card-body">
                  <h5 class="card-title mb-4">Get in Touch</h5>
                  
                  <div class="contact-info">
                    <div class="contact-item mb-3">
                      <i class="fas fa-envelope text-primary me-3"></i>
                      <div>
                        <strong>Email</strong><br>
                        <span class="text-muted">support@edtech.com</span>
                      </div>
                    </div>
                    
                    <div class="contact-item mb-3">
                      <i class="fas fa-phone text-primary me-3"></i>
                      <div>
                        <strong>Phone</strong><br>
                        <span class="text-muted">+1 (555) 123-4567</span>
                      </div>
                    </div>
                    
                    <div class="contact-item mb-3">
                      <i class="fas fa-map-marker-alt text-primary me-3"></i>
                      <div>
                        <strong>Address</strong><br>
                        <span class="text-muted">
                          123 Education St<br>
                          Tech City, TC 12345
                        </span>
                      </div>
                    </div>
                    
                    <div class="contact-item">
                      <i class="fas fa-clock text-primary me-3"></i>
                      <div>
                        <strong>Business Hours</strong><br>
                        <span class="text-muted">
                          Mon - Fri: 9:00 AM - 6:00 PM<br>
                          Sat: 10:00 AM - 4:00 PM
                        </span>
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
  </div>
</template>

<script>
export default {
  name: 'Contact',
  data() {
    return {
      form: {
        firstName: '',
        lastName: '',
        email: '',
        subject: '',
        message: ''
      },
      isSubmitting: false
    }
  },
  methods: {
    async submitForm() {
      this.isSubmitting = true
      
      try {
        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 1000))
        
        // Reset form
        this.form = {
          firstName: '',
          lastName: '',
          email: '',
          subject: '',
          message: ''
        }
        
        alert('Message sent successfully! We will get back to you soon.')
      } catch (error) {
        alert('Error sending message. Please try again.')
      } finally {
        this.isSubmitting = false
      }
    }
  }
}
</script>

<style scoped>
.contact {
  padding: 40px 0;
}

.page-title {
  color: #2c3e50;
  font-weight: 600;
  margin-bottom: 20px;
}

.contact-item {
  display: flex;
  align-items: flex-start;
}

.contact-item i {
  font-size: 1.2em;
  width: 30px;
  margin-top: 5px;
}

.card {
  border: none;
  box-shadow: 0 0 20px rgba(0,0,0,0.1);
  border-radius: 10px;
}

.btn-primary {
  border-radius: 25px;
  padding: 10px 30px;
}
</style>
