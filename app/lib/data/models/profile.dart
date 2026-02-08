import 'package:freezed_annotation/freezed_annotation.dart';

part 'profile.freezed.dart';
part 'profile.g.dart';

@freezed
class Profile with _$Profile {
  const factory Profile({
    @JsonKey(name: 'base_currency') required String baseCurrency,
    @JsonKey(name: 'auto_sync_enabled') required bool autoSyncEnabled,
    @JsonKey(name: 'send_weekly_report') required bool sendWeeklyReport,
    @JsonKey(name: 'default_chart_range') required int defaultChartRange,
    @JsonKey(name: 'default_chart_granularity')
    required String defaultChartGranularity,
    @JsonKey(name: 'push_notifications_enabled')
    @Default(true)
    bool pushNotificationsEnabled,
    @JsonKey(name: 'push_weekly_report') @Default(false) bool pushWeeklyReport,
  }) = _Profile;

  factory Profile.fromJson(Map<String, dynamic> json) =>
      _$ProfileFromJson(json);
}
