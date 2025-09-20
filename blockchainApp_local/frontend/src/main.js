import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createRouter, createWebHistory } from 'vue-router'

// Import components
import App from './App.vue'
import Home from './views/Home.vue'
import Login from './views/Login.vue'
import Register from './views/Register.vue'
import Dashboard from './views/Dashboard.vue'
import Courses from './views/Courses.vue'
import Donations from './views/Donations.vue'
import Schools from './views/Schools.vue'

// Import stores
import { useAuthStore } from './stores/auth'

// Import styles
import 'bootstrap/dist/css/bootstrap.min.css'
import '@fortawesome/fontawesome-free/css/all.min.css'
import './style.css'

// Create router
const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home,
      meta: { requiresAuth: false }
    },
    {
      path: '/login',
      name: 'Login',
      component: Login,
      meta: { requiresAuth: false }
    },
    {
      path: '/register',
      name: 'Register',
      component: Register,
      meta: { requiresAuth: false }
    },
    {
      path: '/dashboard',
      name: 'Dashboard',
      component: Dashboard,
      meta: { requiresAuth: true }
    },
    {
      path: '/courses',
      name: 'Courses',
      component: Courses,
      meta: { requiresAuth: false }
    },
    {
      path: '/donations',
      name: 'Donations',
      component: Donations,
      meta: { requiresAuth: false }
    },
    {
      path: '/schools',
      name: 'Schools',
      component: Schools,
      meta: { requiresAuth: false }
    },
    // Admin routes
    {
      path: '/admin/dashboard',
      name: 'AdminDashboard',
      component: Dashboard,
      meta: { requiresAuth: true, requiresAdmin: true }
    },
    {
      path: '/admin/courses',
      name: 'AdminCourses',
      component: () => import('./views/admin/Courses.vue'),
      meta: { requiresAuth: true, requiresAdmin: true }
    },
    {
      path: '/admin/users',
      name: 'AdminUsers',
      component: () => import('./views/admin/Users.vue'),
      meta: { requiresAuth: true, requiresAdmin: true }
    },
    {
      path: '/admin/schools',
      name: 'AdminSchools',
      component: () => import('./views/admin/Schools.vue'),
      meta: { requiresAuth: true, requiresAdmin: true }
    },
    {
      path: '/admin/donations',
      name: 'AdminDonations',
      component: () => import('./views/admin/Donations.vue'),
      meta: { requiresAuth: true, requiresAdmin: true }
    },
    // Instructor routes
    {
      path: '/instructor/dashboard',
      name: 'InstructorDashboard',
      component: () => import('./views/instructor/Dashboard.vue'),
      meta: { requiresAuth: true, requiresInstructor: true }
    },
    // Course routes
    {
      path: '/courses/create',
      name: 'CreateCourse',
      component: () => import('./views/courses/CreateCourse.vue'),
      meta: { requiresAuth: true, requiresInstructorOrAdmin: true }
    },
    {
      path: '/courses/:id',
      name: 'CourseDetail',
      component: () => import('./views/courses/CourseDetail.vue'),
      meta: { requiresAuth: false }
    },
    {
      path: '/courses/:id/edit',
      name: 'EditCourse',
      component: () => import('./views/courses/EditCourse.vue'),
      meta: { requiresAuth: true, requiresInstructorOrAdmin: true }
    },
    {
      path: '/courses/:id/learn',
      name: 'CourseViewer',
      component: () => import('./views/courses/CourseViewer.vue'),
      meta: { requiresAuth: true, requiresPurchase: true }
    },
    {
      path: '/courses/:courseId/module/:moduleIndex',
      name: 'ModuleViewer',
      component: () => import('./views/courses/ModuleViewer.vue'),
      meta: { requiresAuth: false }
    },
    {
      path: '/courses/create',
      name: 'CreateCourse',
      component: () => import('./views/courses/CreateCourse.vue'),
      meta: { requiresAuth: true, requiresInstructor: true }
    },
    {
      path: '/courses/:id/edit',
      name: 'EditCourse',
      component: () => import('./views/courses/EditCourse.vue'),
      meta: { requiresAuth: true, requiresInstructor: true }
    },
    // Student routes
    {
      path: '/courses/:id',
      name: 'CourseDetail',
      component: () => import('./views/courses/CourseDetail.vue'),
      meta: { requiresAuth: false }
    },
    {
      path: '/certificates',
      name: 'Certificates',
      component: () => import('./views/Certificates.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/progress',
      name: 'Progress',
      component: () => import('./views/Progress.vue'),
      meta: { requiresAuth: true }
    },
    // Donor routes
    {
      path: '/donor/dashboard',
      name: 'DonorDashboard',
      component: Dashboard,
      meta: { requiresAuth: true, requiresDonor: true }
    },
    {
      path: '/donations/new',
      name: 'NewDonation',
      component: () => import('./views/donations/NewDonation.vue'),
      meta: { requiresAuth: true, requiresDonor: true }
    },
    {
      path: '/donations/blockchain',
      name: 'BlockchainDonation',
      component: () => import('./views/BlockchainDonation.vue'),
      meta: { requiresAuth: false }
    },
    // School routes
    {
      path: '/school/dashboard',
      name: 'SchoolDashboard',
      component: Dashboard,
      meta: { requiresAuth: true, requiresSchool: true }
    },
    // Profile and settings
    {
      path: '/profile',
      name: 'Profile',
      component: () => import('./views/Profile.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/settings',
      name: 'Settings',
      component: () => import('./views/Settings.vue'),
      meta: { requiresAuth: true }
    },
    // Catch all route
    {
      path: '/:pathMatch(.*)*',
      name: 'NotFound',
      component: () => import('./views/NotFound.vue')
    }
  ]
})

// Navigation guards
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()
  
  // Initialize auth if not already done
  if (!authStore.isAuthenticated && localStorage.getItem('auth_token')) {
    await authStore.initAuth()
  }

  // Check if route requires authentication
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login')
    return
  }

  // Check role-based access
  if (to.meta.requiresAdmin && !authStore.isAdmin) {
    next('/dashboard')
    return
  }

  if (to.meta.requiresInstructor && !authStore.isInstructor) {
    next('/dashboard')
    return
  }

  if (to.meta.requiresInstructorOrAdmin && !authStore.isInstructor && !authStore.isAdmin) {
    next('/dashboard')
    return
  }

  if (to.meta.requiresSchool && !authStore.isSchool) {
    next('/dashboard')
    return
  }

  if (to.meta.requiresDonor && !authStore.isDonor) {
    next('/dashboard')
    return
  }

  if (to.meta.requiresDonor && !authStore.isDonor) {
    next('/dashboard')
    return
  }

  if (to.meta.requiresSchool && !authStore.isSchool) {
    next('/dashboard')
    return
  }

  // Redirect authenticated users away from login/register
  if (authStore.isAuthenticated && (to.name === 'Login' || to.name === 'Register')) {
    next('/dashboard')
    return
  }

  next()
})

// Create app
const app = createApp(App)

// Use plugins
app.use(createPinia())
app.use(router)

// Mount app
app.mount('#app')

// Import Bootstrap JS
import 'bootstrap/dist/js/bootstrap.bundle.min.js'