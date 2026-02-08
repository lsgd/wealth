/// API configuration for the wealth tracker app.
/// Server URL is configurable since users can self-host.
class ApiConfig {
  static const Duration connectTimeout = Duration(seconds: 30);
  static const Duration receiveTimeout = Duration(seconds: 30);

  /// API endpoints
  static const String loginPath = '/api/auth/login/';
  static const String refreshPath = '/api/auth/refresh/';
  static const String mePath = '/api/auth/me/';
  static const String profilePath = '/api/profile/';
  static const String accountsPath = '/api/accounts/';
  static const String wealthSummaryPath = '/api/wealth/summary/';
  static const String wealthHistoryPath = '/api/wealth/history/';
  static const String deviceRegisterPath = '/api/devices/register/';

  static String accountSnapshotsPath(int accountId) =>
      '/api/accounts/$accountId/snapshots/';

  static String snapshotDetailPath(int snapshotId) =>
      '/api/snapshots/$snapshotId/';

  static String accountSyncPath(int accountId) =>
      '/api/accounts/$accountId/sync/';

  static const String syncAllPath = '/api/accounts/sync/';
}
