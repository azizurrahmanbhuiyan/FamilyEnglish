// Colours and styles: a fresh, light green look.
//
// 📘 LEARN: ThemeData sets the look once; every button and card follows it automatically.
// The names (sky, mint …) are kept so every screen still works; only the colours changed.
import 'package:flutter/material.dart';

class FE {
  static const night = Color(0xFFF1F9F2); // page background: very light green
  static const card = Color(0xFFFFFFFF); // cards and the tutor's bubbles
  static const panel = Color(0xFFE3F3E6); // the bottom panel with the mic
  static const sky = Color(0xFF2E9D57); // main green: buttons, your bubbles, the mic
  static const mint = Color(0xFF1E8A5A); // success and progress
  static const gold = Color(0xFFB07800);
  static const coral = Color(0xFFD9473F);
  static const violet = Color(0xFF6A4FD3);
  static const soft = Color(0xFF5B7363); // quieter text
  static const ink = Color(0xFF15301F); // main text
  static const line = Color(0x1F1B5E3A); // thin borders and empty progress bars
  static const ok = Color(0xFF16A86A);
  static const bad = Color(0xFFE8364A);

  static ThemeData theme() {
    final scheme = ColorScheme.fromSeed(seedColor: sky, brightness: Brightness.light, surface: card)
        .copyWith(primary: sky, onPrimary: Colors.white, onSurface: ink);
    return ThemeData(
      useMaterial3: true,
      colorScheme: scheme,
      scaffoldBackgroundColor: night,
      appBarTheme: const AppBarTheme(backgroundColor: night, foregroundColor: ink, elevation: 0, scrolledUnderElevation: 0),
      cardTheme: CardThemeData(
          color: card,
          elevation: 0,
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(22), side: const BorderSide(color: line))),
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
        fillColor: Colors.white,
        border: OutlineInputBorder(borderRadius: BorderRadius.circular(16), borderSide: const BorderSide(color: line)),
        enabledBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(16), borderSide: const BorderSide(color: line)),
        focusedBorder: OutlineInputBorder(borderRadius: BorderRadius.circular(16), borderSide: const BorderSide(color: sky, width: 2)),
      ),
      navigationBarTheme: NavigationBarThemeData(backgroundColor: Colors.white, indicatorColor: sky.withValues(alpha: .18)),
    );
  }
}
