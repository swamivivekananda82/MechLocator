#!/bin/bash
# Build script for MechLocator on Render

echo "🚗 MechLocator - Building..."

# Install dependencies
pip install -r requirements.txt

# Run migrations
echo "🔄 Running migrations..."
python manage.py makemigrations
python manage.py migrate

# Create superuser if it doesn't exist
echo "👤 Checking for superuser..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    User.objects.create_superuser('admin', 'mechlocator.org@gmail.com', 'admin123456')
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

echo "✅ Build completed successfully!"
