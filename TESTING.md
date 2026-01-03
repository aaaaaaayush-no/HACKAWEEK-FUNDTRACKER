# Testing Guide for Government Fund Tracker

This guide explains how to test the authentication system and role-based access control features.

## Prerequisites

Before testing, ensure you have:
- Python 3.x installed
- Node.js and npm installed
- All dependencies installed (see Installation section below)

## Installation

### Backend Setup

1. Navigate to the Django backend directory:
```bash
cd fundtracker
```

2. Install Python dependencies:
```bash
pip install -r ../requirements.txt
```

3. Run database migrations:
```bash
python manage.py migrate
```

4. Create a superuser (optional, for admin access):
```bash
python manage.py createsuperuser
```

5. Start the Django development server:
```bash
python manage.py runserver 8000
```

The backend API will be available at: `http://127.0.0.1:8000/api/`

### Frontend Setup

1. In a new terminal, navigate to the project root:
```bash
cd /path/to/HACKAWEEK-FUNDTRACKER
```

2. Install npm dependencies:
```bash
npm install
```

3. Start the React development server:
```bash
npm start
```

The frontend will be available at: `http://localhost:3000`

## Testing the System

### 1. Testing User Registration

#### Via Web UI:
1. Open `http://localhost:3000/register`
2. Fill in the registration form:
   - Username: `testcontractor`
   - Email: `contractor@test.com`
   - Password: `testpass123`
   - Confirm Password: `testpass123`
   - Role: Select `Contractor`
3. Click "Register"
4. You should be automatically logged in and redirected to the Contractor Dashboard

#### Via API (using curl):
```bash
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testcontractor",
    "password": "testpass123",
    "email": "contractor@test.com",
    "role": "CONTRACTOR"
  }'
```

Expected response:
```json
{
  "user": {
    "id": 1,
    "username": "testcontractor",
    "email": "contractor@test.com",
    "role": "CONTRACTOR"
  },
  "tokens": {
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  }
}
```

### 2. Testing User Login

#### Via Web UI:
1. Open `http://localhost:3000/login`
2. Enter credentials:
   - Username: `testcontractor`
   - Password: `testpass123`
3. Click "Login"
4. You should be redirected to your role-specific dashboard

#### Via API (using curl):
```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testcontractor",
    "password": "testpass123"
  }'
```

Expected response includes JWT tokens and user info.

### 3. Testing Role-Based Dashboards

Create test users for each role:

#### Contractor User:
```bash
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username": "contractor1", "password": "pass123", "role": "CONTRACTOR"}'
```
Access: `http://localhost:3000/contractor`

#### Government User:
```bash
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username": "govuser", "password": "pass123", "role": "GOVERNMENT"}'
```
Access: `http://localhost:3000/government`

#### Auditor User:
```bash
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username": "auditor1", "password": "pass123", "role": "AUDITOR"}'
```
Access: `http://localhost:3000/audit-log`

### 4. Testing Progress Submission (Contractor)

1. Log in as a contractor user
2. Navigate to the Contractor Dashboard
3. Fill in the progress submission form:
   - Select a project from the dropdown
   - Enter Physical Progress (e.g., 25%)
   - Enter Financial Progress (e.g., 20%)
   - (Optional) Upload evidence images
4. Click "Submit Progress"
5. You should see a success message
6. The submission will appear in "Recent Submissions" with status "PENDING"

#### Via API:
```bash
# First, get your access token from login
TOKEN="your_access_token_here"

curl -X POST http://127.0.0.1:8000/api/progress/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "project": 1,
    "physical_progress": 25,
    "financial_progress": 20
  }'
```

### 5. Testing Progress Approval (Government)

1. Log in as a government user
2. Navigate to the Government Dashboard
3. You should see pending progress submissions in the "Pending Progress Approvals" section
4. Click "Approve" or "Reject" on a pending submission
5. The submission status will update accordingly
6. An audit log entry will be created

#### Via API:
```bash
# Use government user's access token
TOKEN="government_user_token"

# Approve progress with ID 2
curl -X POST http://127.0.0.1:8000/api/progress/2/approve/ \
  -H "Authorization: Bearer $TOKEN"

# Or reject it
curl -X POST http://127.0.0.1:8000/api/progress/2/reject/ \
  -H "Authorization: Bearer $TOKEN"
```

### 6. Testing Audit Log (Auditor)

1. Log in as an auditor user
2. Navigate to the Audit Log page
3. You should see all system activities:
   - User registrations
   - Progress submissions
   - Approvals/rejections
   - Fund releases
4. Use the filter dropdown to filter by action type (CREATE, UPDATE, DELETE)

#### Via API:
```bash
TOKEN="auditor_token"

curl -X GET http://127.0.0.1:8000/api/audit-logs/ \
  -H "Authorization: Bearer $TOKEN"
```

### 7. Testing Public Access

1. Open `http://localhost:3000/` (without logging in)
2. You should see the Public Dashboard with all projects
3. Use the search bar to filter projects by name, location, or ministry
4. Click "View Details" on any project to see detailed information
5. Navigation should show "Home", "Login", and "Register" options

### 8. Testing Protected Routes

Try accessing protected routes without authentication:
- `http://localhost:3000/contractor` → Should redirect to login
- `http://localhost:3000/government` → Should redirect to login
- `http://localhost:3000/audit-log` → Should redirect to login

Try accessing routes with wrong role:
- Login as CONTRACTOR
- Try to access `http://localhost:3000/government` → Should redirect to home
- Try to access `http://localhost:3000/audit-log` → Should redirect to home

### 9. Testing Token Expiration

1. Log in to the application
2. The access token expires after 5 hours
3. When a token expires and you make a request, you should be automatically redirected to the login page

### 10. Testing API Endpoints

#### Get All Projects (Public):
```bash
curl -X GET http://127.0.0.1:8000/api/projects/
```

#### Get User Profile (Authenticated):
```bash
TOKEN="your_access_token"
curl -X GET http://127.0.0.1:8000/api/auth/profile/ \
  -H "Authorization: Bearer $TOKEN"
```

#### Get Pending Progress (Authenticated):
```bash
TOKEN="your_access_token"
curl -X GET http://127.0.0.1:8000/api/progress/pending/ \
  -H "Authorization: Bearer $TOKEN"
```

## Expected User Flows

### Contractor Flow:
1. Register/Login → Contractor Dashboard
2. Select project and submit progress with evidence
3. View submission history and status (PENDING/APPROVED/REJECTED)

### Government Flow:
1. Register/Login → Government Dashboard
2. View pending progress submissions
3. Approve or reject submissions
4. View project statistics and fund releases

### Auditor Flow:
1. Register/Login → Audit Log
2. View all system activities
3. Filter activities by type
4. Monitor transparency and compliance

### Public User Flow:
1. Visit site (no login required)
2. View all projects with progress
3. Search/filter projects
4. View detailed project information

## Troubleshooting

### Backend Issues:

**Port already in use:**
```bash
# Kill the process using port 8000
lsof -ti:8000 | xargs kill -9
```

**Database issues:**
```bash
# Reset database
rm fundtracker/db.sqlite3
python manage.py migrate
```

### Frontend Issues:

**Port already in use:**
```bash
# Kill the process using port 3000
lsof -ti:3000 | xargs kill -9
```

**Module not found:**
```bash
# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install
```

## Testing Checklist

- [ ] User can register with all 4 roles
- [ ] User can login and receive JWT tokens
- [ ] User is redirected to correct dashboard based on role
- [ ] Contractor can submit progress
- [ ] Government can approve/reject progress
- [ ] Auditor can view audit logs
- [ ] Public can view projects without login
- [ ] Protected routes are inaccessible without proper authentication
- [ ] Token expiration works correctly
- [ ] All API endpoints return expected responses
- [ ] UI is responsive on mobile devices
- [ ] Logout functionality works correctly

## Additional Testing

### Admin Interface:
1. Access Django admin at `http://127.0.0.1:8000/admin/`
2. Login with superuser credentials
3. View and manage:
   - Users and UserProfiles
   - Projects and Progress
   - Funds and Audit Logs

### API Documentation:
- Django REST Framework browsable API: `http://127.0.0.1:8000/api/`
- Navigate through endpoints and test them directly in the browser

## Performance Testing

For load testing the API:
```bash
# Install Apache Bench
sudo apt-get install apache2-utils

# Test registration endpoint
ab -n 100 -c 10 -p register.json -T application/json http://127.0.0.1:8000/api/auth/register/

# Create register.json with:
# {"username":"testuser","password":"pass123","role":"PUBLIC"}
```

## Security Testing

1. **SQL Injection:** Try entering SQL commands in form fields
2. **XSS:** Try entering `<script>alert('XSS')</script>` in text fields
3. **CSRF:** Django's CSRF protection should be active
4. **JWT Security:** Tokens should be stored securely in localStorage
5. **Password Security:** Passwords should never be visible in responses

## Need Help?

If you encounter issues:
1. Check the browser console for frontend errors
2. Check the Django console for backend errors
3. Ensure both servers are running
4. Verify all dependencies are installed
5. Check that you're using the correct URLs and ports
