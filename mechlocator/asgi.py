"""
ASGI config for mechlocator project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mechlocator.settings')

application = get_asgi_application()
