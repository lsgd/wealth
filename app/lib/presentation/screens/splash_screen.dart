import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../providers/auth_provider.dart';
import '../providers/core_providers.dart';

class SplashScreen extends ConsumerStatefulWidget {
  const SplashScreen({super.key});

  @override
  ConsumerState<SplashScreen> createState() => _SplashScreenState();
}

class _SplashScreenState extends ConsumerState<SplashScreen> {
  @override
  void initState() {
    super.initState();
    _checkInitialRoute();
  }

  Future<void> _checkInitialRoute() async {
    // Small delay for splash to show
    await Future.delayed(const Duration(milliseconds: 500));

    if (!mounted) return;

    final storage = ref.read(secureStorageProvider);

    // Check if server URL is configured
    final hasServerUrl = await storage.hasServerUrl();
    if (!hasServerUrl) {
      if (mounted) context.go('/server-config');
      return;
    }

    // Check if we have tokens
    final hasTokens = await storage.hasTokens();
    if (!hasTokens) {
      if (mounted) context.go('/login');
      return;
    }

    // Check if biometric is enabled
    final biometricEnabled = await storage.isBiometricEnabled();
    if (biometricEnabled) {
      // Try biometric unlock
      final success =
          await ref.read(authStateProvider.notifier).unlockWithBiometrics();
      if (success) {
        if (mounted) context.go('/dashboard');
        return;
      }
    }

    // Fall back to checking if token is still valid
    final authState = ref.read(authStateProvider);
    authState.when(
      data: (user) {
        if (user != null) {
          context.go('/dashboard');
        } else {
          context.go('/login');
        }
      },
      loading: () {
        // Wait for auth to complete
      },
      error: (_, _) {
        context.go('/login');
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(
              Icons.account_balance_wallet,
              size: 80,
              color: Theme.of(context).colorScheme.primary,
            ),
            const SizedBox(height: 24),
            Text(
              'Wealth Tracker',
              style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                    fontWeight: FontWeight.bold,
                  ),
            ),
            const SizedBox(height: 32),
            const CircularProgressIndicator(),
          ],
        ),
      ),
    );
  }
}
