#!/bin/bash
# Simple startup script for MechLocator on Render

echo "🚗 MechLocator - Starting up..."

# Set environment variables
export DJANGO_SETTINGS_MODULE=mechlocator.settings
export DEBUG=False
export ALLOWED_HOSTS="mechlocator.onrender.com,localhost,127.0.0.1"

# Get port from environment
PORT=${PORT:-10000}

echo "🌐 Using port: $PORT"

# Run migrations
echo "🔄 Running migrations..."
python manage.py migrate

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Start Gunicorn
echo "🚀 Starting Gunicorn server..."
gunicorn mechlocator.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 2 \
    --timeout 30 \
    --keep-alive 2 \
    --max-requests 1000 \
    --max-requests-jitter 50 \
    --access-logfile - \
    --error-logfile - \
    --log-level info
