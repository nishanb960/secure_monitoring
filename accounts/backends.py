from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

class EmailOrUsernameBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(
                Q(username=username) | Q(email=username)
            )
            if user.check_password(password):
                if not user.is_account_locked():
                    user.reset_login_attempts()
                    if request:
                        user.last_login_ip = self.get_client_ip(request)
                        user.save()
                    return user
                else:
                    user.increment_login_attempts()
            else:
                if user:
                    user.increment_login_attempts()
        except User.DoesNotExist:
            return None
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip