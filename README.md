# Link Shortener Backend

A modular Django-based link shortener system with **Role-Based Access Control (RBAC)**, JWT authentication, privacy-safe click analytics, and admin dashboard. **Designed for mobile apps** with JSON API responses.

## Features

### Role-Based Access Control (RBAC)

Three distinct roles with hierarchical permissions:

1. **Guest** (Unauthenticated users)
   - Shorten links with random code
   - Shorten links with custom alias

2. **User** (Authenticated users)
   - All Guest permissions
   - Add notes to links
   - Edit destination URL
   - View click statistics (total clicks, timestamps)

3. **Admin** (System administrators)
   - All User permissions
   - View, edit, activate/deactivate, or delete any link
   - Manage users: create, edit, delete
   - Access dashboard and system settings

- **User Management**
  - User registration and JWT authentication
  - Two roles: User and Admin
  - Admin APIs to create, edit, delete, and list users
  - User filtering and search by username, email, role, and active status

- **Link Management**
  - Shorten URLs with random or custom aliases
  - Edit destination URL or add notes
  - Admin can view, edit, activate/deactivate, or delete any link
  - API for status check (active/inactive) of links
  - List links by specific user (Admin only)
  - Pagination support for all list endpoints

- **Click Analytics (Privacy-Safe)**
  - Track only total clicks and timestamps
  - No IP addresses, referrers, or user-agents stored
  - APIs to get total clicks per link and click timestamps
  - Statistical grouping by day (last 30 days) and week (last 12 weeks)
  - Display recent click timestamps in link details

- **Admin Dashboard**
  - Django Admin interface with django-jazzmin theme
  - Display users, links, and click counts
  - Filters for links and users
  - Dashboard summary with total links and clicks

- **API Documentation**
  - OpenAPI/Swagger documentation using drf-spectacular
  - Interactive API testing interface
  - Comprehensive endpoint documentation with examples

## Tech Stack

- **Backend**: Django 5.0, Django REST Framework
- **Database**: PostgreSQL 15
- **Authentication**: JWT (djangorestframework-simplejwt)
- **API Docs**: drf-spectacular
- **Admin UI**: django-jazzmin
- **Containerization**: Docker, Docker Compose

## Quick Start

### Prerequisites

- Docker and Docker Compose installed
- Python 3.11+ (for local development)

### Installation

1. **Clone the repository**
   \`\`\`bash
   git clone <repository-url>
   cd link-shortener-backend
   \`\`\`

2. **Run setup script**
   \`\`\`bash
   chmod +x scripts/setup.sh
   ./scripts/setup.sh
   \`\`\`

   Or manually:

3. **Create environment file**
   \`\`\`bash
   cp .env.example .env
   \`\`\`
   Edit `.env` and update the values as needed.

4. **Start with Docker**
   \`\`\`bash
   docker-compose up --build
   \`\`\`

5. **Run migrations**
   \`\`\`bash
   docker-compose exec web python manage.py migrate
   \`\`\`

6. **Setup RBAC system**
   \`\`\`bash
   docker-compose exec web python manage.py setup_rbac
   \`\`\`

7. **Create admin user**
   \`\`\`bash
   docker-compose exec web python manage.py create_admin
   \`\`\`

8. **Access the application**
   - API: http://localhost:8000/api/
   - API Docs: http://localhost:8000/api/docs/
   - Admin Dashboard: http://localhost:8000/admin/
   - Login with credentials: admin / admin123

## API Endpoints

### Authentication
- `POST /api/users/register/` - Register new user
- `POST /api/users/login/` - Login and get JWT tokens
- `POST /api/token/refresh/` - Refresh access token
- `GET /api/users/me/` - Get current user profile

### Links
- `GET /api/links/list/` - List all links (filtered by user/admin, paginated)
- `POST /api/links/` - Create new short link
- `GET /api/links/user/{user_id}/` - List links for specific user (Admin only)
- `GET /api/links/{id}/` - Get link details (includes click timestamps)
- `PATCH /api/links/{id}/update/` - Update link
- `DELETE /api/links/{id}/delete/` - Delete link (Admin only)
- `GET /api/links/{id}/stats/` - Get link statistics (daily/weekly grouping)
- `POST /api/links/{id}/toggle-active/` - Toggle link active status (Admin only)
- `GET /api/links/{id}/check-status/` - Check if link is active

### Users (Admin only)
- `GET /api/users/users/` - List all users (with filtering and search)
  - Query params: `?search=username`, `?is_active=true`, `?role__name=User`, `?ordering=-created_at`
- `GET /api/users/users/{id}/` - Get user details
- `PUT /api/users/users/{id}/update/` - Update user (full)
- `PATCH /api/users/users/{id}/update/` - Update user (partial)
- `DELETE /api/users/users/{id}/delete/` - Delete user

### Roles & Permissions
- `GET /api/users/roles/` - List all roles
- `GET /api/users/roles/{id}/` - Get role details
- `GET /api/users/roles/{id}/permissions/` - Get role permissions
- `GET /api/users/permissions/` - List all permissions (Admin only)
- `GET /api/users/permissions/{id}/` - Get permission details (Admin only)

### Analytics (Admin only)
- `GET /api/analytics/` - List all click stats
- `GET /api/analytics/{id}/` - Get click stat details
- `GET /api/analytics/global-stats/` - Get global statistics

### Redirect (Mobile App API)
- `GET /{short_code}/` - Get original URL for short code (returns JSON, tracks click)

**Mobile App Usage:**

This API is designed for mobile applications. Instead of server-side redirects, the redirect endpoint returns JSON with the original URL:

\`\`\`bash
# Request
GET /abc123/

# Response (200 OK)
{
  "short_code": "abc123",
  "original_url": "https://example.com",
  "is_active": true
}
\`\`\`

The mobile app should:
1. Call the redirect endpoint to get the original URL
2. The click is automatically tracked when the endpoint is called
3. Open the URL in the app (browser, webview, or in-app)

**Error Responses:**
- `404 Not Found` - Link does not exist
- `410 Gone` - Link is inactive

## Advanced Features

### Pagination

All list endpoints support pagination with the following query parameters:
- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 20)

Example: `GET /api/links/list/?page=2&page_size=10`

### Filtering & Search

**User List Filtering:**
- Filter by active status: `?is_active=true`
- Filter by role: `?role__name=User`
- Search by username or email: `?search=john`
- Order results: `?ordering=-created_at` (use `-` for descending)

Example: `GET /api/users/users/?is_active=true&role__name=Admin&search=admin&ordering=-created_at`

### Click Statistics

Link statistics include:
- **Total clicks**: Overall click count
- **Recent clicks**: Last 20 click timestamps
- **Daily clicks**: Click count grouped by day (last 30 days)
- **Weekly clicks**: Click count grouped by week (last 12 weeks)

Example response:
\`\`\`json
{
  "total_clicks": 150,
  "recent_clicks": [
    {"clicked_at": "2024-01-15T10:30:00Z"},
    {"clicked_at": "2024-01-15T09:15:00Z"}
  ],
  "daily_clicks": [
    {"day": "2024-01-15", "count": 25},
    {"day": "2024-01-14", "count": 30}
  ],
  "weekly_clicks": [
    {"week": "2024-01-08", "count": 120},
    {"week": "2024-01-01", "count": 95}
  ]
}
\`\`\`

### Permission-Based Access

All endpoints enforce role-based permissions:
- **Guest**: Can create links (no authentication required)
- **User**: Can manage their own links and view statistics
- **Admin**: Full access to all resources

## Project Structure

\`\`\`
link-shortener-backend/
├── config/                 # Django project settings
│   ├── settings/          # Split settings (base, dev, prod)
│   ├── urls.py           # Root URL configuration
│   └── wsgi.py           # WSGI configuration
├── users/                 # User management app
│   ├── models.py         # User model
│   ├── views.py          # User API views
│   ├── serializers.py    # User serializers
│   ├── services.py       # User business logic
│   ├── permissions.py    # Custom permissions
│   ├── management/       # Management commands
│   │   └── commands/
│   │       ├── setup_rbac.py    # Setup roles & permissions
│   │       └── create_admin.py  # Create admin user
│   └── tests/            # User tests
├── links/                 # Link management app
│   ├── models.py         # Link model
│   ├── views.py          # Link API views
│   ├── serializers.py    # Link serializers
│   ├── services.py       # Link business logic
│   └── tests/            # Link tests
├── analytics/             # Analytics app
│   ├── models.py         # ClickStats model
│   ├── views.py          # Analytics API views
│   ├── serializers.py    # Analytics serializers
│   ├── services.py       # Analytics business logic
│   └── tests/            # Analytics tests
├── common/                # Common utilities
│   ├── helpers.py        # Helper functions
│   └── tests/            # Common tests
├── docker-compose.yml    # Docker Compose configuration
├── Dockerfile            # Docker image configuration
├── requirements.txt      # Python dependencies
└── README.md            # This file
\`\`\`

## Role-Based Access Control (RBAC)

### Database Models

**Permission Model**
- `code`: Unique permission code (e.g., 'shorten_link_random')
- `name`: Human-readable name
- `description`: Permission description

**Role Model**
- `name`: Role name (Guest, User, Admin)
- `description`: Role description
- `permissions`: Many-to-many relationship with Permission

**User Model**
- Extends Django's AbstractUser
- `role`: Foreign key to Role model
- `has_permission(permission_code)`: Check if user has specific permission

### Permissions

**Guest Permissions:**
- `shorten_link_random` - Shorten links with random code
- `shorten_link_custom` - Shorten links with custom alias

**User Permissions (includes Guest):**
- `add_note` - Add notes to links
- `edit_link` - Edit destination URL
- `view_stats` - View click statistics

**Admin Permissions (includes User):**
- `manage_all_links` - View, edit, activate/deactivate, or delete any link
- `manage_users` - Create, edit, delete users
- `access_dashboard` - Access dashboard and system settings

### Permission Checking

Endpoints are protected using custom permission classes:
- `CanShortenLink` - All users including guests
- `CanAddNote` - User and Admin only
- `CanEditLink` - User and Admin only
- `CanViewStats` - User and Admin only
- `CanManageAllLinks` - Admin only
- `CanManageUsers` - Admin only

## Privacy-Safe Analytics

This system is designed with privacy in mind:

- **No personal data collection**: We do not store IP addresses, referrers, or user-agents
- **Minimal tracking**: Only link clicks and timestamps are recorded
- **GDPR compliant**: No personally identifiable information (PII) is collected
- **Transparent**: Users know exactly what data is being tracked

## Development

### Local Development (without Docker)

1. **Create virtual environment**
   \`\`\`bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   \`\`\`

2. **Install dependencies**
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

3. **Set up PostgreSQL**
   - Install PostgreSQL
   - Create database: `createdb linkshortener`
   - Update `.env` with database credentials

4. **Run migrations**
   \`\`\`bash
   python manage.py migrate
   \`\`\`

5. **Setup RBAC system**
   \`\`\`bash
   python manage.py setup_rbac
   \`\`\`

6. **Create admin user**
   \`\`\`bash
   python manage.py create_admin
   \`\`\`

7. **Run development server**
   \`\`\`bash
   python manage.py runserver
   \`\`\`

### Running Tests

\`\`\`bash
# Run all tests
docker-compose exec web pytest

# Run specific app tests
docker-compose exec web pytest users/tests/
docker-compose exec web pytest links/tests/
docker-compose exec web pytest analytics/tests/

# Run with coverage
docker-compose exec web pytest --cov=. --cov-report=html
\`\`\`

## Environment Variables

\`\`\`env
# Django settings
DJANGO_SETTINGS_MODULE=config.settings.dev
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=postgresql://postgres:postgres@db:5432/linkshortener

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
\`\`\`

## API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/api/docs/
- **OpenAPI Schema**: http://localhost:8000/api/schema/

The interactive documentation allows you to test all API endpoints directly from your browser.

## License

MIT License
