from datetime import date, datetime

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

    def handle(self, *args, **options):
        if options['backfill']:
            self._handle_backfill(options)
        elif options['date']:
            self._handle_date(options['date'])
        else:
            self._handle_latest()

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
