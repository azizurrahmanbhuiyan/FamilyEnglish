// Unit lessons 3 and 5: Grammar and Speak freely.
//
// 📘 LEARN:
// - GrammarScreen shows the rule first, then one practice task at a time. Each task has a type:
//   fill / fix (type the answer), say (speak the sentence) and make (write your own sentence).
// - SpeakScreen listens for up to a minute, then the server gives feedback (/analyse/).
// - Both call /finish/ at the end, so the lesson is ticked on the website too.
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../speech.dart';
import '../state.dart';
import '../theme.dart';

String _clean(String s) => s.toLowerCase().replaceAll(RegExp(r"[^a-z0-9' ]"), ' ').replaceAll(RegExp(r'\s+'), ' ').trim();

class GrammarScreen extends StatefulWidget {
  final Map<String, dynamic> lesson; // from the unit: rule, examples, practice, key
  final String unitKey;
  final String title;
  const GrammarScreen({super.key, required this.lesson, required this.unitKey, required this.title});

  @override
  State<GrammarScreen> createState() => _GrammarScreenState();
}

class _GrammarScreenState extends State<GrammarScreen> {
  int _i = -1; // -1 = the rule page
  int _right = 0;
  bool? _ok;
  String _feedback = '';
  bool _busy = false;
  Map<String, dynamic>? _finished;
  final _answer = TextEditingController();

  List get _practice => widget.lesson['practice'] as List;
  Map<String, dynamic> get _task => Map<String, dynamic>.from(_practice[_i] as Map);

  void _check() {
    final t = _task;
    final said = _answer.text.trim();
    if (said.isEmpty) return;
    bool ok;
    if (t['type'] == 'make') {
      ok = RegExp('${t['pattern']}', caseSensitive: false).hasMatch(said);
      _feedback = ok ? 'Well done!' : 'Use the words the task asks for and try again.';
    } else {
      final accepted = (t['accepted'] as List).map((a) => _clean('$a')).toList();
      ok = accepted.contains(_clean(said));
      _feedback = ok ? 'Correct!' : 'Answer: ${(t['accepted'] as List).first}';
    }
    setState(() {
      _ok = ok;
      if (ok) _right++;
    });
  }

  Future<void> _say() async {
    setState(() => _busy = true);
    final heard = await Speech.listen(seconds: 10);
    if (!mounted) return;
    if (heard == null) {
      setState(() {
        _busy = false;
        _feedback = Speech.lastProblem ?? "I didn't hear you.";
      });
      return;
    }
    final r = await context.read<AppState>().api.attempt(key: '${widget.lesson['key']}', target: '${_task['prompt']}', said: heard.text);
    final score = (r['score'] as num).toInt();
    setState(() {
      _busy = false;
      _ok = score >= 70;
      if (_ok!) _right++;
      _feedback = '$score% · I heard: “${heard.text}”';
    });
  }

  Future<void> _next() async {
    if (_i + 1 >= _practice.length) {
      final score = (_right * 100 / _practice.length).round();
      final api = context.read<AppState>().api;
      await api.finish(key: '${widget.lesson['key']}', title: '${widget.lesson['title']}', score: score);
      final r = await api.finish(key: widget.unitKey, title: widget.title, score: score);
      setState(() => _finished = {...r, 'avg': score});
      return;
    }
    setState(() {
      _i++;
      _ok = null;
      _feedback = '';
      _answer.clear();
    });
    if (_task['type'] == 'say') Speech.say('${_task['prompt']}');
  }

  @override
  Widget build(BuildContext context) {
    final l = widget.lesson;
    if (_finished != null) return DoneView(title: widget.title, result: _finished!);
    return Scaffold(
      appBar: AppBar(title: Text(widget.title, style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w800))),
      body: ListView(padding: const EdgeInsets.all(16), children: [
        if (_i >= 0) LinearProgressIndicator(value: _i / _practice.length, color: FE.sky, backgroundColor: FE.line),
        const SizedBox(height: 12),
        if (_i < 0) ...[
          Text('${l['title']}', style: const TextStyle(fontSize: 28, fontWeight: FontWeight.w800)),
          Text('${(l['hello'] as List).first}', style: const TextStyle(color: FE.soft)),
          const SizedBox(height: 12),
          Wrap(spacing: 8, runSpacing: 8, children: [
            for (final f in l['formula'] as List)
              Chip(label: Text('$f', style: const TextStyle(fontWeight: FontWeight.w700)), backgroundColor: FE.panel),
          ]),
          const SizedBox(height: 12),
          Card(child: Padding(padding: const EdgeInsets.all(16), child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
            Text('${(l['rule'] as List).first}', style: const TextStyle(fontSize: 17)),
            const SizedBox(height: 8),
            Text('${(l['rule'] as List).last}', style: const TextStyle(color: FE.soft)),
          ]))),
          for (final e in l['examples'] as List)
            ListTile(
              title: Text('${e['en']}', style: const TextStyle(fontWeight: FontWeight.w700)),
              subtitle: Text('${e['bn']}'),
              trailing: IconButton(icon: const Icon(Icons.volume_up, color: FE.sky), onPressed: () => Speech.say('${e['en']}')),
            ),
          const SizedBox(height: 16),
          FilledButton(onPressed: _next, child: const Text('Start practice')),
        ] else ..._taskView(),
      ]),
    );
  }

  List<Widget> _taskView() {
    final t = _task;
    final type = '${t['type']}';
    final ask = switch (type) {
      'fill' => 'Fill the gap:',
      'fix' => 'Fix the mistake. Type the whole sentence:',
      'say' => 'Say this sentence:',
      _ => 'Write your own sentence:',
    };
    return [
      Text(ask, style: const TextStyle(color: FE.soft)),
      const SizedBox(height: 8),
      Text('${t['prompt']}', style: const TextStyle(fontSize: 24, fontWeight: FontWeight.w800)),
      const SizedBox(height: 16),
      if (type == 'say')
        Row(children: [
          IconButton(onPressed: () => Speech.say('${t['prompt']}'), icon: const Icon(Icons.volume_up, color: FE.sky, size: 32)),
          const SizedBox(width: 12),
          Expanded(
            child: FilledButton.icon(
              onPressed: _busy || _ok != null ? null : _say,
              icon: const Icon(Icons.mic),
              label: Text(_busy ? 'Listening…' : 'Tap and speak'),
            ),
          ),
        ])
      else ...[
        TextField(
          controller: _answer,
          enabled: _ok == null,
          autocorrect: false,
          decoration: const InputDecoration(hintText: 'Type here'),
          onSubmitted: (_) => _check(),
        ),
        const SizedBox(height: 12),
        if (_ok == null) FilledButton(onPressed: _check, child: const Text('Check')),
      ],
      if (_feedback.isNotEmpty)
        Padding(
          padding: const EdgeInsets.only(top: 12),
          child: Text(_feedback, style: TextStyle(fontSize: 17, fontWeight: FontWeight.w700, color: _ok == true ? FE.ok : (_ok == false ? FE.bad : FE.soft))),
        ),
      if (_ok != null) ...[
        const SizedBox(height: 16),
        FilledButton(onPressed: _next, child: Text(_i + 1 >= _practice.length ? 'Finish' : 'Next')),
      ],
    ];
  }
}

class SpeakScreen extends StatefulWidget {
  final String lessonKey;
  final String title;
  final String prompt;
  final int seconds;
  final int minWords;
  const SpeakScreen({super.key, required this.lessonKey, required this.title, required this.prompt, this.seconds = 60, this.minWords = 45});

  @override
  State<SpeakScreen> createState() => _SpeakScreenState();
}

class _SpeakScreenState extends State<SpeakScreen> {
  bool _listening = false;
  String _problem = '';
  Map<String, dynamic>? _result;
  Map<String, dynamic>? _finished;

  Future<void> _speak() async {
    setState(() {
      _listening = true;
      _problem = '';
    });
    final started = DateTime.now();
    final heard = await Speech.listen(seconds: widget.seconds);
    if (!mounted) return;
    setState(() => _listening = false);
    if (heard == null) {
      setState(() => _problem = Speech.lastProblem ?? "I didn't hear you.");
      return;
    }
    final secs = DateTime.now().difference(started).inSeconds.clamp(1, widget.seconds);
    final r = await context.read<AppState>().api.analyse(key: widget.lessonKey, prompt: widget.prompt, transcript: heard.text, seconds: secs);
    setState(() => _result = {...r, 'heard': heard.text});
  }

  Future<void> _finish() async {
    final score = (_result!['overall'] as num).toInt();
    final r = await context.read<AppState>().api.finish(key: widget.lessonKey, title: widget.title, score: score);
    setState(() => _finished = {...r, 'avg': score});
  }

  @override
  Widget build(BuildContext context) {
    if (_finished != null) return DoneView(title: widget.title, result: _finished!);
    final r = _result;
    return Scaffold(
      appBar: AppBar(title: Text(widget.title, style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w800))),
      body: ListView(padding: const EdgeInsets.all(16), children: [
        const Text('Speak freely', style: TextStyle(color: FE.soft)),
        Text(widget.prompt, style: const TextStyle(fontSize: 22, fontWeight: FontWeight.w800)),
        const SizedBox(height: 6),
        Text('Aim for ${widget.minWords}+ words. You have up to ${widget.seconds} seconds. Pause for 4 seconds when you finish.',
            style: const TextStyle(color: FE.soft)),
        const SizedBox(height: 20),
        if (r == null) ...[
          Center(
            child: SizedBox(
              width: 110,
              height: 110,
              child: FilledButton(
                style: FilledButton.styleFrom(backgroundColor: _listening ? FE.coral : FE.sky, shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(34))),
                onPressed: _listening ? Speech.stopListening : _speak,
                child: Icon(_listening ? Icons.stop : Icons.mic, size: 46),
              ),
            ),
          ),
          const SizedBox(height: 10),
          Center(child: Text(_listening ? 'Listening… speak now' : 'Tap to start', style: const TextStyle(fontSize: 18, fontWeight: FontWeight.w700))),
          if (_problem.isNotEmpty) Padding(padding: const EdgeInsets.only(top: 12), child: Text(_problem, style: const TextStyle(color: FE.bad))),
        ] else ...[
          Card(child: Padding(padding: const EdgeInsets.all(16), child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
            Text('${r['overall']}%', style: const TextStyle(fontSize: 40, fontWeight: FontWeight.w800, color: FE.mint)),
            Text('${r['words']} words · ${r['wpm']} words a minute', style: const TextStyle(color: FE.soft)),
            const Divider(height: 24),
            for (final t in r['tips'] as List) Padding(padding: const EdgeInsets.only(bottom: 8), child: Text('💡 ${t['en']}\n${t['bn']}')),
            const Divider(height: 24),
            Text('I heard: “${r['heard']}”', style: const TextStyle(color: FE.soft)),
          ]))),
          const SizedBox(height: 12),
          FilledButton(onPressed: _finish, child: const Text('Save and finish')),
          TextButton(onPressed: () => setState(() => _result = null), child: const Text('Try again')),
        ],
      ]),
    );
  }
}

/// The end of a lesson: score, XP and gems.
class DoneView extends StatelessWidget {
  final String title;
  final Map<String, dynamic> result;
  const DoneView({super.key, required this.title, required this.result});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(title, style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w800))),
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(24),
          child: Column(mainAxisSize: MainAxisSize.min, children: [
            const Text('🎉', style: TextStyle(fontSize: 80)),
            Text('${result['avg']}%', style: const TextStyle(fontSize: 48, fontWeight: FontWeight.w800, color: FE.mint)),
            if (result['first'] == true) Text('+${result['xp']} XP · +${result['gems_earned']} 💎', style: const TextStyle(fontSize: 18)),
            const SizedBox(height: 24),
            FilledButton(onPressed: () => Navigator.of(context).pop(), child: const Text('Back to the unit')),
          ]),
        ),
      ),
    );
  }
}
