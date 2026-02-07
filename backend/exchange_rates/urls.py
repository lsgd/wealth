from django.urls import path

from . import views

urlpatterns = [
    path('exchange-rates/', views.ExchangeRateListView.as_view(), name='exchange_rate_list'),
    path('exchange-rates/sync/', views.ExchangeRateSyncView.as_view(), name='exchange_rate_sync'),
]
