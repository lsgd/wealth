from django.contrib import admin

from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'base_currency', 'auto_sync_enabled', 'last_sync_at']
    list_filter = ['base_currency', 'auto_sync_enabled']
    search_fields = ['user__username', 'user__email']
