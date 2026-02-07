from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Broker
from .serializers import BrokerSerializer


class BrokerListView(generics.ListAPIView):
    """List all active brokers."""
    serializer_class = BrokerSerializer
    permission_classes = [IsAuthenticated]
    queryset = Broker.objects.filter(is_active=True)


class BrokerDetailView(generics.RetrieveAPIView):
    """Get broker details by code."""
    serializer_class = BrokerSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'code'
    queryset = Broker.objects.filter(is_active=True)
