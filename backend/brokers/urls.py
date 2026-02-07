from django.urls import path

from . import views
from portfolio.views import BrokerDiscoverView, BrokerDiscoverCompleteAuthView

urlpatterns = [
    path('brokers/', views.BrokerListView.as_view(), name='broker_list'),
    path('brokers/discover/', BrokerDiscoverView.as_view(), name='broker_discover'),
    path('brokers/discover/complete-auth/', BrokerDiscoverCompleteAuthView.as_view(), name='broker_discover_complete_auth'),
    path('brokers/<str:code>/', views.BrokerDetailView.as_view(), name='broker_detail'),
]
