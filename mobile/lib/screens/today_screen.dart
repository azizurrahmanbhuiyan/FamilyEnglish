// Today: journey bar, the 3 daily tasks, this week and the word of the day.
//
// 📘 LEARN:
// - `data['tasks'] as List` — JSON lists arrive as List<dynamic>; we cast before using them.
// - Navigator.push opens a new screen on top; `.then(...)` runs when the learner comes back,
//   so we reload to show the new ✓.
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../speech.dart';
import '../state.dart';
import '../theme.dart';
import '../widgets/loader.dart';
import '../widgets/stats_bar.dart';
import 'unit_screen.dart';

class TodayScreen extends StatelessWidget {
  const TodayScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final state = context.read<AppState>();
    return Loader<Map<String, dynamic>>(
      load: state.api.today,
      builder: (context, d, reload) {
        final journey = d['journey'] as Map<String, dynamic>;
        final tasks = d['tasks'] as List;
        final week = d['week'] as List;
        final word = d['word_of_day'] as Map<String, dynamic>?;
        return Scaffold(
          appBar: AppBar(
            title: const Text('Today', style: TextStyle(fontWeight: FontWeight.w800)),
            actions: [StatsBar(d['bar'] as Map<String, dynamic>), IconButton(onPressed: state.switchLearner, icon: Text('${d['learner']['avatar']}', style: const TextStyle(fontSize: 22)))],
          ),
          body: ListView(padding: const EdgeInsets.all(16), children: [
            Card(
              child: Padding(
                padding: const EdgeInsets.all(18),
                child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                  Text('Hello, ${d['learner']['name']} 👋', style: const TextStyle(color: FE.soft)),
                  const SizedBox(height: 4),
                  Row(children: [
                    Text('Your journey · ${journey['current']} → ${journey['next']}', style: const TextStyle(fontSize: 18, fontWeight: FontWeight.w800)),
                    const Spacer(),
                    Text('${journey['percent']}%', style: const TextStyle(fontSize: 22, fontWeight: FontWeight.w800)),
                  ]),
                  const SizedBox(height: 10),
                  ClipRRect(
                    borderRadius: BorderRadius.circular(8),
                    child: LinearProgressIndicator(value: (journey['percent'] as num) / 100, minHeight: 10, color: FE.mint, backgroundColor: Colors.white12),
                  ),
                  if (d['ielts'] != null) Padding(padding: const EdgeInsets.only(top: 8), child: Text('IELTS ≈ ${d['ielts']}', style: const TextStyle(color: FE.soft))),
                ]),
              ),
            ),
            const SizedBox(height: 16),
            const Text("Today's tasks", style: TextStyle(fontSize: 18, fontWeight: FontWeight.w800)),
            const SizedBox(height: 8),
            for (final t in tasks)
              Card(
                child: ListTile(
                  contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 6),
                  leading: CircleAvatar(
                    backgroundColor: (t['done'] == true ? FE.mint : FE.sky).withValues(alpha: .2),
                    child: Icon(t['done'] == true ? Icons.check : Icons.play_arrow, color: t['done'] == true ? FE.mint : FE.sky),
                  ),
                  title: Text('${t['label']}', style: const TextStyle(fontWeight: FontWeight.w800)),
                  subtitle: Text('${t['emoji']} ${t['unit_title']}'),
                  trailing: Text(t['done'] == true ? '1/1' : '0/1'),
                  onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => UnitScreen(slug: t['unit'] as String))).then((_) => reload()),
                ),
              ),
            const SizedBox(height: 16),
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Row(mainAxisAlignment: MainAxisAlignment.spaceBetween, children: [
                  for (final day in week)
                    Column(children: [
                      CircleAvatar(
                        radius: 18,
                        backgroundColor: day['on'] == true ? FE.coral : Colors.white10,
                        child: Icon(Icons.local_fire_department, size: 18, color: day['on'] == true ? Colors.white : Colors.white30),
                      ),
                      const SizedBox(height: 4),
                      Text('${day['label']}'.substring(0, 2), style: TextStyle(fontSize: 12, fontWeight: day['today'] == true ? FontWeight.w800 : FontWeight.w400)),
                    ]),
                ]),
              ),
            ),
            if (word != null) ...[
              const SizedBox(height: 16),
              Card(
                child: Padding(
                  padding: const EdgeInsets.all(18),
                  child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                    const Text('WORD OF THE DAY', style: TextStyle(color: FE.soft, letterSpacing: 1.5, fontSize: 12, fontWeight: FontWeight.w800)),
                    Row(children: [
                      Text('${word['word']}', style: const TextStyle(fontSize: 30, fontWeight: FontWeight.w800)),
                      IconButton(onPressed: () => Speech.say('${word['word']}'), icon: const Icon(Icons.volume_up, color: FE.sky)),
                    ]),
                    Text('${word['ipa']}', style: const TextStyle(color: FE.soft)),
                    const SizedBox(height: 6),
                    Text('${word['definition']}'),
                    if ((word['bn'] ?? '') != '') Text('${word['bn']}', style: const TextStyle(color: FE.soft)),
                  ]),
                ),
              ),
            ],
          ]),
        );
      },
    );
  }
}
