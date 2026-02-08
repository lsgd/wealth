import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../data/models/wealth_summary.dart';
import '../../data/repositories/wealth_repository.dart';
import 'core_providers.dart';
import 'profile_provider.dart';

/// Provider for the wealth repository.
final wealthRepositoryProvider = Provider<WealthRepository>((ref) {
  final apiClient = ref.watch(apiClientProvider);
  return WealthRepository(apiClient);
});

/// Provider for the current wealth summary.
final wealthSummaryProvider = FutureProvider<WealthSummary>((ref) async {
  final repository = ref.watch(wealthRepositoryProvider);
  return repository.getSummary();
});

/// Provider for chart range setting.
final chartRangeProvider = StateProvider<int>((ref) {
  // Initialize from profile when available
  final profile = ref.watch(profileProvider);
  return profile.whenOrNull(data: (p) => p?.defaultChartRange) ?? 365;
});

/// Provider for chart granularity setting.
final chartGranularityProvider = StateProvider<String>((ref) {
  // Initialize from profile when available
  final profile = ref.watch(profileProvider);
  return profile.whenOrNull(data: (p) => p?.defaultChartGranularity) ?? 'daily';
});

/// Provider for wealth history based on current chart settings.
final wealthHistoryProvider =
    FutureProvider<List<WealthHistoryPoint>>((ref) async {
  final repository = ref.watch(wealthRepositoryProvider);
  final days = ref.watch(chartRangeProvider);
  final granularity = ref.watch(chartGranularityProvider);

  return repository.getHistory(days: days, granularity: granularity);
});
