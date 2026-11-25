// "Who's learning?" — pick a family member.
//
// 📘 LEARN: GridView.count makes a grid; `for (final l in ...)` inside a list builds one tile per learner.
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../state.dart';
import '../theme.dart';

class LearnersScreen extends StatelessWidget {
  const LearnersScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final state = context.watch<AppState>();
    return Scaffold(
      appBar: AppBar(title: const Text("Who's learning?"), actions: [
        IconButton(onPressed: state.logout, icon: const Icon(Icons.logout), tooltip: 'Sign out'),
      ]),
      body: state.learners.isEmpty
          ? const Center(child: Text('Add a learner on the website first.'))
          : GridView.count(
              padding: const EdgeInsets.all(20),
              crossAxisCount: 2,
              mainAxisSpacing: 16,
              crossAxisSpacing: 16,
              children: [
                for (final l in state.learners)
                  InkWell(
                    borderRadius: BorderRadius.circular(22),
                    onTap: () => state.chooseLearner(l),
                    child: Card(
                      child: Column(mainAxisAlignment: MainAxisAlignment.center, children: [
                        Text('${l['avatar']}', style: const TextStyle(fontSize: 56)),
                        const SizedBox(height: 8),
                        Text('${l['name']}', style: const TextStyle(fontSize: 18, fontWeight: FontWeight.w800)),
                      ]),
                    ),
                  ),
              ],
            ),
      bottomNavigationBar: Padding(
        padding: const EdgeInsets.all(16),
        child: Text(state.paid ? 'Family plan ✓' : 'Free: phonics and the first unit', textAlign: TextAlign.center, style: const TextStyle(color: FE.soft)),
      ),
    );
  }
}
