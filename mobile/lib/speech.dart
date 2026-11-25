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

  /// Can this phone listen? (asks for microphone permission the first time)
  static Future<bool> canListen() async {
    _sttReady ??= await _stt.initialize(onError: (_) {}, onStatus: (_) {});
    return _sttReady!;
  }

  /// Listen once (up to 8 seconds) and return what was heard, or null.
  static Future<Heard?> listen({int seconds = 8}) async {
    if (!await canListen()) return null;
    final done = Completer<Heard?>();
    await _stt.listen(
      localeId: 'en_GB',
      listenFor: Duration(seconds: seconds),
      pauseFor: const Duration(seconds: 2),
      listenOptions: SpeechListenOptions(partialResults: false, cancelOnError: true),
      onResult: (SpeechRecognitionResult r) {
        if (r.finalResult && !done.isCompleted) {
          done.complete(Heard(r.recognizedWords, r.hasConfidenceRating ? r.confidence : null));
        }
      },
    );
    // If nothing final arrives, give up after 10 seconds.
    return done.future.timeout(Duration(seconds: seconds + 2), onTimeout: () async {
      await _stt.stop();
      return null;
    });
  }

  static Future<void> stopListening() => _stt.stop();
}
