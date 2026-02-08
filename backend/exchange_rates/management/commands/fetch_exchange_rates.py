from datetime import date, datetime
from decimal import Decimal

from django.core.management.base import BaseCommand

from exchange_rates.services import ExchangeRateService


class Command(BaseCommand):
    help = 'Fetch exchange rates from the Frankfurter API'

    def add_arguments(self, parser):
        parser.add_argument(
            '--date',
            type=str,
            help='Fetch rates for a specific date (YYYY-MM-DD). Defaults to today.',
        )
        parser.add_argument(
            '--backfill',
            action='store_true',
            help='Backfill rates for a date range (requires --start and --end).',
        )
        parser.add_argument(
            '--start',
            type=str,
            help='Start date for backfill (YYYY-MM-DD).',
        )
        parser.add_argument(
            '--end',
            type=str,
            help='End date for backfill (YYYY-MM-DD). Defaults to today.',
        )
        parser.add_argument(
            '--skip-conversions',
            action='store_true',
            help='Skip fixing missing snapshot conversions.',
        )

    def handle(self, *args, **options):
        if options['backfill']:
            self._handle_backfill(options)
        elif options['date']:
            self._handle_date(options['date'])
        else:
            self._handle_latest()

        # Fix missing conversions unless skipped
        if not options.get('skip_conversions'):
            self._fix_missing_conversions()

    def _handle_latest(self):
        self.stdout.write('Fetching latest exchange rates...')
        rates = ExchangeRateService.fetch_latest_rates()
        self.stdout.write(self.style.SUCCESS(
            f'Fetched {len(rates)} new exchange rates for {date.today().isoformat()}'
        ))

    def _handle_date(self, date_str):
        target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        self.stdout.write(f'Fetching exchange rates for {target_date.isoformat()}...')
        rates = ExchangeRateService.fetch_rates_for_date(target_date)
        self.stdout.write(self.style.SUCCESS(
            f'Fetched {len(rates)} new exchange rates for {target_date.isoformat()}'
        ))

    def _handle_backfill(self, options):
        if not options['start']:
            self.stderr.write(self.style.ERROR('--start is required for backfill'))
            return

        start_date = datetime.strptime(options['start'], '%Y-%m-%d').date()
        end_date = (
            datetime.strptime(options['end'], '%Y-%m-%d').date()
            if options['end']
            else date.today()
        )

        self.stdout.write(
            f'Backfilling exchange rates from {start_date.isoformat()} to {end_date.isoformat()}...'
        )
        count = ExchangeRateService.backfill_rates(start_date, end_date)
        self.stdout.write(self.style.SUCCESS(
            f'Backfilled {count} exchange rates'
        ))

    def _fix_missing_conversions(self):
        """Fix snapshots that are missing base currency conversions."""
        from portfolio.models import AccountSnapshot

        # Find snapshots missing base currency conversion
        snapshots = AccountSnapshot.objects.filter(
            balance_base_currency__isnull=True
        ).select_related('account__user__profile')[:100]  # Limit to 100 per run

        if not snapshots:
            return

        self.stdout.write(f'Fixing {len(snapshots)} snapshots with missing conversions...')

        fixed = 0
        for snapshot in snapshots:
            try:
                user_profile = snapshot.account.user.profile
                base_currency = user_profile.base_currency

                if snapshot.currency == base_currency:
                    snapshot.balance_base_currency = snapshot.balance
                    snapshot.base_currency = base_currency
                    snapshot.exchange_rate_used = Decimal('1')
                    snapshot.save()
                    fixed += 1
                    continue

                rate = ExchangeRateService.get_rate(
                    snapshot.currency,
                    base_currency,
                    snapshot.snapshot_date
                )

                if rate and rate != Decimal('1.0'):
                    snapshot.balance_base_currency = snapshot.balance * rate
                    snapshot.base_currency = base_currency
                    snapshot.exchange_rate_used = rate
                    snapshot.save()
                    fixed += 1

            except Exception as e:
                self.stderr.write(f'Error fixing snapshot {snapshot.id}: {e}')

        self.stdout.write(self.style.SUCCESS(f'Fixed {fixed} snapshot conversions'))
