// Learn: the 24 everyday units, grouped by level.
//
// 📘 LEARN: `units.where((u) => u['level'] == level)` filters a list, like a Python list comprehension.
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../state.dart';
import '../theme.dart';
import '../widgets/loader.dart';
import 'unit_screen.dart';

class LearnScreen extends StatelessWidget {
  const LearnScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final api = context.read<AppState>().api;
    return Scaffold(
      appBar: AppBar(title: const Text('Learn', style: TextStyle(fontWeight: FontWeight.w800))),
      body: Loader<List<dynamic>>(
        load: api.units,
        builder: (context, units, reload) => ListView(padding: const EdgeInsets.all(16), children: [
          for (final level in ['A1', 'A2', 'B1']) ...[
            Padding(
              padding: const EdgeInsets.fromLTRB(4, 12, 4, 8),
              child: Text('Everyday English $level', style: const TextStyle(fontSize: 18, fontWeight: FontWeight.w800)),
            ),
            for (final u in units.where((u) => u['level'] == level))
              Card(
                child: InkWell(
                  borderRadius: BorderRadius.circular(22),
                  onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => UnitScreen(slug: u['slug'] as String))).then((_) => reload()),
                  child: Padding(
                    padding: const EdgeInsets.all(16),
                    child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                      Row(children: [
                        Container(
                          padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                          decoration: BoxDecoration(color: (u['number'] as int).isOdd ? FE.sky : FE.violet, borderRadius: BorderRadius.circular(8)),
                          child: Text('Unit ${u['number']}', style: const TextStyle(fontWeight: FontWeight.w800, fontSize: 13)),
                        ),
                        const Spacer(),
                        if (u['locked'] == true) const Icon(Icons.lock, size: 18, color: FE.soft),
                        if (u['done'] == u['total']) const Icon(Icons.check_circle, color: FE.mint),
                      ]),
                      const SizedBox(height: 10),
                      Text('${u['emoji']}  ${u['title']}', style: const TextStyle(fontSize: 20, fontWeight: FontWeight.w800)),
                      const SizedBox(height: 10),
                      LinearProgressIndicator(value: (u['percent'] as num) / 100, color: FE.mint, backgroundColor: FE.line),
                    ]),
                  ),
                ),
              ),
          ],
        ]),
      ),
    );
  }
}
