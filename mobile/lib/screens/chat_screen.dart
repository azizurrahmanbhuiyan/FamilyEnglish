// The Talk conversation and the lesson report.
//
// 📘 LEARN:
// - The tutor's reply comes from the server (/talk/<id>/reply/). With AI on it's a real reply;
//   without AI the server uses prepared lines, so this screen works the same either way.
// - ScrollController lets us scroll to the newest message after each reply.
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../speech.dart';
import '../state.dart';
import '../theme.dart';
import '../widgets/loader.dart';

/// The learner's chosen tutor voice (set when the Talk tab loads).
class TalkVoice {
  static double speed = 1.0;
  static double pitch = 1.0;
  static Future<void> say(String text, {bool slow = false}) => Speech.say(text, slow: slow, speed: speed, pitch: pitch);
}

class ChatScreen extends StatefulWidget {
  final Map<String, dynamic> session;
  const ChatScreen({super.key, required this.session});

  @override
  State<ChatScreen> createState() => _ChatScreenState();
}

class _ChatScreenState extends State<ChatScreen> {
  late final List<Map<String, dynamic>> _msgs = [for (final m in widget.session['messages'] as List) Map<String, dynamic>.from(m)];
  final Map<int, String> _translations = {};
  final _scroll = ScrollController();
  final _text = TextEditingController();
  bool _listening = false, _busy = false, _typing = false, _done = false;
  String _status = 'Tap the microphone and answer';

  int get _id => widget.session['id'] as int;
  int get _turns => _msgs.where((m) => m['role'] == 'user').length;

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) => TalkVoice.say('${_msgs.last['content']}'));
  }

  void _toBottom() => WidgetsBinding.instance.addPostFrameCallback((_) {
        if (_scroll.hasClients) _scroll.animateTo(_scroll.position.maxScrollExtent, duration: const Duration(milliseconds: 300), curve: Curves.easeOut);
      });

  Future<void> _send(String text, {double? confidence, int seconds = 0}) async {
    text = text.trim();
    if (text.isEmpty || _busy) return;
    setState(() {
      _busy = true;
      _msgs.add({'role': 'user', 'content': text});
      _status = 'Your tutor is thinking…';
    });
    _toBottom();
    try {
      final d = Map<String, dynamic>.from(await context.read<AppState>().api.post('/talk/$_id/reply/', {'text': text, 'confidence': confidence, 'seconds': seconds}));
      if (!mounted) return;
      setState(() {
        if ('${d['reply']}'.isNotEmpty) _msgs.add({'role': 'assistant', 'content': d['reply'], 'tip': d['tip']});
        _done = d['done'] == true;
        _status = _done ? 'Great talk! Tap Finish to see your report.' : 'Tap the microphone and answer';
      });
      _toBottom();
      if ('${d['reply']}'.isNotEmpty) TalkVoice.say('${d['reply']}');
    } catch (e) {
      if (mounted) setState(() => _status = 'Network problem — please try again.');
    } finally {
      if (mounted) setState(() => _busy = false);
    }
  }

  Future<void> _speak() async {
    setState(() {
      _listening = true;
      _status = 'Listening… speak now';
    });
    final start = DateTime.now();
    final heard = await Speech.listen(seconds: 20);
    if (!mounted) return;
    setState(() => _listening = false);
    if (heard == null || heard.text.isEmpty) {
      setState(() => _status = "I didn't hear you. Tap the mic and speak clearly.");
      return;
    }
    await _send(heard.text, confidence: heard.confidence, seconds: DateTime.now().difference(start).inSeconds);
  }

  Future<void> _hint() async {
    setState(() => _status = 'Getting a hint…');
    final d = await context.read<AppState>().api.post('/talk/$_id/hint/', {});
    if (mounted) setState(() => _status = '💡 You could say: “${d['hint']}”');
  }

  Future<void> _translate(int i) async {
    if (_translations.containsKey(i)) {
      setState(() => _translations.remove(i));
      return;
    }
    setState(() => _translations[i] = '…');
    final d = await context.read<AppState>().api.post('/talk/$_id/translate/', {'text': _msgs[i]['content']});
    if (mounted) setState(() => _translations[i] = d['text'] == null ? 'Translation needs AI.' : '${d['text']}');
  }

  void _finish() => Navigator.pushReplacement(context, MaterialPageRoute(builder: (_) => ReportScreen(sessionId: _id)));

  @override
  Widget build(BuildContext context) {
    final s = widget.session;
    return Scaffold(
      appBar: AppBar(
        title: Text('${s['title']}', style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w800)),
        actions: [Center(child: Padding(padding: const EdgeInsets.only(right: 12), child: Text('$_turns/${s['max_turns']}', style: const TextStyle(color: FE.soft))))],
      ),
      body: SafeArea(
        child: Column(children: [
          Expanded(
            child: ListView(controller: _scroll, padding: const EdgeInsets.all(14), children: [
              if ('${s['setting']}'.isNotEmpty)
                Card(
                  child: Padding(
                    padding: const EdgeInsets.all(14),
                    child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                      Text('${s['setting']}', style: const TextStyle(fontWeight: FontWeight.w800)),
                      if ('${s['goal']}'.isNotEmpty) Text('🎯 ${s['goal']}', style: const TextStyle(color: FE.soft)),
                    ]),
                  ),
                ),
              for (var i = 0; i < _msgs.length; i++) _bubble(i),
            ]),
          ),
          Container(
            padding: const EdgeInsets.fromLTRB(16, 10, 16, 12),
            decoration: const BoxDecoration(color: Color(0xFF17143F), borderRadius: BorderRadius.vertical(top: Radius.circular(24))),
            child: Column(mainAxisSize: MainAxisSize.min, children: [
              Text(_status, textAlign: TextAlign.center, style: const TextStyle(fontWeight: FontWeight.w700)),
              const SizedBox(height: 8),
              if (_typing)
                Row(children: [
                  Expanded(child: TextField(controller: _text, decoration: const InputDecoration(hintText: 'Type your answer…'), onSubmitted: (_) => _submitTyped())),
                  IconButton(onPressed: _submitTyped, icon: const Icon(Icons.send, color: FE.sky)),
                ]),
              Row(mainAxisAlignment: MainAxisAlignment.spaceEvenly, children: [
                IconButton.filledTonal(onPressed: _busy ? null : _hint, icon: const Text('💡', style: TextStyle(fontSize: 20))),
                SizedBox(
                  width: 76,
                  height: 76,
                  child: FilledButton(
                    style: FilledButton.styleFrom(backgroundColor: _listening ? FE.coral : FE.sky, shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(26))),
                    onPressed: _busy ? null : (_listening ? Speech.stopListening : _speak),
                    child: Icon(_listening ? Icons.stop : Icons.mic, size: 36),
                  ),
                ),
                IconButton.filledTonal(onPressed: () => setState(() => _typing = !_typing), icon: const Icon(Icons.keyboard)),
              ]),
              const SizedBox(height: 8),
              SizedBox(
                width: double.infinity,
                child: _done
                    ? FilledButton(onPressed: _finish, child: const Text('🏁 Finish and see my report'))
                    : OutlinedButton(onPressed: _turns == 0 ? null : _finish, child: const Text('🏁 Finish and see my report')),
              ),
            ]),
          ),
        ]),
      ),
    );
  }

  void _submitTyped() {
    final t = _text.text;
    _text.clear();
    _send(t);
  }

  Widget _bubble(int i) {
    final m = _msgs[i];
    final me = m['role'] == 'user';
    final tip = '${m['tip'] ?? ''}';
    return Align(
      alignment: me ? Alignment.centerRight : Alignment.centerLeft,
      child: Container(
        margin: const EdgeInsets.symmetric(vertical: 6),
        padding: const EdgeInsets.all(12),
        constraints: const BoxConstraints(maxWidth: 320),
        decoration: BoxDecoration(
          color: me ? FE.sky : FE.card,
          borderRadius: BorderRadius.circular(20),
          border: me ? null : Border.all(color: Colors.white12),
        ),
        child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          Text('${m['content']}', style: const TextStyle(fontSize: 17, height: 1.4)),
          if (tip.isNotEmpty) Padding(padding: const EdgeInsets.only(top: 6), child: Text('💡 $tip', style: const TextStyle(color: FE.gold))),
          if (!me)
            Row(mainAxisSize: MainAxisSize.min, children: [
              IconButton(visualDensity: VisualDensity.compact, onPressed: () => TalkVoice.say('${m['content']}'), icon: const Icon(Icons.volume_up, size: 20)),
              IconButton(visualDensity: VisualDensity.compact, onPressed: () => TalkVoice.say('${m['content']}', slow: true), icon: const Icon(Icons.slow_motion_video, size: 20)),
              IconButton(visualDensity: VisualDensity.compact, onPressed: () => _translate(i), icon: const Icon(Icons.translate, size: 20)),
            ]),
          if (_translations[i] != null) Text(_translations[i]!, style: const TextStyle(color: FE.soft)),
        ]),
      ),
    );
  }
}

// ------------------------------------------------------------------ the lesson report

class ReportScreen extends StatelessWidget {
  final int sessionId;
  const ReportScreen({super.key, required this.sessionId});

  @override
  Widget build(BuildContext context) {
    final api = context.read<AppState>().api;
    return Scaffold(
      appBar: AppBar(title: const Text('Lesson report', style: TextStyle(fontWeight: FontWeight.w800))),
      body: Loader<Map<String, dynamic>>(
        load: () async => Map<String, dynamic>.from(await api.post('/talk/$sessionId/finish/', {})),
        builder: (context, d, reload) {
          final r = Map<String, dynamic>.from(d['report']);
          final better = r['better'] as List;
          return ListView(padding: const EdgeInsets.all(16), children: [
            Text('${d['title']}', style: const TextStyle(fontSize: 24, fontWeight: FontWeight.w800)),
            const SizedBox(height: 12),
            Row(children: [
              _stat('${(r['new_words'] as List).length}', 'new words'),
              _stat('${r['vocab_total']}', 'words so far'),
              _stat('${r['words']}', 'words spoken'),
            ]),
            if ((r['new_words'] as List).isNotEmpty)
              Padding(
                padding: const EdgeInsets.only(top: 12),
                child: Wrap(spacing: 6, runSpacing: 6, children: [for (final w in r['new_words'] as List) Chip(label: Text('$w'))]),
              ),
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                  const Text('How you did', style: TextStyle(fontSize: 18, fontWeight: FontWeight.w800)),
                  if (r['pronunciation'] != null) _bar('👄 Pronunciation', r['pronunciation'] as int),
                  _bar('🌊 Fluency', r['fluency'] as int),
                  if (r['grammar'] != null) _bar('🧩 Grammar', r['grammar'] as int),
                  if ('${r['best']}'.isNotEmpty) ...[
                    const SizedBox(height: 12),
                    const Text('⭐ YOUR BEST ANSWER', style: TextStyle(color: FE.gold, fontWeight: FontWeight.w800, fontSize: 12)),
                    Text('“${r['best']}”', style: const TextStyle(fontSize: 16)),
                  ],
                ]),
              ),
            ),
            Card(
              color: const Color(0xFFEEF1FF),
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                  const Text('🔑 KEY TAKEAWAY', style: TextStyle(color: Color(0xFF5A5E8E), fontWeight: FontWeight.w800, fontSize: 12)),
                  Text('${r['takeaway']}', style: const TextStyle(color: Color(0xFF1C1D40), fontSize: 17, fontWeight: FontWeight.w700)),
                  if ('${r['takeaway_bn']}'.isNotEmpty) Text('${r['takeaway_bn']}', style: const TextStyle(color: Color(0xFF1C1D40))),
                ]),
              ),
            ),
            if (better.isNotEmpty) const Padding(padding: EdgeInsets.fromLTRB(4, 16, 4, 6), child: Text('Better ways to say it', style: TextStyle(fontSize: 18, fontWeight: FontWeight.w800))),
            for (final b in better)
              Card(
                child: Padding(
                  padding: const EdgeInsets.all(14),
                  child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                    Text('You said: “${b['you']}”', style: const TextStyle(color: FE.soft, decoration: TextDecoration.lineThrough)),
                    const SizedBox(height: 8),
                    SayCard(sessionId: sessionId, text: '${b['better']}'),
                    if ('${b['tip']}'.isNotEmpty) Padding(padding: const EdgeInsets.only(top: 6), child: Text('💡 ${b['tip']}')),
                    if ('${b['tip_bn']}'.isNotEmpty) Text('${b['tip_bn']}', style: const TextStyle(color: FE.soft)),
                    if ((b['alts'] as List).isNotEmpty) const Padding(padding: EdgeInsets.only(top: 10), child: Text('OTHER WAYS TO SAY IT', style: TextStyle(color: FE.soft, fontWeight: FontWeight.w800, fontSize: 12))),
                    for (final a in b['alts'] as List) SayCard(sessionId: sessionId, text: '$a'),
                  ]),
                ),
              ),
            if (better.isEmpty && r['ai'] != true)
              const Padding(padding: EdgeInsets.all(8), child: Text('When AI is on, the report also shows corrections and better ways to say your sentences.', style: TextStyle(color: FE.soft))),
            const SizedBox(height: 16),
            FilledButton(onPressed: () => Navigator.pop(context), child: const Text('Continue')),
            const SizedBox(height: 24),
          ]);
        },
      ),
    );
  }

  Widget _stat(String n, String label) => Expanded(
        child: Card(
          child: Padding(
            padding: const EdgeInsets.symmetric(vertical: 14, horizontal: 6),
            child: Column(children: [
              Text(n, style: const TextStyle(fontSize: 26, fontWeight: FontWeight.w800, color: FE.sky)),
              Text(label, textAlign: TextAlign.center, style: const TextStyle(color: FE.soft, fontSize: 12)),
            ]),
          ),
        ),
      );

  Widget _bar(String label, int v) => Padding(
        padding: const EdgeInsets.only(top: 10),
        child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          Row(children: [Text(label), const Spacer(), Text('$v%', style: const TextStyle(fontWeight: FontWeight.w800))]),
          const SizedBox(height: 4),
          LinearProgressIndicator(value: v / 100, color: FE.mint, backgroundColor: Colors.white12),
        ]),
      );
}

/// A better sentence: listen to it, then say it and get a score.
class SayCard extends StatefulWidget {
  final int sessionId;
  final String text;
  const SayCard({super.key, required this.sessionId, required this.text});

  @override
  State<SayCard> createState() => _SayCardState();
}

class _SayCardState extends State<SayCard> {
  bool _listening = false;
  int? _score;

  Future<void> _say() async {
    setState(() => _listening = true);
    final heard = await Speech.listen(seconds: 12);
    if (!mounted) return;
    setState(() => _listening = false);
    if (heard == null || heard.text.isEmpty) return;
    final d = await context.read<AppState>().api.post('/talk/${widget.sessionId}/practice/',
        {'target': widget.text, 'said': heard.text, 'confidence': heard.confidence});
    if (mounted) setState(() => _score = (d['score'] as num).toInt());
  }

  @override
  Widget build(BuildContext context) => Container(
        margin: const EdgeInsets.only(top: 6),
        padding: const EdgeInsets.all(10),
        decoration: BoxDecoration(color: Colors.white10, borderRadius: BorderRadius.circular(14)),
        child: Row(children: [
          Expanded(child: Text(widget.text, style: const TextStyle(fontWeight: FontWeight.w700, fontSize: 16))),
          IconButton(onPressed: () => TalkVoice.say(widget.text), icon: const Icon(Icons.volume_up, color: FE.sky)),
          IconButton(onPressed: _listening ? Speech.stopListening : _say, icon: Icon(_listening ? Icons.stop : Icons.mic, color: _listening ? FE.coral : FE.sky)),
          if (_score != null) Text('$_score%', style: TextStyle(fontWeight: FontWeight.w800, color: _score! >= 70 ? FE.mint : FE.coral)),
        ]),
      );
}
