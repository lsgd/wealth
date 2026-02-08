import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../data/models/account.dart';
import '../providers/accounts_provider.dart';
import '../providers/auth_provider.dart';
import '../providers/wealth_provider.dart';
import '../widgets/account_card.dart';
import '../widgets/quick_snapshot_sheet.dart';
import '../widgets/wealth_line_chart.dart';
import '../widgets/wealth_summary_card.dart';

class DashboardScreen extends ConsumerStatefulWidget {
  const DashboardScreen({super.key});

  @override
  ConsumerState<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends ConsumerState<DashboardScreen> {
  bool _checkedQuickSnapshot = false;
  final Set<int> _syncingAccounts = {};
  bool _syncingAll = false;

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      _checkQuickSnapshotPrompt();
    });
  }

  Future<void> _checkQuickSnapshotPrompt() async {
    if (_checkedQuickSnapshot) return;
    _checkedQuickSnapshot = true;

    final accountsNeeding =
        await ref.read(accountsNeedingSnapshotsProvider.future);

    if (accountsNeeding.isNotEmpty && mounted) {
      _showQuickSnapshotSheet(accountsNeeding);
    }
  }

  void _showQuickSnapshotSheet(List accounts) {
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      useSafeArea: true,
      builder: (context) => QuickSnapshotSheet(
        accounts: accounts.cast(),
        onDismiss: () => Navigator.pop(context),
        onSnapshotsAdded: () {
          Navigator.pop(context);
          _refresh();
        },
      ),
    );
  }

  Future<void> _refresh() async {
    ref.invalidate(wealthSummaryProvider);
    ref.invalidate(wealthHistoryProvider);
    ref.invalidate(accountsProvider);
    ref.invalidate(accountsNeedingSnapshotsProvider);
  }

  Future<void> _syncAccount(Account account) async {
    if (_syncingAccounts.contains(account.id)) return;

    setState(() => _syncingAccounts.add(account.id));
    try {
      final repo = ref.read(accountRepositoryProvider);
      await repo.syncAccount(account.id);
      await _refresh();
    } finally {
      if (mounted) {
        setState(() => _syncingAccounts.remove(account.id));
      }
    }
  }

  Future<void> _syncAllAccounts() async {
    if (_syncingAll) return;

    setState(() => _syncingAll = true);
    try {
      final repo = ref.read(accountRepositoryProvider);
      await repo.syncAllAccounts();
      await _refresh();
    } finally {
      if (mounted) {
        setState(() => _syncingAll = false);
      }
    }
  }

  /// Check if any account supports auto-sync.
  bool _hasAutoSyncAccounts(List<Account> accounts) {
    return accounts
        .any((a) => a.syncEnabled && a.broker.supportsAutoSync);
  }

  @override
  Widget build(BuildContext context) {
    final wealthSummary = ref.watch(wealthSummaryProvider);
    final wealthHistory = ref.watch(wealthHistoryProvider);
    final accounts = ref.watch(accountsProvider);
    final authState = ref.watch(authStateProvider);

    return Scaffold(
      appBar: AppBar(
        title: const Text('Wealth Tracker'),
        actions: [
          IconButton(
            icon: const Icon(Icons.settings),
            onPressed: () => context.push('/settings'),
          ),
        ],
      ),
      body: RefreshIndicator(
        onRefresh: _refresh,
        child: CustomScrollView(
          slivers: [
            // Greeting
            SliverToBoxAdapter(
              child: Padding(
                padding: const EdgeInsets.fromLTRB(16, 16, 16, 8),
                child: authState.whenOrNull(
                  data: (user) => Text(
                    'Hello, ${user?.firstName ?? user?.username ?? 'there'}!',
                    style: Theme.of(context).textTheme.titleLarge,
                  ),
                ),
              ),
            ),

            // Wealth Summary Card
            SliverToBoxAdapter(
              child: Padding(
                padding: const EdgeInsets.symmetric(horizontal: 16),
                child: wealthSummary.when(
                  data: (summary) => WealthSummaryCard(summary: summary),
                  loading: () => const _LoadingCard(height: 100),
                  error: (e, _) => _ErrorCard(message: e.toString()),
                ),
              ),
            ),

            // Chart
            SliverToBoxAdapter(
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: wealthHistory.when(
                  data: (history) => WealthLineChart(
                    history: history,
                    currency:
                        wealthSummary.valueOrNull?.baseCurrency ?? 'CHF',
                  ),
                  loading: () => const _LoadingCard(height: 250),
                  error: (e, _) => _ErrorCard(message: e.toString()),
                ),
              ),
            ),

            // Quick Snapshot Banner
            _QuickSnapshotBanner(
              onTap: () async {
                final accountsNeeding =
                    await ref.read(accountsNeedingSnapshotsProvider.future);
                if (accountsNeeding.isNotEmpty && mounted) {
                  _showQuickSnapshotSheet(accountsNeeding);
                }
              },
            ),

            // Accounts Header
            SliverToBoxAdapter(
              child: Padding(
                padding: const EdgeInsets.fromLTRB(16, 8, 16, 8),
                child: Row(
                  children: [
                    Text(
                      'Accounts',
                      style: Theme.of(context).textTheme.titleMedium,
                    ),
                    if (accounts.valueOrNull != null) ...[
                      const SizedBox(width: 8),
                      Text(
                        '(${accounts.valueOrNull!.length})',
                        style: Theme.of(context).textTheme.bodySmall,
                      ),
                    ],
                    const Spacer(),
                    if (accounts.valueOrNull != null &&
                        _hasAutoSyncAccounts(accounts.valueOrNull!))
                      TextButton.icon(
                        onPressed: _syncingAll ? null : _syncAllAccounts,
                        icon: _syncingAll
                            ? SizedBox(
                                width: 16,
                                height: 16,
                                child: CircularProgressIndicator(
                                  strokeWidth: 2,
                                  color: Theme.of(context).colorScheme.primary,
                                ),
                              )
                            : const Icon(Icons.sync, size: 18),
                        label: const Text('Sync All'),
                      ),
                  ],
                ),
              ),
            ),

            // Accounts List
            accounts.when(
              data: (accountList) {
                if (accountList.isEmpty) {
                  return const SliverToBoxAdapter(
                    child: Padding(
                      padding: EdgeInsets.all(32),
                      child: Center(
                        child: Text('No accounts yet'),
                      ),
                    ),
                  );
                }
                return SliverPadding(
                  padding: const EdgeInsets.symmetric(horizontal: 16),
                  sliver: SliverList(
                    delegate: SliverChildBuilderDelegate(
                      (context, index) {
                        final account = accountList[index];
                        final canSync = account.syncEnabled &&
                            account.broker.supportsAutoSync;
                        return Padding(
                          padding: const EdgeInsets.only(bottom: 8),
                          child: AccountCard(
                            account: account,
                            baseCurrency:
                                wealthSummary.valueOrNull?.baseCurrency ??
                                    'CHF',
                            onSnapshotAdded: _refresh,
                            onSync: canSync
                                ? () => _syncAccount(account)
                                : null,
                            isSyncing: _syncingAccounts.contains(account.id),
                          ),
                        );
                      },
                      childCount: accountList.length,
                    ),
                  ),
                );
              },
              loading: () => SliverToBoxAdapter(
                child: Padding(
                  padding: const EdgeInsets.all(16),
                  child: Column(
                    children: List.generate(
                      3,
                      (_) => const Padding(
                        padding: EdgeInsets.only(bottom: 8),
                        child: _LoadingCard(height: 80),
                      ),
                    ),
                  ),
                ),
              ),
              error: (e, _) => SliverToBoxAdapter(
                child: Padding(
                  padding: const EdgeInsets.all(16),
                  child: _ErrorCard(message: e.toString()),
                ),
              ),
            ),

            // Bottom padding
            const SliverToBoxAdapter(
              child: SizedBox(height: 32),
            ),
          ],
        ),
      ),
    );
  }
}

class _LoadingCard extends StatelessWidget {
  final double height;

  const _LoadingCard({required this.height});

  @override
  Widget build(BuildContext context) {
    return Card(
      child: SizedBox(
        height: height,
        child: const Center(
          child: CircularProgressIndicator(),
        ),
      ),
    );
  }
}

class _ErrorCard extends StatelessWidget {
  final String message;

  const _ErrorCard({required this.message});

  @override
  Widget build(BuildContext context) {
    return Card(
      color: Theme.of(context).colorScheme.errorContainer,
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Row(
          children: [
            Icon(
              Icons.error_outline,
              color: Theme.of(context).colorScheme.error,
            ),
            const SizedBox(width: 12),
            Expanded(
              child: Text(
                message,
                style: TextStyle(
                  color: Theme.of(context).colorScheme.onErrorContainer,
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _QuickSnapshotBanner extends ConsumerWidget {
  final VoidCallback onTap;

  const _QuickSnapshotBanner({required this.onTap});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final accountsNeeding = ref.watch(accountsNeedingSnapshotsProvider);

    return accountsNeeding.when(
      data: (accounts) {
        if (accounts.isEmpty) return const SliverToBoxAdapter(child: SizedBox.shrink());

        return SliverToBoxAdapter(
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 16),
            child: Card(
              color: Theme.of(context).colorScheme.primaryContainer,
              child: InkWell(
                onTap: onTap,
                borderRadius: BorderRadius.circular(12),
                child: Padding(
                  padding: const EdgeInsets.all(12),
                  child: Row(
                    children: [
                      Icon(
                        Icons.edit_note,
                        color: Theme.of(context).colorScheme.onPrimaryContainer,
                      ),
                      const SizedBox(width: 12),
                      Expanded(
                        child: Text(
                          '${accounts.length} account${accounts.length == 1 ? '' : 's'} need${accounts.length == 1 ? 's' : ''} balance update',
                          style: TextStyle(
                            color: Theme.of(context).colorScheme.onPrimaryContainer,
                          ),
                        ),
                      ),
                      Icon(
                        Icons.chevron_right,
                        color: Theme.of(context).colorScheme.onPrimaryContainer,
                      ),
                    ],
                  ),
                ),
              ),
            ),
          ),
        );
      },
      loading: () => const SliverToBoxAdapter(child: SizedBox.shrink()),
      error: (_, _) => const SliverToBoxAdapter(child: SizedBox.shrink()),
    );
  }
}
