from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.conf import settings
import os

@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """Health check endpoint"""
    return Response({
        'status': 'healthy',
        'message': 'Konsultabot API is running',
        'version': '1.0.0'
    })

@api_view(['GET'])
@permission_classes([AllowAny])
def api_status(request):
    """API status and configuration info"""
    return Response({
        'app_name': getattr(settings, 'APP_NAME', 'Konsultabot'),
        'campus_name': getattr(settings, 'CAMPUS_NAME', 'EVSU DULAG'),
        'google_ai_configured': bool(getattr(settings, 'GOOGLE_API_KEY', '')),
        'debug_mode': settings.DEBUG,
        'database': 'sqlite3',
        'features': {
            'multi_language': True,
            'voice_support': False,  # Will be handled by mobile app
            'google_ai': bool(getattr(settings, 'GOOGLE_API_KEY', '')),
            'knowledge_base': True,
            'user_authentication': True
        }
    })
