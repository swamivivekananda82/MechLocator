import logging
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.models import User
from .models import OTPCode, UserSession, LoginAttempt
from django.utils import timezone
from datetime import timedelta

logger = logging.getLogger(__name__)


def send_otp_email(user, otp_code, purpose='login'):
    """Send OTP code to user's email."""
    try:
        subject = get_email_subject(purpose)
        html_message = render_otp_email_template(user, otp_code, purpose)
        plain_message = strip_tags(html_message)
        
        # Send email
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        
        logger.info(f"OTP email sent to {user.email} for {purpose}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send OTP email to {user.email}: {str(e)}")
        return False


def get_email_subject(purpose):
    """Get email subject based on purpose."""
    subjects = {
        'login': 'MechLocator - Your Login OTP Code',
        'password_reset': 'MechLocator - Password Reset OTP',
        'email_verification': 'MechLocator - Email Verification OTP',
    }
    return subjects.get(purpose, 'MechLocator - OTP Code')


def render_otp_email_template(user, otp_code, purpose):
    """Render OTP email template."""
    context = {
        'user': user,
        'otp_code': otp_code.code,
        'purpose': purpose,
        'expires_in': '10 minutes',
        'app_name': 'MechLocator',
        'current_time': timezone.now(),
    }
    
    template_name = f'otp_auth/emails/{purpose}_otp.html'
    return render_to_string(template_name, context)


def send_login_alert_email(user, session_info):
    """Send login alert email to user."""
    try:
        subject = 'MechLocator - New Login Detected'
        html_message = render_login_alert_template(user, session_info)
        plain_message = strip_tags(html_message)
        
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        
        logger.info(f"Login alert email sent to {user.email}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send login alert email to {user.email}: {str(e)}")
        return False


def render_login_alert_template(user, session_info):
    """Render login alert email template."""
    context = {
        'user': user,
        'session_info': session_info,
        'app_name': 'MechLocator',
        'current_time': timezone.now(),
    }
    
    return render_to_string('otp_auth/emails/login_alert.html', context)


def get_client_ip(request):
    """Get client IP address from request."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def track_login_attempt(request, username, success, failure_reason=''):
    """Track login attempt for security monitoring."""
    try:
        user = User.objects.filter(username=username).first()
        ip_address = get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        
        LoginAttempt.objects.create(
            user=user,
            username=username,
            ip_address=ip_address,
            user_agent=user_agent,
            success=success,
            failure_reason=failure_reason
        )
        
    except Exception as e:
        logger.error(f"Failed to track login attempt: {str(e)}")


def create_user_session(request, user):
    """Create a new user session record."""
    try:
        ip_address = get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        session_key = request.session.session_key
        
        UserSession.objects.create(
            user=user,
            session_key=session_key,
            ip_address=ip_address,
            user_agent=user_agent,
        )
        
    except Exception as e:
        logger.error(f"Failed to create user session: {str(e)}")


def end_user_session(request, user):
    """End user session."""
    try:
        session_key = request.session.session_key
        UserSession.objects.filter(
            user=user,
            session_key=session_key,
            is_active=True
        ).update(
            logout_time=timezone.now(),
            is_active=False
        )
        
    except Exception as e:
        logger.error(f"Failed to end user session: {str(e)}")


def get_recent_login_attempts(username, hours=24):
    """Get recent login attempts for a username."""
    cutoff_time = timezone.now() - timedelta(hours=hours)
    return LoginAttempt.objects.filter(
        username=username,
        attempt_time__gte=cutoff_time
    ).order_by('-attempt_time')


def is_account_locked(username, max_attempts=5, lockout_hours=1):
    """Check if account is locked due to too many failed attempts."""
    recent_attempts = get_recent_login_attempts(username, lockout_hours)
    failed_attempts = recent_attempts.filter(success=False)
    
    return failed_attempts.count() >= max_attempts
