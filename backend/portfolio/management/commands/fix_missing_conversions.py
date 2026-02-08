"""
Management command to fix snapshots missing base currency conversions.
"""
from decimal import Decimal

from django.core.management.base import BaseCommand

from exchange_rates.services import ExchangeRateService
from portfolio.models import AccountSnapshot


class Command(BaseCommand):
    help = 'Fix snapshots that are missing base currency conversions'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be fixed without making changes',
        )
        parser.add_argument(
            '--limit',
            type=int,
            default=0,
            help='Limit number of snapshots to process (0 = no limit)',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        limit = options['limit']

        # Find snapshots missing base currency conversion where currency differs from user's base
        snapshots = AccountSnapshot.objects.filter(
            balance_base_currency__isnull=True
        ).select_related('account__user__profile')

        if limit:
            snapshots = snapshots[:limit]

        total = snapshots.count()
        if total == 0:
            self.stdout.write(self.style.SUCCESS('No snapshots with missing conversions found'))
            return

        self.stdout.write(f'Found {total} snapshots with missing conversions')

        fixed = 0
        skipped = 0
        errors = 0

        for snapshot in snapshots:
            try:
                user_profile = snapshot.account.user.profile
                base_currency = user_profile.base_currency

                # Skip if same currency (should just copy balance)
                if snapshot.currency == base_currency:
                    if not dry_run:
                        snapshot.balance_base_currency = snapshot.balance
                        snapshot.base_currency = base_currency
                        snapshot.exchange_rate_used = Decimal('1')
                        snapshot.save()
                    fixed += 1
                    self.stdout.write(
                        f'  {snapshot.account.name} {snapshot.snapshot_date}: '
                        f'{snapshot.currency} {snapshot.balance} (same currency)'
                    )
                    continue

                # Get exchange rate
                rate = ExchangeRateService.get_rate(
                    snapshot.currency,
                    base_currency,
                    snapshot.snapshot_date
                )

                if rate and rate != Decimal('1.0'):
                    converted = snapshot.balance * rate
                    if not dry_run:
                        snapshot.balance_base_currency = converted
                        snapshot.base_currency = base_currency
                        snapshot.exchange_rate_used = rate
                        snapshot.save()
                    fixed += 1
                    self.stdout.write(
                        f'  {snapshot.account.name} {snapshot.snapshot_date}: '
                        f'{snapshot.currency} {snapshot.balance} -> {base_currency} {converted:.2f} (rate: {rate})'
                    )
                else:
                    skipped += 1
                    self.stdout.write(self.style.WARNING(
                        f'  {snapshot.account.name} {snapshot.snapshot_date}: '
                        f'No rate found for {snapshot.currency} -> {base_currency}'
                    ))

            except Exception as e:
                errors += 1
                self.stderr.write(self.style.ERROR(
                    f'  Error processing snapshot {snapshot.id}: {e}'
                ))

        prefix = '[DRY RUN] ' if dry_run else ''
        self.stdout.write(self.style.SUCCESS(
            f'\n{prefix}Fixed: {fixed}, Skipped: {skipped}, Errors: {errors}'
        ))
