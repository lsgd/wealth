// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'broker.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

_$BrokerImpl _$$BrokerImplFromJson(Map<String, dynamic> json) => _$BrokerImpl(
  code: json['code'] as String,
  name: json['name'] as String,
  supportsAutoSync: json['supports_auto_sync'] as bool? ?? false,
);

Map<String, dynamic> _$$BrokerImplToJson(_$BrokerImpl instance) =>
    <String, dynamic>{
      'code': instance.code,
      'name': instance.name,
      'supports_auto_sync': instance.supportsAutoSync,
    };
