// Colours and styles that match the website's night-blue look.
//
// 📘 LEARN: ThemeData sets the look once; every button and card follows it automatically.
import 'package:flutter/material.dart';

class FE {
  static const night = Color(0xFF110F33);
  static const card = Color(0xFF1E1A4A);
  static const sky = Color(0xFF1D8FFF);
  static const mint = Color(0xFF2FE0B5);
  static const gold = Color(0xFFFFC247);
  static const coral = Color(0xFFFF6363);
  static const violet = Color(0xFF8B6BFF);
  static const soft = Color(0xFFB9BCE6);
  static const ok = Color(0xFF16A86A);
  static const bad = Color(0xFFE8364A);

  static ThemeData theme() {
    final scheme = ColorScheme.fromSeed(seedColor: sky, brightness: Brightness.dark, surface: night);
    return ThemeData(
      useMaterial3: true,
      colorScheme: scheme,
      scaffoldBackgroundColor: night,
      cardTheme: CardThemeData(color: card, elevation: 0, shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(22))),
      filledButtonTheme: FilledButtonThemeData(
        style: FilledButton.styleFrom(
          backgroundColor: sky,
          foregroundColor: Colors.white,
          minimumSize: const Size.fromHeight(54),
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
          textStyle: const TextStyle(fontSize: 17, fontWeight: FontWeight.w800),
        ),
      ),
      inputDecorationTheme: InputDecorationTheme(
        filled: true,
        fillColor: Colors.white.withValues(alpha: .07),
        border: OutlineInputBorder(borderRadius: BorderRadius.circular(16), borderSide: BorderSide.none),
      ),
      navigationBarTheme: NavigationBarThemeData(backgroundColor: const Color(0xFF100D2C), indicatorColor: sky.withValues(alpha: .25)),
    );
  }
}
