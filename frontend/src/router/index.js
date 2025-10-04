import { createRouter, createWebHistory } from 'vue-router'

// Import views/components
import OrganizationList from '@/views/OrganizationList.vue'
import OrganizationDetail from '@/views/OrganizationDetail.vue'
import LoginForm from '@/views/auth/LoginForm.vue'
import RegisterForm from '@/views/auth/RegisterForm.vue'
import UserProfile from '@/views/user/UserProfile.vue'
import FollowedOrganizations from '@/views/user/FollowedOrganizations.vue'

const routes = [
  {
    path: '/',
    name: 'OrganizationList',
    component: OrganizationList,
    meta: { 
      title: 'Organizations',
      requiresAuth: false 
    }
  },
  {
    path: '/organizations/:slug',
    name: 'OrganizationDetail',
    component: OrganizationDetail,
    meta: { 
      title: 'Organization Detail',
      requiresAuth: false 
    }
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginForm,
    meta: { 
      title: 'Login',
      requiresAuth: false,
      guestOnly: true // Logged in users shouldn't see login
    }
  },
  {
    path: '/register',
    name: 'Register', 
    component: RegisterForm,
    meta: { 
      title: 'Register',
      requiresAuth: false,
      guestOnly: true
    }
  },
  {
    path: '/profile',
    name: 'UserProfile',
    component: UserProfile,
    meta: { 
      title: 'Profile',
      requiresAuth: true 
    }
  },
  {
    path: '/followed',
    name: 'FollowedOrganizations',
    component: FollowedOrganizations,
    meta: { 
      title: 'Followed Organizations',
      requiresAuth: true 
    }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/NotFound.vue'),
    meta: { title: 'Page Not Found' }
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

// Navigation guard for authentication
router.beforeEach((to, from, next) => {
  // Get auth status from localStorage or store
  const token = localStorage.getItem('token')
  const isAuthenticated = !!token

  // Set document title
  document.title = to.meta.title ? `${to.meta.title} - OrgTracker` : 'OrgTracker'

  // Check if route requires authentication
  if (to.meta.requiresAuth && !isAuthenticated) {
    // Redirect to login if not authenticated
    next({ 
      name: 'Login', 
      query: { redirect: to.fullPath } 
    })
    return
  }

  // Check if route is guest only (login/register)
  if (to.meta.guestOnly && isAuthenticated) {
    // Redirect authenticated users away from login/register
    next({ name: 'OrganizationList' })
    return
  }

  next()
})

export default router