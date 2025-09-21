from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserProfile

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'student_id', 'first_name', 'last_name', 'course', 'year_level', 'is_active', 'created_at')
    list_filter = ('is_active', 'course', 'year_level', 'created_at')
    search_fields = ('email', 'student_id', 'first_name', 'last_name')
    ordering = ('-created_at',)
    
    fieldsets = UserAdmin.fieldsets + (
        ('EVSU Student Info', {
            'fields': ('student_id', 'course', 'year_level')
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('EVSU Student Info', {
            'fields': ('student_id', 'course', 'year_level')
        }),
    )

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'preferred_language', 'voice_enabled', 'notifications_enabled', 'theme_preference')
    list_filter = ('preferred_language', 'voice_enabled', 'notifications_enabled', 'theme_preference')
    search_fields = ('user__email', 'user__student_id', 'user__first_name', 'user__last_name')
