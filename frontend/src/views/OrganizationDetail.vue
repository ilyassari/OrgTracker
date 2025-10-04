<template>
    <n-layout>
      <!-- Header -->
      <n-layout-header bordered style="height: 64px; padding: 0 24px;">
        <div style="display: flex; align-items: center; height: 100%; justify-content: space-between;">
          <n-button text @click="$router.back()">
            ← Back
          </n-button>
          
          <div style="display: flex; align-items: center; gap: 12px;">
            <template v-if="isAuthenticated">
              <n-button text @click="$router.push('/followed')">
                Followed Organizations
              </n-button>
              <n-button text @click="$router.push('/profile')">
                Profile
              </n-button>
              <n-button type="error" ghost @click="handleLogout">
                Logout
              </n-button>
            </template>
            <template v-else>
              <n-button @click="$router.push('/login')">
                Login
              </n-button>
            </template>
          </div>
        </div>
      </n-layout-header>
  
      <n-layout-content style="padding: 24px;">
        <n-spin :show="loading">
          <div v-if="organization" style="max-width: 1200px; margin: 0 auto;">
            <!-- Organization Header -->
            <n-card style="margin-bottom: 24px;">
              <div style="display: flex; gap: 24px; align-items: flex-start;">
                <n-avatar
                  :size="120"
                  :src="organization.logo"
                  :fallback-src="getDefaultLogo()"
                  style="flex-shrink: 0; border: 3px solid #f0f0f0;"
                />
                
                <div style="flex: 1;">
                  <n-space vertical size="small">
                    <div>
                      <h1 style="margin: 0 0 8px 0; font-size: 32px;">{{ organization.name }}</h1>
                      <n-tag
                        :type="getOrgTypeColor(organization.org_type)"
                        size="large"
                        round
                      >
                        {{ getOrgTypeLabel(organization.org_type) }}
                      </n-tag>
                    </div>
                    
                    <n-space size="large">
                      <div>
                        <n-icon :component="LocationIcon" style="margin-right: 8px; color: #666;" />
                        <span style="font-size: 16px; color: #666;">{{ getCountryName(organization.nation) }}</span>
                      </div>
                      <div>
                        <n-icon :component="CalendarIcon" style="margin-right: 8px; color: #666;" />
                        <span style="font-size: 16px; color: #666;">Founded in {{ formatYear(organization.founding_date) }}</span>
                      </div>
                      <div v-if="organization.headcount">
                        <n-icon :component="PeopleIcon" style="margin-right: 8px; color: #666;" />
                        <span style="font-size: 16px; color: #666;">{{ formatHeadcount(organization.headcount) }} employees</span>
                      </div>
                    </n-space>
                  </n-space>
                </div>
  
                <!-- Follow Button -->
                <div v-if="isAuthenticated" style="flex-shrink: 0;">
                  <n-button
                    :type="isFollowing ? 'error' : 'primary'"
                    :ghost="isFollowing"
                    size="large"
                    :loading="followLoading"
                    @click="toggleFollow"
                  >
                    <template #icon>
                      <n-icon :component="isFollowing ? HeartIcon : HeartOutlineIcon" />
                    </template>
                    {{ isFollowing ? 'Unfollow' : 'Follow' }}
                  </n-button>
                </div>
              </div>
            </n-card>
  
            <!-- Statistics -->
            <n-grid :cols="4" :x-gap="16" style="margin-bottom: 24px;">
              <n-grid-item>
                <n-card>
                  <n-statistic label="Organization Type">
                    <template #default>
                      {{ getOrgTypeLabel(organization.org_type) }}
                    </template>
                  </n-statistic>
                </n-card>
              </n-grid-item>
              
              <n-grid-item>
                <n-card>
                  <n-statistic label="Country">
                    <template #default>
                      {{ getCountryName(organization.nation) }}
                    </template>
                  </n-statistic>
                </n-card>
              </n-grid-item>
              
              <n-grid-item>
                <n-card>
                  <n-statistic label="Years Active">
                    <template #default>
                      {{ getYearsActive(organization.founding_date) }}
                    </template>
                  </n-statistic>
                </n-card>
              </n-grid-item>
              
              <n-grid-item>
                <n-card>
                  <n-statistic label="Employees" :value="organization.headcount || 'N/A'">
                  </n-statistic>
                </n-card>
              </n-grid-item>
            </n-grid>
  
            <!-- Details -->
            <n-card title="Organization Details">
              <n-descriptions :column="2" bordered>
                <n-descriptions-item label="Name">
                  {{ organization.name }}
                </n-descriptions-item>
                
                <n-descriptions-item label="Slug">
                  <n-tag size="small">{{ organization.slug }}</n-tag>
                </n-descriptions-item>
                
                <n-descriptions-item label="Organization Type">
                  {{ getOrgTypeLabel(organization.org_type) }}
                </n-descriptions-item>
                
                <n-descriptions-item label="Country">
                  {{ getCountryName(organization.nation) }}
                </n-descriptions-item>
                
                <n-descriptions-item label="Founding Date">
                  {{ formatFullDate(organization.founding_date) }}
                </n-descriptions-item>
                
                <n-descriptions-item label="Employee Count">
                  {{ organization.headcount ? formatHeadcount(organization.headcount) : 'Not specified' }}
                </n-descriptions-item>
                
                <n-descriptions-item label="Created At" v-if="organization.created_at">
                  {{ formatFullDate(organization.created_at) }}
                </n-descriptions-item>
                
                <n-descriptions-item label="Last Updated" v-if="organization.updated_at">
                  {{ formatFullDate(organization.updated_at) }}
                </n-descriptions-item>
              </n-descriptions>
            </n-card>
          </div>
  
          <!-- Error State -->
          <div v-else-if="!loading" style="text-align: center; padding: 60px 0;">
            <n-empty description="Organization not found">
              <template #extra>
                <n-button type="primary" @click="$router.push('/')">
                  Back to Organizations
                </n-button>
              </template>
            </n-empty>
          </div>
        </n-spin>
      </n-layout-content>
    </n-layout>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import { useRoute, useRouter } from 'vue-router'
  import { useMessage } from 'naive-ui'
  import { LocationOutline as LocationIcon, Calendar as CalendarIcon, People as PeopleIcon, Heart as HeartIcon, HeartOutline as HeartOutlineIcon } from '@vicons/ionicons5'
  import apiClient from '@/services/api'
  
  const route = useRoute()
  const router = useRouter()
  const message = useMessage()
  
  const organization = ref(null)
  const loading = ref(false)
  const isFollowing = ref(false)
  const followLoading = ref(false)
  const isAuthenticated = ref(false)
  
  const checkAuthStatus = () => {
    const token = localStorage.getItem('token')
    isAuthenticated.value = !!token
  }
  
  const fetchOrganization = async () => {
    try {
      loading.value = true
      const slug = route.params.slug
      const response = await apiClient.get(`/api/organizations/${slug}/`)
      organization.value = response.data
      
      if (isAuthenticated.value) {
        await checkFollowStatus()
      }
    } catch (error) {
      console.error('Failed to fetch organization:', error)
      message.error('Failed to load organization')
      organization.value = null
    } finally {
      loading.value = false
    }
  }
  
  const checkFollowStatus = async () => {
    if (!isAuthenticated.value) return
    
    try {
      const response = await apiClient.get('/api/userbase/followed-organizations/')
      const followedOrgs = response.data.results || response.data || []
      isFollowing.value = followedOrgs.some(org => org.id === organization.value.id)
    } catch (error) {
      console.warn('Could not check follow status:', error)
    }
  }
  
  const toggleFollow = async () => {
    if (!isAuthenticated.value) {
      message.warning('Please login to follow organizations')
      return
    }
  
    try {
      followLoading.value = true
      
      if (isFollowing.value) {
        await apiClient.post(`/api/userbase/unfollow/${organization.value.slug}/`)
        isFollowing.value = false
        message.success(`Unfollowed ${organization.value.name}`)
      } else {
        await apiClient.post(`/api/userbase/follow/${organization.value.slug}/`)
        isFollowing.value = true
        message.success(`Following ${organization.value.name}`)
      }
    } catch (error) {
      console.error('Follow action failed:', error)
      message.error('Failed to update follow status')
    } finally {
      followLoading.value = false
    }
  }
  
  const getOrgTypeLabel = (type) => {
    const labels = {
      0: 'Sole proprietorship',
      1: 'Holding',
      2: 'Small and medium-sized enterprises',
      3: 'Civil society organization'
    }
    return labels[type] || 'Unknown'
  }
  
  const getOrgTypeColor = (type) => {
    const colors = {
      0: 'default',
      1: 'success',
      2: 'info',
      3: 'warning'
    }
    return colors[type] || 'default'
  }
  
  const getCountryName = (countryCode) => {
    const countries = {
      'TR': 'Turkey', 'US': 'United States', 'DE': 'Germany', 'KR': 'South Korea',
      'JP': 'Japan', 'FR': 'France', 'GB': 'United Kingdom', 'NL': 'Netherlands',
      'CH': 'Switzerland', 'CN': 'China', 'IT': 'Italy', 'SE': 'Sweden',
      'NO': 'Norway', 'FI': 'Finland', 'PL': 'Poland', 'CZ': 'Czech Republic', 'HU': 'Hungary'
    }
    return countries[countryCode] || countryCode
  }
  
  const formatYear = (dateString) => {
    if (!dateString) return 'Unknown'
    return new Date(dateString).getFullYear()
  }
  
  const formatFullDate = (dateString) => {
    if (!dateString) return 'Unknown'
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    })
  }
  
  const formatHeadcount = (count) => {
    if (count >= 1000000) return `${(count / 1000000).toFixed(1)}M`
    if (count >= 1000) return `${(count / 1000).toFixed(1)}K`
    return count.toLocaleString()
  }
  
  const getYearsActive = (foundingDate) => {
    if (!foundingDate) return 'N/A'
    const years = new Date().getFullYear() - new Date(foundingDate).getFullYear()
    return `${years} years`
  }
  
  const getDefaultLogo = () => {
    if (!organization.value) return ''
    
    const canvas = document.createElement('canvas')
    canvas.width = 120
    canvas.height = 120
    const ctx = canvas.getContext('2d')
    
    let hash = 0
    for (let i = 0; i < organization.value.name.length; i++) {
      hash = organization.value.name.charCodeAt(i) + ((hash << 5) - hash)
    }
    
    const color = `hsl(${hash % 360}, 70%, 50%)`
    ctx.fillStyle = color
    ctx.fillRect(0, 0, 120, 120)
    
    ctx.fillStyle = 'white'
    ctx.font = 'bold 60px Arial'
    ctx.textAlign = 'center'
    ctx.textBaseline = 'middle'
    ctx.fillText(organization.value.name.charAt(0).toUpperCase(), 60, 60)
    
    return canvas.toDataURL()
  }
  
  const handleLogout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    isAuthenticated.value = false
    message.success('Logged out successfully')
    router.push('/')
  }
  
  onMounted(() => {
    checkAuthStatus()
    fetchOrganization()
  })
  </script>