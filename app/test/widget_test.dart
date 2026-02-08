import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'package:wealth_tracker/app.dart';

void main() {
  testWidgets('App loads splash screen', (WidgetTester tester) async {
    await tester.pumpWidget(
      const ProviderScope(
        child: WealthApp(),
      ),
    );

    // Verify that splash screen shows app name
    expect(find.text('Wealth Tracker'), findsOneWidget);
  });
}
