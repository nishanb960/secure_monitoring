from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.cache import cache
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import get_user_model

User = get_user_model()

@never_cache
@csrf_protect
def login_view(request):
    if request.user.is_authenticated:
        return redirect('monitoring:dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Check rate limiting
        ip = request.META.get('REMOTE_ADDR')
        cache_key = f'login_attempts_{ip}'
        attempts = cache.get(cache_key, 0)
        
        if attempts >= 10:
            messages.error(request, 'Too many login attempts. Try again later.')
            return render(request, 'accounts/login.html')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Check if account is locked
            if hasattr(user, 'is_account_locked') and user.is_account_locked():
                messages.error(request, 'Account is locked. Try again after 30 minutes.')
                return render(request, 'accounts/login.html')
            
            login(request, user)
            cache.delete(cache_key)
            
            # Log login action
            try:
                from logs.models import AuditLog
                AuditLog.objects.create(
                    user=user,
                    action='LOGIN',
                    status_code=200,
                    ip_address=request.META.get('REMOTE_ADDR'),
                    user_agent=request.META.get('HTTP_USER_AGENT', '')
                )
            except:
                pass 
            
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('monitoring:dashboard')
        else:
            cache.set(cache_key, attempts + 1, 300)  # 5 minutes
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'accounts/login.html')

@login_required
def logout_view(request):
    # Log logout
    try:
        from logs.models import AuditLog
        AuditLog.objects.create(
            user=request.user,
            action='LOGOUT',
            status_code=200,
            ip_address=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
    except:
        pass
    
    logout(request)
    messages.success(request, 'Successfully logged out')
    return redirect('accounts:login')

# Temporarily disable 2FA views
def setup_2fa(request):
    messages.info(request, '2FA setup coming soon')
    return redirect('monitoring:dashboard')

def verify_2fa(request):
    return redirect('accounts:login')