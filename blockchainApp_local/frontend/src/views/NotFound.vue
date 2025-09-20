<template>
  <div class="not-found">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-6 text-center">
          <div class="error-content">
            <h1 class="display-1 text-primary">404</h1>
            <h2>Page Not Found</h2>
            <p class="text-muted mb-4">
              The page you're looking for doesn't exist or has been moved.
            </p>
            <div class="d-flex justify-content-center gap-3">
              <router-link to="/" class="btn btn-primary">
                <i class="fas fa-home me-2"></i>Go Home
              </router-link>
              <button class="btn btn-outline-secondary" @click="goBack">
                <i class="fas fa-arrow-left me-2"></i>Go Back
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'NotFound',
  methods: {
    goBack() {
      this.$router.go(-1)
    }
  }
}
</script>

<style scoped>
.not-found {
  padding: 100px 0;
  min-height: 50vh;
}

.error-content {
  padding: 40px 20px;
}

.display-1 {
  font-size: 6rem;
  font-weight: 700;
  line-height: 1.2;
}
</style>
