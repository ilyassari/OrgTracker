<template>
    <n-layout>
      <!-- Header -->
      <n-layout-header bordered style="height: 64px; padding: 0 24px;">
        <div style="display: flex; align-items: center; height: 100%; justify-content: space-between;">
          <div style="display: flex; align-items: center;">
            <h2 style="margin: 0; color: #18a058;">{{ appTitle }}</h2>
          </div>
          
          <!-- User menu -->
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
              <n-button type="primary" @click="$router.push('/register')">
                Register
              </n-button>
            </template>
          </div>
        </div>
      </n-layout-header>
  
      <n-layout-content style="padding: 24px;">
        <!-- Filters Section -->
        <n-card title="Filter Organizations" style="margin-bottom: 24px;">
          <n-form
            :model="filters"
            label-placement="left"
            label-width="120px"
          >
            <n-grid :cols="4" :x-gap="16" :y-gap="12">
              <!-- Name filter -->
              <n-grid-item>
                <n-form-item label="Name">
                  <n-input
                    v-model:value="filters.name"
                    placeholder="Search by name..."
                    clearable
                    @input="debouncedSearch"
                  />
                </n-form-item>
              </n-grid-item>
  
              <!-- Organization Type filter -->
              <n-grid-item>
                <n-form-item label="Type">
                  <n-select
                    v-model:value="filters.org_type"
                    multiple
                    :options="orgTypeOptions"
                    placeholder="Select types..."
                    clearable
                    @update:value="applyFilters"
                  />
                </n-form-item>
              </n-grid-item>
  
              <!-- Country filter -->
              <n-grid-item>
                <n-form-item label="Country">
                  <n-select
                    v-model:value="filters.country"
                    :options="countryOptions"
                    placeholder="Select country..."
                    clearable
                    filterable
                    @update:value="applyFilters"
                  />
                </n-form-item>
              </n-grid-item>
  
              <!-- Employee count range -->
              <n-grid-item>
                <n-form-item label="Employees">
                  <n-space>
                    <n-input-number
                      v-model:value="filters.headcount_min"
                      placeholder="Min"
                      :min="0"
                      style="width: 80px;"
                      @update:value="debouncedSearch"
                    />
                    <span>-</span>
                    <n-input-number
                      v-model:value="filters.headcount_max"
                      placeholder="Max"
                      :min="0"
                      style="width: 80px;"
                      @update:value="debouncedSearch"
                    />
                  </n-space>
                </n-form-item>
              </n-grid-item>
  
              <!-- Founding date range -->
              <n-grid-item :span="2">
                <n-form-item label="Founded">
                  <n-space>
                    <n-date-picker
                      v-model:value="filters.founding_date_from"
                      type="date"
                      placeholder="From date"
                      clearable
                      @update:value="applyFilters"
                    />
                    <n-date-picker
                      v-model:value="filters.founding_date_to"
                      type="date"
                      placeholder="To date"
                      clearable
                      @update:value="applyFilters"
                    />
                  </n-space>
                </n-form-item>
              </n-grid-item>
  
              <!-- Clear filters button -->
              <n-grid-item>
                <n-button @click="clearFilters" style="width: 100%;">
                  Clear Filters
                </n-button>
              </n-grid-item>
            </n-grid>
          </n-form>
        </n-card>
  
        <!-- Organizations Grid -->
        <n-spin :show="loading">
          <div v-if="organizations.length === 0 && !loading">
            <n-empty description="No organizations found">
              <template #extra>
                <n-button @click="clearFilters">Clear Filters</n-button>
              </template>
            </n-empty>
          </div>
  
          <n-grid v-else :cols="3" :x-gap="16" :y-gap="16">
            <n-grid-item v-for="org in organizations" :key="org.id">
              <OrganizationCard :organization="org" />
            </n-grid-item>
          </n-grid>
        </n-spin>
  
        <!-- Pagination -->
        <div style="display: flex; justify-content: center; margin-top: 24px;" v-if="pagination.totalPages > 1">
          <n-pagination
            v-model:page="pagination.currentPage"
            :page-count="pagination.totalPages"
            :page-size="pagination.pageSize"
            show-size-picker
            :page-sizes="[12, 24, 48]"
            @update:page="handlePageChange"
            @update:page-size="handlePageSizeChange"
          />
        </div>
      </n-layout-content>
    </n-layout>
  </template>
  
  <script setup>
  import { ref, reactive, onMounted, computed } from 'vue'
  import { useRouter } from 'vue-router'
  import { useMessage } from 'naive-ui'
  import OrganizationCard from '@/components/OrganizationCard.vue'
  import apiClient from '@/services/api'
  
  const router = useRouter()
  const message = useMessage()
  
  // Reactive data
  const organizations = ref([])
  const loading = ref(false)
  const isAuthenticated = ref(false)
  
  // App configuration
  const appTitle = import.meta.env.VITE_APP_TITLE || 'OrgTracker'
  
  // Filters
  const filters = reactive({
    name: '',
    org_type: [],
    country: '',
    founding_date_from: null,
    founding_date_to: null,
    headcount_min: null,
    headcount_max: null
  })
  
  // Pagination
  const pagination = reactive({
    currentPage: 1,
    pageSize: 12,
    totalPages: 1,
    totalCount: 0
  })
  
  // Filter options
  const orgTypeOptions = [
    { label: 'Sole proprietorship', value: 0 },
    { label: 'Holding', value: 1 },
    { label: 'Small and medium-sized enterprises', value: 2 },
    { label: 'Civil society organization', value: 3 }
  ]
  
  const countryOptions = [
    { label: 'Turkey', value: 'TR' },
    { label: 'United States', value: 'US' },
    { label: 'Germany', value: 'DE' },
    { label: 'South Korea', value: 'KR' },
    { label: 'Japan', value: 'JP' },
    { label: 'France', value: 'FR' },
    { label: 'United Kingdom', value: 'GB' },
    { label: 'Netherlands', value: 'NL' },
    { label: 'Switzerland', value: 'CH' },
    { label: 'China', value: 'CN' },
    { label: 'Italy', value: 'IT' },
    { label: 'Sweden', value: 'SE' },
    { label: 'Norway', value: 'NO' },
    { label: 'Finland', value: 'FI' },
    { label: 'Poland', value: 'PL' },
    { label: 'Czech Republic', value: 'CZ' },
    { label: 'Hungary', value: 'HU' }
  ]
  
  // Check authentication status
  const checkAuthStatus = () => {
    const token = localStorage.getItem('token')
    isAuthenticated.value = !!token
  }
  
  // Fetch organizations from API
  const fetchOrganizations = async () => {
    try {
      loading.value = true
      
      const params = {
        page: pagination.currentPage,
        page_size: pagination.pageSize
      }
  
      // Add filters to params
      if (filters.name) params.name = filters.name
      if (filters.org_type?.length) params.org_type = filters.org_type.join(',')
      if (filters.country) params.country = filters.country
      if (filters.founding_date_from) {
        params.founding_date_from = formatDate(filters.founding_date_from)
      }
      if (filters.founding_date_to) {
        params.founding_date_to = formatDate(filters.founding_date_to)
      }
      if (filters.headcount_min !== null && filters.headcount_min !== undefined) {
        params.headcount_min = filters.headcount_min
      }
      if (filters.headcount_max !== null && filters.headcount_max !== undefined) {
        params.headcount_max = filters.headcount_max
      }
  
      const response = await apiClient.get('/api/organizations/', { params })
      
      organizations.value = response.data.results || response.data
      
      // Handle pagination if API returns paginated response
      if (response.data.count !== undefined) {
        pagination.totalCount = response.data.count
        pagination.totalPages = Math.ceil(response.data.count / pagination.pageSize)
      }
      
    } catch (error) {
      console.error('Failed to fetch organizations:', error)
      message.error('Failed to load organizations')
      organizations.value = []
    } finally {
      loading.value = false
    }
  }
  
  // Format date for API
  const formatDate = (timestamp) => {
    if (!timestamp) return null
    const date = new Date(timestamp)
    return date.toISOString().split('T')[0]
  }
  
  // Debounced search for text inputs
  let searchTimeout = null
  const debouncedSearch = () => {
    if (searchTimeout) clearTimeout(searchTimeout)
    searchTimeout = setTimeout(() => {
      pagination.currentPage = 1 // Reset to first page on search
      fetchOrganizations()
    }, 500)
  }
  
  // Apply filters immediately
  const applyFilters = () => {
    pagination.currentPage = 1 // Reset to first page on filter
    fetchOrganizations()
  }
  
  // Clear all filters
  const clearFilters = () => {
    Object.keys(filters).forEach(key => {
      if (Array.isArray(filters[key])) {
        filters[key] = []
      } else {
        filters[key] = key.includes('headcount') ? null : ''
      }
    })
    filters.founding_date_from = null
    filters.founding_date_to = null
    pagination.currentPage = 1
    fetchOrganizations()
  }
  
  // Pagination handlers
  const handlePageChange = (page) => {
    pagination.currentPage = page
    fetchOrganizations()
  }
  
  const handlePageSizeChange = (pageSize) => {
    pagination.pageSize = pageSize
    pagination.currentPage = 1
    fetchOrganizations()
  }
  
  // Logout functionality
  const handleLogout = () => {
    localStorage.removeItem('token')
    isAuthenticated.value = false
    message.success('Logged out successfully')
  }
  
  // Component lifecycle
  onMounted(() => {
    checkAuthStatus()
    fetchOrganizations()
  })
  </script>
  
  <style scoped>
  .n-layout-header {
    display: flex;
    align-items: center;
  }
  </style>