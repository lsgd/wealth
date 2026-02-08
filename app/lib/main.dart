import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'app.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // TODO: Initialize Firebase
  // await Firebase.initializeApp(
  //   options: DefaultFirebaseOptions.currentPlatform,
  // );

  // TODO: Configure Crashlytics
  // FlutterError.onError = FirebaseCrashlytics.instance.recordFlutterFatalError;

  runApp(
    const ProviderScope(
      child: WealthApp(),
    ),
  );
}
