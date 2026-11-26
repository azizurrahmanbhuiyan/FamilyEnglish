// Talk: the AI tutor tab — daily talk, role-plays, Read and talk, and the setup questions.
//
// 📘 LEARN:
// - Every lesson rule (what is free, which topic is today's) lives on the server (talk/engine.py),
//   so the app and the website always agree. The app only shows the data and sends answers.
// - ChoiceChip / FilterChip are Material widgets for "pick one" and "pick many".
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../api.dart';
import '../speech.dart';
import '../state.dart';
import '../theme.dart';
import '../widgets/loader.dart';
import 'chat_screen.dart';

/// Start a talk on the server and open the conversation screen.
Future<void> startTalk(BuildContext context, Map<String, dynamic> body) async {
  final api = context.read<AppState>().api;
  try {
    final s = Map<String, dynamic>.from(await api.post('/talk/start/', body));
    if (!context.mounted) return;
    await Navigator.push(context, MaterialPageRoute(builder: (_) => ChatScreen(session: s)));
  } on ApiException catch (e) {
    if (!context.mounted) return;
    ScaffoldMessenger.of(context).showSnackBar(SnackBar(
        content: Text(e.isLocked ? '🔒 This is in the family plan. You can unlock it on the website.' : e.message)));
  }
}

class TalkScreen extends StatelessWidget {
  const TalkScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final api = context.read<AppState>().api;
    return Loader<Map<String, dynamic>>(
      load: () async => Map<String, dynamic>.from(await api.get('/talk/home/')),
      builder: (context, d, reload) {
        TalkVoice.speed = (d['speed'] as num?)?.toDouble() ?? 1.0;
        TalkVoice.pitch = (d['pitch'] as num?)?.toDouble() ?? 1.0;
        final daily = d['daily'] as Map<String, dynamic>;
        final minutes = (d['minutes'] as num).toInt(), goal = (d['goal'] as num).toInt();
        Future<void> open(Widget w) => Navigator.push(context, MaterialPageRoute(builder: (_) => w)).then((_) => reload());
        return Scaffold(
          appBar: AppBar(
            title: const Text('Talk', style: TextStyle(fontWeight: FontWeight.w800)),
            actions: [IconButton(onPressed: () => open(const TalkSetupScreen()), icon: const Icon(Icons.tune))],
          ),
          body: ListView(padding: const EdgeInsets.all(16), children: [
            if (d['setup_done'] != true)
              Card(
                color: FE.violet.withValues(alpha: .25),
                child: ListTile(
                  leading: const Text('👋', style: TextStyle(fontSize: 28)),
                  title: const Text('Set up your tutor first', style: TextStyle(fontWeight: FontWeight.w800)),
                  subtitle: const Text('Your level, topics and how to correct you'),
                  onTap: () => open(const TalkSetupScreen()),
                ),
              ),
            Card(
              child: Padding(
                padding: const EdgeInsets.all(18),
                child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                  Row(children: [
                    const Text("TODAY'S GOAL", style: TextStyle(color: FE.soft, fontWeight: FontWeight.w800, fontSize: 12)),
                    const Spacer(),
                    Text('$minutes / $goal min', style: const TextStyle(fontWeight: FontWeight.w700)),
                  ]),
                  const SizedBox(height: 8),
                  LinearProgressIndicator(value: goal == 0 ? 0.0 : (minutes / goal).clamp(0, 1).toDouble(), color: FE.mint, backgroundColor: FE.line),
                  const SizedBox(height: 16),
                  Text('${daily['emoji']} Daily talk: ${daily['title']}', style: const TextStyle(fontSize: 22, fontWeight: FontWeight.w800)),
                  const SizedBox(height: 6),
                  Text('“${daily['question']}”', style: const TextStyle(fontSize: 17)),
                  const SizedBox(height: 14),
                  SizedBox(
                    width: double.infinity,
                    child: daily['ok'] == true
                        ? FilledButton.icon(
                            onPressed: () => startTalk(context, {'kind': 'daily'}).then((_) => reload()),
                            icon: const Icon(Icons.mic),
                            label: const Text("Start today's talk"))
                        : const OutlinedButton(onPressed: null, child: Text("🔒 Today's free talk is done")),
                  ),
                ]),
              ),
            ),
            const SizedBox(height: 8),
            Row(children: [
              Expanded(child: _Tile('🎭', 'Role-play', 'Real situations', () => open(const RoleplaysScreen()))),
              const SizedBox(width: 10),
              Expanded(child: _Tile('📰', 'Read and talk', 'Read, then discuss', () => open(const ReadScreen()))),
            ]),
            const Padding(padding: EdgeInsets.fromLTRB(4, 18, 4, 8), child: Text('Role-plays for you', style: TextStyle(fontSize: 18, fontWeight: FontWeight.w800))),
            for (final r in d['for_you'] as List) RoleplayTile(Map<String, dynamic>.from(r), onDone: reload),
            if ((d['recent'] as List).isNotEmpty) ...[
              const Padding(padding: EdgeInsets.fromLTRB(4, 18, 4, 8), child: Text('Your lesson reports', style: TextStyle(fontSize: 18, fontWeight: FontWeight.w800))),
              for (final s in d['recent'] as List)
                Card(
                  child: ListTile(
                    title: Text('${s['title']}'),
                    subtitle: Text('${s['date']}'),
                    trailing: Text('${s['score']}%', style: const TextStyle(fontWeight: FontWeight.w800, color: FE.mint)),
                    onTap: () => open(ReportScreen(sessionId: s['id'] as int)),
                  ),
                ),
            ],
          ]),
        );
      },
    );
  }
}

class _Tile extends StatelessWidget {
  final String emoji, title, sub;
  final VoidCallback onTap;
  const _Tile(this.emoji, this.title, this.sub, this.onTap);

  @override
  Widget build(BuildContext context) => Card(
        child: InkWell(
          borderRadius: BorderRadius.circular(22),
          onTap: onTap,
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              Text(emoji, style: const TextStyle(fontSize: 30)),
              const SizedBox(height: 6),
              Text(title, style: const TextStyle(fontSize: 17, fontWeight: FontWeight.w800)),
              Text(sub, style: const TextStyle(color: FE.soft, fontSize: 13)),
            ]),
          ),
        ),
      );
}

class RoleplayTile extends StatelessWidget {
  final Map<String, dynamic> r;
  final Future<void> Function()? onDone;
  const RoleplayTile(this.r, {super.key, this.onDone});

  @override
  Widget build(BuildContext context) => Card(
        child: ListTile(
          leading: Text('${r['icon']}', style: const TextStyle(fontSize: 28)),
          title: Text('${r['title']}', style: const TextStyle(fontWeight: FontWeight.w800)),
          subtitle: Text('${r['goal']}', maxLines: 2, overflow: TextOverflow.ellipsis),
          trailing: r['locked'] == true ? const Icon(Icons.lock, size: 18, color: FE.soft) : const Icon(Icons.chevron_right),
          onTap: () => startTalk(context, {'kind': 'roleplay', 'ref': r['slug']}).then((_) => onDone?.call()),
        ),
      );
}

// ------------------------------------------------------------------ setup questions

class TalkSetupScreen extends StatefulWidget {
  const TalkSetupScreen({super.key});

  @override
  State<TalkSetupScreen> createState() => _TalkSetupScreenState();
}

class _TalkSetupScreenState extends State<TalkSetupScreen> {
  Map<String, dynamic>? _opts;
  final Map<String, dynamic> _p = {};
  bool _saving = false;

  @override
  void initState() {
    super.initState();
    context.read<AppState>().api.get('/talk/profile/').then((d) {
      if (!mounted) return;
      setState(() {
        _opts = Map<String, dynamic>.from(d['options']);
        _p.addAll(Map<String, dynamic>.from(d['profile']));
        _p['interests'] = List<String>.from(_p['interests'] as List);
      });
    });
  }

  Widget _title(String t) => Padding(padding: const EdgeInsets.fromLTRB(0, 20, 0, 8), child: Text(t, style: const TextStyle(fontSize: 18, fontWeight: FontWeight.w800)));

  Widget _pickOne(String field, List items, String Function(dynamic) label, dynamic Function(dynamic) value) => Wrap(spacing: 8, runSpacing: 8, children: [
        for (final it in items)
          ChoiceChip(label: Text(label(it)), selected: _p[field] == value(it), onSelected: (_) => setState(() => _p[field] = value(it))),
      ]);

  Future<void> _save() async {
    setState(() => _saving = true);
    try {
      await context.read<AppState>().api.post('/talk/profile/', _p);
      if (mounted) Navigator.pop(context);
    } catch (e) {
      if (mounted) {
        setState(() => _saving = false);
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('$e')));
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    final o = _opts;
    if (o == null) return const Scaffold(body: Center(child: CircularProgressIndicator()));
    final interests = _p['interests'] as List<String>;
    return Scaffold(
      appBar: AppBar(title: const Text('Set up your tutor', style: TextStyle(fontWeight: FontWeight.w800))),
      body: ListView(padding: const EdgeInsets.all(16), children: [
        _title('1 · Your English level'),
        _pickOne('level', o['levels'] as List, (x) => '${x['n']} · ${x['en']}', (x) => x['n']),
        Padding(
          padding: const EdgeInsets.only(top: 6),
          child: Text('${(o['levels'] as List).firstWhere((x) => x['n'] == _p['level'], orElse: () => {'desc': ''})['desc']}', style: const TextStyle(color: FE.soft)),
        ),
        _title('2 · Why are you learning?'),
        _pickOne('reason', o['reasons'] as List, (x) => '${x['emoji']} ${x['en']}', (x) => x['key']),
        _title('3 · What is hardest for you?'),
        _pickOne('challenge', o['challenges'] as List, (x) => '${x['emoji']} ${x['en']}', (x) => x['key']),
        _title('4 · When should your tutor correct you?'),
        _pickOne('correct', o['correct'] as List, (x) => '${x['en']}', (x) => x['key']),
        _title('5 · Pick at least 3 topics'),
        Wrap(spacing: 8, runSpacing: 8, children: [
          for (final t in o['interests'] as List)
            FilterChip(
              label: Text('${t['emoji']} ${t['en']}'),
              selected: interests.contains(t['key']),
              onSelected: (on) => setState(() {
                if (on) {
                  interests.add(t['key'] as String);
                } else {
                  interests.remove(t['key']);
                }
              }),
            ),
        ]),
        _title("6 · Your tutor's voice and speed"),
        _pickOne('voice', o['voices'] as List, (x) => '🔈 ${x['en']}', (x) => x['key']),
        const SizedBox(height: 8),
        _pickOne('speed', o['speeds'] as List, (x) => '${x['label']}', (x) => (x['value'] as num).toDouble()),
        TextButton.icon(
          onPressed: () {
            final v = (o['voices'] as List).firstWhere((x) => x['key'] == _p['voice'], orElse: () => {'pitch': 1.0});
            Speech.say("Hello! I'm your English tutor. Let's have a chat.",
                speed: (_p['speed'] as num?)?.toDouble() ?? 1.0, pitch: (v['pitch'] as num).toDouble());
          },
          icon: const Icon(Icons.volume_up),
          label: const Text('Try the voice'),
        ),
        _title('7 · Daily goal'),
        _pickOne('daily_minutes', o['goals'] as List, (x) => '$x min', (x) => x),
        const SizedBox(height: 24),
        FilledButton(
          onPressed: _saving || interests.length < 3 ? null : _save,
          child: Text(interests.length < 3 ? 'Choose ${3 - interests.length} more topic(s)' : 'Save and start talking'),
        ),
        const SizedBox(height: 24),
      ]),
    );
  }
}

// ------------------------------------------------------------------ role-play library

class RoleplaysScreen extends StatelessWidget {
  const RoleplaysScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final api = context.read<AppState>().api;
    return Loader<Map<String, dynamic>>(
      load: () async => Map<String, dynamic>.from(await api.get('/talk/roleplays/')),
      builder: (context, d, reload) {
        final cats = d['categories'] as List;
        final tabs = <String>['For you', 'Popular', for (final c in cats) '${c['en']}'];
        final lists = <List>[d['for_you'] as List, d['popular'] as List, for (final c in cats) c['items'] as List];
        return DefaultTabController(
          length: tabs.length,
          child: Scaffold(
            appBar: AppBar(
              title: const Text('Role-play', style: TextStyle(fontWeight: FontWeight.w800)),
              bottom: TabBar(isScrollable: true, tabs: [for (final t in tabs) Tab(text: t)]),
            ),
            floatingActionButton: d['custom_ok'] == true
                ? FloatingActionButton.extended(onPressed: () => _custom(context), icon: const Icon(Icons.auto_awesome), label: const Text('Create your own'))
                : null,
            body: TabBarView(children: [
              for (final l in lists)
                ListView(padding: const EdgeInsets.all(12), children: [for (final r in l) RoleplayTile(Map<String, dynamic>.from(r))]),
            ]),
          ),
        );
      },
    );
  }

  void _custom(BuildContext context) {
    final setting = TextEditingController(), persona = TextEditingController();
    showDialog<void>(
      context: context,
      builder: (dialogContext) => AlertDialog(
        title: const Text('Your own role-play'),
        content: Column(mainAxisSize: MainAxisSize.min, children: [
          TextField(controller: setting, maxLength: 280, decoration: const InputDecoration(labelText: 'The situation', hintText: 'Asking my landlord to fix a tap')),
          TextField(controller: persona, maxLength: 180, decoration: const InputDecoration(labelText: 'Your tutor plays…', hintText: 'a busy but friendly landlord')),
        ]),
        actions: [
          TextButton(onPressed: () => Navigator.pop(dialogContext), child: const Text('Cancel')),
          FilledButton(
            onPressed: () {
              Navigator.pop(dialogContext);
              startTalk(context, {'kind': 'custom', 'setting': setting.text, 'persona': persona.text});
            },
            child: const Text('Start'),
          ),
        ],
      ),
    );
  }
}

// ------------------------------------------------------------------ Read and talk

class ReadScreen extends StatelessWidget {
  const ReadScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final api = context.read<AppState>().api;
    return Scaffold(
      appBar: AppBar(title: const Text('Read and talk', style: TextStyle(fontWeight: FontWeight.w800))),
      body: Loader<Map<String, dynamic>>(
        load: () async => Map<String, dynamic>.from(await api.get('/talk/read/')),
        builder: (context, d, reload) => ListView(padding: const EdgeInsets.all(16), children: [
          for (final c in d['sections'] as List) ...[
            Padding(padding: const EdgeInsets.fromLTRB(4, 14, 4, 8), child: Text('${c['emoji']} ${c['title']}', style: const TextStyle(fontSize: 18, fontWeight: FontWeight.w800))),
            SizedBox(
              height: 130,
              child: ListView(scrollDirection: Axis.horizontal, children: [
                for (final it in c['items'] as List)
                  SizedBox(
                    width: 220,
                    child: Card(
                      child: InkWell(
                        borderRadius: BorderRadius.circular(22),
                        onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => ArticleScreen(slug: it['slug'] as String))),
                        child: Padding(
                          padding: const EdgeInsets.all(14),
                          child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                            Text('${it['title']}', maxLines: 3, overflow: TextOverflow.ellipsis, style: const TextStyle(fontWeight: FontWeight.w700, fontSize: 16)),
                            const Spacer(),
                            if (it['locked'] == true) const Icon(Icons.lock, size: 16, color: FE.soft) else if (it['free'] == true) const Text('Free', style: TextStyle(color: FE.mint, fontWeight: FontWeight.w800)),
                          ]),
                        ),
                      ),
                    ),
                  ),
              ]),
            ),
          ],
        ]),
      ),
    );
  }
}

class ArticleScreen extends StatelessWidget {
  final String slug;
  const ArticleScreen({super.key, required this.slug});

  @override
  Widget build(BuildContext context) {
    final api = context.read<AppState>().api;
    return Scaffold(
      appBar: AppBar(title: const Text('Read and talk', style: TextStyle(fontWeight: FontWeight.w800))),
      body: Loader<Map<String, dynamic>>(
        load: () async => Map<String, dynamic>.from(await api.get('/talk/read/$slug/')),
        builder: (context, a, reload) {
          final paras = '${a['body']}'.split('\n\n');
          return ListView(padding: const EdgeInsets.all(16), children: [
            Text('${a['title']}', style: const TextStyle(fontSize: 26, fontWeight: FontWeight.w800)),
            Align(
              alignment: Alignment.centerLeft,
              child: TextButton.icon(
                onPressed: () => Speech.say(paras.join(' '), speed: TalkVoice.speed * .95, pitch: TalkVoice.pitch),
                icon: const Icon(Icons.volume_up),
                label: const Text('Listen'),
              ),
            ),
            for (final p in paras)
              InkWell(
                onTap: () => Speech.say(p, speed: TalkVoice.speed * .95, pitch: TalkVoice.pitch),
                child: Padding(padding: const EdgeInsets.only(bottom: 14), child: Text(p, style: const TextStyle(fontSize: 18, height: 1.6))),
              ),
            if ((a['words'] as List).isNotEmpty) ...[
              const Text('Useful words', style: TextStyle(fontSize: 18, fontWeight: FontWeight.w800)),
              for (final w in a['words'] as List)
                ListTile(
                  dense: true,
                  title: Text('${w[0]}', style: const TextStyle(fontWeight: FontWeight.w800)),
                  subtitle: Text('${w[1]}'),
                  onTap: () => Speech.say('${w[0]}'),
                ),
            ],
            const SizedBox(height: 12),
            FilledButton.icon(
              onPressed: () => startTalk(context, {'kind': 'article', 'ref': slug}),
              icon: const Icon(Icons.mic),
              label: const Text('Talk about it'),
            ),
            const SizedBox(height: 24),
          ]);
        },
      ),
    );
  }
}
