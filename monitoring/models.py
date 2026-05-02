from django.db import models
from django.contrib.auth import get_user_model
from cryptography.fernet import Fernet
from django.conf import settings
import uuid

User = get_user_model()

class SecurityDevice(models.Model):
    DEVICE_TYPES = (
        ('camera', 'CCTV Camera'),
        ('access_control', 'Access Control System'),
        ('alarm', 'Alarm System'),
        ('sensor', 'Motion/Temperature Sensor'),
    )
    
    device_id = models.UUIDField(default=uuid.uuid4, unique=True)
    device_name = models.CharField(max_length=100)
    device_type = models.CharField(max_length=20, choices=DEVICE_TYPES)
    location = models.CharField(max_length=200)
    ip_address = models.GenericIPAddressField()
    api_key_encrypted = models.TextField()
    is_active = models.BooleanField(default=True)
    last_heartbeat = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def set_api_key(self, api_key):
        cipher = Fernet(settings.ENCRYPTION_KEY.encode())
        self.api_key_encrypted = cipher.encrypt(api_key.encode()).decode()
    
    def get_api_key(self):
        cipher = Fernet(settings.ENCRYPTION_KEY.encode())
        return cipher.decrypt(self.api_key_encrypted.encode()).decode()
    
    def __str__(self):
        return f"{self.device_name} - {self.location}"

class AccessLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    access_type = models.CharField(max_length=50)
    location = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    is_authorized = models.BooleanField(default=False)
    notes = models.TextField(null=True, blank=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['timestamp', 'location']),
            models.Index(fields=['user', 'is_authorized']),
        ]
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.user.username} - {self.access_type} at {self.location}"

class SecurityEvent(models.Model):
    EVENT_TYPES = (
        ('unauthorized_access', 'Unauthorized Access'),
        ('suspicious_activity', 'Suspicious Activity'),
        ('device_failure', 'Device Failure'),
        ('security_breach', 'Security Breach'),
        ('emergency', 'Emergency'),
    )
    
    SEVERITY = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    )
    
    event_id = models.UUIDField(default=uuid.uuid4, unique=True)
    event_type = models.CharField(max_length=50, choices=EVENT_TYPES)
    severity = models.CharField(max_length=10, choices=SEVERITY)
    description = models.TextField()
    location = models.CharField(max_length=200)
    detected_by = models.ForeignKey(SecurityDevice, on_delete=models.SET_NULL, null=True)
    resolved = models.BooleanField(default=False)
    resolved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    screenshot = models.ImageField(upload_to='security_events/', null=True, blank=True)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.get_event_type_display()} - {self.severity} at {self.location}"

class CCTVFeed(models.Model):
    camera = models.ForeignKey(SecurityDevice, on_delete=models.CASCADE)
    stream_url_encrypted = models.TextField()
    is_recording = models.BooleanField(default=False)
    recording_started_at = models.DateTimeField(null=True, blank=True)
    motion_detection = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def set_stream_url(self, url):
        cipher = Fernet(settings.ENCRYPTION_KEY.encode())
        self.stream_url_encrypted = cipher.encrypt(url.encode()).decode()
    
    def get_stream_url(self):
        cipher = Fernet(settings.ENCRYPTION_KEY.encode())
        return cipher.decrypt(self.stream_url_encrypted.encode()).decode()
    
    def __str__(self):
        return f"Feed for {self.camera.device_name}"