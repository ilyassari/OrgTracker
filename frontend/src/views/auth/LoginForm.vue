<template>
    <div style="min-height: 100vh; display: flex; align-items: center; justify-content: center; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
      <n-card 
        title="Login to OrgTracker"
        style="width: 400px; max-width: 90vw;"
        :bordered="false"
        size="large"
      >
        <template #header-extra>
          <n-button text @click="$router.push('/')">
            ← Back to Organizations
          </n-button>
        </template>
  
        <n-form
          ref="formRef"
          :model="formData"
          :rules="rules"
          @submit.prevent="handleSubmit"
        >
          <n-form-item path="username" label="Username">
            <n-input
              v-model:value="formData.username"
              placeholder="Enter your username"
              size="large"
              @keydown.enter.prevent="handleSubmit"
            />
          </n-form-item>
  
          <n-form-item path="password" label="Password">
            <n-input
              v-model:value="formData.password"
              type="password"
              placeholder="Enter your password"
              size="large"
              show-password-on="mousedown"
              @keydown.enter.prevent="handleSubmit"
            />
          </n-form-item>
  
          <n-form-item>
            <n-button
              type="primary"
              size="large"
              :loading="loading"
              @click="handleSubmit"
              style="width: 100%;"
            >
              Login
            </n-button>
          </n-form-item>
  
          <n-divider>
            <span style="color: #666; font-size: 14px;">Don't have an account?</span>
          </n-divider>
  
          <n-button
            quaternary
            size="large"
            @click="$router.push('/register')"
            style="width: 100%;"
          >
            Create New Account
          </n-button>
        </n-form>
  
        <!-- Login Error Display -->
        <n-alert
          v-if="error"
          title="Login Failed"
          type="error"
          style="margin-top: 16px;"
          closable
          @close="error = ''"
        >
          {{ error }}
        </n-alert>
  
        <!-- Demo Account Info -->
        <n-card 
          style="margin-top: 24px; background: #f8f9fa;"
          size="small"
        >
          <template #header>
            <span style="font-size: 14px; color: #666;">Demo Account</span>
          </template>
          <div style="font-size: 13px; color: #888;">
            <p><strong>Username:</strong> testuser1</p>
            <p><strong>Password:</strong> Test123456</p>
            <p style="margin-top: 8px; font-style: italic;">
              Use this account to test the application features.
            </p>
          </div>
        </n-card>
      </n-card>
    </div>
  </template>
  
  <script setup>
  import { ref, reactive } from 'vue'
  import { useRouter } from 'vue-router'
  import { useMessage } from 'naive-ui'
  import apiClient from '@/services/api'
  
  const router = useRouter()
  const message = useMessage()
  
  // Form data
  const formRef = ref(null)
  const loading = ref(false)
  const error = ref('')
  
  const formData = reactive({
    username: '',
    password: ''
  })
  
  // Form validation rules
  const rules = {
    username: [
      {
        required: true,
        message: 'Username is required',
        trigger: ['input', 'blur']
      },
      {
        min: 3,
        message: 'Username must be at least 3 characters',
        trigger: ['input', 'blur']
      }
    ],
    password: [
      {
        required: true,
        message: 'Password is required',
        trigger: ['input', 'blur']
      },
      {
        min: 6,
        message: 'Password must be at least 6 characters',
        trigger: ['input', 'blur']
      }
    ]
  }
  
  // Handle form submission
  const handleSubmit = async () => {
    try {
      // Validate form
      await formRef.value?.validate()
      
      loading.value = true
      error.value = ''
  
      // Make login request
      const response = await apiClient.post('/api/userbase/auth/login/', {
        username: formData.username,
        password: formData.password
      })
  
      // Handle successful login
      const { access_token, key, user } = response.data
      
      // Store token (prefer key from dj-rest-auth if available)
      const token = key || access_token
      if (token) {
        localStorage.setItem('token', token)
        
        // Store user info
        if (user) {
          localStorage.setItem('user', JSON.stringify(user))
        }
  
        message.success(`Welcome back, ${user?.username || formData.username}!`)
        
        // Redirect to intended page or home
        const redirectTo = router.currentRoute.value.query.redirect || '/'
        router.push(redirectTo)
      } else {
        throw new Error('No authentication token received')
      }
  
    } catch (err) {
      console.error('Login error:', err)
      
      if (err.response?.status === 400) {
        error.value = 'Invalid username or password'
      } else if (err.response?.status === 401) {
        error.value = 'Invalid credentials'
      } else if (err.response?.data?.non_field_errors) {
        error.value = err.response.data.non_field_errors[0]
      } else if (err.response?.data?.detail) {
        error.value = err.response.data.detail
      } else {
        error.value = 'Login failed. Please try again.'
      }
    } finally {
      loading.value = false
    }
  }
  
  // Auto-fill demo credentials
  const fillDemoCredentials = () => {
    formData.username = 'testuser'
    formData.password = 'test123456'
  }
  </script>
  
  <style scoped>
  .n-card {
    box-shadow: 0 12px 24px rgba(0, 0, 0, 0.1);
  }
  
  .n-form-item {
    margin-bottom: 20px;
  }
  
  .n-divider {
    margin: 24px 0 16px 0;
  }
  </style>