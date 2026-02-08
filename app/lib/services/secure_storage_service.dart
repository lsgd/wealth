import 'package:flutter_secure_storage/flutter_secure_storage.dart';

/// Service for securely storing sensitive data like tokens and server URL.
class SecureStorageService {
  static const _serverUrlKey = 'server_url';
  static const _accessTokenKey = 'access_token';
  static const _refreshTokenKey = 'refresh_token';
  static const _biometricEnabledKey = 'biometric_enabled';
  static const _themeModeKey = 'theme_mode';
  static const _dateFormatKey = 'date_format';

  final FlutterSecureStorage _storage;

  SecureStorageService()
      : _storage = const FlutterSecureStorage(
          aOptions: AndroidOptions(),
          iOptions: IOSOptions(
            accessibility: KeychainAccessibility.first_unlock_this_device,
          ),
        );

  // Server URL management

  Future<String?> getServerUrl() => _storage.read(key: _serverUrlKey);

  Future<void> setServerUrl(String url) =>
      _storage.write(key: _serverUrlKey, value: url);

  Future<bool> hasServerUrl() async {
    final url = await getServerUrl();
    return url != null && url.isNotEmpty;
  }

  // Token management

  Future<String?> getAccessToken() => _storage.read(key: _accessTokenKey);

  Future<String?> getRefreshToken() => _storage.read(key: _refreshTokenKey);

  Future<void> setTokens(String accessToken, String refreshToken) async {
    await Future.wait([
      _storage.write(key: _accessTokenKey, value: accessToken),
      _storage.write(key: _refreshTokenKey, value: refreshToken),
    ]);
  }

  Future<bool> hasTokens() async {
    final access = await getAccessToken();
    return access != null && access.isNotEmpty;
  }

  Future<void> clearTokens() async {
    await Future.wait([
      _storage.delete(key: _accessTokenKey),
      _storage.delete(key: _refreshTokenKey),
    ]);
  }

  // Biometric preference

  Future<bool> isBiometricEnabled() async {
    final value = await _storage.read(key: _biometricEnabledKey);
    return value == 'true';
  }

  Future<void> setBiometricEnabled(bool enabled) =>
      _storage.write(key: _biometricEnabledKey, value: enabled.toString());

  // Theme mode (system, light, dark)

  Future<String> getThemeMode() async {
    final value = await _storage.read(key: _themeModeKey);
    return value ?? 'system';
  }

  Future<void> setThemeMode(String mode) =>
      _storage.write(key: _themeModeKey, value: mode);

  // Date format (system, dmy, mdy, ymd)

  Future<String> getDateFormat() async {
    final value = await _storage.read(key: _dateFormatKey);
    return value ?? 'system';
  }

  Future<void> setDateFormat(String format) =>
      _storage.write(key: _dateFormatKey, value: format);

  // Clear all data (for logout)

  Future<void> clearAll() async {
    await Future.wait([
      _storage.delete(key: _accessTokenKey),
      _storage.delete(key: _refreshTokenKey),
      _storage.delete(key: _biometricEnabledKey),
      // Note: We keep server URL so user doesn't have to re-enter it
    ]);
  }
}
