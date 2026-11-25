// A first test: the app's theme builds. Run all tests with `flutter test`.
//
// 📘 LEARN: tests run on GitHub before every build, so a mistake is caught before it reaches a phone.
import 'package:familyenglish_app/theme.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  test('theme uses the night background', () {
    final theme = FE.theme();
    expect(theme.scaffoldBackgroundColor, FE.night);
    expect(theme.useMaterial3, isTrue);
  });
}
