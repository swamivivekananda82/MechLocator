from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from mechanics.admin import admin_site, CustomUserAdmin
from django.contrib.auth.models import User

# Register custom admin configurations with default admin site
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

urlpatterns = [
    path('admin/', admin.site.urls),  # Use default admin with custom configurations
    path('', include('mechanics.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('otp/', include('otp_auth.urls')),  # OTP authentication
]

# Serve static and media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
