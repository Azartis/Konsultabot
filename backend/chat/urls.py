from django.urls import path
from . import views

urlpatterns = [
    path('send/', views.send_message, name='send_message'),
    path('history/', views.conversation_history, name='conversation_history'),
    path('sessions/', views.chat_sessions, name='chat_sessions'),
    path('sessions/end/', views.end_session, name='end_session'),
    path('knowledge/', views.knowledge_base, name='knowledge_base'),
    path('campus-info/', views.campus_info, name='campus_info'),
    path('search/', views.search_knowledge, name='search_knowledge'),
]
