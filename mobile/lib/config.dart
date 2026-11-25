// 📘 LEARN: `const` values are fixed when the app is built. Change API_URL to switch servers.
//
// Your live site:        https://familyenglish.global/api/v1
// Android emulator + your PC running `python manage.py runserver`:  http://10.0.2.2:8000/api/v1
// A real phone on the same Wi-Fi as your PC: http://<your PC's IP, e.g. 192.168.0.105>:8000/api/v1
//
// You can also pass it when running:  flutter run --dart-define=API_URL=http://10.0.2.2:8000/api/v1
const String apiUrl = String.fromEnvironment('API_URL', defaultValue: 'https://familyenglish.global/api/v1');
