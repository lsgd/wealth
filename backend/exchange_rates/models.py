from decimal import Decimal
from typing import Optional

from django.db import models


class ExchangeRate(models.Model):
    """Historical currency exchange rates."""

    from_currency = models.CharField(max_length=3)
    to_currency = models.CharField(max_length=3)
    rate = models.DecimalField(max_digits=20, decimal_places=10)
    rate_date = models.DateField()

    source = models.CharField(
        max_length=50,
        default='frankfurter',
        help_text='Data source (frankfurter, manual, etc.)'
    )
    fetched_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'exchange_rates'
        unique_together = ['from_currency', 'to_currency', 'rate_date']
        indexes = [
            models.Index(fields=['rate_date']),
            models.Index(fields=['from_currency', 'to_currency', 'rate_date']),
        ]

    def __str__(self):
        return f"{self.from_currency}/{self.to_currency}: {self.rate} ({self.rate_date})"

    @classmethod
    def get_rate(cls, from_currency: str, to_currency: str, date) -> Optional[Decimal]:
        """Get exchange rate for a specific date with fallback."""
        if from_currency == to_currency:
            return Decimal('1.0')

        # Try exact date first
        rate = cls.objects.filter(
            from_currency=from_currency,
            to_currency=to_currency,
            rate_date=date
        ).first()

        if rate:
            return rate.rate

        # Fallback to most recent rate before the date
        rate = cls.objects.filter(
            from_currency=from_currency,
            to_currency=to_currency,
            rate_date__lte=date
        ).order_by('-rate_date').first()

        if rate:
            return rate.rate

        # Try inverse rate
        inverse = cls.objects.filter(
            from_currency=to_currency,
            to_currency=from_currency,
            rate_date__lte=date
        ).order_by('-rate_date').first()

        if inverse:
            return Decimal('1.0') / inverse.rate

        return None
