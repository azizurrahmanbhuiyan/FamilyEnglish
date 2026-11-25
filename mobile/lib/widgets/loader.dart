// Load data from the API and show a spinner, an error with "Try again", or the result.
//
// 📘 LEARN: this is a *generic* widget — `<T>` means it works for any type of data.
// Pull down to refresh (RefreshIndicator) calls `load` again.
import 'package:flutter/material.dart';

import '../api.dart';
import '../theme.dart';

class Loader<T> extends StatefulWidget {
  final Future<T> Function() load;
  final Widget Function(BuildContext context, T data, Future<void> Function() reload) builder;
  const Loader({super.key, required this.load, required this.builder});

  @override
  State<Loader<T>> createState() => _LoaderState<T>();
}

class _LoaderState<T> extends State<Loader<T>> {
  T? _data;
  Object? _error;

  @override
  void initState() {
    super.initState();
    _reload();
  }

  Future<void> _reload() async {
    try {
      final d = await widget.load();
      if (mounted) {
        setState(() {
          _data = d;
          _error = null;
        });
      }
    } catch (e) {
      if (mounted) setState(() => _error = e);
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_error != null && _data == null) {
      final locked = _error is ApiException && (_error as ApiException).isLocked;
      return Center(
        child: Padding(
          padding: const EdgeInsets.all(24),
          child: Column(mainAxisSize: MainAxisSize.min, children: [
            Text(locked ? '🔒' : '📡', style: const TextStyle(fontSize: 48)),
            const SizedBox(height: 8),
            Text(locked ? 'This part is in the family plan.' : '$_error', textAlign: TextAlign.center, style: const TextStyle(color: FE.soft)),
            const SizedBox(height: 16),
            if (!locked)
              OutlinedButton(
                onPressed: () {
                  setState(() => _error = null);
                  _reload();
                },
                child: const Text('Try again'),
              ),
          ]),
        ),
      );
    }
    if (_data == null) return const Center(child: CircularProgressIndicator());
    return RefreshIndicator(onRefresh: _reload, child: widget.builder(context, _data as T, _reload));
  }
}
