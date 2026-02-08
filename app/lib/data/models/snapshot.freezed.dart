// coverage:ignore-file
// GENERATED CODE - DO NOT MODIFY BY HAND
// ignore_for_file: type=lint
// ignore_for_file: unused_element, deprecated_member_use, deprecated_member_use_from_same_package, use_function_type_syntax_for_parameters, unnecessary_const, avoid_init_to_null, invalid_override_different_default_values_named, prefer_expression_function_bodies, annotate_overrides, invalid_annotation_target, unnecessary_question_mark

part of 'snapshot.dart';

// **************************************************************************
// FreezedGenerator
// **************************************************************************

T _$identity<T>(T value) => value;

final _privateConstructorUsedError = UnsupportedError(
  'It seems like you constructed your class using `MyClass._()`. This constructor is only meant to be used by freezed and you are not supposed to need it nor use it.\nPlease check the documentation here for more information: https://github.com/rrousselGit/freezed#adding-getters-and-methods-to-our-models',
);

AccountSnapshot _$AccountSnapshotFromJson(Map<String, dynamic> json) {
  return _AccountSnapshot.fromJson(json);
}

/// @nodoc
mixin _$AccountSnapshot {
  int get id => throw _privateConstructorUsedError;
  String get balance => throw _privateConstructorUsedError;
  String get currency => throw _privateConstructorUsedError;
  @JsonKey(name: 'balance_base_currency')
  String? get balanceBaseCurrency => throw _privateConstructorUsedError;
  @JsonKey(name: 'base_currency')
  String? get baseCurrency => throw _privateConstructorUsedError;
  @JsonKey(name: 'snapshot_date')
  String get snapshotDate => throw _privateConstructorUsedError;
  @JsonKey(name: 'snapshot_source')
  String? get snapshotSource => throw _privateConstructorUsedError;
  @JsonKey(name: 'created_at')
  String? get createdAt => throw _privateConstructorUsedError;

  /// Serializes this AccountSnapshot to a JSON map.
  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;

  /// Create a copy of AccountSnapshot
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  $AccountSnapshotCopyWith<AccountSnapshot> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $AccountSnapshotCopyWith<$Res> {
  factory $AccountSnapshotCopyWith(
    AccountSnapshot value,
    $Res Function(AccountSnapshot) then,
  ) = _$AccountSnapshotCopyWithImpl<$Res, AccountSnapshot>;
  @useResult
  $Res call({
    int id,
    String balance,
    String currency,
    @JsonKey(name: 'balance_base_currency') String? balanceBaseCurrency,
    @JsonKey(name: 'base_currency') String? baseCurrency,
    @JsonKey(name: 'snapshot_date') String snapshotDate,
    @JsonKey(name: 'snapshot_source') String? snapshotSource,
    @JsonKey(name: 'created_at') String? createdAt,
  });
}

/// @nodoc
class _$AccountSnapshotCopyWithImpl<$Res, $Val extends AccountSnapshot>
    implements $AccountSnapshotCopyWith<$Res> {
  _$AccountSnapshotCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  /// Create a copy of AccountSnapshot
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? balance = null,
    Object? currency = null,
    Object? balanceBaseCurrency = freezed,
    Object? baseCurrency = freezed,
    Object? snapshotDate = null,
    Object? snapshotSource = freezed,
    Object? createdAt = freezed,
  }) {
    return _then(
      _value.copyWith(
            id: null == id
                ? _value.id
                : id // ignore: cast_nullable_to_non_nullable
                      as int,
            balance: null == balance
                ? _value.balance
                : balance // ignore: cast_nullable_to_non_nullable
                      as String,
            currency: null == currency
                ? _value.currency
                : currency // ignore: cast_nullable_to_non_nullable
                      as String,
            balanceBaseCurrency: freezed == balanceBaseCurrency
                ? _value.balanceBaseCurrency
                : balanceBaseCurrency // ignore: cast_nullable_to_non_nullable
                      as String?,
            baseCurrency: freezed == baseCurrency
                ? _value.baseCurrency
                : baseCurrency // ignore: cast_nullable_to_non_nullable
                      as String?,
            snapshotDate: null == snapshotDate
                ? _value.snapshotDate
                : snapshotDate // ignore: cast_nullable_to_non_nullable
                      as String,
            snapshotSource: freezed == snapshotSource
                ? _value.snapshotSource
                : snapshotSource // ignore: cast_nullable_to_non_nullable
                      as String?,
            createdAt: freezed == createdAt
                ? _value.createdAt
                : createdAt // ignore: cast_nullable_to_non_nullable
                      as String?,
          )
          as $Val,
    );
  }
}

/// @nodoc
abstract class _$$AccountSnapshotImplCopyWith<$Res>
    implements $AccountSnapshotCopyWith<$Res> {
  factory _$$AccountSnapshotImplCopyWith(
    _$AccountSnapshotImpl value,
    $Res Function(_$AccountSnapshotImpl) then,
  ) = __$$AccountSnapshotImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call({
    int id,
    String balance,
    String currency,
    @JsonKey(name: 'balance_base_currency') String? balanceBaseCurrency,
    @JsonKey(name: 'base_currency') String? baseCurrency,
    @JsonKey(name: 'snapshot_date') String snapshotDate,
    @JsonKey(name: 'snapshot_source') String? snapshotSource,
    @JsonKey(name: 'created_at') String? createdAt,
  });
}

/// @nodoc
class __$$AccountSnapshotImplCopyWithImpl<$Res>
    extends _$AccountSnapshotCopyWithImpl<$Res, _$AccountSnapshotImpl>
    implements _$$AccountSnapshotImplCopyWith<$Res> {
  __$$AccountSnapshotImplCopyWithImpl(
    _$AccountSnapshotImpl _value,
    $Res Function(_$AccountSnapshotImpl) _then,
  ) : super(_value, _then);

  /// Create a copy of AccountSnapshot
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? balance = null,
    Object? currency = null,
    Object? balanceBaseCurrency = freezed,
    Object? baseCurrency = freezed,
    Object? snapshotDate = null,
    Object? snapshotSource = freezed,
    Object? createdAt = freezed,
  }) {
    return _then(
      _$AccountSnapshotImpl(
        id: null == id
            ? _value.id
            : id // ignore: cast_nullable_to_non_nullable
                  as int,
        balance: null == balance
            ? _value.balance
            : balance // ignore: cast_nullable_to_non_nullable
                  as String,
        currency: null == currency
            ? _value.currency
            : currency // ignore: cast_nullable_to_non_nullable
                  as String,
        balanceBaseCurrency: freezed == balanceBaseCurrency
            ? _value.balanceBaseCurrency
            : balanceBaseCurrency // ignore: cast_nullable_to_non_nullable
                  as String?,
        baseCurrency: freezed == baseCurrency
            ? _value.baseCurrency
            : baseCurrency // ignore: cast_nullable_to_non_nullable
                  as String?,
        snapshotDate: null == snapshotDate
            ? _value.snapshotDate
            : snapshotDate // ignore: cast_nullable_to_non_nullable
                  as String,
        snapshotSource: freezed == snapshotSource
            ? _value.snapshotSource
            : snapshotSource // ignore: cast_nullable_to_non_nullable
                  as String?,
        createdAt: freezed == createdAt
            ? _value.createdAt
            : createdAt // ignore: cast_nullable_to_non_nullable
                  as String?,
      ),
    );
  }
}

/// @nodoc
@JsonSerializable()
class _$AccountSnapshotImpl implements _AccountSnapshot {
  const _$AccountSnapshotImpl({
    required this.id,
    required this.balance,
    required this.currency,
    @JsonKey(name: 'balance_base_currency') this.balanceBaseCurrency,
    @JsonKey(name: 'base_currency') this.baseCurrency,
    @JsonKey(name: 'snapshot_date') required this.snapshotDate,
    @JsonKey(name: 'snapshot_source') this.snapshotSource,
    @JsonKey(name: 'created_at') this.createdAt,
  });

  factory _$AccountSnapshotImpl.fromJson(Map<String, dynamic> json) =>
      _$$AccountSnapshotImplFromJson(json);

  @override
  final int id;
  @override
  final String balance;
  @override
  final String currency;
  @override
  @JsonKey(name: 'balance_base_currency')
  final String? balanceBaseCurrency;
  @override
  @JsonKey(name: 'base_currency')
  final String? baseCurrency;
  @override
  @JsonKey(name: 'snapshot_date')
  final String snapshotDate;
  @override
  @JsonKey(name: 'snapshot_source')
  final String? snapshotSource;
  @override
  @JsonKey(name: 'created_at')
  final String? createdAt;

  @override
  String toString() {
    return 'AccountSnapshot(id: $id, balance: $balance, currency: $currency, balanceBaseCurrency: $balanceBaseCurrency, baseCurrency: $baseCurrency, snapshotDate: $snapshotDate, snapshotSource: $snapshotSource, createdAt: $createdAt)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$AccountSnapshotImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.balance, balance) || other.balance == balance) &&
            (identical(other.currency, currency) ||
                other.currency == currency) &&
            (identical(other.balanceBaseCurrency, balanceBaseCurrency) ||
                other.balanceBaseCurrency == balanceBaseCurrency) &&
            (identical(other.baseCurrency, baseCurrency) ||
                other.baseCurrency == baseCurrency) &&
            (identical(other.snapshotDate, snapshotDate) ||
                other.snapshotDate == snapshotDate) &&
            (identical(other.snapshotSource, snapshotSource) ||
                other.snapshotSource == snapshotSource) &&
            (identical(other.createdAt, createdAt) ||
                other.createdAt == createdAt));
  }

  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  int get hashCode => Object.hash(
    runtimeType,
    id,
    balance,
    currency,
    balanceBaseCurrency,
    baseCurrency,
    snapshotDate,
    snapshotSource,
    createdAt,
  );

  /// Create a copy of AccountSnapshot
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  @pragma('vm:prefer-inline')
  _$$AccountSnapshotImplCopyWith<_$AccountSnapshotImpl> get copyWith =>
      __$$AccountSnapshotImplCopyWithImpl<_$AccountSnapshotImpl>(
        this,
        _$identity,
      );

  @override
  Map<String, dynamic> toJson() {
    return _$$AccountSnapshotImplToJson(this);
  }
}

abstract class _AccountSnapshot implements AccountSnapshot {
  const factory _AccountSnapshot({
    required final int id,
    required final String balance,
    required final String currency,
    @JsonKey(name: 'balance_base_currency') final String? balanceBaseCurrency,
    @JsonKey(name: 'base_currency') final String? baseCurrency,
    @JsonKey(name: 'snapshot_date') required final String snapshotDate,
    @JsonKey(name: 'snapshot_source') final String? snapshotSource,
    @JsonKey(name: 'created_at') final String? createdAt,
  }) = _$AccountSnapshotImpl;

  factory _AccountSnapshot.fromJson(Map<String, dynamic> json) =
      _$AccountSnapshotImpl.fromJson;

  @override
  int get id;
  @override
  String get balance;
  @override
  String get currency;
  @override
  @JsonKey(name: 'balance_base_currency')
  String? get balanceBaseCurrency;
  @override
  @JsonKey(name: 'base_currency')
  String? get baseCurrency;
  @override
  @JsonKey(name: 'snapshot_date')
  String get snapshotDate;
  @override
  @JsonKey(name: 'snapshot_source')
  String? get snapshotSource;
  @override
  @JsonKey(name: 'created_at')
  String? get createdAt;

  /// Create a copy of AccountSnapshot
  /// with the given fields replaced by the non-null parameter values.
  @override
  @JsonKey(includeFromJson: false, includeToJson: false)
  _$$AccountSnapshotImplCopyWith<_$AccountSnapshotImpl> get copyWith =>
      throw _privateConstructorUsedError;
}
