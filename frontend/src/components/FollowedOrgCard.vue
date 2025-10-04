<template>
    <n-card
      hoverable
      style="height: 100%; cursor: pointer;"
      @click="goToDetail"
    >
      <!-- Card header with logo and unfollow button -->
      <template #header>
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <div style="display: flex; align-items: center; gap: 12px;">
            <n-avatar
              :size="40"
              :src="organization.logo"
              :fallback-src="getDefaultLogo()"
              style="flex-shrink: 0;"
            />
            <div style="min-width: 0;">
              <div style="font-weight: 600; font-size: 16px; margin-bottom: 4px; word-break: break-word;">
                {{ organization.name }}
              </div>
              <n-tag
                :type="getOrgTypeColor(organization.org_type)"
                size="small"
                round
              >
                {{ getOrgTypeLabel(organization.org_type) }}
              </n-tag>
            </div>
          </div>
          
          <!-- Unfollow button -->
          <div @click.stop>
            <n-button
              type="error"
              ghost
              size="small"
              :loading="unfollowLoading"
              @click="handleUnfollow"
            >
              Unfollow
            </n-button>
          </div>
        </div>
      </template>
  
      <!-- Card content -->
      <div style="padding: 0;">
        <n-space vertical size="small">
          <!-- Country and founding date -->
          <div style="display: flex; justify-content: space-between; align-items: center;">
            <span style="color: #666; font-size: 14px;">
              <n-icon :component="LocationIcon" style="margin-right: 4px;" />
              {{ getCountryName(organization.nation) }}
            </span>
            <span style="color: #666; font-size: 14px;">
              Founded: {{ formatDate(organization.founding_date) }}
            </span>
          </div>
  
          <!-- Employee count -->
          <div v-if="organization.headcount" style="display: flex; align-items: center;">
            <n-icon :component="PeopleIcon" style="margin-right: 8px; color: #18a058;" />
            <span style="font-weight: 500;">
              {{ formatHeadcount(organization.headcount) }} employees
            </span>
          </div>
  
          <n-divider style="margin: 12px 0;" />
          
          <!-- Action area -->
          <div style="display: flex; justify-content: space-between; align-items: center;">
            <n-button text type="primary" @click.stop="goToDetail">
              View Details →
            </n-button>
            
            <!-- Following badge -->
            <n-tag type="success" size="small">
              <template #icon>
                <n-icon :component="HeartIcon" />
              </template>
              Following
            </n-tag>
          </div>
  
          <!-- Follow date if available -->
          <div v-if="followDate" style="font-size: 12px; color: #999; text-align: center;">
            Following since {{ followDate }}
          </div>
        </n-space>
      </div>
    </n-card>
  </template>
  
  <script setup>
  import { ref, computed } from 'vue'
  import { useRouter } from 'vue-router'
  import { useMessage } from 'naive-ui'
  import { LocationOutline as LocationIcon, People as PeopleIcon, Heart as HeartIcon } from '@vicons/ionicons5'
  
  // Props
  const props = defineProps({
    organization: {
      type: Object,
      required: true
    }
  })
  
  // Emits
  const emit = defineEmits(['unfollow'])
  
  // Reactive data
  const router = useRouter()
  const message = useMessage()
  const unfollowLoading = ref(false)
  
  // Computed properties
  const followDate = computed(() => {
    // This would come from backend if we track follow dates
    return null
  })
  
  // Organization type helpers
  const getOrgTypeLabel = (type) => {
    const labels = {
      0: 'Sole proprietorship',
      1: 'Holding',
      2: 'SME',
      3: 'NGO'
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
  
  // Country name helper
  const getCountryName = (countryCode) => {
    const countries = {
      'TR': 'Turkey',
      'US': 'United States',
      'DE': 'Germany',
      'KR': 'South Korea',
      'JP': 'Japan',
      'FR': 'France',
      'GB': 'United Kingdom',
      'NL': 'Netherlands',
      'CH': 'Switzerland',
      'CN': 'China',
      'IT': 'Italy',
      'SE': 'Sweden',
      'NO': 'Norway',
      'FI': 'Finland',
      'PL': 'Poland',
      'CZ': 'Czech Republic',
      'HU': 'Hungary'
    }
    return countries[countryCode] || countryCode
  }
  
  // Date formatting
  const formatDate = (dateString) => {
    if (!dateString) return 'Unknown'
    const date = new Date(dateString)
    return date.getFullYear()
  }
  
  // Headcount formatting
  const formatHeadcount = (count) => {
    if (count >= 1000000) {
      return `${(count / 1000000).toFixed(1)}M`
    } else if (count >= 1000) {
      return `${(count / 1000).toFixed(1)}K`
    }
    return count.toLocaleString()
  }
  
  // Default logo fallback
  const getDefaultLogo = () => {
    const canvas = document.createElement('canvas')
    canvas.width = 40
    canvas.height = 40
    const ctx = canvas.getContext('2d')
    
    // Simple hash function to generate color
    let hash = 0
    for (let i = 0; i < props.organization.name.length; i++) {
      hash = props.organization.name.charCodeAt(i) + ((hash << 5) - hash)
    }
    
    const color = `hsl(${hash % 360}, 70%, 50%)`
    ctx.fillStyle = color
    ctx.fillRect(0, 0, 40, 40)
    
    // Add first letter of organization name
    ctx.fillStyle = 'white'
    ctx.font = 'bold 20px Arial'
    ctx.textAlign = 'center'
    ctx.textBaseline = 'middle'
    ctx.fillText(props.organization.name.charAt(0).toUpperCase(), 20, 20)
    
    return canvas.toDataURL()
  }
  
  // Navigation
  const goToDetail = () => {
    router.push(`/organizations/${props.organization.slug}`)
  }
  
  // Unfollow functionality
  const handleUnfollow = async () => {
    try {
      unfollowLoading.value = true
      emit('unfollow', props.organization.slug)
      message.success(`Unfollowed ${props.organization.name}`)
    } catch (error) {
      console.error('Unfollow error:', error)
      message.error('Failed to unfollow organization')
    } finally {
      unfollowLoading.value = false
    }
  }
  </script>
  
  <style scoped>
  .n-card {
    transition: all 0.3s ease;
  }
  
  .n-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
  }
  
  .n-avatar {
    border: 2px solid #f0f0f0;
  }
  </style>