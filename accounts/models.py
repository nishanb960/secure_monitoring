from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from cryptography.fernet import Fernet
from django.conf import settings

class User(AbstractUser):
    ROLE_CHOICES = (
        ('superadmin', 'Super Admin'),
        ('security', 'Security Personnel'),
        ('faculty', 'Faculty Member'),
        ('student', 'Student'),
        ('visitor', 'Visitor'),
    )
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    employee_id = models.CharField(max_length=50, unique=True, null=True, blank=True)
    phone_number = models.CharField(max_length=15)
    two_factor_enabled = models.BooleanField(default=False)
    otp_secret = models.CharField(max_length=100, null=True, blank=True)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    login_attempts = models.IntegerField(default=0)
    account_locked_until = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def is_account_locked(self):
        if self.account_locked_until and self.account_locked_until > timezone.now():
            return True
        return False
    
    def increment_login_attempts(self):
        self.login_attempts += 1
        if self.login_attempts >= 5:
            self.account_locked_until = timezone.now() + timezone.timedelta(minutes=30)
            self.login_attempts = 0
        self.save()
    
    def reset_login_attempts(self):
        self.login_attempts = 0
        self.account_locked_until = None
        self.save()
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        permissions = [
            ("view_monitoring_dashboard", "Can view monitoring dashboard"),
            ("manage_cctv_feed", "Can manage CCTV feeds"),
            ("view_access_logs", "Can view access logs"),
            ("manage_security_events", "Can manage security events"),
        ]

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
    department = models.CharField(max_length=100, null=True, blank=True)
    emergency_contact = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s profile"