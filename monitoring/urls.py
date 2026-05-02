from django.urls import path
from . import views

app_name = 'monitoring'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('api/realtime/', views.realtime_monitor, name='realtime_api'),
    path('api/access-control/', views.access_control, name='access_control'),
]