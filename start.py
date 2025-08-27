#!/usr/bin/env python
"""
Simple startup script for MechLocator on Render
"""

import os
import sys
import django
from django.core.management import execute_from_command_line

# Set up environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mechlocator.settings')
os.environ['DEBUG'] = 'False'
os.environ['ALLOWED_HOSTS'] = '0.0.0.0,localhost,127.0.0.1,*'

# Initialize Django
django.setup()

def main():
    print("🚗 MechLocator - Starting up...")
    
    # Get port from environment (Render sets this)
    port = os.environ.get('PORT', '10000')
    print(f"🌐 Using port: {port}")
    
    # Create migrations
    print("🔄 Creating migrations...")
    execute_from_command_line(['manage.py', 'makemigrations'])
    
    # Apply migrations
    print("🔄 Applying migrations...")
    execute_from_command_line(['manage.py', 'migrate'])
    
    # Create superuser if needed
    print("👤 Checking for superuser...")
    try:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser('admin', 'admin@mechlocator.com', 'admin123456')
            print("✅ Superuser created: admin/admin123456")
        else:
            print("✅ Superuser already exists")
    except Exception as e:
        print(f"⚠️ Could not create superuser: {e}")
    
    # Populate sample data
    print("🔄 Populating sample data...")
    try:
        execute_from_command_line(['manage.py', 'populate_sample_data'])
    except Exception as e:
        print(f"⚠️ Sample data population failed: {e}")
    
    # Collect static files
    print("📁 Collecting static files...")
    try:
        execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])
    except Exception as e:
        print(f"⚠️ Static file collection failed: {e}")
    
    # Start server
    print(f"🚀 Starting MechLocator on 0.0.0.0:{port}...")
    print(f"🌐 Access your application at: http://your-server-ip:{port}")
    
    execute_from_command_line([
        'manage.py', 
        'runserver', 
        f'0.0.0.0:{port}',
        '--noreload',
        '--nothreading'
    ])

if __name__ == '__main__':
    main()
