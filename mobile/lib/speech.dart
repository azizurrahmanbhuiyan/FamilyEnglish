// The phone's voice (text-to-speech) and ears (speech-to-text), set to British English.
//
// 📘 LEARN:
// - A class with `static` members works like a module: Speech.say('hello') from anywhere.
// - `Completer` turns a callback (onResult) into a Future we can `await`.
import 'dart:async';

import 'package:flutter_tts/flutter_tts.dart';
import 'package:speech_to_text/speech_recognition_result.dart';
import 'package:speech_to_text/speech_to_text.dart';

class Heard {
  final String text;
  final double? confidence;
  Heard(this.text, this.confidence);
}

class Speech {
  static final FlutterTts _tts = FlutterTts();
  static final SpeechToText _stt = SpeechToText();
  static bool _ttsReady = false;
  static bool? _sttReady;

  /// speed and pitch come from the learner's Talk settings (1.0 = normal).
  static Future<void> say(String text, {bool slow = false, double speed = 1.0, double pitch = 1.0}) async {
    if (!_ttsReady) {
      await _tts.setLanguage('en-GB');
      await _tts.awaitSpeakCompletion(true);
      _ttsReady = true;
    }
    await _tts.setSpeechRate((slow ? 0.25 : 0.45) * speed); // Android: 0.5 is normal speed
    await _tts.setPitch(pitch);
    await _tts.stop();
    await _tts.speak(text);
  }

  /// Why the last listen gave nothing (shown to the learner), or null.
  static String? lastProblem;
  static String? _locale;
  static void Function(String status)? _onStatus;
  static void Function(String error)? _onError;

  /// Can this phone listen? (asks for microphone permission the first time)
  static Future<bool> canListen() async {
    if (_sttReady != true) {
      _sttReady = await _stt.initialize(
        onError: (e) => _onError?.call(e.errorMsg),
        onStatus: (s) => _onStatus?.call(s),
      );
    }
    if (_sttReady == true && _locale == null) {
      // Use a British voice if the phone has one, otherwise any English, otherwise the phone's own.
      final ids = (await _stt.locales()).map((l) => l.localeId).toList();
      String? pick(bool Function(String) ok) => ids.where(ok).cast<String?>().firstWhere((_) => true, orElse: () => null);
      _locale = pick((id) => id.replaceAll('-', '_').toLowerCase() == 'en_gb') ??
          pick((id) => id.toLowerCase().startsWith('en')) ??
          '';
    }
    return _sttReady == true;
  }

  /// Listen once and return what was heard, or null (then [lastProblem] says why).
  ///
  /// 📘 LEARN: we keep the words as they arrive (partial results). When the phone says it has
  /// stopped — the learner paused, tapped stop, or time ran out — we use the last words we got,
  /// so a short answer like "sure" is never lost.
  static Future<Heard?> listen({int seconds = 8}) async {
    lastProblem = null;
    if (!await canListen()) {
      lastProblem = 'The microphone is not allowed. Allow it in Settings → Apps → FamilyEnglish → Permissions.';
      return null;
    }
    await _tts.stop(); // the tutor's voice must not talk over the learner
    final done = Completer<Heard?>();
    String words = '';
    double? confidence;
    void finish() {
      if (done.isCompleted) return;
      if (words.trim().isEmpty) {
        lastProblem ??= "I didn't hear you. Tap the mic, wait for the beep, then speak.";
        done.complete(null);
      } else {
        done.complete(Heard(words.trim(), confidence));
      }
    }

    _onStatus = (s) {
      if (s == 'done' || s == 'notListening') Future.delayed(const Duration(milliseconds: 800), finish);
    };
    _onError = (e) {
      if (e.contains('network')) {
        lastProblem = 'Listening needs the internet on this phone. Check your connection.';
      } else if (e.contains('permission')) {
        lastProblem = 'The microphone is not allowed. Allow it in Settings → Apps → FamilyEnglish → Permissions.';
      }
      finish();
    };
    await _stt.listen(
      localeId: (_locale == null || _locale!.isEmpty) ? null : _locale,
      listenFor: Duration(seconds: seconds),
      pauseFor: const Duration(seconds: 4),
      listenOptions: SpeechListenOptions(partialResults: true, cancelOnError: false),
      onResult: (SpeechRecognitionResult r) {
        words = r.recognizedWords;
        if (r.hasConfidenceRating && r.confidence > 0) confidence = r.confidence;
        if (r.finalResult) finish();
      },
    );
    // Safety net: never wait forever.
    return done.future.timeout(Duration(seconds: seconds + 4), onTimeout: () async {
      await _stt.stop();
      finish();
      return done.future;
    });
  }

  static Future<void> stopListening() => _stt.stop();
}
