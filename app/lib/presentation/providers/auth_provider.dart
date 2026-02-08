import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/config/api_config.dart';
import '../../data/models/user.dart';
import 'core_providers.dart';

/// Auth state - null means not authenticated.
final authStateProvider =
    AsyncNotifierProvider<AuthNotifier, User?>(() => AuthNotifier());

class AuthNotifier extends AsyncNotifier<User?> {
  @override
  Future<User?> build() async {
    // Check if we have tokens on startup
    final storage = ref.read(secureStorageProvider);
    final hasTokens = await storage.hasTokens();

    if (!hasTokens) return null;

    // Try to validate the token
    try {
      return await _fetchCurrentUser();
    } catch (e) {
      // Token invalid, clear it
      await storage.clearTokens();
      return null;
    }
  }

  Future<User> _fetchCurrentUser() async {
    final apiClient = ref.read(apiClientProvider);
    final response = await apiClient.get(ApiConfig.mePath);
    return User.fromJson(response.data as Map<String, dynamic>);
  }

  /// Login with username and password.
  Future<void> login(String username, String password) async {
    state = const AsyncLoading();

    try {
      final apiClient = ref.read(apiClientProvider);
      final storage = ref.read(secureStorageProvider);

      final response = await apiClient.post(
        ApiConfig.loginPath,
        data: {
          'username': username,
          'password': password,
        },
      );

      final accessToken = response.data['access'] as String;
      final refreshToken = response.data['refresh'] as String;

      await storage.setTokens(accessToken, refreshToken);

      // Fetch user info
      final user = await _fetchCurrentUser();
      state = AsyncData(user);
    } catch (e) {
      state = AsyncError(e, StackTrace.current);
      rethrow;
    }
  }

  /// Logout and clear tokens.
  Future<void> logout() async {
    final storage = ref.read(secureStorageProvider);
    await storage.clearAll();
    state = const AsyncData(null);
  }

  /// Attempt to unlock with biometrics.
  /// Returns true if successful.
  Future<bool> unlockWithBiometrics() async {
    final biometricService = ref.read(biometricServiceProvider);
    final storage = ref.read(secureStorageProvider);

    // Check if biometric is enabled
    final biometricEnabled = await storage.isBiometricEnabled();
    if (!biometricEnabled) return false;

    // Authenticate with biometrics
    final authenticated = await biometricService.authenticate();
    if (!authenticated) return false;

    // Validate token
    try {
      final user = await _fetchCurrentUser();
      state = AsyncData(user);
      return true;
    } catch (e) {
      return false;
    }
  }
}

/// Provider to check if biometric unlock is available and enabled.
final biometricAvailableProvider = FutureProvider<bool>((ref) async {
  final biometricService = ref.watch(biometricServiceProvider);
  final storage = ref.watch(secureStorageProvider);

  final isAvailable = await biometricService.isAvailable();
  final isEnabled = await storage.isBiometricEnabled();

  return isAvailable && isEnabled;
});

/// Provider to check if server URL is configured.
final hasServerUrlProvider = FutureProvider<bool>((ref) async {
  final storage = ref.watch(secureStorageProvider);
  return await storage.hasServerUrl();
});
