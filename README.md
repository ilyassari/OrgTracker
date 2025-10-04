# OrgTracker - Organization Management System

Full-stack web application for tracking and managing organizations with advanced filtering and user follow functionality.
This document was prepared based on the [study case](./study_case.md).  

## Overview

OrgTracker allows users to browse organizations, filter them by multiple criteria, follow organizations of interest, and manage their profile. Built with Django REST Framework backend and Vue.js frontend.

## Features

- User authentication (register, login, logout)
- Organization browsing with advanced filtering
- Follow/unfollow organizations
- User profile and followed organizations management
- Pre-loaded sample organizations
- Interactive API documentation
- Fully dockerized development environment

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd OrgTracker/project
   ```

2. **Create environment file**
   
   Create `.env.dev` file in project root:
   ```env
   DEBUG=1
   SECRET_KEY=your-secret-key-change-in-production
   DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
   CORS_ALLOWED_HOSTS=http://localhost:5173
   
   DATABASE=postgres
   SQL_ENGINE=django.db.backends.postgresql
   SQL_DATABASE=orgtracker_db
   SQL_USER=postgres
   SQL_PASSWORD=postgres123
   SQL_HOST=db
   SQL_PORT=5432
   
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=postgres123
   POSTGRES_DB=orgtracker_db
   
   DJANGO_SUPERUSER_USERNAME=admin
   DJANGO_SUPERUSER_EMAIL=admin@orgtracker.com
   DJANGO_SUPERUSER_PASSWORD=Admin123*
   
   BASE_URL=http://localhost:8000
   VITE_API_BASE_URL=http://localhost:8000
   VITE_APP_TITLE=OrgTracker
   ```

3. **Start the application**
   ```bash
   docker-compose up --build
   ```

   This will automatically:
   - Initialize PostgreSQL database
   - Run Django migrations
   - Create admin user & test users
   - Load 100 sample organizations
   - Start backend server on port 8000
   - Start frontend server on port 5173

4. **Access the application**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - Admin Panel: http://localhost:8000/admin
   - API Docs: http://localhost:8000/api/docs

## Project Structure

```
project/
├── backend/                # Django REST API
│   ├── apps/
│   │   ├── organization/   # Organization management
│   │   ├── userbase/       # User & follow system
│   │   └── core/           # Shared utilities
│   ├── config/             # Django settings
│   └── README.md           # Backend documentation
│
├── frontend/               # Vue.js application
│   ├── src/
│   │   ├── components/     # Reusable components
│   │   ├── views/          # Page components
│   │   ├── services/       # API client
│   │   └── router/         # Routing
│   └── README.md           # Frontend documentation
│
├── docker-compose.yml      # Development environment
├── .env.dev                # Environment variables
└── README.md               # This file
```

## Technology Stack

**Backend:**
- Django 5.2.6
- Django REST Framework 3.16.1
- PostgreSQL 15.0
- JWT Authentication

**Frontend:**
- Vue.js 3
- Vite 7.1.6
- Naive UI
- Axios

**DevOps:**
- Docker & Docker Compose
- PostgreSQL Container

## Basic Usage

### Default Admin Account
- Username: `admin`
- Password: `Admin123*`
- Access: http://localhost:8000/admin

### API Documentation
Interactive Swagger documentation available at: http://localhost:8000/api/docs

### Sample Organizations
100 organizations automatically loaded on first run including corporations, SMEs, and NGOs from various countries.

## Development

For detailed development instructions, see:
- [Backend README](backend/README.md) - API development, models, tests
- [Frontend README](frontend/README.md) - Component development, routing, state

### Common Commands

```bash
# View logs
docker-compose logs -f

# Restart services
docker-compose restart

# Stop services
docker-compose down

# Rebuild containers
docker-compose up --build

# Access backend shell
docker exec -it orgtracker-backend bash

# Access frontend shell
docker exec -it orgtracker-frontend sh
```

## Testing

```bash
# Backend tests
docker exec orgtracker-backend python manage.py test

# View test coverage
docker exec orgtracker-backend python manage.py test --verbosity=2
```

Test Results: 51/53 tests passing (96% success rate)

## Documentation

- **Main README** (this file): Quick start and overview
- **[Backend README](backend/README.md)**: API endpoints, models, development
- **[Frontend README](frontend/README.md)**: Components, routing, state management

## Troubleshooting

### Port conflicts
If ports 8000 or 5173 are already in use:
```bash
# Find and kill process
lsof -ti:8000 | xargs kill -9
lsof -ti:5173 | xargs kill -9
```

### Database issues
```bash
# Reset database
docker-compose down -v
docker-compose up --build
```

### Container issues
```bash
# Remove all containers and rebuild
docker-compose down
docker system prune -a
docker-compose up --build
```

## Production Deployment

For production deployment:
1. Create `.env.prod` with production values
2. Set `DEBUG=0`
3. Use strong `SECRET_KEY`
4. Configure `ALLOWED_HOSTS`
5. Use production WSGI server (Gunicorn)
6. Set up Nginx reverse proxy

## License

MIT License
