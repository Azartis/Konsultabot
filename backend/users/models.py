from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import EmailValidator, ValidationError
import re

class CustomUser(AbstractUser):
    """Extended user model for EVSU students"""
    student_id = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True, validators=[EmailValidator()])
    course = models.CharField(max_length=100, blank=True, null=True)
    year_level = models.IntegerField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(blank=True, null=True)
    
    # Fix the reverse accessor conflicts
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='customuser_set',
        related_query_name='customuser',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='customuser_set',
        related_query_name='customuser',
    )
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'student_id']
    
    def clean(self):
        super().clean()
        # Validate EVSU email domain
        if self.email and not self._is_evsu_email(self.email):
            raise ValidationError('Only EVSU email addresses are allowed')
    
    def _is_evsu_email(self, email):
        """Validate if email belongs to EVSU domain"""
        evsu_domains = ['@evsu.edu.ph', '@student.evsu.edu.ph']
        return any(email.lower().endswith(domain) for domain in evsu_domains)
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.student_id})"

class UserProfile(models.Model):
    """Additional user profile information"""
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    preferred_language = models.CharField(
        max_length=20, 
        choices=[
            ('english', 'English'),
            ('bisaya', 'Bisaya'),
            ('waray', 'Waray'),
            ('tagalog', 'Tagalog'),
        ],
        default='english'
    )
    voice_enabled = models.BooleanField(default=False)
    notifications_enabled = models.BooleanField(default=True)
    theme_preference = models.CharField(
        max_length=20,
        choices=[
            ('light', 'Light'),
            ('dark', 'Dark'),
            ('auto', 'Auto'),
        ],
        default='auto'
    )
    
    def __str__(self):
        return f"Profile for {self.user.get_full_name()}"
