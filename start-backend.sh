#!/bin/bash

# Quick Start Script for Fund Tracker Backend
# This script sets up and runs the Django backend

echo "=========================================="
echo "Fund Tracker Backend Setup"
echo "=========================================="
echo ""

# Check if we're in the right directory
if [ ! -f "requirements.txt" ]; then
    echo "❌ Error: requirements.txt not found!"
    echo "Please run this script from the project root directory."
    exit 1
fi

echo "📦 Step 1: Installing Python dependencies..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies!"
    exit 1
fi

echo "✅ Dependencies installed successfully!"
echo ""

cd fundtracker

echo "🔧 Step 2: Running database migrations..."
python manage.py migrate

if [ $? -ne 0 ]; then
    echo "❌ Failed to run migrations!"
    exit 1
fi

echo "✅ Migrations completed successfully!"
echo ""

echo "✨ Step 3: Creating sample data (optional)..."
python manage.py shell << 'EOF'
from django.contrib.auth.models import User
from core.models import UserProfile, Project, Progress, Fund
from datetime import date

# Create sample projects if they don't exist
if Project.objects.count() == 0:
    project1 = Project.objects.create(
        name="Road Expansion Project",
        location="Kathmandu ward 10",
        ministry="Ministry of Infrastructure",
        contractor="ABC Construction",
        total_budget=500000.00,
        start_date=date(2026, 1, 1),
        end_date=date(2027, 1, 1)
    )
    
    project2 = Project.objects.create(
        name="School Building Project",
        location="Kathmandu ward 5",
        ministry="Ministry of Education",
        contractor="XYZ Builders",
        total_budget=300000.00,
        start_date=date(2026, 1, 15),
        end_date=date(2026, 12, 31)
    )
    
    # Create sample funds
    Fund.objects.create(project=project1, amount=150000.00)
    Fund.objects.create(project=project2, amount=100000.00)
    
    print("✅ Created sample projects and funds")
else:
    print("ℹ️  Sample projects already exist")
EOF

echo ""
echo "=========================================="
echo "🚀 Starting Django Development Server"
echo "=========================================="
echo ""
echo "Backend API will be available at:"
echo "  http://127.0.0.1:8000/api/"
echo ""
echo "Press CTRL+C to stop the server"
echo ""

python manage.py runserver 8000
