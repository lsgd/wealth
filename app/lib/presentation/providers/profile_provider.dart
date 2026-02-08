import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../data/models/profile.dart';
import '../../data/repositories/profile_repository.dart';
import 'core_providers.dart';

/// Provider for the profile repository.
final profileRepositoryProvider = Provider<ProfileRepository>((ref) {
  final apiClient = ref.watch(apiClientProvider);
  return ProfileRepository(apiClient);
});

/// Provider for the user's profile.
final profileProvider = FutureProvider<Profile?>((ref) async {
  final repository = ref.watch(profileRepositoryProvider);
  try {
    return await repository.getProfile();
  } catch (e) {
    return null;
  }
});
