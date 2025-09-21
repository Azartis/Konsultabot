"""
URL configuration for konsultabot_backend project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

def api_status(request):
    return JsonResponse({
        'status': 'success',
        'message': 'Konsultabot Django Backend is running!',
        'version': '1.0.0',
        'endpoints': {
            'admin': '/admin/',
            'users': '/api/users/',
            'chat': '/api/chat/',
            'api_docs': '/api/'
        }
    })

urlpatterns = [
    path('', api_status, name='api_status'),
    path('api/', api_status, name='api_root'),
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/chat/', include('chat.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
