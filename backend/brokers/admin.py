from django.contrib import admin

from .models import Broker


@admin.register(Broker)
class BrokerAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'integration_type', 'country', 'is_active', 'supports_2fa']
    list_filter = ['integration_type', 'country', 'is_active']
    search_fields = ['name', 'code']
    readonly_fields = ['created_at', 'updated_at']
