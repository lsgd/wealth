from django.db import models


class Broker(models.Model):
    """Pre-defined list of supported brokers/financial institutions."""

    INTEGRATION_TYPES = [
        ('fints', 'FinTS Protocol'),
        ('rest', 'REST API'),
        ('graphql', 'GraphQL API'),
    ]

    code = models.CharField(
        max_length=50,
        unique=True,
        help_text='Internal broker identifier (e.g., dkb, commerzbank)'
    )
    name = models.CharField(max_length=100)
    integration_type = models.CharField(
        max_length=20,
        choices=INTEGRATION_TYPES
    )

    # FinTS-specific fields
    bank_identifier = models.CharField(
        max_length=20,
        blank=True,
        help_text='BLZ for German banks'
    )
    fints_server = models.URLField(
        blank=True,
        help_text='FinTS server URL'
    )

    # API-specific fields
    api_base_url = models.URLField(
        blank=True,
        help_text='Base URL for REST/GraphQL APIs'
    )

    # Metadata
    logo_url = models.URLField(blank=True)
    website_url = models.URLField(blank=True)
    country = models.CharField(max_length=2, default='DE')
    is_active = models.BooleanField(default=True)
    supports_2fa = models.BooleanField(default=False)
    supports_auto_sync = models.BooleanField(
        default=False,
        help_text='Whether accounts can be synced automatically without user interaction (e.g., decoupled TAN)'
    )

    # JSON schema defining required credentials
    credential_schema = models.JSONField(
        default=dict,
        help_text='JSON schema defining required credential fields'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'brokers'
        ordering = ['name']

    def __str__(self):
        return self.name
