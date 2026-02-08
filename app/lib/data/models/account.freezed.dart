// coverage:ignore-file
// GENERATED CODE - DO NOT MODIFY BY HAND
// ignore_for_file: type=lint
// ignore_for_file: unused_element, deprecated_member_use, deprecated_member_use_from_same_package, use_function_type_syntax_for_parameters, unnecessary_const, avoid_init_to_null, invalid_override_different_default_values_named, prefer_expression_function_bodies, annotate_overrides, invalid_annotation_target, unnecessary_question_mark

part of 'account.dart';

// **************************************************************************
// FreezedGenerator
// **************************************************************************

T _$identity<T>(T value) => value;

final _privateConstructorUsedError = UnsupportedError(
  'It seems like you constructed your class using `MyClass._()`. This constructor is only meant to be used by freezed and you are not supposed to need it nor use it.\nPlease check the documentation here for more information: https://github.com/rrousselGit/freezed#adding-getters-and-methods-to-our-models',
);

Account _$AccountFromJson(Map<String, dynamic> json) {
  return _Account.fromJson(json);
}

/// @nodoc
mixin _$Account {
  int get id => throw _privateConstructorUsedError;
  String get name => throw _privateConstructorUsedError;
  Broker get broker => throw _privateConstructorUsedError;
  @JsonKey(name: 'account_identifier')
  String? get accountIdentifier => throw _privateConstructorUsedError;
  @JsonKey(name: 'account_type')
  String get accountType => throw _privateConstructorUsedError;
  String get currency => throw _privateConstructorUsedError;
  @JsonKey(name: 'is_manual')
  bool get isManual => throw _privateConstructorUsedError;
  @JsonKey(name: 'sync_enabled')
  bool get syncEnabled => throw _privateConstructorUsedError;
  String get status => throw _privateConstructorUsedError;
  @JsonKey(name: 'last_sync_at')
  String? get lastSyncAt => throw _privateConstructorUsedError;
  @JsonKey(name: 'last_sync_error')
  String? get lastSyncError => throw _privateConstructorUsedError;
  @JsonKey(name: 'latest_snapshot')
  AccountSnapshot? get latestSnapshot => throw _privateConstructorUsedError;
  @JsonKey(name: 'created_at')
  String? get createdAt => throw _privateConstructorUsedError;
  @JsonKey(name: 'updated_at')
  String? get updatedAt => throw _privateConstructorUsedError;

  /// Serializes this Account to a JSON map.
  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;

  /// Create a copy of Account
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  $AccountCopyWith<Account> get copyWith => throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $AccountCopyWith<$Res> {
  factory $AccountCopyWith(Account value, $Res Function(Account) then) =
      _$AccountCopyWithImpl<$Res, Account>;
  @useResult
  $Res call({
    int id,
    String name,
    Broker broker,
    @JsonKey(name: 'account_identifier') String? accountIdentifier,
    @JsonKey(name: 'account_type') String accountType,
    String currency,
    @JsonKey(name: 'is_manual') bool isManual,
    @JsonKey(name: 'sync_enabled') bool syncEnabled,
    String status,
    @JsonKey(name: 'last_sync_at') String? lastSyncAt,
    @JsonKey(name: 'last_sync_error') String? lastSyncError,
    @JsonKey(name: 'latest_snapshot') AccountSnapshot? latestSnapshot,
    @JsonKey(name: 'created_at') String? createdAt,
    @JsonKey(name: 'updated_at') String? updatedAt,
  });

  $BrokerCopyWith<$Res> get broker;
  $AccountSnapshotCopyWith<$Res>? get latestSnapshot;
}

/// @nodoc
class _$AccountCopyWithImpl<$Res, $Val extends Account>
    implements $AccountCopyWith<$Res> {
  _$AccountCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  /// Create a copy of Account
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? name = null,
    Object? broker = null,
    Object? accountIdentifier = freezed,
    Object? accountType = null,
    Object? currency = null,
    Object? isManual = null,
    Object? syncEnabled = null,
    Object? status = null,
    Object? lastSyncAt = freezed,
    Object? lastSyncError = freezed,
    Object? latestSnapshot = freezed,
    Object? createdAt = freezed,
    Object? updatedAt = freezed,
  }) {
    return _then(
      _value.copyWith(
            id: null == id
                ? _value.id
                : id // ignore: cast_nullable_to_non_nullable
                      as int,
            name: null == name
                ? _value.name
                : name // ignore: cast_nullable_to_non_nullable
                      as String,
            broker: null == broker
                ? _value.broker
                : broker // ignore: cast_nullable_to_non_nullable
                      as Broker,
            accountIdentifier: freezed == accountIdentifier
                ? _value.accountIdentifier
                : accountIdentifier // ignore: cast_nullable_to_non_nullable
                      as String?,
            accountType: null == accountType
                ? _value.accountType
                : accountType // ignore: cast_nullable_to_non_nullable
                      as String,
            currency: null == currency
                ? _value.currency
                : currency // ignore: cast_nullable_to_non_nullable
                      as String,
            isManual: null == isManual
                ? _value.isManual
                : isManual // ignore: cast_nullable_to_non_nullable
                      as bool,
            syncEnabled: null == syncEnabled
                ? _value.syncEnabled
                : syncEnabled // ignore: cast_nullable_to_non_nullable
                      as bool,
            status: null == status
                ? _value.status
                : status // ignore: cast_nullable_to_non_nullable
                      as String,
            lastSyncAt: freezed == lastSyncAt
                ? _value.lastSyncAt
                : lastSyncAt // ignore: cast_nullable_to_non_nullable
                      as String?,
            lastSyncError: freezed == lastSyncError
                ? _value.lastSyncError
                : lastSyncError // ignore: cast_nullable_to_non_nullable
                      as String?,
            latestSnapshot: freezed == latestSnapshot
                ? _value.latestSnapshot
                : latestSnapshot // ignore: cast_nullable_to_non_nullable
                      as AccountSnapshot?,
            createdAt: freezed == createdAt
                ? _value.createdAt
                : createdAt // ignore: cast_nullable_to_non_nullable
                      as String?,
            updatedAt: freezed == updatedAt
                ? _value.updatedAt
                : updatedAt // ignore: cast_nullable_to_non_nullable
                      as String?,
          )
          as $Val,
    );
  }

  /// Create a copy of Account
  /// with the given fields replaced by the non-null parameter values.
  @override
  @pragma('vm:prefer-inline')
  $BrokerCopyWith<$Res> get broker {
    return $BrokerCopyWith<$Res>(_value.broker, (value) {
      return _then(_value.copyWith(broker: value) as $Val);
    });
  }

  /// Create a copy of Account
  /// with the given fields replaced by the non-null parameter values.
  @override
  @pragma('vm:prefer-inline')
  $AccountSnapshotCopyWith<$Res>? get latestSnapshot {
    if (_value.latestSnapshot == null) {
      return null;
    }

    return $AccountSnapshotCopyWith<$Res>(_value.latestSnapshot!, (value) {
      return _then(_value.copyWith(latestSnapshot: value) as $Val);
    });
  }
}

/// @nodoc
abstract class _$$AccountImplCopyWith<$Res> implements $AccountCopyWith<$Res> {
  factory _$$AccountImplCopyWith(
    _$AccountImpl value,
    $Res Function(_$AccountImpl) then,
  ) = __$$AccountImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call({
    int id,
    String name,
    Broker broker,
    @JsonKey(name: 'account_identifier') String? accountIdentifier,
    @JsonKey(name: 'account_type') String accountType,
    String currency,
    @JsonKey(name: 'is_manual') bool isManual,
    @JsonKey(name: 'sync_enabled') bool syncEnabled,
    String status,
    @JsonKey(name: 'last_sync_at') String? lastSyncAt,
    @JsonKey(name: 'last_sync_error') String? lastSyncError,
    @JsonKey(name: 'latest_snapshot') AccountSnapshot? latestSnapshot,
    @JsonKey(name: 'created_at') String? createdAt,
    @JsonKey(name: 'updated_at') String? updatedAt,
  });

  @override
  $BrokerCopyWith<$Res> get broker;
  @override
  $AccountSnapshotCopyWith<$Res>? get latestSnapshot;
}

/// @nodoc
class __$$AccountImplCopyWithImpl<$Res>
    extends _$AccountCopyWithImpl<$Res, _$AccountImpl>
    implements _$$AccountImplCopyWith<$Res> {
  __$$AccountImplCopyWithImpl(
    _$AccountImpl _value,
    $Res Function(_$AccountImpl) _then,
  ) : super(_value, _then);

  /// Create a copy of Account
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? name = null,
    Object? broker = null,
    Object? accountIdentifier = freezed,
    Object? accountType = null,
    Object? currency = null,
    Object? isManual = null,
    Object? syncEnabled = null,
    Object? status = null,
    Object? lastSyncAt = freezed,
    Object? lastSyncError = freezed,
    Object? latestSnapshot = freezed,
    Object? createdAt = freezed,
    Object? updatedAt = freezed,
  }) {
    return _then(
      _$AccountImpl(
        id: null == id
            ? _value.id
            : id // ignore: cast_nullable_to_non_nullable
                  as int,
        name: null == name
            ? _value.name
            : name // ignore: cast_nullable_to_non_nullable
                  as String,
        broker: null == broker
            ? _value.broker
            : broker // ignore: cast_nullable_to_non_nullable
                  as Broker,
        accountIdentifier: freezed == accountIdentifier
            ? _value.accountIdentifier
            : accountIdentifier // ignore: cast_nullable_to_non_nullable
                  as String?,
        accountType: null == accountType
            ? _value.accountType
            : accountType // ignore: cast_nullable_to_non_nullable
                  as String,
        currency: null == currency
            ? _value.currency
            : currency // ignore: cast_nullable_to_non_nullable
                  as String,
        isManual: null == isManual
            ? _value.isManual
            : isManual // ignore: cast_nullable_to_non_nullable
                  as bool,
        syncEnabled: null == syncEnabled
            ? _value.syncEnabled
            : syncEnabled // ignore: cast_nullable_to_non_nullable
                  as bool,
        status: null == status
            ? _value.status
            : status // ignore: cast_nullable_to_non_nullable
                  as String,
        lastSyncAt: freezed == lastSyncAt
            ? _value.lastSyncAt
            : lastSyncAt // ignore: cast_nullable_to_non_nullable
                  as String?,
        lastSyncError: freezed == lastSyncError
            ? _value.lastSyncError
            : lastSyncError // ignore: cast_nullable_to_non_nullable
                  as String?,
        latestSnapshot: freezed == latestSnapshot
            ? _value.latestSnapshot
            : latestSnapshot // ignore: cast_nullable_to_non_nullable
                  as AccountSnapshot?,
        createdAt: freezed == createdAt
            ? _value.createdAt
            : createdAt // ignore: cast_nullable_to_non_nullable
                  as String?,
        updatedAt: freezed == updatedAt
            ? _value.updatedAt
            : updatedAt // ignore: cast_nullable_to_non_nullable
                  as String?,
      ),
    );
  }
}

/// @nodoc
@JsonSerializable()
class _$AccountImpl extends _Account {
  const _$AccountImpl({
    required this.id,
    required this.name,
    required this.broker,
    @JsonKey(name: 'account_identifier') this.accountIdentifier,
    @JsonKey(name: 'account_type') required this.accountType,
    required this.currency,
    @JsonKey(name: 'is_manual') required this.isManual,
    @JsonKey(name: 'sync_enabled') required this.syncEnabled,
    required this.status,
    @JsonKey(name: 'last_sync_at') this.lastSyncAt,
    @JsonKey(name: 'last_sync_error') this.lastSyncError,
    @JsonKey(name: 'latest_snapshot') this.latestSnapshot,
    @JsonKey(name: 'created_at') this.createdAt,
    @JsonKey(name: 'updated_at') this.updatedAt,
  }) : super._();

  factory _$AccountImpl.fromJson(Map<String, dynamic> json) =>
      _$$AccountImplFromJson(json);

  @override
  final int id;
  @override
  final String name;
  @override
  final Broker broker;
  @override
  @JsonKey(name: 'account_identifier')
  final String? accountIdentifier;
  @override
  @JsonKey(name: 'account_type')
  final String accountType;
  @override
  final String currency;
  @override
  @JsonKey(name: 'is_manual')
  final bool isManual;
  @override
  @JsonKey(name: 'sync_enabled')
  final bool syncEnabled;
  @override
  final String status;
  @override
  @JsonKey(name: 'last_sync_at')
  final String? lastSyncAt;
  @override
  @JsonKey(name: 'last_sync_error')
  final String? lastSyncError;
  @override
  @JsonKey(name: 'latest_snapshot')
  final AccountSnapshot? latestSnapshot;
  @override
  @JsonKey(name: 'created_at')
  final String? createdAt;
  @override
  @JsonKey(name: 'updated_at')
  final String? updatedAt;

  @override
  String toString() {
    return 'Account(id: $id, name: $name, broker: $broker, accountIdentifier: $accountIdentifier, accountType: $accountType, currency: $currency, isManual: $isManual, syncEnabled: $syncEnabled, status: $status, lastSyncAt: $lastSyncAt, lastSyncError: $lastSyncError, latestSnapshot: $latestSnapshot, createdAt: $createdAt, updatedAt: $updatedAt)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$AccountImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.name, name) || other.name == name) &&
            (identical(other.broker, broker) || other.broker == broker) &&
            (identical(other.accountIdentifier, accountIdentifier) ||
                other.accountIdentifier == accountIdentifier) &&
            (identical(other.accountType, accountType) ||
                other.accountType == accountType) &&
            (identical(other.currency, currency) ||
                other.currency == currency) &&
            (identical(other.isManual, isManual) ||
                other.isManual == isManual) &&
            (identical(other.syncEnabled, syncEnabled) ||
                other.syncEnabled == syncEnabled) &&
            (identical(other.status, status) || other.status == status) &&
            (identical(other.lastSyncAt, lastSyncAt) ||
                other.lastSyncAt == lastSyncAt) &&
            (identical(other.lastSyncError, lastSyncError) ||
                other.lastSyncError == lastSyncError) &&
            (identical(other.latestSnapshot, latestSnapshot) ||
                other.latestSnapshot == latestSnapshot) &&
            (identical(other.createdAt, createdAt) ||
                other.createdAt == createdAt) &&
            (identical(other.updatedAt, updatedAt) ||
                other.updatedAt == updatedAt));
  }

  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  int get hashCode => Object.hash(
    runtimeType,
    id,
    name,
    broker,
    accountIdentifier,
    accountType,
    currency,
    isManual,
    syncEnabled,
    status,
    lastSyncAt,
    lastSyncError,
    latestSnapshot,
    createdAt,
    updatedAt,
  );

  /// Create a copy of Account
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  @pragma('vm:prefer-inline')
  _$$AccountImplCopyWith<_$AccountImpl> get copyWith =>
      __$$AccountImplCopyWithImpl<_$AccountImpl>(this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$AccountImplToJson(this);
  }
}

abstract class _Account extends Account {
  const factory _Account({
    required final int id,
    required final String name,
    required final Broker broker,
    @JsonKey(name: 'account_identifier') final String? accountIdentifier,
    @JsonKey(name: 'account_type') required final String accountType,
    required final String currency,
    @JsonKey(name: 'is_manual') required final bool isManual,
    @JsonKey(name: 'sync_enabled') required final bool syncEnabled,
    required final String status,
    @JsonKey(name: 'last_sync_at') final String? lastSyncAt,
    @JsonKey(name: 'last_sync_error') final String? lastSyncError,
    @JsonKey(name: 'latest_snapshot') final AccountSnapshot? latestSnapshot,
    @JsonKey(name: 'created_at') final String? createdAt,
    @JsonKey(name: 'updated_at') final String? updatedAt,
  }) = _$AccountImpl;
  const _Account._() : super._();

  factory _Account.fromJson(Map<String, dynamic> json) = _$AccountImpl.fromJson;

  @override
  int get id;
  @override
  String get name;
  @override
  Broker get broker;
  @override
  @JsonKey(name: 'account_identifier')
  String? get accountIdentifier;
  @override
  @JsonKey(name: 'account_type')
  String get accountType;
  @override
  String get currency;
  @override
  @JsonKey(name: 'is_manual')
  bool get isManual;
  @override
  @JsonKey(name: 'sync_enabled')
  bool get syncEnabled;
  @override
  String get status;
  @override
  @JsonKey(name: 'last_sync_at')
  String? get lastSyncAt;
  @override
  @JsonKey(name: 'last_sync_error')
  String? get lastSyncError;
  @override
  @JsonKey(name: 'latest_snapshot')
  AccountSnapshot? get latestSnapshot;
  @override
  @JsonKey(name: 'created_at')
  String? get createdAt;
  @override
  @JsonKey(name: 'updated_at')
  String? get updatedAt;

  /// Create a copy of Account
  /// with the given fields replaced by the non-null parameter values.
  @override
  @JsonKey(includeFromJson: false, includeToJson: false)
  _$$AccountImplCopyWith<_$AccountImpl> get copyWith =>
      throw _privateConstructorUsedError;
}
