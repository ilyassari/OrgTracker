<template>
    <n-layout>
      <!-- Header -->
      <n-layout-header bordered style="height: 64px; padding: 0 24px;">
        <div style="display: flex; align-items: center; height: 100%; justify-content: space-between;">
          <div style="display: flex; align-items: center; gap: 16px;">
            <n-button text @click="$router.push('/')">
              ← Back to Organizations
            </n-button>
            <h2 style="margin: 0; color: #18a058;">My Profile</h2>
          </div>
          
          <div style="display: flex; align-items: center; gap: 12px;">
            <n-button text @click="$router.push('/followed')">
              Followed Organizations
            </n-button>
            <n-button type="error" ghost @click="handleLogout">
              Logout
            </n-button>
          </div>
        </div>
      </n-layout-header>
  
      <n-layout-content style="padding: 24px;">
        <div style="max-width: 800px; margin: 0 auto;">
          <!-- Profile Header -->
          <n-card style="margin-bottom: 24px;">
            <div style="display: flex; align-items: center; gap: 24px;">
              <n-avatar
                :size="100"
                round
                style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); font-size: 48px; font-weight: bold;"
              >
                {{ getUserInitials }}
              </n-avatar>
              
              <div style="flex: 1;">
                <h1 style="margin: 0 0 8px 0;">{{ user?.first_name }} {{ user?.last_name }}</h1>
                <p style="margin: 0; color: #666; font-size: 16px;">@{{ user?.username }}</p>
                <p style="margin: 8px 0 0 0; color: #999; font-size: 14px;">{{ user?.email }}</p>
              </div>
  
              <n-statistic 
                label="Following" 
                :value="followCount"
                style="text-align: center;"
              >
                <template #suffix>
                  <span style="font-size: 14px;">organizations</span>
                </template>
              </n-statistic>
            </div>
          </n-card>
  
          <!-- User Information -->
          <n-card title="Account Information" style="margin-bottom: 24px;">
            <n-descriptions :column="1" bordered>
              <n-descriptions-item label="Username">
                {{ user?.username }}
              </n-descriptions-item>
              
              <n-descriptions-item label="Email">
                {{ user?.email }}
              </n-descriptions-item>
              
              <n-descriptions-item label="First Name">
                {{ user?.first_name }}
              </n-descriptions-item>
              
              <n-descriptions-item label="Last Name">
                {{ user?.last_name }}
              </n-descriptions-item>
              
              <n-descriptions-item label="Account Type">
                <n-tag :type="user?.is_superuser ? 'error' : user?.is_staff ? 'warning' : 'success'">
                  {{ user?.is_superuser ? 'Administrator' : user?.is_staff ? 'Staff' : 'Regular User' }}
                </n-tag>
              </n-descriptions-item>
              
              <n-descriptions-item label="Date Joined" v-if="user?.date_joined">
                {{ formatDate(user.date_joined) }}
              </n-descriptions-item>
              
              <n-descriptions-item label="Last Login" v-if="user?.last_login">
                {{ formatDate(user.last_login) }}
              </n-descriptions-item>
            </n-descriptions>
          </n-card>
  
          <!-- Activity Summary -->
          <n-grid :cols="2" :x-gap="16" style="margin-bottom: 24px;">
            <n-grid-item>
              <n-card>
                <n-statistic label="Organizations Following" :value="followCount">
                  <template #prefix>
                    <n-icon :component="HeartIcon" style="color: #e74c3c;" />
                  </template>
                </n-statistic>
                <template #action>
                  <n-button text type="primary" @click="$router.push('/followed')">
                    View All →
                  </n-button>
                </template>
              </n-card>
            </n-grid-item>
            
            <n-grid-item>
              <n-card>
                <n-statistic label="Member Since">
                  <template #default>
                    {{ getMemberDuration }}
                  </template>
                  <template #prefix>
                    <n-icon :component="CalendarIcon" style="color: #3498db;" />
                  </template>
                </n-statistic>
              </n-card>
            </n-grid-item>
          </n-grid>
  
          <!-- Account Actions -->
          <n-card title="Account Actions">
            <n-space vertical>
              <n-button @click="$router.push('/followed')" block>
                <template #icon>
                  <n-icon :component="HeartIcon" />
                </template>
                View Followed Organizations
              </n-button>
              
              <n-button @click="$router.push('/')" block>
                <template #icon>
                  <n-icon :component="BusinessIcon" />
                </template>
                Browse All Organizations
              </n-button>
              
              <n-divider style="margin: 12px 0;" />
              
              <n-button type="error" ghost @click="confirmLogout" block>
                <template #icon>
                  <n-icon :component="LogoutIcon" />
                </template>
                Logout
              </n-button>
            </n-space>
          </n-card>
        </div>
      </n-layout-content>
    </n-layout>
  </template>
  
  <script setup>
  import { ref, computed, onMounted } from 'vue'
  import { useRouter } from 'vue-router'
  import { useMessage, useDialog } from 'naive-ui'
  import { Heart as HeartIcon, Calendar as CalendarIcon, Business as BusinessIcon, LogOutOutline as LogoutIcon } from '@vicons/ionicons5'
  import apiClient from '@/services/api'
  
  const router = useRouter()
  const message = useMessage()
  const dialog = useDialog()
  
  const user = ref(null)
  const followCount = ref(0)
  
  const getUserInitials = computed(() => {
    if (!user.value) return '?'
    const first = user.value.first_name?.charAt(0) || ''
    const last = user.value.last_name?.charAt(0) || ''
    return (first + last).toUpperCase() || user.value.username?.charAt(0).toUpperCase() || '?'
  })
  
  const getMemberDuration = computed(() => {
    if (!user.value?.date_joined) return 'N/A'
    
    const joinDate = new Date(user.value.date_joined)
    const now = new Date()
    const diffTime = Math.abs(now - joinDate)
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
    
    if (diffDays < 30) {
      return `${diffDays} days`
    } else if (diffDays < 365) {
      const months = Math.floor(diffDays / 30)
      return `${months} month${months > 1 ? 's' : ''}`
    } else {
      const years = Math.floor(diffDays / 365)
      return `${years} year${years > 1 ? 's' : ''}`
    }
  })
  
  const fetchUserProfile = async () => {
    try {
      const response = await apiClient.get('/api/userbase/auth/user/')
      user.value = response.data
    } catch (error) {
      console.error('Failed to fetch user profile:', error)
      message.error('Failed to load profile')
      
      // If auth fails, redirect to login
      if (error.response?.status === 401 || error.response?.status === 403) {
        localStorage.removeItem('token')
        localStorage.removeItem('user')
        router.push('/login')
      }
    }
  }
  
  const fetchFollowCount = async () => {
    try {
      const response = await apiClient.get('/api/userbase/followed-organizations/')
      const data = response.data.results || response.data || []
      followCount.value = Array.isArray(data) ? data.length : response.data.count || 0
    } catch (error) {
      console.warn('Could not fetch follow count:', error)
      followCount.value = 0
    }
  }
  
  const formatDate = (dateString) => {
    if (!dateString) return 'Unknown'
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }
  
  const confirmLogout = () => {
    dialog.warning({
      title: 'Logout',
      content: 'Are you sure you want to logout?',
      positiveText: 'Logout',
      negativeText: 'Cancel',
      onPositiveClick: handleLogout
    })
  }
  
  const handleLogout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    message.success('Logged out successfully')
    router.push('/')
  }
  
  onMounted(() => {
    fetchUserProfile()
    fetchFollowCount()
  })
  </script>
  
  <style scoped>
  .n-statistic {
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    padding: 16px;
    background: #fafafa;
  }
  </style>