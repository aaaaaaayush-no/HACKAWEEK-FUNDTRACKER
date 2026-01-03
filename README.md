# HACKAWEEK-FUNDTRACKER

Government Fund Tracking System with JWT authentication and role-based access control.

## 🚀 Quick Start

### Option 1: Using the Setup Script (Recommended)

```bash
# Install and start backend
./start-backend.sh
```

### Option 2: Manual Setup

#### Backend Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
cd fundtracker
python manage.py migrate

# Start server
python manage.py runserver 8000
```

#### Frontend Setup
```bash
# In a new terminal
npm install
npm start
```

## 📚 Documentation

- **[TESTING.md](TESTING.md)** - Comprehensive testing guide with all features and API examples
- **Backend API**: http://127.0.0.1:8000/api/
- **Frontend**: http://localhost:3000

## ✅ Verify Backend is Working

```bash
# Test API endpoint
curl http://127.0.0.1:8000/api/

# Expected response:
# {"projects":"http://127.0.0.1:8000/api/projects/", ...}
```

## 🔑 Features

- JWT-based authentication
- 4 user roles: PUBLIC, CONTRACTOR, GOVERNMENT, AUDITOR
- Progress submission and approval workflow
- Complete audit trail
- Role-based dashboards

## 🛠️ Troubleshooting

If you get "ModuleNotFoundError: No module named 'django'":
```bash
pip install -r requirements.txt
```

If you get database errors:
```bash
cd fundtracker
python manage.py migrate
```

See [TESTING.md](TESTING.md) for more troubleshooting tips.
