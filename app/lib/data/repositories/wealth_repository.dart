import '../../core/config/api_config.dart';
import '../datasources/api_client.dart';
import '../models/wealth_summary.dart';

class WealthRepository {
  final ApiClient _apiClient;

  WealthRepository(this._apiClient);

  /// Fetch the current wealth summary.
  Future<WealthSummary> getSummary() async {
    final response = await _apiClient.get(ApiConfig.wealthSummaryPath);
    return WealthSummary.fromJson(response.data as Map<String, dynamic>);
  }

  /// Fetch wealth history for charting.
  Future<List<WealthHistoryPoint>> getHistory({
    required int days,
    required String granularity,
  }) async {
    final response = await _apiClient.get(
      ApiConfig.wealthHistoryPath,
      queryParameters: {
        'days': days,
        'granularity': granularity,
      },
    );
    final data = response.data as Map<String, dynamic>;
    final history = data['history'] as List<dynamic>? ?? [];
    return history
        .map((json) =>
            WealthHistoryPoint.fromJson(json as Map<String, dynamic>))
        .toList();
  }
}
