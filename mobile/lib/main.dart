// The app starts here.
//
// 📘 LEARN:
// - Everything on screen is a Widget. StatelessWidget = no changing data; StatefulWidget = has data that changes.
// - ChangeNotifierProvider puts AppState at the top so any screen can read it with
//   context.watch<AppState>() (rebuild on change) or context.read<AppState>() (just use it).
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import 'screens/home_shell.dart';
import 'screens/learners_screen.dart';
import 'screens/login_screen.dart';
import 'state.dart';
import 'theme.dart';

void main() {
  runApp(ChangeNotifierProvider(create: (_) => AppState()..load(), child: const FamilyEnglishApp()));
}

class FamilyEnglishApp extends StatelessWidget {
  const FamilyEnglishApp({super.key});

  @override
  Widget build(BuildContext context) {
    final state = context.watch<AppState>();
    Widget home;
    if (!state.ready) {
      home = const Scaffold(body: Center(child: CircularProgressIndicator()));
    } else if (!state.loggedIn) {
      home = const LoginScreen();
    } else if (state.learner == null) {
      home = const LearnersScreen();
    } else {
      home = const HomeShell();
    }
    return MaterialApp(title: 'FamilyEnglish', debugShowCheckedModeBanner: false, theme: FE.theme(), home: home);
  }
}
