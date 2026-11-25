// One unit: what you will be able to do, and its 5 lessons.
// Lessons 1 (key words) and 2 (sound practice) work in the app now; the others open on the website
// until you build them in the next lessons of your Flutter course.
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../state.dart';
import '../theme.dart';
import '../widgets/loader.dart';
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
                subtitle: Text('${u['outcome']}', style: const TextStyle(fontSize: 17, color: Colors.white)),
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
    List<Map<String, dynamic>> items;
    if (kind == 'words') {
      items = List<Map<String, dynamic>>.from(u['words'] as List);
    } else if (kind == 'sounds') {
      items = List<Map<String, dynamic>>.from(u['phrases'] as List);
    } else {
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(
        content: Text('Coming in the next lesson of your Flutter course! Use the website for this one for now.'),
      ));
      return;
    }
    Navigator.push(
      context,
      MaterialPageRoute(builder: (_) => RepeatScreen(lessonKey: 'unit:${u['slug']}:${l['n']}', title: '${u['title']} · ${l['title']}', items: items)),
    ).then((_) => reload());
  }
}
