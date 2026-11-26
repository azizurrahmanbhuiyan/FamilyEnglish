// The bridge between the app and the FamilyEnglish website (Django REST API).
//
// 📘 LEARN:
// - `Future<T>` is a value that arrives later (like a promise). `async`/`await` wait for it.
// - `Map<String, dynamic>` is Dart's version of a Python dict holding JSON.
// - We decode `bodyBytes` with utf8 so Bangla text shows correctly.
import 'dart:convert';

import 'package:http/http.dart' as http;

import 'config.dart';

class ApiException implements Exception {
  final int status;
  final String message;
  ApiException(this.status, this.message);

  bool get isLocked => status == 402; // "this part is in the family plan"

  @override
  String toString() => message;
}

class Api {
  String? token;   // from /auth/login/
  int? learnerId;  // which family member is learning

  Map<String, String> get _headers => {
        'Content-Type': 'application/json',
        if (token != null) 'Authorization': 'Token $token',
        if (learnerId != null) 'X-Learner': '$learnerId',
      };

  Future<dynamic> get(String path, [Map<String, String>? query]) async {
    final uri = Uri.parse('$apiUrl$path').replace(queryParameters: query);
    final res = await http.get(uri, headers: _headers).timeout(const Duration(seconds: 20));
    return _decode(res);
  }

  Future<dynamic> post(String path, Map<String, dynamic> body) async {
    final res = await http
        .post(Uri.parse('$apiUrl$path'), headers: _headers, body: jsonEncode(body))
        .timeout(const Duration(seconds: 20));
    return _decode(res);
  }

  dynamic _decode(http.Response res) {
    final text = utf8.decode(res.bodyBytes);
    final data = text.isEmpty ? null : jsonDecode(text);
    if (res.statusCode >= 200 && res.statusCode < 300) return data;
    final msg = (data is Map && data['detail'] != null) ? '${data['detail']}' : 'Something went wrong (${res.statusCode}).';
    throw ApiException(res.statusCode, msg);
  }

  // ---- the endpoints the app uses ----------------------------------------------------------
  Future<Map<String, dynamic>> login(String email, String password) async =>
      Map<String, dynamic>.from(await post('/auth/login/', {'email': email, 'password': password}));
  Future<void> passwordCode(String email) async => await post('/auth/password/code/', {'email': email});
  Future<Map<String, dynamic>> passwordReset(String email, String code, String password) async =>
      Map<String, dynamic>.from(await post('/auth/password/reset/', {'email': email, 'code': code, 'password': password}));
  Future<Map<String, dynamic>> passwordChange(String oldPassword, String newPassword) async =>
      Map<String, dynamic>.from(await post('/auth/password/change/', {'old': oldPassword, 'new': newPassword}));
  Future<Map<String, dynamic>> today() async => Map<String, dynamic>.from(await get('/today/'));
  Future<List<dynamic>> units() async => List<dynamic>.from(await get('/units/'));
  Future<Map<String, dynamic>> unit(String slug) async => Map<String, dynamic>.from(await get('/units/$slug/'));
  Future<Map<String, dynamic>> progress() async => Map<String, dynamic>.from(await get('/progress/'));

  Future<Map<String, dynamic>> attempt({required String key, required String target, required String said, double? confidence}) async =>
      Map<String, dynamic>.from(await post('/attempt/', {'key': key, 'target': target, 'said': said, 'confidence': confidence, 'seconds': 5}));

  Future<Map<String, dynamic>> analyse({required String key, required String prompt, required String transcript, required int seconds}) async =>
      Map<String, dynamic>.from(await post('/analyse/', {'key': key, 'prompt': prompt, 'transcript': transcript, 'seconds': seconds}));
  Future<Map<String, dynamic>> finish({required String key, required String title, required int score}) async =>
      Map<String, dynamic>.from(await post('/finish/', {'key': key, 'title': title, 'score': score}));
}
