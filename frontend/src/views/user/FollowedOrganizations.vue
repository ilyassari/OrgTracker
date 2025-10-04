<template>
    <n-layout>
      <!-- Header -->
      <n-layout-header bordered style="height: 64px; padding: 0 24px;">
        <div style="display: flex; align-items: center; height: 100%; justify-content: space-between;">
          <div style="display: flex; align-items: center; gap: 16px;">
            <n-button text @click="$router.push('/')">
              ← Back to Organizations
            </n-button>
            <h2 style="margin: 0; color: #18a058;">Followed Organizations</h2>
          </div>
          
          <div style="display: flex; align-items: center; gap: 12px;">
            <n-button text @click="$router.push('/profile')">
              Profile
            </n-button>
            <n-button type="error" ghost @click="handleLogout">
              Logout
            </n-button>
          </div>
        </div>
      </n-layout-header>
  
      <n-layout-content style="padding: 24px;">
        <!-- Page Title and Stats -->
        <div style="margin-bottom: 24px;">
          <n-space align="center" justify="space-between">
            <div>
              <h1 style="margin: 0 0 8px 0;">My Followed Organizations</h1>
              <p style="margin: 0; color: #666;">
                Keep track of organizations you're interested in
              </p>
            </div>
            
            <n-statistic 
              label="Total Following" 
              :value="followedOrgs.length"
              style="text-align: center;"
            />
          </n-space>
        </div>
  
        <!-- Filter/Search Bar -->
        <n-card style="margin-bottom: 24px;" v-if="followedOrgs.length > 0">
          <n-form inline>
            <n-form-item label="Search">
              <n-input
                v-model:value="searchQuery"
                placeholder="Search your followed organizations..."
                clearable
                style="width: 300px;"
              />
            </n-form-item>
            
            <n-form-item label="Type">
              <n-select
                v-model:value="selectedType"
                :options="orgTypeOptions"
                placeholder="All types"
                clearable
                style="width: 200px;"
              />
            </n-form-item>
            
            <n-form-item label="Sort by">
              <n-select
                v-model:value="sortBy"
                :options="sortOptions"
                style="width: 150px;"
              />
            </n-form-item>
          </n-form>
        </n-card>
  
        <!-- Loading State -->
        <n-spin :show="loading">
          <!-- Empty State -->
          <div v-if="followedOrgs.length === 0 && !loading" style="text-align: center; padding: 60px 0;">
            <n-empty description="You haven't followed any organizations yet">
              <template #icon>
                <n-icon size="48" style="color: #ccc;">
                  <HeartOutline />
                </n-icon>
              </template>
              <template #extra>
                <n-button type="primary" @click="$router.push('/')">
                  Explore Organizations
                </n-button>
              </template>
            </n-empty>
          </div>
  
          <!-- Organizations Grid -->
          <div v-else-if="filteredOrgs.length > 0">
            <n-grid :cols="3" :x-gap="16" :y-gap="16">
              <n-grid-item v-for="org in paginatedOrgs" :key="org.id">
                <FollowedOrgCard :organization="org" @unfollow="handleUnfollow" />
              </n-grid-item>
            </n-grid>
  
            <!-- Pagination -->
            <div style="display: flex; justify-content: center; margin-top: 32px;" v-if="totalPages > 1">
              <n-pagination
                v-model:page="currentPage"
                :page-count="totalPages"
                :page-size="pageSize"
                show-size-picker
                :page-sizes="[9, 18, 36]"
                @update:page="currentPage = $event"
                @update:page-size="handlePageSizeChange"
              />
            </div>
          </div>
  
          <!-- No Results from Filter -->
          <div v-else-if="followedOrgs.length > 0 && filteredOrgs.length === 0" style="text-align: center; padding: 40px 0;">
            <n-empty description="No organizations match your search criteria">
              <template #extra>
                <n-button @click="clearFilters">Clear Filters</n-button>
              </template>
            </n-empty>
          </div>
        </n-spin>
  
        <!-- Quick Actions -->
        <n-card title="Quick Actions" style="margin-top: 32px;" v-if="followedOrgs.length > 0">
          <n-space>
            <n-button @click="$router.push('/')">
              Discover More Organizations
            </n-button>
            
            <n-button 
              @click="unfollowAll" 
              type="error" 
              ghost
              :loading="unfollowAllLoading"
              v-if="followedOrgs.length > 0"
            >
              Unfollow All
            </n-button>
          </n-space>
        </n-card>
      </n-layout-content>
    </n-layout>
  </template>
  
  <script setup>
  import { ref, computed, onMounted, watch } from 'vue'
  import { useRouter } from 'vue-router'
  import { useMessage, useDialog } from 'naive-ui'
  import { HeartOutline } from '@vicons/ionicons5'
  import FollowedOrgCard from '@/components/FollowedOrgCard.vue'
  import apiClient from '@/services/api'
  
  const router = useRouter()
  const message = useMessage()
  const dialog = useDialog()
  
  // Reactive data
  const followedOrgs = ref([])
  const loading = ref(false)
  const unfollowAllLoading = ref(false)
  
  // Filter and search
  const searchQuery = ref('')
  const selectedType = ref(null)
  const sortBy = ref('name')
  
  // Pagination
  const currentPage = ref(1)
  const pageSize = ref(9)
  
  // Filter options
  const orgTypeOptions = [
    { label: 'Sole proprietorship', value: 0 },
    { label: 'Holding', value: 1 },
    { label: 'SME', value: 2 },
    { label: 'NGO', value: 3 }
  ]
  
  const sortOptions = [
    { label: 'Name (A-Z)', value: 'name' },
    { label: 'Name (Z-A)', value: 'name_desc' },
    { label: 'Recently Added', value: 'recent' },
    { label: 'Employee Count', value: 'headcount' },
    { label: 'Founded Date', value: 'founding_date' }
  ]
  
  // Computed properties
  const filteredOrgs = computed(() => {
    let filtered = [...followedOrgs.value]
    
    // Search filter
    if (searchQuery.value) {
      const query = searchQuery.value.toLowerCase()
      filtered = filtered.filter(org => 
        org.name.toLowerCase().includes(query) ||
        org.nation.toLowerCase().includes(query)
      )
    }
    
    // Type filter
    if (selectedType.value !== null) {
      filtered = filtered.filter(org => org.org_type === selectedType.value)
    }
    
    // Sort
    filtered.sort((a, b) => {
      switch (sortBy.value) {
        case 'name_desc':
          return b.name.localeCompare(a.name)
        case 'recent':
          return new Date(b.created_at || 0) - new Date(a.created_at || 0)
        case 'headcount':
          return (b.headcount || 0) - (a.headcount || 0)
        case 'founding_date':
          return new Date(b.founding_date) - new Date(a.founding_date)
        default: // name
          return a.name.localeCompare(b.name)
      }
    })
    
    return filtered
  })
  
  const totalPages = computed(() => Math.ceil(filteredOrgs.value.length / pageSize.value))
  
  const paginatedOrgs = computed(() => {
    const start = (currentPage.value - 1) * pageSize.value
    const end = start + pageSize.value
    return filteredOrgs.value.slice(start, end)
  })
  
  // Methods
  const fetchFollowedOrganizations = async () => {
    try {
      loading.value = true
      const response = await apiClient.get('/api/userbase/followed-organizations/')
      followedOrgs.value = response.data.results || response.data || []
    } catch (error) {
      console.error('Failed to fetch followed organizations:', error)
      message.error('Failed to load followed organizations')
      followedOrgs.value = []
    } finally {
      loading.value = false
    }
  }
  
  const handleUnfollow = async (orgSlug) => {
    try {
      await apiClient.post(`/api/userbase/unfollow/${orgSlug}/`)
      
      // Remove from local list
      followedOrgs.value = followedOrgs.value.filter(org => org.slug !== orgSlug)
      
      // Reset to page 1 if current page becomes empty
      if (paginatedOrgs.value.length === 0 && currentPage.value > 1) {
        currentPage.value = 1
      }
      
      message.success('Organization unfollowed')
    } catch (error) {
      console.error('Failed to unfollow organization:', error)
      message.error('Failed to unfollow organization')
    }
  }
  
  const unfollowAll = () => {
    dialog.warning({
      title: 'Unfollow All Organizations',
      content: `Are you sure you want to unfollow all ${followedOrgs.value.length} organizations? This action cannot be undone.`,
      positiveText: 'Unfollow All',
      negativeText: 'Cancel',
      onPositiveClick: async () => {
        try {
          unfollowAllLoading.value = true
          
          // Unfollow all organizations
          const promises = followedOrgs.value.map(org => 
            apiClient.post(`/api/userbase/unfollow/${org.slug}/`)
          )
          
          await Promise.all(promises)
          followedOrgs.value = []
          
          message.success('Unfollowed all organizations')
        } catch (error) {
          console.error('Failed to unfollow all:', error)
          message.error('Failed to unfollow some organizations')
          // Refresh the list to see which ones failed
          fetchFollowedOrganizations()
        } finally {
          unfollowAllLoading.value = false
        }
      }
    })
  }
  
  const clearFilters = () => {
    searchQuery.value = ''
    selectedType.value = null
    currentPage.value = 1
  }
  
  const handlePageSizeChange = (newSize) => {
    pageSize.value = newSize
    currentPage.value = 1
  }
  
  const handleLogout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    message.success('Logged out successfully')
    router.push('/')
  }
  
  // Watch for filter changes to reset pagination
  watch([searchQuery, selectedType], () => {
    currentPage.value = 1
  })
  
  // Lifecycle
  onMounted(() => {
    fetchFollowedOrganizations()
  })
  </script>
  
  <style scoped>
  .n-statistic {
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    padding: 16px 24px;
    background: #fafafa;
  }
  
  .n-layout-header {
    display: flex;
    align-items: center;
  }
  </style>