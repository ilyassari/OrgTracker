<template>
    <div style="min-height: 100vh; display: flex; align-items: center; justify-content: center; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
      <n-card 
        style="width: 600px; max-width: 90vw; text-align: center;"
        :bordered="false"
        size="large"
      >
        <!-- 404 Icon -->
        <div style="margin-bottom: 24px;">
          <n-icon 
            :component="WarningIcon" 
            size="120" 
            style="color: #f5a623;"
          />
        </div>
  
        <!-- Title -->
        <h1 style="margin: 0 0 16px 0; font-size: 72px; color: #333;">404</h1>
        <h2 style="margin: 0 0 16px 0; font-size: 32px; color: #666;">Page Not Found</h2>
        
        <!-- Description -->
        <p style="margin: 0 0 32px 0; font-size: 16px; color: #999;">
          The page you're looking for doesn't exist or has been moved.
        </p>
  
        <!-- Action Buttons -->
        <n-space justify="center" size="large">
          <n-button 
            type="primary" 
            size="large"
            @click="$router.push('/')"
          >
            <template #icon>
              <n-icon :component="HomeIcon" />
            </template>
            Back to Home
          </n-button>
          
          <n-button 
            size="large"
            @click="$router.back()"
          >
            <template #icon>
              <n-icon :component="ArrowBackIcon" />
            </template>
            Go Back
          </n-button>
        </n-space>
  
        <!-- Helpful Links -->
        <n-divider style="margin: 32px 0;" />
        
        <div style="text-align: left;">
          <h3 style="margin: 0 0 16px 0; font-size: 18px; color: #666;">Quick Links</h3>
          <n-space vertical>
            <n-button text type="primary" @click="$router.push('/')">
              Browse Organizations
            </n-button>
            
            <n-button text type="primary" @click="$router.push('/followed')" v-if="isAuthenticated">
              My Followed Organizations
            </n-button>
            
            <n-button text type="primary" @click="$router.push('/profile')" v-if="isAuthenticated">
              My Profile
            </n-button>
            
            <n-button text type="primary" @click="$router.push('/login')" v-if="!isAuthenticated">
              Login
            </n-button>
            
            <n-button text type="primary" @click="$router.push('/register')" v-if="!isAuthenticated">
              Register
            </n-button>
          </n-space>
        </div>
  
        <!-- Search suggestion -->
        <n-card 
          style="margin-top: 32px; background: #f8f9fa;"
          size="small"
        >
          <template #header>
            <span style="font-size: 14px; color: #666;">Looking for something specific?</span>
          </template>
          <div style="font-size: 14px; color: #888;">
            <p style="margin: 0;">
              Try searching for organizations by name, type, or country on our homepage.
            </p>
          </div>
        </n-card>
      </n-card>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import { WarningOutline as WarningIcon, Home as HomeIcon, ArrowBack as ArrowBackIcon } from '@vicons/ionicons5'
  
  const isAuthenticated = ref(false)
  
  const checkAuthStatus = () => {
    const token = localStorage.getItem('token')
    isAuthenticated.value = !!token
  }
  
  onMounted(() => {
    checkAuthStatus()
  })
  </script>
  
  <style scoped>
  .n-card {
    box-shadow: 0 12px 24px rgba(0, 0, 0, 0.1);
  }
  </style>