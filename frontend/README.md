# OrgTracker Frontend

Vue.js 3 application with Vite for organization browsing, filtering, and user management.

## Overview

Modern, responsive frontend application for the OrgTracker platform. Built with Vue 3, Vite, and Naive UI component library.

## Technology Stack

- **Vue.js 3** - Progressive JavaScript framework with Composition API
- **Vite 7.1.6** - Fast build tool and dev server with HMR
- **Naive UI** - Modern Vue 3 component library
- **Axios** - Promise-based HTTP client
- **Vue Router 4** - Official router for Vue.js
- **Pinia** - Vue store (not yet implemented, ready for use)

## Features

### User Interface
- **Organization List** - Grid view with cards, pagination, search
- **Advanced Filtering** - Name, type, country, date range, employee count
- **Organization Detail** - Complete organization information page
- **Follow System** - Follow/unfollow organizations with visual feedback
- **Followed Organizations** - Personal list with search and filters
- **User Profile** - Account information and statistics
- **Authentication** - Login and registration pages
- **Responsive Design** - Mobile-friendly layout

### User Experience
- Loading states and spinners
- Empty state handling
- Error messages and notifications
- Confirmation dialogs
- Form validation
- Hot module replacement (HMR)
- Smooth transitions

## Development Setup

### Prerequisites

- Node.js 20 or higher
- npm or yarn package manager

### Local Development

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Environment configuration**
   
   Environment variables are loaded from project root `.env.dev` file:
   ```env
   VITE_API_BASE_URL=http://localhost:8000
   VITE_APP_TITLE=OrgTracker
   ```

4. **Start development server**
   ```bash
   npm run dev
   ```
   
   Application will be available at http://localhost:5173

### Docker Development

```bash
# From project root
docker-compose up frontend
```

The Docker setup includes:
- Hot module replacement
- Volume mounting for live code changes
- Host binding for external access
- Node modules isolation

## Available Scripts

```bash
# Development server with hot reload
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Lint code
npm run lint
```

## Project Structure

```
frontend/
├── public/              # Static assets
├── src/
│   ├── components/      # Reusable Vue components
│   │   ├── OrganizationCard.vue
│   │   ├── FollowedOrgCard.vue
│   │   └── ...
│   ├── views/          # Page components
│   │   ├── OrganizationList.vue
│   │   ├── OrganizationDetail.vue
│   │   ├── auth/
│   │   │   ├── LoginForm.vue
│   │   │   └── RegisterForm.vue
│   │   └── user/
│   │       ├── UserProfile.vue
│   │       └── FollowedOrganizations.vue
│   ├── router/         # Vue Router configuration
│   │   └── index.js
│   ├── services/       # API service functions
│   │   └── api.js
│   ├── assets/         # Build-time assets (CSS, images)
│   ├── App.vue         # Root component
│   └── main.js         # Application entry point
├── package.json
├── vite.config.js      # Vite configuration
└── jsconfig.json       # JavaScript configuration
```

## Core Components

### Organization Components
- **OrganizationList.vue** - Main listing page with advanced filters
- **OrganizationCard.vue** - Individual organization card with follow button
- **OrganizationDetail.vue** - Detailed organization view
- **FilterPanel** - Integrated into list view for filtering

### User Components  
- **LoginForm.vue** - User login with validation
- **RegisterForm.vue** - User registration with custom fields
- **UserProfile.vue** - Profile management and statistics
- **FollowedOrganizations.vue** - User's followed organizations list
- **FollowedOrgCard.vue** - Card for followed organizations

### Shared Components
- **App.vue** - Root application with Naive UI providers
- **NotFound.vue** - 404 error page

## API Integration

### Base Configuration

```javascript
// services/api.js
import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  }
})

// Request interceptor for authentication
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Token ${token}`
  }
  return config
})

export default apiClient
```

### Authentication Flow
```javascript
// Register
POST /api/userbase/auth/registration/
→ Returns token → Store in localStorage → Redirect to home

// Login
POST /api/userbase/auth/login/
→ Returns token → Store in localStorage → Redirect to intended page

// Logout
→ Remove token from localStorage → Redirect to home
```

### Organizations API
```javascript
// List with filters
GET /api/organizations/?country=TR&org_type=2,3

// Get detail
GET /api/organizations/{slug}/

// Create (authenticated)
POST /api/organizations/
Authorization: Token <token>
```

### Follow System
```javascript
// Follow
POST /api/userbase/follow/{slug}/
Authorization: Token <token>

// Unfollow
POST /api/userbase/unfollow/{slug}/
Authorization: Token <token>

// List followed
GET /api/userbase/followed-organizations/
Authorization: Token <token>
```

## Routing

```javascript
// router/index.js
const routes = [
  { path: '/', component: OrganizationList },
  { path: '/organizations/:slug', component: OrganizationDetail },
  { path: '/login', component: LoginForm, meta: { guestOnly: true } },
  { path: '/register', component: RegisterForm, meta: { guestOnly: true } },
  { path: '/profile', component: UserProfile, meta: { requiresAuth: true } },
  { path: '/followed', component: FollowedOrganizations, meta: { requiresAuth: true } },
  { path: '/:pathMatch(.*)*', component: NotFound }
]
```

**Route Guards:**
- `requiresAuth` - Redirects to login if not authenticated
- `guestOnly` - Redirects authenticated users away from login/register
- Redirect query parameter for post-login navigation

## State Management

Currently using localStorage for:
- JWT token
- User information

Authentication state checked via:
```javascript
const token = localStorage.getItem('token')
const isAuthenticated = !!token
```

**Note:** Pinia store ready for implementation if needed for complex state management.


## Form Handling

### Organization Filters
```javascript
const filters = reactive({
  name: '',
  org_type: [],
  country: '',
  founding_date_from: null,
  founding_date_to: null,
  headcount_min: null,
  headcount_max: null
})
```

### Debounced Search
```javascript
let searchTimeout = null
const debouncedSearch = () => {
  if (searchTimeout) clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    fetchOrganizations()
  }, 500)
}
```

### Form Validation
```javascript
const rules = {
  username: [
    { required: true, message: 'Username is required' },
    { min: 3, message: 'Username must be at least 3 characters' }
  ],
  email: [
    { required: true, message: 'Email is required' },
    { type: 'email', message: 'Please enter a valid email' }
  ]
}
```

## Build and Deployment

### Development Build
```bash
npm run dev
# Runs on http://localhost:5173 with HMR
```

### Production Build
```bash
npm run build
# Output in dist/ directory
# Optimized, minified, tree-shaken
```

### Preview Production Build
```bash
npm run preview
# Test production build locally
```

## Environment Variables

### Development (.env.dev in project root)
```env
VITE_API_BASE_URL=http://localhost:8000
VITE_APP_TITLE=OrgTracker
```

**Note:** Vite only exposes variables prefixed with `VITE_` to the client.

## Performance Considerations

### Optimization
- Component lazy loading with dynamic imports
- Debounced search inputs (500ms)
- Pagination to limit data fetching
- Image lazy loading for logos
- API response caching consideration

### Bundle Size
```bash
npm run build -- --report
# Analyze bundle size
```

## Common Tasks

### Adding a New Page
1. Create component in `src/views/`
2. Add route in `src/router/index.js`
3. Add navigation link if needed

### Adding API Endpoint
1. Add method to `src/services/api.js` or create new service file
2. Use in component with error handling

### Adding Component
1. Create in `src/components/`
2. Import and use in views
3. Document props and events

## Troubleshooting

### Port Already in Use
```bash
# Kill process on port 5173
lsof -ti:5173 | xargs kill -9
```

### Module Not Found
```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

### HMR Not Working
- Check Docker volume mounts
- Ensure CHOKIDAR_USEPOLLING=true in docker-compose

### Build Fails
```bash
# Check for TypeScript/ESLint errors
npm run lint
```

## Resources

- [Vue.js Documentation](https://vuejs.org/)
- [Vite Documentation](https://vitejs.dev/)
- [Naive UI Components](https://www.naiveui.com/)
- [Vue Router Documentation](https://router.vuejs.org/)
- [Axios Documentation](https://axios-http.com/)