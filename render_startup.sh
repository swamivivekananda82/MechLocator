#!/bin/bash

# MechLocator Render Startup Script
# This script sets up the database and starts the server

echo "🚗 MechLocator - Starting up on Render..."
echo "=========================================="

# Set environment variables
export DJANGO_SETTINGS_MODULE=mechlocator.settings
export DEBUG=False
export ALLOWED_HOSTS="0.0.0.0,localhost,127.0.0.1,*"

# Get port from environment (Render sets this)
PORT=${PORT:-10000}
echo "🌐 Using port: $PORT"

# Create database migrations
echo "🔄 Creating database migrations..."
python manage.py makemigrations

# Apply migrations
echo "🔄 Applying database migrations..."
python manage.py migrate

# Create superuser if it doesn't exist
echo "👤 Checking for superuser..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    User.objects.create_superuser('admin', 'admin@mechlocator.com', 'admin123456')
    print('✅ Superuser created: admin/admin123456')
else:
    print('✅ Superuser already exists')
"

# Populate sample data
echo "🔄 Populating sample data..."
python manage.py populate_sample_data

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Start the server
echo "🚀 Starting MechLocator on 0.0.0.0:$PORT..."
echo "🌐 Access your application at: http://your-server-ip:$PORT"
echo "Press Ctrl+C to stop the server"

# Start Django development server
python manage.py runserver 0.0.0.0:$PORT --noreload --nothreading
