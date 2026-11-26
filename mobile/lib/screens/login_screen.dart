// Log in with the same email and password as the website.
//
// 📘 LEARN: a StatefulWidget keeps the typed text (TextEditingController), a `busy` flag and an
// error message. setState(() {...}) changes them and redraws the screen.
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../state.dart';
import '../theme.dart';
import 'password_screen.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final _email = TextEditingController();
  final _password = TextEditingController();
  bool _busy = false;
  String? _error;

  Future<void> _submit() async {
    setState(() {
      _busy = true;
      _error = null;
    });
    try {
      await context.read<AppState>().login(_email.text.trim(), _password.text);
    } catch (e) {
      setState(() => _error = '$e');
    } finally {
      if (mounted) setState(() => _busy = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: ListView(
          padding: const EdgeInsets.all(24),
          children: [
            const SizedBox(height: 40),
            const Text('🐦', textAlign: TextAlign.center, style: TextStyle(fontSize: 72)),
            const SizedBox(height: 12),
            const Text('FamilyEnglish', textAlign: TextAlign.center, style: TextStyle(fontSize: 30, fontWeight: FontWeight.w800)),
            const Text('ঘরে বসে, পরিবারের সবাই মিলে ইংরেজি', textAlign: TextAlign.center, style: TextStyle(color: FE.soft)),
            const SizedBox(height: 36),
            TextField(controller: _email, keyboardType: TextInputType.emailAddress, decoration: const InputDecoration(labelText: 'Email')),
            const SizedBox(height: 12),
            TextField(controller: _password, obscureText: true, decoration: const InputDecoration(labelText: 'Password'), onSubmitted: (_) => _submit()),
            if (_error != null) Padding(padding: const EdgeInsets.only(top: 12), child: Text(_error!, style: const TextStyle(color: FE.coral))),
            const SizedBox(height: 24),
            FilledButton(onPressed: _busy ? null : _submit, child: Text(_busy ? 'Signing in…' : 'Sign in')),
            TextButton(
              onPressed: () => Navigator.of(context).push(MaterialPageRoute(
                  builder: (_) => ForgotPasswordScreen(email: _email.text.trim()))),
              child: const Text('Forgot password? / পাসওয়ার্ড ভুলে গেছেন?'),
            ),
            const SizedBox(height: 8),
            const Text('No account? Sign up free on familyenglish.global', textAlign: TextAlign.center, style: TextStyle(color: FE.soft)),
          ],
        ),
      ),
    );
  }
}
