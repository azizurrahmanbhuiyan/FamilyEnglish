// 🔥 streak · 💎 gems · 🏆 XP — the same numbers as the website's top bar.
import 'package:flutter/material.dart';

import '../theme.dart';

class StatsBar extends StatelessWidget {
  final Map<String, dynamic> bar;
  const StatsBar(this.bar, {super.key});

  Widget _stat(IconData icon, Color color, Object value) => Padding(
        padding: const EdgeInsets.only(left: 12),
        child: Row(children: [Icon(icon, color: color, size: 20), const SizedBox(width: 4), Text('$value', style: const TextStyle(fontWeight: FontWeight.w800))]),
      );

  @override
  Widget build(BuildContext context) => Row(mainAxisSize: MainAxisSize.min, children: [
        _stat(Icons.local_fire_department, bar['active_today'] == true ? FE.coral : FE.soft, bar['streak'] ?? 0),
        _stat(Icons.diamond, FE.violet, bar['gems'] ?? 0),
        _stat(Icons.emoji_events, FE.gold, bar['xp'] ?? 0),
      ]);
}
