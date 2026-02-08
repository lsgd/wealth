import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../data/models/account.dart';
import '../../data/repositories/account_repository.dart';
import 'core_providers.dart';

/// Provider for the account repository.
final accountRepositoryProvider = Provider<AccountRepository>((ref) {
  final apiClient = ref.watch(apiClientProvider);
  return AccountRepository(apiClient);
});

/// Provider for fetching all accounts.
final accountsProvider = FutureProvider<List<Account>>((ref) async {
  final repository = ref.watch(accountRepositoryProvider);
  return repository.getAccounts();
});

/// Provider for accounts that need manual snapshot entry today.
final accountsNeedingSnapshotsProvider =
    FutureProvider<List<Account>>((ref) async {
  final accounts = await ref.watch(accountsProvider.future);

  return accounts.where((account) {
    // Only accounts that need manual entry (manual or sync disabled)
    if (!account.needsManualEntry) return false;

    // Check if missing today's snapshot
    return account.isMissingTodaySnapshot();
  }).toList();
});
