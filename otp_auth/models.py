from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import random
import string


class OTPCode(models.Model):
    """Model for storing OTP codes for user authentication."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    purpose = models.CharField(max_length=20, choices=[
        ('login', 'Login'),
        ('password_reset', 'Password Reset'),
        ('email_verification', 'Email Verification'),
    ])
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"OTP for {self.user.username} - {self.purpose}"
    
    def is_expired(self):
        """Check if OTP has expired."""
        return timezone.now() > self.expires_at
    
    def is_valid(self):
        """Check if OTP is valid (not used and not expired)."""
        return not self.is_used and not self.is_expired()
    
    @classmethod
    def generate_otp(cls, user, purpose='login', expiry_minutes=10):
        """Generate a new OTP for the user."""
        # Delete any existing unused OTPs for this user and purpose
        cls.objects.filter(
            user=user, 
            purpose=purpose, 
            is_used=False
        ).update(is_used=True)
        
        # Generate 6-digit OTP
        code = ''.join(random.choices(string.digits, k=6))
        
        # Create new OTP
        otp = cls.objects.create(
            user=user,
            code=code,
            expires_at=timezone.now() + timezone.timedelta(minutes=expiry_minutes),
            purpose=purpose
        )
        
        return otp


class UserSession(models.Model):
    """Model for tracking user login sessions."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session_key = models.CharField(max_length=40)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    login_time = models.DateTimeField(auto_now_add=True)
    logout_time = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-login_time']
    
    def __str__(self):
        return f"Session for {self.user.username} - {self.login_time}"
    
    def end_session(self):
        """End the current session."""
        self.logout_time = timezone.now()
        self.is_active = False
        self.save()


class LoginAttempt(models.Model):
    """Model for tracking login attempts for security."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    username = models.CharField(max_length=150)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    attempt_time = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField(default=False)
    failure_reason = models.CharField(max_length=100, blank=True)
    
    class Meta:
        ordering = ['-attempt_time']
    
    def __str__(self):
        status = "Success" if self.success else "Failed"
        return f"Login attempt for {self.username} - {status}"
