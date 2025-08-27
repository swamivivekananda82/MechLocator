from django.urls import path
from . import views

app_name = 'otp_auth'

urlpatterns = [
    path('login/', views.login_with_otp, name='login'),
    path('verify/', views.verify_otp, name='verify_otp'),
    path('logout/', views.logout_with_session, name='logout'),
]
