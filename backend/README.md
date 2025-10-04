# OrgTracker Backend

Django REST Framework API for organization management and user authentication.

## Architecture

- **Django 5.2.6** with REST Framework
- **JWT Authentication** via dj-rest-auth
- **PostgreSQL** database
- **Docker** containerized development

## Apps Structure

```
backend/apps/
├── core/           # Shared utilities and base models
├── organization/   # Organization CRUD and filtering
└── userbase/      # User management and follow system
```

## API Endpoints

### Authentication (`/api/userbase/auth/`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/registration/` | User registration | No |
| POST | `/login/` | User login | No |
| POST | `/logout/` | User logout | Yes |
| GET | `/user/` | Get user profile | Yes |
| POST | `/password/change/` | Change password | Yes |

**Registration Request:**
```json
{
    "username": "testuser",
    "email": "test@example.com",
    "password1": "securepass123",
    "password2": "securepass123",
    "first_name": "Test",
    "last_name": "User"
}
```

### Organizations (`/api/organizations/`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/` | List/filter organizations | No |
| POST | `/` | Create organization | Yes |
| GET | `/{slug}/` | Get organization detail | No |
| PUT | `/{slug}/` | Update organization | Yes |
| PATCH | `/{slug}/` | Partial update | Yes |
| DELETE | `/{slug}/` | Delete organization | Yes |

**Organization Model:**
```python
{
    "name": "string",           # Organization name
    "slug": "auto-generated",   # SEO-friendly URL slug
    "logo": "image_file",       # Logo upload (optional)
    "org_type": 0-3,           # Organization type
    "nation": "country_code",   # ISO country code
    "founding_date": "YYYY-MM-DD",
    "headcount": "integer"      # Employee count (optional)
}
```

**Organization Types:**
- `0`: Sole proprietorship
- `1`: Holding company
- `2`: Small and medium-sized enterprises (SME)
- `3`: Civil society organization (NGO)

### Advanced Filtering

Filter organizations using query parameters:

```
GET /api/organizations/?country=TR&org_type=2,3&headcount_max=50
```

**Available Filters:**
- `name` - Contains search (case-insensitive)
- `org_type` - Comma-separated values: `2,3`
- `country` - ISO country code: `TR`, `US`, `DE`
- `founding_date_from` - Date: `2000-01-01`
- `founding_date_to` - Date: `2025-12-31`
- `headcount_min` - Minimum employees: `10`
- `headcount_max` - Maximum employees: `100`

**Example Queries:**
```bash
# Turkish SMEs and NGOs under 50 employees
/api/organizations/?country=TR&org_type=2,3&headcount_max=50

# US tech companies founded after 2000
/api/organizations/?country=US&name=tech&founding_date_from=2000-01-01

# Large corporations (>1000 employees)
/api/organizations/?headcount_min=1000
```

### Follow System (`/api/userbase/`)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/follow/{slug}/` | Follow organization | Yes |
| POST | `/unfollow/{slug}/` | Unfollow organization | Yes |
| GET | `/followed-organizations/` | List followed orgs | Yes |

## Development Setup

### Local Development

1. **Install dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Environment variables**
   Create `.env` file or set via Docker Compose.

3. **Database setup**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py load_sample_organizations
   ```

4. **Run development server**
   ```bash
   python manage.py runserver
   ```

### Docker Development

```bash
# From project root
docker-compose up backend
```

### Management Commands

```bash
# Load 100 sample organizations
python manage.py load_sample_organizations

# Create admin user
python manage.py createsuperuser

# Run tests
python manage.py test

# Access Django shell
python manage.py shell
```

## Authentication

### JWT Token Flow

1. **Registration/Login** returns JWT token
2. **API Requests** include: `Authorization: Token <jwt_token>`
3. **Token** required for write operations and follow system

### User Model Extensions

Custom User model includes:
- Standard Django User fields
- `followed_organizations` - ManyToMany relationship

## Database Models

### Organization Model
```python
class Organization(models.Model):
    name = models.CharField(max_length=50)
    logo = models.ImageField(upload_to=image_path, null=True, blank=True)
    org_type = models.IntegerField(choices=OrgType.choices)
    nation = CountryField(blank_label="(select country)")
    founding_date = models.DateField()
    headcount = models.PositiveIntegerField(null=True, blank=True)
    slug = AutoSlugField(populate_from="name", unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### User Model
```python
class User(AbstractUser):
    followed_organizations = models.ManyToManyField(
        Organization,
        blank=True,
        related_name="followers"
    )
```

## API Documentation

Interactive documentation available at:
- **Swagger UI**: http://localhost:8000/api/docs/
- **ReDoc**: http://localhost:8000/api/redoc/

## Testing

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test apps.organization

# Test with coverage
coverage run --source='.' manage.py test
coverage report
```

## Production Considerations

### Settings
- Set `DEBUG=False`
- Use strong `SECRET_KEY`
- Configure `ALLOWED_HOSTS`
- Set up proper logging

### Database
- Use PostgreSQL in production# frontend
