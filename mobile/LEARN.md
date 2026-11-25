# FamilyEnglish app — learn Flutter by building it

You learn by doing: each lesson adds one real feature to the FamilyEnglish phone app.
Lesson 1 (this folder) is already written for you — your job is to **run it, read it and change it**.
Every file has 📘 LEARN notes explaining the new idea it uses.

---

## Lesson 0 — Install (one evening)

1. Install **Flutter** on Windows: https://docs.flutter.dev/get-started/install/windows/mobile
   (it installs Dart too). Choose "Android" as the target.
2. Install **Android Studio** (for the Android SDK and an emulator) and **VS Code** with the
   *Flutter* extension.
3. Open a terminal and run `flutter doctor`. Fix anything with a red ✗ until it is all green
   (accept licences with `flutter doctor --android-licenses`).
4. In Android Studio → *Device Manager*, create a phone emulator (Pixel, Android 14).

## Lesson 1 — Run the app (this folder)

1. Make an empty Flutter project, then copy this folder's files into it:

   ```bash
   flutter create --org global.familyenglish familyenglish_app
   ```

   Copy `lib/`, `pubspec.yaml`, `analysis_options.yaml` and `LEARN.md` from this zip into the new
   `familyenglish_app` folder (replace the files it made). Then:

   ```bash
   cd familyenglish_app
   flutter pub get
   ```

2. Let the app use the internet, microphone and voice. Open
   `android/app/src/main/AndroidManifest.xml` and add, **above** `<application`:

   ```xml
   <uses-permission android:name="android.permission.INTERNET"/>
   <uses-permission android:name="android.permission.RECORD_AUDIO"/>
   <queries>
       <intent><action android:name="android.speech.RecognitionService"/></intent>
       <intent><action android:name="android.intent.action.TTS_SERVICE"/></intent>
   </queries>
   ```

   and inside the `<application ...>` tag add `android:usesCleartextTraffic="true"`
   (only needed while you test against `http://` on your own PC).

3. Run the FamilyEnglish website on your PC (from the v14 zip):

   ```bash
   python manage.py migrate
   python manage.py runserver 0.0.0.0:8000
   ```

4. Start the emulator, then run the app pointing at your PC:

   ```bash
   flutter run --dart-define=API_URL=http://10.0.2.2:8000/api/v1
   ```

   (`10.0.2.2` is how the Android emulator reaches your PC.)
   On a real phone on the same Wi-Fi, use your PC's IP instead (find it with `ipconfig`) and add that
   IP to `FE_ALLOWED_HOSTS` in `.env`.
   Against the live site after you upload v14: just `flutter run` — it uses https://familyenglish.global.

5. Sign in with your website email and password, pick a learner, open **Learn → Hello and goodbye →
   Lesson 1** and say the words. Check the website: the same XP, gems and ✓ appear there too.

### Read the code in this order

| File | What you learn |
|---|---|
| `lib/main.dart` | Widgets, the app's first screen, Provider |
| `lib/state.dart` | App state, `ChangeNotifier`, saving the login |
| `lib/api.dart` | `async`/`await`, HTTP, JSON |
| `lib/screens/login_screen.dart` | StatefulWidget, text fields, `setState` |
| `lib/screens/today_screen.dart` | Lists, cards, `Navigator.push` |
| `lib/widgets/loader.dart` | A reusable widget with generics `<T>` |
| `lib/screens/repeat_screen.dart` | Speech, `RichText`, calling the API and finishing a lesson |

### Your homework (do these yourself — ask Claude if you get stuck)

1. Change the colours in `lib/theme.dart` and the welcome text on the login screen.
2. On the Today screen, show `shorts_today` ("Short videos said today: N") — the API already sends it.
3. In `repeat_screen.dart`, add a **bookmark** button. Hint: there is no `/bookmark/` API yet — add one in
   `api/views.py` (copy `studio.views.api_bookmark`) and a `bookmark()` method in `lib/api.dart`.
4. Build the app for your own phone: `flutter build apk --release` and install
   `build/app/outputs/flutter-apk/app-release.apk`.

---

## What comes next

| Lesson | You will build | New Flutter ideas |
|---|---|---|
| 2 | Scripted conversation (lesson 4 of each unit) | chat bubbles, `ListView.builder`, auto-scroll |
| 3 | Short videos feed | `PageView` (swipe), animations, `/shorts/` API |
| 4 | Dictionary + My Words | search box, debounce, bookmarks API |
| 5 | Speech analyzer | continuous listening, timers, charts |
| 6 | Daily reminder notifications, app icon, splash | `flutter_local_notifications`, assets |
| 7 | Publish on Google Play | signing key, Play Console, closed testing |

## The API (already on the website, v14)

All under `/api/v1/`. Send `Authorization: Token <token>` and `X-Learner: <id>`.

| Method | Path | What |
|---|---|---|
| POST | `auth/login/` | `{email, password}` → token, family, learners |
| POST | `auth/logout/` | delete the token |
| GET | `me/` | family and learners |
| GET | `today/` | tasks, journey, week, word of the day, streak/gems/XP |
| GET | `units/` , `units/<slug>/` | units; words, phrases, conversation of one unit |
| GET | `grammar/` | the 38 grammar lessons |
| POST | `attempt/` | `{key, target, said, confidence}` → score, word marks |
| POST | `finish/` | `{key, title, score}` → XP and gems (first time) |
| GET | `shorts/?topic=&offset=` | short videos feed |
| POST | `shorts/try/` | `{id, said}` → score |
| GET | `progress/` | scores, CEFR/IELTS, time, history, badges |
| GET | `dictionary/?q=` | word, IPA, meaning, Bangla |

Free families get the same limits as on the website (status 402 = "family plan only").

---

## Lesson 2 — A free Android app built by GitHub (no Flutter on your PC needed)

Every time you `git push` a change inside `mobile/`, GitHub builds the app for you
(`.github/workflows/android-app.yml`): it makes the Android files, checks the code, runs the tests,
builds **FamilyEnglish.apk**, and publishes it as a free download.

### Your first build
1. Push the project to GitHub: `git add -A`, `git commit -m "Android app"`, `git push`.
2. On github.com open your repo → **Actions** → **Android app**. Wait about 8–10 minutes for the green tick.
3. Download the app:
   - every push: open the run → **Artifacts** → **FamilyEnglish-apk** (a zip with the APK inside), or
   - pushes to `main`: the repo's **Releases** page → **FamilyEnglish.apk**.
4. On the phone, open the APK and allow "Install unknown apps" for your browser or Files app once.
5. Sign in with an account made on familyenglish.global (sign-up with the email code happens on the website).

Share the free download with anyone: `https://github.com/<your-username>/<repo>/releases/latest`
(this works for everyone only if the repository is **public**; for a private repo, send the APK file itself).

### If the build goes red ❌
Open the red step and read the last lines. `Check the code` and `Build the APK` show the file and line of a
mistake (for example `lib/screens/today_screen.dart:42`). Fix it, push again — a new build starts by itself.

### Make updates install over the old app (do this once)
Without your own signing key, each build is signed with a new test key, so the phone says
"App not installed" — uninstall the old one first. To fix it for good, make one key and keep it safe forever
(if you lose it, you can never update the app on phones or on Google Play):

```
keytool -genkeypair -v -keystore familyenglish.jks -keyalg RSA -keysize 2048 -validity 10000 -alias familyenglish
```
(`keytool` comes with Java or Android Studio. Choose a strong password and write it down.)

Turn the key into text — PowerShell:
```
[Convert]::ToBase64String([IO.File]::ReadAllBytes("familyenglish.jks")) | Set-Clipboard
```
Then on GitHub: repo → **Settings → Secrets and variables → Actions → New repository secret**, add:

| Secret | Value |
| --- | --- |
| `ANDROID_KEYSTORE_BASE64` | the text you just copied |
| `ANDROID_KEYSTORE_PASSWORD` | the keystore password |
| `ANDROID_KEY_ALIAS` | `familyenglish` |
| `ANDROID_KEY_PASSWORD` | the key password (often the same) |

Never put the `.jks` file in git (it is in `.gitignore`). Keep a copy in Google Drive and on a USB stick.

### 📘 What you learned
- **CI (continuous integration)**: a robot computer builds and tests your code on every push.
- A **workflow** is a list of steps in YAML; `${{ github.run_number }}` makes each version number bigger,
  which Android needs to accept an update.
- **Signing**: Android only lets an app update itself if the new version is signed with the same key.

### Homework
Change the Login screen's subtitle in `lib/screens/login_screen.dart`, push, and install the new build.


## Lesson 3 — The Talk tab (AI conversations)

The fourth tab, **Talk**, uses `/api/v1/talk/...` (see `api/talk.py`). Files to read:

- `lib/screens/talk_screen.dart` — the Talk home, setup questions (ChoiceChip / FilterChip), role-play
  library (TabBar) and Read and talk (horizontal lists).
- `lib/screens/chat_screen.dart` — the conversation (a ListView of bubbles + a mic button) and the
  lesson report. `SayCard` lets you listen to a better sentence and say it for a score.

Try it: change the bubble colours in `_bubble()`, push, and download the new APK from the Actions tab.
