// One unit: what you will be able to do, and its 5 lessons.
// All five lessons work in the app: key words, sound practice, grammar, a scripted conversation
// and speaking freely.
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../state.dart';
import '../theme.dart';
import '../widgets/loader.dart';
import 'lesson_screens.dart';
import 'repeat_screen.dart';

class UnitScreen extends StatelessWidget {
  final String slug;
  const UnitScreen({super.key, required this.slug});

  @override
  Widget build(BuildContext context) {
    final api = context.read<AppState>().api;
    return Scaffold(
      appBar: AppBar(),
      body: Loader<Map<String, dynamic>>(
        load: () => api.unit(slug),
        builder: (context, u, reload) {
          final lessons = u['lessons'] as List;
          return ListView(padding: const EdgeInsets.all(16), children: [
            Text('${u['emoji']} ${u['title']}', style: const TextStyle(fontSize: 28, fontWeight: FontWeight.w800)),
            Text('${u['desc']}', style: const TextStyle(color: FE.soft)),
            const SizedBox(height: 16),
            Card(
              child: ListTile(
                leading: const CircleAvatar(backgroundColor: FE.ok, child: Icon(Icons.check, color: Colors.white)),
                title: const Text('At the end of this unit, you can:', style: TextStyle(color: FE.soft, fontSize: 13)),
                subtitle: Text('${u['outcome']}', style: const TextStyle(fontSize: 17, color: FE.ink)),
              ),
            ),
            const SizedBox(height: 12),
            if (u['locked'] == true)
              const Card(child: Padding(padding: EdgeInsets.all(20), child: Text('🔒 This unit is in the family plan. The first unit is free.'))),
            for (final l in lessons)
              Card(
                child: ListTile(
                  contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                  leading: CircleAvatar(
                    radius: 24,
                    backgroundColor: l['done'] == true ? FE.mint : FE.violet,
                    child: Icon(_icon('${l['kind']}'), color: Colors.white),
                  ),
                  title: Text('Lesson ${l['n']} - ${l['title']}', style: const TextStyle(fontWeight: FontWeight.w800)),
                  subtitle: Text('${l['difficulty']}'.toUpperCase(), style: const TextStyle(letterSpacing: 1.5, fontSize: 12)),
                  trailing: l['done'] == true ? const Icon(Icons.check_circle, color: FE.mint) : const Icon(Icons.chevron_right),
                  onTap: u['locked'] == true ? null : () => _open(context, u, l as Map<String, dynamic>, reload),
                ),
              ),
          ]);
        },
      ),
    );
  }

  IconData _icon(String kind) => switch (kind) {
        'words' => Icons.repeat,
        'sounds' => Icons.graphic_eq,
        'speak' => Icons.mic,
        _ => Icons.chat_bubble,
      };

  void _open(BuildContext context, Map<String, dynamic> u, Map<String, dynamic> l, Future<void> Function() reload) {
    final kind = l['kind'];
    final key = 'unit:${u['slug']}:${l['n']}';
    final title = '${u['title']} · ${l['title']}';
    Widget screen;
    if (kind == 'words') {
      screen = RepeatScreen(lessonKey: key, title: title, items: List<Map<String, dynamic>>.from(u['words'] as List));
    } else if (kind == 'sounds') {
      screen = RepeatScreen(lessonKey: key, title: title, items: List<Map<String, dynamic>>.from(u['phrases'] as List));
    } else if (kind == 'convo') {
      final lines = [
        for (final c in u['conversation'] as List) {'prompt': c['coach'], 'text': c['reply'], 'bn': c['hint']}
      ];
      screen = RepeatScreen(lessonKey: key, title: title, items: lines);
    } else if (kind == 'grammar' && u['grammar_lesson'] != null) {
      screen = GrammarScreen(lesson: Map<String, dynamic>.from(u['grammar_lesson'] as Map), unitKey: key, title: title);
    } else {
      screen = SpeakScreen(
        lessonKey: key,
        title: title,
        prompt: '${u['speak_prompt']}',
        seconds: (u['speak_seconds'] as num?)?.toInt() ?? 60,
        minWords: (u['speak_min_words'] as num?)?.toInt() ?? 45,
      );
    }
    Navigator.push(context, MaterialPageRoute(builder: (_) => screen)).then((_) => reload());
  }
}
