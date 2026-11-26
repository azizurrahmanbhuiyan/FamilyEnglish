// Forgot password (emailed 6-digit code) and change password.
//
// 📘 LEARN: one screen with two steps. `_sent` decides which fields show: first the email,
// then the code and the new password. Navigator.pop closes the screen when it worked.
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../state.dart';
import '../theme.dart';

class ForgotPasswordScreen extends StatefulWidget {
  final String email;
  const ForgotPasswordScreen({super.key, this.email = ''});

  @override
  State<ForgotPasswordScreen> createState() => _ForgotPasswordScreenState();
}

class _ForgotPasswordScreenState extends State<ForgotPasswordScreen> {
  late final _email = TextEditingController(text: widget.email);
  final _code = TextEditingController();
  final _password = TextEditingController();
  bool _sent = false;
  bool _busy = false;
  String? _error;
  String? _info;

  Future<void> _run(Future<void> Function() job) async {
    setState(() {
      _busy = true;
      _error = null;
    });
    try {
      await job();
    } catch (e) {
      if (mounted) setState(() => _error = '$e');
    } finally {
      if (mounted) setState(() => _busy = false);
    }
  }

  Future<void> _sendCode() => _run(() async {
        await context.read<AppState>().api.passwordCode(_email.text.trim());
        setState(() {
          _sent = true;
          _info = 'If an account exists, we sent a 6-digit code to its email. Check spam too.';
        });
      });

  Future<void> _save() => _run(() async {
        await context.read<AppState>().resetPassword(_email.text.trim(), _code.text.trim(), _password.text);
        if (mounted) Navigator.of(context).pop();
      });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Forgot password')),
      body: ListView(
        padding: const EdgeInsets.all(24),
        children: [
          const Text('পাসওয়ার্ড ভুলে গেছেন? ইমেইলে একটি কোড পাঠাব, তারপর নতুন পাসওয়ার্ড দিন।',
              style: TextStyle(color: FE.soft)),
          const SizedBox(height: 20),
          TextField(
              controller: _email,
              enabled: !_sent,
              keyboardType: TextInputType.emailAddress,
              decoration: const InputDecoration(labelText: 'Email')),
          if (_sent) ...[
            const SizedBox(height: 12),
            TextField(
                controller: _code,
                keyboardType: TextInputType.number,
                maxLength: 6,
                decoration: const InputDecoration(labelText: '6-digit code')),
            TextField(
                controller: _password,
                obscureText: true,
                decoration: const InputDecoration(labelText: 'New password (at least 8 characters)'),
                onSubmitted: (_) => _save()),
          ],
          if (_info != null) Padding(padding: const EdgeInsets.only(top: 12), child: Text(_info!, style: const TextStyle(color: FE.mint))),
          if (_error != null) Padding(padding: const EdgeInsets.only(top: 12), child: Text(_error!, style: const TextStyle(color: FE.coral))),
          const SizedBox(height: 24),
          FilledButton(
            onPressed: _busy ? null : (_sent ? _save : _sendCode),
            child: Text(_busy ? 'Please wait…' : (_sent ? 'Save and sign in' : 'Send me a code')),
          ),
          if (_sent)
            TextButton(onPressed: _busy ? null : _sendCode, child: const Text('Send the code again')),
        ],
      ),
    );
  }
}

/// A small dialog to change the password while signed in.
Future<void> showChangePassword(BuildContext context) {
  final old = TextEditingController();
  final fresh = TextEditingController();
  String? error;
  bool busy = false;
  return showDialog(
    context: context,
    builder: (ctx) => StatefulBuilder(
      builder: (ctx, setState) => AlertDialog(
        title: const Text('Change password'),
        content: Column(mainAxisSize: MainAxisSize.min, children: [
          TextField(controller: old, obscureText: true, decoration: const InputDecoration(labelText: 'Current password')),
          TextField(controller: fresh, obscureText: true, decoration: const InputDecoration(labelText: 'New password (at least 8)')),
          if (error != null) Padding(padding: const EdgeInsets.only(top: 12), child: Text(error!, style: const TextStyle(color: FE.coral))),
        ]),
        actions: [
          TextButton(onPressed: () => Navigator.of(ctx).pop(), child: const Text('Cancel')),
          FilledButton(
            onPressed: busy
                ? null
                : () async {
                    setState(() {
                      busy = true;
                      error = null;
                    });
                    try {
                      await context.read<AppState>().changePassword(old.text, fresh.text);
                      if (ctx.mounted) Navigator.of(ctx).pop();
                      if (context.mounted) {
                        ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Your new password is saved.')));
                      }
                    } catch (e) {
                      setState(() {
                        busy = false;
                        error = '$e';
                      });
                    }
                  },
            child: Text(busy ? 'Saving…' : 'Save'),
          ),
        ],
      ),
    ),
  );
}
