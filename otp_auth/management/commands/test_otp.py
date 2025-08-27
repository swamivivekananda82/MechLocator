from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from otp_auth.models import OTPCode
from otp_auth.utils import send_otp_email


class Command(BaseCommand):
    help = 'Test OTP generation and email sending'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username to test OTP for')

    def handle(self, *args, **options):
        username = options['username']
        
        try:
            user = User.objects.get(username=username)
            self.stdout.write(f"Testing OTP for user: {user.username} ({user.email})")
            
            # Generate OTP
            otp = OTPCode.generate_otp(user, purpose='login')
            self.stdout.write(f"Generated OTP: {otp.code}")
            self.stdout.write(f"Expires at: {otp.expires_at}")
            
            # Send email
            if send_otp_email(user, otp, 'login'):
                self.stdout.write(
                    self.style.SUCCESS(f"OTP email sent successfully to {user.email}")
                )
            else:
                self.stdout.write(
                    self.style.ERROR("Failed to send OTP email")
                )
                
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f"User '{username}' not found")
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"Error: {str(e)}")
            )
