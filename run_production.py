#!/usr/bin/env python
"""
Production startup script for MechLocator
Binds to 0.0.0.0:10000 for public internet access
"""

import os
import sys
import django
from django.core.management import execute_from_command_line
from django.core.wsgi import get_wsgi_application

def main():
    """Main function to start the Django development server for production"""
    
    # Set Django settings module
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mechlocator.settings')
    
    # Configure for production
    os.environ['DEBUG'] = 'False'
    os.environ['ALLOWED_HOSTS'] = '0.0.0.0,localhost,127.0.0.1,*'
    
    # Initialize Django
    django.setup()
    
    # Collect static files if needed
    if not os.path.exists('staticfiles'):
        print("Collecting static files...")
        execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])
    
    # Run migrations if needed
    print("Running migrations...")
    execute_from_command_line(['manage.py', 'migrate'])
    
    # Start the server
    print("Starting MechLocator on 0.0.0.0:10000...")
    print("Access your application at: http://your-server-ip:10000")
    print("Press Ctrl+C to stop the server")
    
    # Start Django development server on 0.0.0.0:10000
    execute_from_command_line([
        'manage.py', 
        'runserver', 
        '0.0.0.0:10000',
        '--noreload',  # Disable auto-reload for production
        '--nothreading',  # Single-threaded for better security
    ])

if __name__ == '__main__':
    main()
