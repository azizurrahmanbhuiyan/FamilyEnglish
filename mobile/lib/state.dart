// App-wide state: the login, the family's learners and the chosen learner.
//
// 📘 LEARN:
// - `ChangeNotifier` + `notifyListeners()` tells every screen that uses this state to rebuild.
//   (Provider makes it available everywhere — see main.dart.)
// - SharedPreferences saves small values on the phone, so you stay logged in after closing the app.
import 'package:flutter/foundation.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'api.dart';

class AppState extends ChangeNotifier {
  final Api api = Api();
  bool ready = false;          // finished loading saved login?
  List<Map<String, dynamic>> learners = [];
  Map<String, dynamic>? learner;
  bool paid = false;

  bool get loggedIn => api.token != null;

  Future<void> load() async {
    final prefs = await SharedPreferences.getInstance();
    api.token = prefs.getString('token');
    final id = prefs.getInt('learner');
    if (api.token != null) {
      try {
        final me = Map<String, dynamic>.from(await api.get('/me/'));
        _setFamily(me);
        if (id != null) {
          final match = learners.where((l) => l['id'] == id);
          if (match.isNotEmpty) chooseLearner(match.first, save: false);
        }
      } catch (_) {
        api.token = null; // token expired or server unreachable: ask to log in again
      }
    }
    ready = true;
    notifyListeners();
  }

  void _setFamily(Map<String, dynamic> data) {
    learners = List<Map<String, dynamic>>.from(data['learners'] as List);
    paid = data['family']?['paid'] == true;
  }

  Future<void> login(String email, String password) async {
    final data = await api.login(email, password);
    api.token = data['token'] as String;
    _setFamily(data);
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('token', api.token!);
    if (learners.length == 1) chooseLearner(learners.first);
    notifyListeners();
  }

  /// Forgot password: the emailed code + a new password signs you in.
  Future<void> resetPassword(String email, String code, String password) async {
    final data = await api.passwordReset(email, code, password);
    api.token = data['token'] as String;
    _setFamily(data);
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('token', api.token!);
    if (learners.length == 1) chooseLearner(learners.first);
    notifyListeners();
  }

  /// Change password while signed in. The server gives this phone a new token.
  Future<void> changePassword(String oldPassword, String newPassword) async {
    final data = await api.passwordChange(oldPassword, newPassword);
    api.token = data['token'] as String;
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('token', api.token!);
  }

  void chooseLearner(Map<String, dynamic> l, {bool save = true}) {
    learner = l;
    api.learnerId = l['id'] as int;
    if (save) SharedPreferences.getInstance().then((p) => p.setInt('learner', api.learnerId!));
    notifyListeners();
  }

  void switchLearner() {
    learner = null;
    api.learnerId = null;
    notifyListeners();
  }

  Future<void> logout() async {
    try {
      await api.post('/auth/logout/', {});
    } catch (_) {}
    final prefs = await SharedPreferences.getInstance();
    await prefs.clear();
    api.token = null;
    api.learnerId = null;
    learner = null;
    learners = [];
    notifyListeners();
  }
}
