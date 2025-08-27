from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.utils import timezone
import logging

from .models import OTPCode
from .utils import send_otp_email, track_login_attempt, create_user_session, end_user_session

logger = logging.getLogger(__name__)


def login_with_otp(request):
    """Handle login with OTP authentication."""
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            otp = OTPCode.generate_otp(user, purpose='login')
            
            if send_otp_email(user, otp, 'login'):
                request.session['pending_login_user_id'] = user.id
                messages.success(request, f'OTP sent to {user.email}')
                track_login_attempt(request, username, True)
                return redirect('otp_auth:verify_otp')
            else:
                messages.error(request, 'Failed to send OTP.')
                track_login_attempt(request, username, False, 'OTP send failed')
        else:
            messages.error(request, 'Invalid credentials.')
            track_login_attempt(request, username, False, 'Invalid credentials')
    
    return render(request, 'otp_auth/login.html')


def verify_otp(request):
    """Verify OTP code and complete login."""
    if request.method == 'POST':
        otp_code = request.POST.get('otp_code', '').strip()
        user_id = request.session.get('pending_login_user_id')
        
        if not user_id:
            messages.error(request, 'Invalid session.')
            return redirect('otp_auth:login')
        
        try:
            user = User.objects.get(id=user_id)
            otp = OTPCode.objects.filter(
                user=user,
                code=otp_code,
                purpose='login',
                is_used=False
            ).first()
            
            if otp and otp.is_valid():
                otp.is_used = True
                otp.save()
                login(request, user)
                create_user_session(request, user)
                
                del request.session['pending_login_user_id']
                messages.success(request, f'Welcome back, {user.first_name or user.username}!')
                return redirect('mechanics:home')
            else:
                messages.error(request, 'Invalid or expired OTP.')
                
        except User.DoesNotExist:
            messages.error(request, 'User not found.')
    
    return render(request, 'otp_auth/verify_otp.html')


@login_required
def logout_with_session(request):
    """Logout user and end session."""
    if request.user.is_authenticated:
        end_user_session(request, request.user)
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('mechanics:home')
