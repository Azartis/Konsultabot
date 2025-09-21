from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class KnowledgeBase(models.Model):
    """Knowledge base for AI responses"""
    LANGUAGE_CHOICES = [
        ('english', 'English'),
        ('bisaya', 'Bisaya'),
        ('waray', 'Waray'),
        ('tagalog', 'Tagalog'),
    ]
    
    CATEGORY_CHOICES = [
        ('greeting', 'Greeting'),
        ('enrollment', 'Enrollment'),
        ('academics', 'Academics'),
        ('schedule', 'Schedule'),
        ('facilities', 'Facilities'),
        ('financial', 'Financial'),
        ('services', 'Services'),
        ('campus', 'Campus'),
        ('general', 'General'),
    ]
    
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    question = models.TextField()
    answer = models.TextField()
    language = models.CharField(max_length=20, choices=LANGUAGE_CHOICES, default='english')
    keywords = models.TextField(help_text="Comma-separated keywords for matching")
    confidence_score = models.FloatField(default=1.0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-confidence_score', '-created_at']
    
    def __str__(self):
        return f"{self.category} - {self.question[:50]}..."

class CampusInfo(models.Model):
    """Campus-specific information"""
    CATEGORY_CHOICES = [
        ('academics', 'Academics'),
        ('facilities', 'Facilities'),
        ('services', 'Services'),
        ('contact', 'Contact'),
        ('events', 'Events'),
        ('announcements', 'Announcements'),
    ]
    
    LANGUAGE_CHOICES = [
        ('english', 'English'),
        ('bisaya', 'Bisaya'),
        ('waray', 'Waray'),
        ('tagalog', 'Tagalog'),
    ]
    
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    title = models.CharField(max_length=200)
    content = models.TextField()
    language = models.CharField(max_length=20, choices=LANGUAGE_CHOICES, default='english')
    tags = models.CharField(max_length=500, help_text="Comma-separated tags")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title

class Conversation(models.Model):
    """Chat conversation history"""
    MODE_CHOICES = [
        ('online', 'Online'),
        ('offline', 'Offline'),
    ]
    
    LANGUAGE_CHOICES = [
        ('english', 'English'),
        ('bisaya', 'Bisaya'),
        ('waray', 'Waray'),
        ('tagalog', 'Tagalog'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversations')
    message = models.TextField()
    response = models.TextField()
    language_detected = models.CharField(max_length=20, choices=LANGUAGE_CHOICES, default='english')
    mode = models.CharField(max_length=20, choices=MODE_CHOICES, default='offline')
    confidence_score = models.FloatField(default=0.0)
    response_time = models.FloatField(default=0.0, help_text="Response time in seconds")
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"

class ChatSession(models.Model):
    """Chat session management"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_sessions')
    session_id = models.CharField(max_length=100, unique=True)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    message_count = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-started_at']
    
    def __str__(self):
        return f"Session {self.session_id} - {self.user.get_full_name()}"
