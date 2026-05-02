from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
import json

@login_required
def dashboard(request):
    """Main monitoring dashboard"""
    context = {
        'user': request.user,
    }
    return render(request, 'monitoring/dashboard.html', context)

@login_required
def realtime_monitor(request):
    """API endpoint for real-time monitoring data"""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    
    try:
        from .models import SecurityEvent
        
        time_threshold = timezone.now() - timedelta(minutes=5)
        
        recent_events = SecurityEvent.objects.filter(
            timestamp__gte=time_threshold
        ).values('event_type', 'severity', 'location', 'timestamp')[:10]
        
        data = {
            'events': list(recent_events),
            'timestamp': timezone.now().isoformat(),
            'status': 'active'
        }
        return JsonResponse(data)
    except Exception as e:
        # Return empty data if models not yet created
        return JsonResponse({
            'events': [],
            'timestamp': timezone.now().isoformat(),
            'status': 'initializing'
        })

@login_required
def access_control(request):
    """Handle access control requests"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body) if request.body else {}
            location = data.get('location', 'unknown')
            access_type = data.get('access_type', 'entry')
            
            # Log access attempt
            try:
                from .models import AccessLog
                AccessLog.objects.create(
                    user=request.user if request.user.is_authenticated else None,
                    access_type=access_type,
                    location=location,
                    ip_address=request.META.get('REMOTE_ADDR'),
                    user_agent=request.META.get('HTTP_USER_AGENT', ''),
                    is_authorized=True
                )
            except:
                pass
            
            return JsonResponse({
                'access': 'granted',
                'message': f'Access granted to {location}',
                'user': request.user.username
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)