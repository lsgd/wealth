from datetime import date, timedelta
from decimal import Decimal
from typing import List

import requests

from .models import ExchangeRate


class ExchangeRateService:
    """Service for fetching and managing exchange rates from Frankfurter API."""

    API_BASE = 'https://api.frankfurter.dev/v1'
    SUPPORTED_CURRENCIES = ['EUR', 'USD', 'CHF', 'GBP']

    @classmethod
    def fetch_rates_for_date(cls, target_date: date) -> List[ExchangeRate]:
        """Fetch all exchange rates for a specific date."""
        created_rates = []

        for base_currency in cls.SUPPORTED_CURRENCIES:
            symbols = [c for c in cls.SUPPORTED_CURRENCIES if c != base_currency]

            response = requests.get(
                f'{cls.API_BASE}/{target_date.isoformat()}',
                params={'base': base_currency, 'symbols': ','.join(symbols)},
                timeout=30
            )

            if response.ok:
                data = response.json()
                rates = data.get('rates', {})

                for to_currency, rate in rates.items():
                    exchange_rate, created = ExchangeRate.objects.update_or_create(
                        from_currency=base_currency,
                        to_currency=to_currency,
                        rate_date=target_date,
                        defaults={
                            'rate': Decimal(str(rate)),
                            'source': 'frankfurter'
                        }
                    )
                    if created:
                        created_rates.append(exchange_rate)

        return created_rates

    @classmethod
    def fetch_latest_rates(cls) -> List[ExchangeRate]:
        """Fetch the latest available exchange rates."""
        return cls.fetch_rates_for_date(date.today())

    @classmethod
    def backfill_rates(cls, start_date: date, end_date: date) -> int:
        """Backfill historical exchange rates."""
        count = 0
        current = start_date

        while current <= end_date:
            rates = cls.fetch_rates_for_date(current)
            count += len(rates)
            current += timedelta(days=1)

        return count

    @classmethod
    def get_rate(
        cls,
        from_currency: str,
        to_currency: str,
        rate_date: date
    ) -> Decimal:
        """Get exchange rate, fetching if necessary."""
        rate = ExchangeRate.get_rate(from_currency, to_currency, rate_date)

        if rate is None:
            # Try to fetch from API
            cls.fetch_rates_for_date(rate_date)
            rate = ExchangeRate.get_rate(from_currency, to_currency, rate_date)

        return rate if rate else Decimal('1.0')
