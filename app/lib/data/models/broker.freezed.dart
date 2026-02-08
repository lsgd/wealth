// coverage:ignore-file
// GENERATED CODE - DO NOT MODIFY BY HAND
// ignore_for_file: type=lint
// ignore_for_file: unused_element, deprecated_member_use, deprecated_member_use_from_same_package, use_function_type_syntax_for_parameters, unnecessary_const, avoid_init_to_null, invalid_override_different_default_values_named, prefer_expression_function_bodies, annotate_overrides, invalid_annotation_target, unnecessary_question_mark

part of 'broker.dart';

// **************************************************************************
// FreezedGenerator
// **************************************************************************

T _$identity<T>(T value) => value;

final _privateConstructorUsedError = UnsupportedError(
  'It seems like you constructed your class using `MyClass._()`. This constructor is only meant to be used by freezed and you are not supposed to need it nor use it.\nPlease check the documentation here for more information: https://github.com/rrousselGit/freezed#adding-getters-and-methods-to-our-models',
);

Broker _$BrokerFromJson(Map<String, dynamic> json) {
  return _Broker.fromJson(json);
}

/// @nodoc
mixin _$Broker {
  String get code => throw _privateConstructorUsedError;
  String get name => throw _privateConstructorUsedError;
  @JsonKey(name: 'supports_auto_sync')
  bool get supportsAutoSync => throw _privateConstructorUsedError;

  /// Serializes this Broker to a JSON map.
  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;

  /// Create a copy of Broker
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  $BrokerCopyWith<Broker> get copyWith => throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $BrokerCopyWith<$Res> {
  factory $BrokerCopyWith(Broker value, $Res Function(Broker) then) =
      _$BrokerCopyWithImpl<$Res, Broker>;
  @useResult
  $Res call({
    String code,
    String name,
    @JsonKey(name: 'supports_auto_sync') bool supportsAutoSync,
  });
}

/// @nodoc
class _$BrokerCopyWithImpl<$Res, $Val extends Broker>
    implements $BrokerCopyWith<$Res> {
  _$BrokerCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  /// Create a copy of Broker
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? code = null,
    Object? name = null,
    Object? supportsAutoSync = null,
  }) {
    return _then(
      _value.copyWith(
            code: null == code
                ? _value.code
                : code // ignore: cast_nullable_to_non_nullable
                      as String,
            name: null == name
                ? _value.name
                : name // ignore: cast_nullable_to_non_nullable
                      as String,
            supportsAutoSync: null == supportsAutoSync
                ? _value.supportsAutoSync
                : supportsAutoSync // ignore: cast_nullable_to_non_nullable
                      as bool,
          )
          as $Val,
    );
  }
}

/// @nodoc
abstract class _$$BrokerImplCopyWith<$Res> implements $BrokerCopyWith<$Res> {
  factory _$$BrokerImplCopyWith(
    _$BrokerImpl value,
    $Res Function(_$BrokerImpl) then,
  ) = __$$BrokerImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call({
    String code,
    String name,
    @JsonKey(name: 'supports_auto_sync') bool supportsAutoSync,
  });
}

/// @nodoc
class __$$BrokerImplCopyWithImpl<$Res>
    extends _$BrokerCopyWithImpl<$Res, _$BrokerImpl>
    implements _$$BrokerImplCopyWith<$Res> {
  __$$BrokerImplCopyWithImpl(
    _$BrokerImpl _value,
    $Res Function(_$BrokerImpl) _then,
  ) : super(_value, _then);

  /// Create a copy of Broker
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? code = null,
    Object? name = null,
    Object? supportsAutoSync = null,
  }) {
    return _then(
      _$BrokerImpl(
        code: null == code
            ? _value.code
            : code // ignore: cast_nullable_to_non_nullable
                  as String,
        name: null == name
            ? _value.name
            : name // ignore: cast_nullable_to_non_nullable
                  as String,
        supportsAutoSync: null == supportsAutoSync
            ? _value.supportsAutoSync
            : supportsAutoSync // ignore: cast_nullable_to_non_nullable
                  as bool,
      ),
    );
  }
}

/// @nodoc
@JsonSerializable()
class _$BrokerImpl implements _Broker {
  const _$BrokerImpl({
    required this.code,
    required this.name,
    @JsonKey(name: 'supports_auto_sync') this.supportsAutoSync = false,
  });

  factory _$BrokerImpl.fromJson(Map<String, dynamic> json) =>
      _$$BrokerImplFromJson(json);

  @override
  final String code;
  @override
  final String name;
  @override
  @JsonKey(name: 'supports_auto_sync')
  final bool supportsAutoSync;

  @override
  String toString() {
    return 'Broker(code: $code, name: $name, supportsAutoSync: $supportsAutoSync)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$BrokerImpl &&
            (identical(other.code, code) || other.code == code) &&
            (identical(other.name, name) || other.name == name) &&
            (identical(other.supportsAutoSync, supportsAutoSync) ||
                other.supportsAutoSync == supportsAutoSync));
  }

  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  int get hashCode => Object.hash(runtimeType, code, name, supportsAutoSync);

  /// Create a copy of Broker
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  @pragma('vm:prefer-inline')
  _$$BrokerImplCopyWith<_$BrokerImpl> get copyWith =>
      __$$BrokerImplCopyWithImpl<_$BrokerImpl>(this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$BrokerImplToJson(this);
  }
}

abstract class _Broker implements Broker {
  const factory _Broker({
    required final String code,
    required final String name,
    @JsonKey(name: 'supports_auto_sync') final bool supportsAutoSync,
  }) = _$BrokerImpl;

  factory _Broker.fromJson(Map<String, dynamic> json) = _$BrokerImpl.fromJson;

  @override
  String get code;
  @override
  String get name;
  @override
  @JsonKey(name: 'supports_auto_sync')
  bool get supportsAutoSync;

  /// Create a copy of Broker
  /// with the given fields replaced by the non-null parameter values.
  @override
  @JsonKey(includeFromJson: false, includeToJson: false)
  _$$BrokerImplCopyWith<_$BrokerImpl> get copyWith =>
      throw _privateConstructorUsedError;
}
