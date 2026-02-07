from django.contrib import admin

from .models import ExchangeRate


@admin.register(ExchangeRate)
class ExchangeRateAdmin(admin.ModelAdmin):
    list_display = ['from_currency', 'to_currency', 'rate', 'rate_date', 'source']
    list_filter = ['from_currency', 'to_currency', 'source']
    search_fields = ['from_currency', 'to_currency']
    date_hierarchy = 'rate_date'
