// Progress: five skill scores, level, learning time and history.
//
// 📘 LEARN: `num` covers both int and double — JSON numbers can be either.
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../state.dart';
import '../theme.dart';
import 'password_screen.dart';
import '../widgets/loader.dart';

class ProgressScreen extends StatelessWidget {
  const ProgressScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final state = context.read<AppState>();
    return Scaffold(
      appBar: AppBar(title: const Text('Progress', style: TextStyle(fontWeight: FontWeight.w800)), actions: [
        IconButton(onPressed: () => showChangePassword(context), icon: const Icon(Icons.key), tooltip: 'Change password'),
        IconButton(onPressed: state.logout, icon: const Icon(Icons.logout), tooltip: 'Sign out'),
      ]),
      body: Loader<Map<String, dynamic>>(
        load: state.api.progress,
        builder: (context, p, reload) {
          final sc = p['scores'] as Map<String, dynamic>;
          final parts = sc['parts'] as List;
          final history = p['history'] as List;
          final badges = (p['badges'] as List).where((b) => b['earned'] == true).toList();
          return ListView(padding: const EdgeInsets.all(16), children: [
            Card(
              child: Padding(
                padding: const EdgeInsets.all(18),
                child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                  Row(children: [
                    const Text('English proficiency', style: TextStyle(fontSize: 18, fontWeight: FontWeight.w800)),
                    const Spacer(),
                    if (sc['cefr'] != null) Chip(label: Text('${sc['cefr']} · IELTS ≈ ${sc['ielts']}')),
                  ]),
                  const SizedBox(height: 8),
                  for (final part in parts) ...[
                    const SizedBox(height: 10),
                    Row(children: [
                      Text('${part['en']}'),
                      const Spacer(),
                      Text(part['score'] == null ? '–' : '${part['score']}', style: const TextStyle(fontWeight: FontWeight.w800)),
                    ]),
                    const SizedBox(height: 4),
                    LinearProgressIndicator(value: ((part['score'] ?? 0) as num) / 100, color: FE.sky, backgroundColor: FE.line, minHeight: 8),
                  ],
                ]),
              ),
            ),
            Row(children: [
              Expanded(child: _stat('${(p['learning_minutes'] as num) ~/ 60}h ${(p['learning_minutes'] as num) % 60}m', 'Learning time')),
              Expanded(child: _stat('${p['lessons']}', 'Lessons')),
            ]),
            if (badges.isNotEmpty)
              Card(
                child: Padding(
                  padding: const EdgeInsets.all(16),
                  child: Wrap(spacing: 12, runSpacing: 12, children: [
                    for (final b in badges) Chip(avatar: Text('${b['icon']}'), label: Text('${b['name']}')),
                  ]),
                ),
              ),
            const Padding(padding: EdgeInsets.fromLTRB(4, 16, 4, 8), child: Text('Lesson history', style: TextStyle(fontSize: 18, fontWeight: FontWeight.w800))),
            for (final h in history)
              ListTile(leading: const Icon(Icons.check_circle, color: FE.mint), title: Text('${h['title']}'), subtitle: Text('${h['date']}'), trailing: Text('${h['score']}%')),
            if (history.isEmpty) const Padding(padding: EdgeInsets.all(16), child: Text('Finished lessons will appear here.', style: TextStyle(color: FE.soft))),
          ]);
        },
      ),
    );
  }

  Widget _stat(String value, String label) => Card(
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
            Text(value, style: const TextStyle(fontSize: 24, fontWeight: FontWeight.w800)),
            Text(label, style: const TextStyle(color: FE.soft)),
          ]),
        ),
      );
}
