// "Repeat after me": hear the word, say it, see which words were clear.
//
// 📘 LEARN:
// - RichText + TextSpan let one line have different styles (the underlined target sound).
// - The server does the scoring (/attempt/), so the app and the website give the same scores.
// - When all items are done we call /finish/ to save the lesson and earn XP and gems.
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../speech.dart';
import '../state.dart';
import '../theme.dart';

class RepeatScreen extends StatefulWidget {
  final String lessonKey;
  final String title;
  final List<Map<String, dynamic>> items;
  const RepeatScreen({super.key, required this.lessonKey, required this.title, required this.items});

  @override
  State<RepeatScreen> createState() => _RepeatScreenState();
}

class _RepeatScreenState extends State<RepeatScreen> {
  int _i = 0;
  final List<int> _scores = [];
  int _best = 0;
  bool _listening = false;
  bool _advanced = false;
  Map<String, dynamic>? _result; // {score, marks, heard}
  Map<String, dynamic>? _finished;

  Map<String, dynamic> get _item => widget.items[_i];
  int get _pass => _advanced ? 85 : 70;

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) => Speech.say('${_item['prompt'] ?? _item['text']}'));
  }

  Future<void> _speak() async {
    setState(() => _listening = true);
    final heard = await Speech.listen();
    if (!mounted) return;
    setState(() => _listening = false);
    if (heard == null || heard.text.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(Speech.lastProblem ?? "I didn't hear you. Tap the mic and speak clearly.")));
      return;
    }
    final api = context.read<AppState>().api;
    final r = await api.attempt(key: widget.lessonKey, target: '${_item['text']}', said: heard.text, confidence: heard.confidence);
    final score = (r['score'] as num).toInt();
    if (score > _best) _best = score;
    setState(() => _result = {...r, 'heard': heard.text});
  }

  Future<void> _next() async {
    _scores.add(_best);
    if (_i + 1 >= widget.items.length) {
      final avg = (_scores.reduce((a, b) => a + b) / _scores.length).round();
      final api = context.read<AppState>().api;
      final r = await api.finish(key: widget.lessonKey, title: widget.title, score: avg);
      setState(() => _finished = {...r, 'avg': avg});
      return;
    }
    setState(() {
      _i++;
      _best = 0;
      _result = null;
    });
    Speech.say('${_item['prompt'] ?? _item['text']}');
  }

  @override
  Widget build(BuildContext context) {
    if (_finished != null) return _doneView();
    final it = _item;
    final r = _result;
    final ok = r != null && (r['score'] as num) >= _pass;
    return Scaffold(
      appBar: AppBar(title: Text(widget.title, style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w800))),
      body: SafeArea(
        child: Column(children: [
          LinearProgressIndicator(value: _i / widget.items.length, color: FE.sky, backgroundColor: FE.line),
          const SizedBox(height: 16),
          const Text('🐦', style: TextStyle(fontSize: 80)),
          SegmentedButton<bool>(
            segments: const [ButtonSegment(value: false, label: Text('Regular')), ButtonSegment(value: true, label: Text('Advanced'))],
            selected: {_advanced},
            onSelectionChanged: (s) => setState(() => _advanced = s.first),
          ),
          Expanded(
            child: SingleChildScrollView(
              padding: const EdgeInsets.all(16),
              child: Container(
                width: double.infinity,
                padding: const EdgeInsets.all(20),
                decoration: BoxDecoration(color: FE.panel, borderRadius: BorderRadius.circular(26)),
                child: DefaultTextStyle(
                  style: const TextStyle(color: FE.ink),
                  child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                    if (it['prompt'] != null) ...[
                      Row(crossAxisAlignment: CrossAxisAlignment.start, children: [
                        const Text('🐦 ', style: TextStyle(fontSize: 22)),
                        Expanded(child: Text('${it['prompt']}', style: const TextStyle(fontSize: 19, fontWeight: FontWeight.w700))),
                        IconButton(onPressed: () => Speech.say('${it['prompt']}'), icon: const Icon(Icons.volume_up, color: FE.sky)),
                      ]),
                      const Text('Your answer — say this:', style: TextStyle(color: FE.soft)),
                      const SizedBox(height: 8),
                    ],
                    if (r == null && it['prompt'] == null)
                      const Text('Speak and get feedback on the underlined sound.', style: TextStyle(color: FE.soft))
                    else if (r == null)
                      const SizedBox.shrink()
                    else ...[
                      Row(children: [
                        Icon(ok ? Icons.check_circle : Icons.cancel, color: ok ? FE.ok : FE.bad),
                        const SizedBox(width: 6),
                        Text(ok ? 'Correct' : 'Try again', style: TextStyle(fontSize: 24, fontWeight: FontWeight.w800, color: ok ? FE.ok : FE.bad)),
                        const Spacer(),
                        Text('${r['score']}%', style: TextStyle(fontSize: 30, fontWeight: FontWeight.w800, color: ok ? FE.ok : FE.bad)),
                      ]),
                      if (!ok && (it['tip_en'] ?? '') != '') Padding(padding: const EdgeInsets.only(top: 6), child: Text('${it['tip_en']}')),
                      Padding(padding: const EdgeInsets.only(top: 6), child: Text('I heard: “${r['heard']}”', style: const TextStyle(color: FE.soft))),
                    ],
                    const Divider(height: 28),
                    _wordView(it, r),
                    if ((it['ipa'] ?? '') != '') Text('${it['ipa']}', style: const TextStyle(fontSize: 18, color: FE.soft)),
                    if ((it['bn'] ?? '') != '') Text('${it['bn']}', style: const TextStyle(color: FE.soft)),
                    const SizedBox(height: 12),
                    Row(children: [
                      IconButton(onPressed: () => Speech.say('${it['text']}'), icon: const Icon(Icons.volume_up, color: FE.sky, size: 32)),
                      IconButton(onPressed: () => Speech.say('${it['text']}', slow: true), icon: const Icon(Icons.slow_motion_video, color: FE.sky, size: 32)),
                    ]),
                  ]),
                ),
              ),
            ),
          ),
          Padding(
            padding: const EdgeInsets.fromLTRB(16, 0, 16, 16),
            child: r == null
                ? Column(children: [
                    Text(_listening ? 'Listening…' : 'Tap to speak', style: const TextStyle(fontSize: 18, fontWeight: FontWeight.w700)),
                    const SizedBox(height: 10),
                    SizedBox(
                      width: 96,
                      height: 96,
                      child: FilledButton(
                        style: FilledButton.styleFrom(backgroundColor: _listening ? FE.coral : FE.sky, shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(30))),
                        onPressed: _listening ? Speech.stopListening : _speak,
                        child: Icon(_listening ? Icons.stop : Icons.mic, size: 42),
                      ),
                    ),
                  ])
                : ok
                    ? FilledButton(onPressed: _next, child: const Text('Continue'))
                    : Row(children: [
                        Expanded(child: FilledButton(onPressed: () => setState(() => _result = null), child: const Text('Retry'))),
                        const SizedBox(width: 12),
                        Expanded(child: OutlinedButton(onPressed: _next, child: const Text('Skip'))),
                      ]),
          ),
        ]),
      ),
    );
  }

  /// The word with its target sound underlined, or coloured green/red after a try.
  Widget _wordView(Map<String, dynamic> it, Map<String, dynamic>? r) {
    const big = TextStyle(fontSize: 34, fontWeight: FontWeight.w700, color: FE.ink);
    final marks = (r?['marks'] as List?) ?? [];
    if (marks.isNotEmpty) {
      return RichText(
        text: TextSpan(style: big, children: [
          for (final m in marks) TextSpan(text: '${m['w']} ', style: TextStyle(color: m['ok'] == true ? FE.ok : FE.bad)),
        ]),
      );
    }
    final target = '${it['target'] ?? ''}';
    if (target.isEmpty) return Text('${it['text']}', style: big);
    return RichText(
      text: TextSpan(style: big, children: [
        TextSpan(text: '${it['before']}'),
        TextSpan(text: target, style: const TextStyle(decoration: TextDecoration.underline, decorationThickness: 3)),
        TextSpan(text: '${it['after']}'),
      ]),
    );
  }

  Widget _doneView() {
    final f = _finished!;
    return Scaffold(
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(24),
          child: Column(mainAxisAlignment: MainAxisAlignment.center, children: [
            const Text('🐦', style: TextStyle(fontSize: 96)),
            Text('${f['avg']}%', style: const TextStyle(fontSize: 56, fontWeight: FontWeight.w800, color: FE.mint)),
            Text((f['avg'] as int) >= 70 ? 'Well done!' : 'Good effort — practise once more!', style: const TextStyle(fontSize: 20, fontWeight: FontWeight.w700)),
            const SizedBox(height: 12),
            if (f['first'] == true) Text('⚡ +${f['xp']} XP   💎 +${f['gems_earned']}', style: const TextStyle(fontSize: 18)),
            const SizedBox(height: 32),
            FilledButton(onPressed: () => Navigator.pop(context), child: const Text('Continue')),
          ]),
        ),
      ),
    );
  }
}
