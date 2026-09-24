import 'package:flutter/material.dart';

/// Calm paper in light, near-black in dark. Gold focus. Follows the system.
const Color kGold = Color(0xFFC9A227);
const Color kInk = Color(0xFF1C1916);
const Color kPaper = Color(0xFFF7F4EE);
const Color kNight = Color(0xFF12110E);
const Color kIvory = Color(0xFFF4EFE6);

ThemeData buildAppTheme() => buildLightTheme();

ThemeData buildLightTheme() {
  return _base(
    const ColorScheme.light(
      primary: kGold,
      onPrimary: kInk,
      secondary: kInk,
      onSecondary: kPaper,
      surface: kPaper,
      onSurface: kInk,
      error: Color(0xFF8C2F2F),
      onError: kPaper,
    ),
    buttonBg: kInk,
    buttonFg: kPaper,
  );
}

ThemeData buildDarkTheme() {
  return _base(
    const ColorScheme.dark(
      primary: kGold,
      onPrimary: kInk,
      secondary: kGold,
      onSecondary: kInk,
      surface: kNight,
      onSurface: kIvory,
      error: Color(0xFFE7A3A3),
      onError: kInk,
    ),
    buttonBg: kGold,
    buttonFg: kInk,
  );
}

ThemeData _base(ColorScheme scheme, {required Color buttonBg, required Color buttonFg}) {
  return ThemeData(
    useMaterial3: true,
    colorScheme: scheme,
    scaffoldBackgroundColor: scheme.surface,
    appBarTheme: AppBarTheme(
      backgroundColor: scheme.surface,
      foregroundColor: scheme.onSurface,
      elevation: 0,
      centerTitle: false,
    ),
    cardTheme: CardThemeData(
      color: scheme.brightness == Brightness.dark ? const Color(0xFF1C1A16) : const Color(0xFFFFFDF8),
      elevation: 0,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(14),
        side: BorderSide(color: scheme.outlineVariant),
      ),
    ),
    filledButtonTheme: FilledButtonThemeData(
      style: FilledButton.styleFrom(
        backgroundColor: buttonBg,
        foregroundColor: buttonFg,
        minimumSize: const Size.fromHeight(48),
        textStyle: const TextStyle(fontWeight: FontWeight.w600, fontSize: 16),
      ),
    ),
    focusColor: kGold,
    inputDecorationTheme: InputDecorationTheme(
      filled: true,
      fillColor: scheme.brightness == Brightness.dark ? const Color(0xFF1C1A16) : const Color(0xFFFFFDF8),
      border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
      focusedBorder: OutlineInputBorder(
        borderRadius: BorderRadius.circular(10),
        borderSide: const BorderSide(color: kGold, width: 2),
      ),
    ),
  );
}
