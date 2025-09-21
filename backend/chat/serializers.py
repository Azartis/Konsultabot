from rest_framework import serializers
from .models import KnowledgeBase, CampusInfo, Conversation, ChatSession

class KnowledgeBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = KnowledgeBase
        fields = '__all__'

class CampusInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampusInfo
        fields = '__all__'

class ConversationSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    
    class Meta:
        model = Conversation
        fields = ['id', 'user', 'user_name', 'message', 'response', 'language_detected', 
                 'mode', 'confidence_score', 'response_time', 'timestamp']
        read_only_fields = ['id', 'user', 'timestamp']

class ChatMessageSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=2000)
    language = serializers.CharField(max_length=20, required=False, default='english')
    session_id = serializers.CharField(max_length=100, required=False, allow_blank=True, allow_null=True)

class ChatResponseSerializer(serializers.Serializer):
    response = serializers.CharField()
    language = serializers.CharField()
    intent = serializers.CharField()
    mode = serializers.CharField()
    confidence = serializers.FloatField()
    response_time = serializers.FloatField()
    session_id = serializers.CharField()

class ChatSessionSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    
    class Meta:
        model = ChatSession
        fields = ['id', 'user', 'user_name', 'session_id', 'started_at', 
                 'ended_at', 'is_active', 'message_count']
        read_only_fields = ['id', 'user', 'started_at', 'ended_at']
