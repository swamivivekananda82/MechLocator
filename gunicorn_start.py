#!/usr/bin/env python
"""
Gunicorn startup script for MechLocator on Render
Handles database setup and starts Gunicorn server
"""

import os
import sys
import django
import subprocess
from pathlib import Path

def setup_environment():
    """Set up environment variables for production"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mechlocator.settings')
    os.environ['DEBUG'] = 'False'
    os.environ['ALLOWED_HOSTS'] = 'mechlocator.onrender.com,localhost,127.0.0.1'
    
    # Set port for Render (Render provides PORT environment variable)
    port = os.environ.get('PORT', '10000')
    os.environ['PORT'] = port

def run_command(command, description):
    """Run a Django management command"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Error: {e.stderr}")
        return False

def setup_database():
    """Set up the database with migrations and sample data"""
    print("🗄️ Setting up database...")
    
    # Run makemigrations
    if not run_command(['python', 'manage.py', 'makemigrations'], "Creating migrations"):
        return False
    
    # Run migrate
    if not run_command(['python', 'manage.py', 'migrate'], "Applying migrations"):
        return False
    
    # Create superuser if it doesn't exist
    print("👤 Checking for superuser...")
    try:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        if not User.objects.filter(is_superuser=True).exists():
            print("👤 Creating superuser...")
            # Create a default superuser
            User.objects.create_superuser(
                username='admin',
                email='mechlocator.org@gmail.com',
                password='admin123456'
            )
            print("✅ Superuser created: admin/admin123456")
        else:
            print("✅ Superuser already exists")
    except Exception as e:
        print(f"⚠️ Could not create superuser: {e}")
    
    # Populate sample data
    if not run_command(['python', 'manage.py', 'populate_sample_data'], "Populating sample data"):
        print("⚠️ Sample data population failed, continuing...")
    
    return True

def collect_static_files():
    """Collect static files"""
    print("📁 Collecting static files...")
    return run_command(['python', 'manage.py', 'collectstatic', '--noinput'], "Collecting static files")

def start_gunicorn():
    """Start the Gunicorn server"""
    port = os.environ.get('PORT', '10000')
    
    print(f"🚀 Starting MechLocator with Gunicorn on 0.0.0.0:{port}...")
    print(f"🌐 Access your application at: https://mechlocator.onrender.com")
    
    # Start Gunicorn
    try:
        subprocess.run([
            'gunicorn',
            'mechlocator.wsgi:application',
            f'--bind=0.0.0.0:{port}',
            '--workers=2',
            '--timeout=30',
            '--keep-alive=2',
            '--max-requests=1000',
            '--max-requests-jitter=50',
            '--access-logfile=-',
            '--error-logfile=-',
            '--log-level=info'
        ], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Server failed to start: {e}")
        return False
    
    return True

def main():
    """Main function"""
    print("🚗 MechLocator - Starting up with Gunicorn...")
    print("=" * 50)
    
    # Setup environment
    setup_environment()
    
    # Initialize Django
    django.setup()
    
    # Setup database
    if not setup_database():
        print("❌ Database setup failed. Exiting...")
        sys.exit(1)
    
    # Collect static files
    if not collect_static_files():
        print("⚠️ Static file collection failed, continuing...")
    
    # Start Gunicorn server
    if not start_gunicorn():
        print("❌ Server failed to start. Exiting...")
        sys.exit(1)

if __name__ == '__main__':
    main()
