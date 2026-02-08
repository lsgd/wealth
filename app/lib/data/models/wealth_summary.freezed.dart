// coverage:ignore-file
// GENERATED CODE - DO NOT MODIFY BY HAND
// ignore_for_file: type=lint
// ignore_for_file: unused_element, deprecated_member_use, deprecated_member_use_from_same_package, use_function_type_syntax_for_parameters, unnecessary_const, avoid_init_to_null, invalid_override_different_default_values_named, prefer_expression_function_bodies, annotate_overrides, invalid_annotation_target, unnecessary_question_mark

part of 'wealth_summary.dart';

// **************************************************************************
// FreezedGenerator
// **************************************************************************

T _$identity<T>(T value) => value;

final _privateConstructorUsedError = UnsupportedError(
  'It seems like you constructed your class using `MyClass._()`. This constructor is only meant to be used by freezed and you are not supposed to need it nor use it.\nPlease check the documentation here for more information: https://github.com/rrousselGit/freezed#adding-getters-and-methods-to-our-models',
);

WealthSummary _$WealthSummaryFromJson(Map<String, dynamic> json) {
  return _WealthSummary.fromJson(json);
}

/// @nodoc
mixin _$WealthSummary {
  @JsonKey(name: 'total_wealth')
  double get totalWealth => throw _privateConstructorUsedError;
  @JsonKey(name: 'base_currency')
  String get baseCurrency => throw _privateConstructorUsedError;
  @JsonKey(name: 'account_count')
  int get accountCount => throw _privateConstructorUsedError;

  /// Serializes this WealthSummary to a JSON map.
  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;

  /// Create a copy of WealthSummary
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  $WealthSummaryCopyWith<WealthSummary> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $WealthSummaryCopyWith<$Res> {
  factory $WealthSummaryCopyWith(
    WealthSummary value,
    $Res Function(WealthSummary) then,
  ) = _$WealthSummaryCopyWithImpl<$Res, WealthSummary>;
  @useResult
  $Res call({
    @JsonKey(name: 'total_wealth') double totalWealth,
    @JsonKey(name: 'base_currency') String baseCurrency,
    @JsonKey(name: 'account_count') int accountCount,
  });
}

/// @nodoc
class _$WealthSummaryCopyWithImpl<$Res, $Val extends WealthSummary>
    implements $WealthSummaryCopyWith<$Res> {
  _$WealthSummaryCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  /// Create a copy of WealthSummary
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? totalWealth = null,
    Object? baseCurrency = null,
    Object? accountCount = null,
  }) {
    return _then(
      _value.copyWith(
            totalWealth: null == totalWealth
                ? _value.totalWealth
                : totalWealth // ignore: cast_nullable_to_non_nullable
                      as double,
            baseCurrency: null == baseCurrency
                ? _value.baseCurrency
                : baseCurrency // ignore: cast_nullable_to_non_nullable
                      as String,
            accountCount: null == accountCount
                ? _value.accountCount
                : accountCount // ignore: cast_nullable_to_non_nullable
                      as int,
          )
          as $Val,
    );
  }
}

/// @nodoc
abstract class _$$WealthSummaryImplCopyWith<$Res>
    implements $WealthSummaryCopyWith<$Res> {
  factory _$$WealthSummaryImplCopyWith(
    _$WealthSummaryImpl value,
    $Res Function(_$WealthSummaryImpl) then,
  ) = __$$WealthSummaryImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call({
    @JsonKey(name: 'total_wealth') double totalWealth,
    @JsonKey(name: 'base_currency') String baseCurrency,
    @JsonKey(name: 'account_count') int accountCount,
  });
}

/// @nodoc
class __$$WealthSummaryImplCopyWithImpl<$Res>
    extends _$WealthSummaryCopyWithImpl<$Res, _$WealthSummaryImpl>
    implements _$$WealthSummaryImplCopyWith<$Res> {
  __$$WealthSummaryImplCopyWithImpl(
    _$WealthSummaryImpl _value,
    $Res Function(_$WealthSummaryImpl) _then,
  ) : super(_value, _then);

  /// Create a copy of WealthSummary
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? totalWealth = null,
    Object? baseCurrency = null,
    Object? accountCount = null,
  }) {
    return _then(
      _$WealthSummaryImpl(
        totalWealth: null == totalWealth
            ? _value.totalWealth
            : totalWealth // ignore: cast_nullable_to_non_nullable
                  as double,
        baseCurrency: null == baseCurrency
            ? _value.baseCurrency
            : baseCurrency // ignore: cast_nullable_to_non_nullable
                  as String,
        accountCount: null == accountCount
            ? _value.accountCount
            : accountCount // ignore: cast_nullable_to_non_nullable
                  as int,
      ),
    );
  }
}

/// @nodoc
@JsonSerializable()
class _$WealthSummaryImpl implements _WealthSummary {
  const _$WealthSummaryImpl({
    @JsonKey(name: 'total_wealth') required this.totalWealth,
    @JsonKey(name: 'base_currency') required this.baseCurrency,
    @JsonKey(name: 'account_count') required this.accountCount,
  });

  factory _$WealthSummaryImpl.fromJson(Map<String, dynamic> json) =>
      _$$WealthSummaryImplFromJson(json);

  @override
  @JsonKey(name: 'total_wealth')
  final double totalWealth;
  @override
  @JsonKey(name: 'base_currency')
  final String baseCurrency;
  @override
  @JsonKey(name: 'account_count')
  final int accountCount;

  @override
  String toString() {
    return 'WealthSummary(totalWealth: $totalWealth, baseCurrency: $baseCurrency, accountCount: $accountCount)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$WealthSummaryImpl &&
            (identical(other.totalWealth, totalWealth) ||
                other.totalWealth == totalWealth) &&
            (identical(other.baseCurrency, baseCurrency) ||
                other.baseCurrency == baseCurrency) &&
            (identical(other.accountCount, accountCount) ||
                other.accountCount == accountCount));
  }

  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  int get hashCode =>
      Object.hash(runtimeType, totalWealth, baseCurrency, accountCount);

  /// Create a copy of WealthSummary
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  @pragma('vm:prefer-inline')
  _$$WealthSummaryImplCopyWith<_$WealthSummaryImpl> get copyWith =>
      __$$WealthSummaryImplCopyWithImpl<_$WealthSummaryImpl>(this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$WealthSummaryImplToJson(this);
  }
}

abstract class _WealthSummary implements WealthSummary {
  const factory _WealthSummary({
    @JsonKey(name: 'total_wealth') required final double totalWealth,
    @JsonKey(name: 'base_currency') required final String baseCurrency,
    @JsonKey(name: 'account_count') required final int accountCount,
  }) = _$WealthSummaryImpl;

  factory _WealthSummary.fromJson(Map<String, dynamic> json) =
      _$WealthSummaryImpl.fromJson;

  @override
  @JsonKey(name: 'total_wealth')
  double get totalWealth;
  @override
  @JsonKey(name: 'base_currency')
  String get baseCurrency;
  @override
  @JsonKey(name: 'account_count')
  int get accountCount;

  /// Create a copy of WealthSummary
  /// with the given fields replaced by the non-null parameter values.
  @override
  @JsonKey(includeFromJson: false, includeToJson: false)
  _$$WealthSummaryImplCopyWith<_$WealthSummaryImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

WealthHistoryPoint _$WealthHistoryPointFromJson(Map<String, dynamic> json) {
  return _WealthHistoryPoint.fromJson(json);
}

/// @nodoc
mixin _$WealthHistoryPoint {
  String get date => throw _privateConstructorUsedError;
  @JsonKey(name: 'total_wealth')
  double get totalWealth => throw _privateConstructorUsedError;

  /// Serializes this WealthHistoryPoint to a JSON map.
  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;

  /// Create a copy of WealthHistoryPoint
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  $WealthHistoryPointCopyWith<WealthHistoryPoint> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $WealthHistoryPointCopyWith<$Res> {
  factory $WealthHistoryPointCopyWith(
    WealthHistoryPoint value,
    $Res Function(WealthHistoryPoint) then,
  ) = _$WealthHistoryPointCopyWithImpl<$Res, WealthHistoryPoint>;
  @useResult
  $Res call({String date, @JsonKey(name: 'total_wealth') double totalWealth});
}

/// @nodoc
class _$WealthHistoryPointCopyWithImpl<$Res, $Val extends WealthHistoryPoint>
    implements $WealthHistoryPointCopyWith<$Res> {
  _$WealthHistoryPointCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  /// Create a copy of WealthHistoryPoint
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({Object? date = null, Object? totalWealth = null}) {
    return _then(
      _value.copyWith(
            date: null == date
                ? _value.date
                : date // ignore: cast_nullable_to_non_nullable
                      as String,
            totalWealth: null == totalWealth
                ? _value.totalWealth
                : totalWealth // ignore: cast_nullable_to_non_nullable
                      as double,
          )
          as $Val,
    );
  }
}

/// @nodoc
abstract class _$$WealthHistoryPointImplCopyWith<$Res>
    implements $WealthHistoryPointCopyWith<$Res> {
  factory _$$WealthHistoryPointImplCopyWith(
    _$WealthHistoryPointImpl value,
    $Res Function(_$WealthHistoryPointImpl) then,
  ) = __$$WealthHistoryPointImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call({String date, @JsonKey(name: 'total_wealth') double totalWealth});
}

/// @nodoc
class __$$WealthHistoryPointImplCopyWithImpl<$Res>
    extends _$WealthHistoryPointCopyWithImpl<$Res, _$WealthHistoryPointImpl>
    implements _$$WealthHistoryPointImplCopyWith<$Res> {
  __$$WealthHistoryPointImplCopyWithImpl(
    _$WealthHistoryPointImpl _value,
    $Res Function(_$WealthHistoryPointImpl) _then,
  ) : super(_value, _then);

  /// Create a copy of WealthHistoryPoint
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({Object? date = null, Object? totalWealth = null}) {
    return _then(
      _$WealthHistoryPointImpl(
        date: null == date
            ? _value.date
            : date // ignore: cast_nullable_to_non_nullable
                  as String,
        totalWealth: null == totalWealth
            ? _value.totalWealth
            : totalWealth // ignore: cast_nullable_to_non_nullable
                  as double,
      ),
    );
  }
}

/// @nodoc
@JsonSerializable()
class _$WealthHistoryPointImpl implements _WealthHistoryPoint {
  const _$WealthHistoryPointImpl({
    required this.date,
    @JsonKey(name: 'total_wealth') required this.totalWealth,
  });

  factory _$WealthHistoryPointImpl.fromJson(Map<String, dynamic> json) =>
      _$$WealthHistoryPointImplFromJson(json);

  @override
  final String date;
  @override
  @JsonKey(name: 'total_wealth')
  final double totalWealth;

  @override
  String toString() {
    return 'WealthHistoryPoint(date: $date, totalWealth: $totalWealth)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$WealthHistoryPointImpl &&
            (identical(other.date, date) || other.date == date) &&
            (identical(other.totalWealth, totalWealth) ||
                other.totalWealth == totalWealth));
  }

  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  int get hashCode => Object.hash(runtimeType, date, totalWealth);

  /// Create a copy of WealthHistoryPoint
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  @pragma('vm:prefer-inline')
  _$$WealthHistoryPointImplCopyWith<_$WealthHistoryPointImpl> get copyWith =>
      __$$WealthHistoryPointImplCopyWithImpl<_$WealthHistoryPointImpl>(
        this,
        _$identity,
      );

  @override
  Map<String, dynamic> toJson() {
    return _$$WealthHistoryPointImplToJson(this);
  }
}

abstract class _WealthHistoryPoint implements WealthHistoryPoint {
  const factory _WealthHistoryPoint({
    required final String date,
    @JsonKey(name: 'total_wealth') required final double totalWealth,
  }) = _$WealthHistoryPointImpl;

  factory _WealthHistoryPoint.fromJson(Map<String, dynamic> json) =
      _$WealthHistoryPointImpl.fromJson;

  @override
  String get date;
  @override
  @JsonKey(name: 'total_wealth')
  double get totalWealth;

  /// Create a copy of WealthHistoryPoint
  /// with the given fields replaced by the non-null parameter values.
  @override
  @JsonKey(includeFromJson: false, includeToJson: false)
  _$$WealthHistoryPointImplCopyWith<_$WealthHistoryPointImpl> get copyWith =>
      throw _privateConstructorUsedError;
}
