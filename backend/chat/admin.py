from django.contrib import admin
from .models import KnowledgeBase, CampusInfo, Conversation, ChatSession

@admin.register(KnowledgeBase)
class KnowledgeBaseAdmin(admin.ModelAdmin):
    list_display = ('category', 'question', 'language', 'confidence_score', 'is_active', 'created_at')
    list_filter = ('category', 'language', 'is_active', 'created_at')
    search_fields = ('question', 'answer', 'keywords')
    list_editable = ('is_active', 'confidence_score')
    ordering = ('-confidence_score', '-created_at')

@admin.register(CampusInfo)
class CampusInfoAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'language', 'is_active', 'created_at')
    list_filter = ('category', 'language', 'is_active', 'created_at')
    search_fields = ('title', 'content', 'tags')
    list_editable = ('is_active',)
    ordering = ('-created_at',)

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message_preview', 'language_detected', 'mode', 'confidence_score', 'timestamp')
    list_filter = ('language_detected', 'mode', 'timestamp')
    search_fields = ('user__email', 'user__student_id', 'message', 'response')
    readonly_fields = ('timestamp',)
    ordering = ('-timestamp',)
    
    def message_preview(self, obj):
        return obj.message[:50] + "..." if len(obj.message) > 50 else obj.message
    message_preview.short_description = 'Message'

@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ('session_id', 'user', 'message_count', 'is_active', 'started_at', 'ended_at')
    list_filter = ('is_active', 'started_at')
    search_fields = ('session_id', 'user__email', 'user__student_id')
    readonly_fields = ('started_at', 'ended_at')
    ordering = ('-started_at',)
