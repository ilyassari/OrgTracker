<template>
    <div style="min-height: 100vh; display: flex; align-items: center; justify-content: center; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
      <n-card 
        title="Create Account"
        style="width: 450px; max-width: 90vw;"
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
          <n-grid :cols="2" :x-gap="12">
            <n-grid-item>
              <n-form-item path="first_name" label="First Name">
                <n-input
                  v-model:value="formData.first_name"
                  placeholder="First name"
                  size="large"
                />
              </n-form-item>
            </n-grid-item>
            
            <n-grid-item>
              <n-form-item path="last_name" label="Last Name">
                <n-input
                  v-model:value="formData.last_name"
                  placeholder="Last name"
                  size="large"
                />
              </n-form-item>
            </n-grid-item>
          </n-grid>
  
          <n-form-item path="username" label="Username">
            <n-input
              v-model:value="formData.username"
              placeholder="Choose a username"
              size="large"
            />
          </n-form-item>
  
          <n-form-item path="email" label="Email">
            <n-input
              v-model:value="formData.email"
              type="email"
              placeholder="Enter your email"
              size="large"
            />
          </n-form-item>
  
          <n-form-item path="password1" label="Password">
            <n-input
              v-model:value="formData.password1"
              type="password"
              placeholder="Create a password"
              size="large"
              show-password-on="mousedown"
            />
          </n-form-item>
  
          <n-form-item path="password2" label="Confirm Password">
            <n-input
              v-model:value="formData.password2"
              type="password"
              placeholder="Confirm your password"
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
              Create Account
            </n-button>
          </n-form-item>
  
          <n-divider>
            <span style="color: #666; font-size: 14px;">Already have an account?</span>
          </n-divider>
  
          <n-button
            quaternary
            size="large"
            @click="$router.push('/login')"
            style="width: 100%;"
          >
            Sign In Instead
          </n-button>
        </n-form>
  
        <!-- Registration Error Display -->
        <n-alert
          v-if="error"
          title="Registration Failed"
          type="error"
          style="margin-top: 16px;"
          closable
          @close="error = ''"
        >
          <div v-if="typeof error === 'string'">{{ error }}</div>
          <div v-else>
            <div v-for="(msgs, field) in error" :key="field">
              <strong>{{ formatFieldName(field) }}:</strong>
              <ul style="margin-left: 20px;">
                <li v-for="msg in msgs" :key="msg">{{ msg }}</li>
              </ul>
            </div>
          </div>
        </n-alert>
  
        <!-- Success Message -->
        <n-alert
          v-if="success"
          title="Account Created Successfully!"
          type="success"
          style="margin-top: 16px;"
        >
          Your account has been created. You can now log in with your credentials.
        </n-alert>
  
        <!-- Password Requirements -->
        <n-card 
          style="margin-top: 24px; background: #f8f9fa;"
          size="small"
        >
          <template #header>
            <span style="font-size: 14px; color: #666;">Password Requirements</span>
          </template>
          <div style="font-size: 13px; color: #888;">
            <ul style="margin-left: 20px;">
              <li>At least 8 characters long</li>
              <li>Cannot be too similar to your username</li>
              <li>Cannot be a commonly used password</li>
              <li>Cannot be entirely numeric</li>
            </ul>
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
  const success = ref(false)
  
  const formData = reactive({
    first_name: '',
    last_name: '',
    username: '',
    email: '',
    password1: '',
    password2: ''
  })
  
  // Form validation rules
  const rules = {
    first_name: [
      {
        required: true,
        message: 'First name is required',
        trigger: ['input', 'blur']
      }
    ],
    last_name: [
      {
        required: true,
        message: 'Last name is required',
        trigger: ['input', 'blur']
      }
    ],
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
      },
      {
        pattern: /^[a-zA-Z0-9_]+$/,
        message: 'Username can only contain letters, numbers and underscores',
        trigger: ['input', 'blur']
      }
    ],
    email: [
      {
        required: true,
        message: 'Email is required',
        trigger: ['input', 'blur']
      },
      {
        type: 'email',
        message: 'Please enter a valid email address',
        trigger: ['input', 'blur']
      }
    ],
    password1: [
      {
        required: true,
        message: 'Password is required',
        trigger: ['input', 'blur']
      },
      {
        min: 8,
        message: 'Password must be at least 8 characters',
        trigger: ['input', 'blur']
      }
    ],
    password2: [
      {
        required: true,
        message: 'Password confirmation is required',
        trigger: ['input', 'blur']
      },
      {
        validator: (rule, value) => {
          return value === formData.password1
        },
        message: 'Passwords do not match',
        trigger: ['input', 'blur']
      }
    ]
  }
  
  // Format field names for error display
  const formatFieldName = (field) => {
    const fieldNames = {
      username: 'Username',
      email: 'Email',
      password1: 'Password',
      password2: 'Password Confirmation',
      first_name: 'First Name',
      last_name: 'Last Name',
      non_field_errors: 'General'
    }
    return fieldNames[field] || field
  }
  
  // Handle form submission
  const handleSubmit = async () => {
    try {
      // Validate form
      await formRef.value?.validate()
      
      loading.value = true
      error.value = ''
      success.value = false
  
      // Make registration request
      const response = await apiClient.post('/api/userbase/auth/registration/', {
        username: formData.username,
        email: formData.email,
        password1: formData.password1,
        password2: formData.password2,
        first_name: formData.first_name,
        last_name: formData.last_name
      })
  
      // Handle successful registration
      const { access_token, key, user } = response.data
      
      // Store token immediately if provided (auto-login after registration)
      const token = key || access_token
      if (token) {
        localStorage.setItem('token', token)
        
        // Store user info
        if (user) {
          localStorage.setItem('user', JSON.stringify(user))
        }
  
        message.success(`Welcome to OrgTracker, ${user?.first_name || formData.first_name}!`)
        
        // Redirect to home page
        router.push('/')
      } else {
        // Registration successful but no auto-login
        success.value = true
        message.success('Account created successfully! Please log in.')
        
        // Redirect to login page after a delay
        setTimeout(() => {
          router.push('/login')
        }, 2000)
      }
  
    } catch (err) {
      console.error('Registration error:', err)
      
      if (err.response?.data) {
        const errorData = err.response.data
        
        // Handle field-specific errors
        if (typeof errorData === 'object' && !Array.isArray(errorData)) {
          error.value = errorData
        } else if (errorData.detail) {
          error.value = errorData.detail
        } else if (Array.isArray(errorData)) {
          error.value = errorData.join(', ')
        } else {
          error.value = 'Registration failed. Please check your information.'
        }
      } else {
        error.value = 'Registration failed. Please try again.'
      }
    } finally {
      loading.value = false
    }
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
  
  ul {
    margin: 8px 0;
  }
  
  li {
    margin-bottom: 4px;
  }
  </style>