import 'package:local_auth/local_auth.dart';

/// Service for biometric authentication (Face ID / Touch ID).
class BiometricService {
  final LocalAuthentication _localAuth = LocalAuthentication();

  /// Check if biometric authentication is available on this device.
  Future<bool> isAvailable() async {
    final canCheck = await _localAuth.canCheckBiometrics;
    final isSupported = await _localAuth.isDeviceSupported();
    return canCheck && isSupported;
  }

  /// Get the list of available biometric types.
  Future<List<BiometricType>> getAvailableBiometrics() async {
    return await _localAuth.getAvailableBiometrics();
  }

  /// Check if Face ID is available.
  Future<bool> hasFaceId() async {
    final types = await getAvailableBiometrics();
    return types.contains(BiometricType.face);
  }

  /// Check if Touch ID / Fingerprint is available.
  Future<bool> hasFingerprint() async {
    final types = await getAvailableBiometrics();
    return types.contains(BiometricType.fingerprint);
  }

  /// Authenticate using biometrics.
  /// Returns true if authentication was successful.
  Future<bool> authenticate({
    String reason = 'Authenticate to access Wealth Tracker',
  }) async {
    try {
      return await _localAuth.authenticate(
        localizedReason: reason,
        biometricOnly: true,
      );
    } catch (e) {
      return false;
    }
  }
}
