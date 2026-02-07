from rest_framework import serializers

from .models import Broker


class BrokerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Broker
        fields = [
            'id', 'code', 'name', 'integration_type',
            'country', 'is_active', 'supports_2fa',
            'credential_schema', 'logo_url', 'website_url'
        ]
