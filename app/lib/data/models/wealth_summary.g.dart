// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'wealth_summary.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

_$WealthSummaryImpl _$$WealthSummaryImplFromJson(Map<String, dynamic> json) =>
    _$WealthSummaryImpl(
      totalWealth: (json['total_wealth'] as num).toDouble(),
      baseCurrency: json['base_currency'] as String,
      accountCount: (json['account_count'] as num).toInt(),
    );

Map<String, dynamic> _$$WealthSummaryImplToJson(_$WealthSummaryImpl instance) =>
    <String, dynamic>{
      'total_wealth': instance.totalWealth,
      'base_currency': instance.baseCurrency,
      'account_count': instance.accountCount,
    };

_$WealthHistoryPointImpl _$$WealthHistoryPointImplFromJson(
  Map<String, dynamic> json,
) => _$WealthHistoryPointImpl(
  date: json['date'] as String,
  totalWealth: (json['total_wealth'] as num).toDouble(),
);

Map<String, dynamic> _$$WealthHistoryPointImplToJson(
  _$WealthHistoryPointImpl instance,
) => <String, dynamic>{
  'date': instance.date,
  'total_wealth': instance.totalWealth,
};
