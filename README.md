# FamilyEnglish

A low-cost, Bangla-first website where children and parents learn English together, from the
42 letter sounds to confident everyday and academic English. Built with Django.

It follows the loop **placement test → study plan → daily lesson → practice → home task**:

- **Family account.** Any adult (parent, grandparent or elder) opens it and can pay for everyone.
  Up to 5 learner profiles, with an optional 4-digit code for each child. Co-managers (for example
  the other parent or a grandparent) can be added.
- **Placement test.** A tap game for little learners (Levels 0–2), and a reader test for older children
  and adults: Listening (the browser reads aloud), Reading, Writing, plus a Speaking checklist.
- **Study planner.** Pick a finish level, the months you have and study days per week. Lessons are spread
  over the Sunday–Thursday school week, with a review day after every 6 lessons and a family-English day
  every Friday. Plans that are too fast are refused. A new plan keeps finished lessons.
- **Lessons.** Four steps: watch a free video, read the note (Kid view in English, Parent view in Bangla),
  practise, then a home task. Practice types are tap-the-picture, dictation (hear and type) and quiz.
  Stars, streaks and a parent dashboard track progress.
- **Topic videos.** Every lesson has its own short narrated video (about 30 seconds), built from the
  lesson's own content: title, sound and action, example words with pictures, quiz questions and answers.
  The browser reads it aloud with captions, a slow-voice mode and full screen. Nothing autoplays.
  There are no files to host and no tracking. Edit a lesson in /admin and its video updates. The code is
  in `learning/video.py` (scenes) and `static/js/topic-video.js` (player). Official-channel videos are
  listed under "More videos".
- **Dashboard.** A sidebar app shell with XP, streak, stars, skill progress bars, a 4-week activity grid
  and a weekly family leaderboard (`learning/stats.py`). Each lesson gives 20 XP plus 10 XP per star.
- **AI level test** (`course/smart_test.py`). Listening, Reading, Grammar, Writing and Speaking. Each
  objective section starts with Easy + Medium questions and adds an Advanced round only for learners who
  pass Medium. Writing and speaking are marked by a stronger AI model (`FE_AI_TEST_MODEL`) with a 0–8
  rubric, or by the built-in rubric when AI is off. The AI writes a Bangla + English report. Results give
  a level and a category (Easy / Medium / Advanced) per skill and also update the placement.
- **Skill course** (`course/` app, `course/content/*.py`). 75 lessons: Listening, Speaking, Reading,
  Writing and Grammar, each with 5 Easy, 5 Medium and 5 Advanced lessons. Every lesson has English and
  Bangla notes, guidance for Bangla speakers, common mistakes (avoid → use), practice and a self-test.
  - **Lessons ordered from the test** (`course/path.py`): each skill starts at its tested category; the
    weakest skill comes up twice as often. "Make my plan" turns the path into the study plan.
  - **Mistake detection while practising** (`course/grading.py`): every answer is marked on the server;
    the learner sees a word-by-word comparison (wrong / missing words), the right answer, the reason, Bangla
    notes from the checker, missed words for speaking, and AI feedback for free answers.
  - **Self-test after each lesson** (pass mark 60%, stars at 75% and 90%) with a full answer review.
  - **Weak spots and practice by question type** (32 question types) from the last 90 days of answers.
- **Progress** (`growth/` app): XP ledger, streaks with 3 freezes a month, daily goals, 15 badges,
  6-month heatmap, score trends, weekly leagues (Bronze → Diamond; other families only see avatar +
  nickname), XP panel, profile with signed-in devices, idea board with votes, What's new, EN/বাংলা switch.
- **IELTSly-style practice tools** (`practice/` app), built for families:
  - **Level checks & skill practice.** Re-test one skill (Phonics, Listening, Reading, Writing) to update
    that skill's level, or play a 10-question round taken from lessons at the learner's level.
  - **Word dictation.** Easy, medium, hard and mixed; 10-word practice or a 20-mark test (each word plays twice).
  - **Typing speed.** 30 s / 1 min / 2 min tests, WPM and accuracy, trend and family best.
  - **Speaking practice.** The browser's speech recognition (Chrome) listens. Levels 0–4 repeat sentences
    and see which words were not heard; Levels 5–8 answer questions and get tips.
  - **Writing helper.** Corrects writing with a Bangla note for each fix. Its built-in checker covers
    capitals, full stops, a/an, he/she + verb-s and common Bangla-English mistakes
    ("cousin brother", "discuss about", "I am agree").
  - **Ask the tutor ("Tuntuni").** A chat for English questions in English or Bangla. Parents can read
    each child's chat from the Family page.
  - **Vocabulary flashcards.** 16 topic decks (160 words) with pictures, Bangla meanings and examples,
    reviewed on a spaced-repetition schedule (Leitner boxes: 1, 2, 4, 8 and 16 days).
  - **My reports & streaks.** Level history, test results, speaking average, words learned, a 12-week
    streak grid and the family leaderboard.
  - **Refer & earn.** Each family gets a code and a link. A new family joining with it gets 7 extra trial
    days. When the new family first pays, the inviting family gets 30 free days, plus a commission
    (`FE_REFERRAL_COMMISSION_PCT`, default 10%) on every confirmed payment, withdrawable by bKash from
    ৳500 after a 7-day hold. Pay withdrawals by hand and mark them Paid in /admin (Payout requests).
  - **How to use FamilyEnglish.** 10 guides on the same topics as IELTSly's tutorial series, with Bangla
    steps. Add your own recorded video to each one in /admin (Tutorials → youtube_id).
  - **Support.** Families send questions; you reply in /admin (Support tickets).
  - **AI is optional.** Put `FE_AI_API_KEY` (an Anthropic API key) in `.env` to switch on AI answers for
    the tutor, the writing helper and speaking feedback. `FE_AI_DAILY_LIMIT` (default 20) caps AI replies
    per learner per day. Without a key, everything works with the built-in feedback, at no cost.
- **Talk at home** (`learning/family_talk.py`, sentences in `learning/seed/family_talk_*.py`). Every kids'
  lesson has six mini-talks — Me & Sister, Me & Brother, Me & Mamma, Me & Daddy, Me & Grandma, Me & Grandpa —
  two short lines each (child, then family member) with Bangla, using the lesson's sound or topic. Play with
  two voices, check the child's line with the microphone, tick "We said it together" (+5 XP). Families can
  ask the AI for a fresh set per lesson (saved for that family only). `python manage.py seed_family_talk`
  loads the built-in 840 lines (also run by `seed_curriculum`).
  Plus 30 theme lessons (`learning/seed/talk_topics_*.py`, `python manage.py seed_talk_topics`): 11 daily-life
  (good morning … good night, prayers, healthy food), 13 topics (alphabet, numbers, rhymes, animals, fish,
  birds, body, colours, shapes, seasons, planets, sports) and 6 trips (zoo, botanical garden, amusement park,
  museum, sea beach, historical places), each with 8 picture words and six family talks.
- **Free and paid.** Everything about phonics sounds (every `skill="phonics"` lesson, its videos, links and
  family talks, phonics practice and the phonics check, the picture test) is free. Everything else needs the
  family plan: ৳299/month, ৳1500/6 months, ৳2500/year (`core/models.py`, `core/access.py`). No free trial
  by default (`FE_FREE_TRIAL_DAYS`); invited families get `REFERRAL_EXTRA_TRIAL_DAYS`.
- **Full courses** (`learning/tracks.py`): young child 3 years, school student 2 years, IELTS 3/6/9/12 months (suggested from the level test),
  parent who studied 1 year, grandparent or adult who studied little 3 years. New lessons are spread over each stage; the days in
  between repeat earlier lessons; Fridays are family days.
- **Word weeks** (`practice/words.py`): the 3000 most frequent words for children, parents and grandparents
  (156 weekly sets) and the 7000 most frequent for school students and IELTS (104 weekly sets), with
  British IPA. Each week: listen (British voice), say (microphone, en-GB), spell what you hear, write
  sentences (British spelling check, AI feedback when on), then the words join the flashcard reviews.
  Load with `python manage.py seed_wordlists`. The first 1000 children's words have Bangla meanings;
  fill the rest with `python manage.py fill_word_meanings --limit 2000` (needs `FE_AI_API_KEY`, under $1
  in all). See `practice/data/README.md` for sources and licences.
- **British pronunciation**: 30 speaking lessons (`course/content/pronunciation.py`) from the silent r and
  short vowels to linking, weak forms, intonation and IELTS chunking. The site's voice prefers the best
  British voices on the device and tells families how to install one if missing.
- **Short video clips** (`learning/clips.py`). Every lesson shows 4–5 on-topic clips, each at most 5 minutes
  and at most 20 minutes in total. Long videos are cut YouGlish-style: only the chapter that matches the
  lesson plays (embed `start`/`end`). No playlists, live streams or videos over an hour. Trusted channels
  (BBC Learning English, British Council, Alphablocks, Oxford Owl…) show at once; other channels wait for
  approval in /admin → Video clips. Find clips with a free YouTube API key (`FE_YOUTUBE_API_KEY`):
  `python manage.py find_clips --limit 30` (about 30 lessons fit the free daily quota; run it daily until
  all lessons have clips). You can also add a clip by hand: paste the link, start and end (e.g. 1:20–4:05).
- **Curriculum.** 9 levels. Level 0 has all 42 sounds in 7 groups (Jolly Phonics teaching order) with
  Alphablocks videos. Levels 1–8 have starter modules using Alphablocks, British Council LearnEnglish Kids,
  Oxford Owl and BBC Learning English.
- **Pricing.** Free 14-day trial. After that, free accounts can open the first module of every level.
  Family plans cost ৳199/month, ৳999 for 6 months or ৳1,799 for 12 months. Payment is manual
  bKash/Nagad: the family submits a TrxID and an admin confirms it.

## The speaking app (v12, `/app/`)

Signed-in learners land on **Today** (`/app/`). Five tabs, plus **More** for family, plan and every older tool:

| Tab | What it has |
|---|---|
| Today | 3 daily tasks (sound drill · new words · conversation), CEFR journey bar, Saturday–Friday streak, word and coach of the day |
| Learn | 24 everyday units (A1–B1), 5 lessons each; Grammar coach A1–C (41 lessons); Pronunciation course (22 lessons in 6 stages) and 7 shadowing stories; IELTS band 6 / 7 / 8+; links to phonics, word weeks, skill course, kids' ladder |
| Phonics Year | Levels 0–2 = 36 weeks × 5 days (`learning/seed/phonics_year.py`, built by `learning/phonics_year.py`, loaded by `seed_curriculum`). Parent view with a step-by-step guide (Bangla/English) and Kid view, printable week plans at `/learn/phonics-year/week/<n>/`, five two-part checks with family/class results at `/learn/phonics-year/`. Weeks 1–2 free. All stories, actions and examples are our own |
| Pronunciation handbook | 23 PDFs in `course/handouts/` (not static), listed at `/course/handbook/`, downloaded through `course.views.handout` (01–02 free, the rest family plan). Map in `course/handouts.py`; 13 matching app lessons in `course/content/handbook.py` (pr-h…, gr-all-tenses, rd-family-qa) flow into the student and IELTS plans |
| Talk | AI tutor conversations: setup questions, daily talk on your topics, 57 role-plays + your own, Read and talk (18 groups, 400+ topics), lesson report with better ways to say it. Works without AI using prepared lines. `FE_TALK_AI_DAILY_LIMIT` (default 60) caps AI calls per learner per day |
| Coach | Pronunciation coach (sound drills), speech analyzer, presentation rehearsal, 11 role-play coaches (free talk with AI when `FE_AI_API_KEY` is set) |
| Discover | Short videos (watch a line, say it back — 600+ animated shorts plus real clips), dictionary (British IPA, English meaning, Bangla), word of the day, My Words |
| Progress | 5-skill pentagon, CEFR + IELTS estimate, learning time, 7-day chart, history, badges, certificates, gems and streak freezes |

**Real video shorts:** in /admin → Video clips, add the *Say line* (the exact sentence spoken) to any approved clip under
60 seconds; it then appears in Short videos under "Real videos" and in the "For you" feed. Free families get 5 shorts a day.

Free families can try the first unit (Hello and goodbye) and the first grammar lesson; the rest is in the family plan.
Speech is checked in the browser (Chrome on Android or a computer works best); other browsers fall back to typing or self-checking.
Content lives in `studio/content/` (units, grammar, coaches, IELTS, sounds) — edit the Python lists to add more.

## Pronunciation course and stories (v16, `/app/learn/pronunciation/`)

22 short lessons in six stages, in the order people learn to speak clearly:
1. **Start here** — first pronunciation lesson (sounds, stress, rhythm), the phonemic chart.
2. **Consonants** — voiced/voiceless, clear word endings, the two "th" sounds, the British R.
3. **Vowels** — /ɪ/ vs /iː/, /æ/ vs /e/, long and short British vowels, the schwa, diphthongs and triphthongs.
4. **Endings and spelling** — -ed endings, suffixes (-ly, -able, -tion, -ful, -less), silent letters, tricky words.
5. **Rhythm and connected speech** — weak forms, contractions and reductions, linking, assimilation, intonation.
6. **British accent and fluency** — modern British (RP) accent, shadowing.

Each lesson is a chat lesson (hello → key symbols → rule in English and Bangla → spoken examples → practice) followed
by an 8-item word drill scored by speech recognition. The first two lessons are free. **Stories**
(`/app/learn/stories/`): 7 short stories (two retold fables, five FamilyEnglish originals) marked for linking,
weak forms and intonation — read and listen, shadow line by line, then take a word quiz. The first story is free.
The Grammar coach gained three tense lessons (present perfect continuous, past perfect continuous, all tenses at a
glance). Topics follow common pronunciation teaching; all explanations, examples, word lists and stories are our own.
Content lives in `studio/content/pronunciation.py` and `studio/content/stories.py`.

## Android app (`mobile/`, built free by GitHub)

The Flutter app lives in `mobile/`. Every push that changes it runs `.github/workflows/android-app.yml` on GitHub:
it builds **FamilyEnglish.apk**, keeps it under Actions → Artifacts, and on `main` publishes it on the Releases
page as a free download. Step-by-step (first build, installing on a phone, signing key so updates install over
the old app): `mobile/LEARN.md`, Lesson 2. The `mobile/` folder is not needed on the web server.

## Mobile app API (v14, `/api/v1/`)

A JSON API for the FamilyEnglish phone app (Flutter), built with Django REST Framework. The app logs in with
the family's email and password (`POST /api/v1/auth/login/` → token) and then sends
`Authorization: Token <token>` and `X-Learner: <learner id>` with every request. It reuses the studio's own
scoring, XP, gems and free/paid rules. Endpoints: `me`, `today`, `units`, `units/<slug>`, `grammar`, `attempt`,
`finish`, `shorts`, `shorts/try`, `progress`, `dictionary`. After uploading v14 run
`pip install -r requirements.txt` and `python manage.py migrate` (creates the login-token table).

## Going global (v15)

**Languages.** The site works in 112 languages. People pick their language on the 🌐 button (`/language/`) or
when they sign up; it is saved to their account. Arabic, Urdu, Persian, Hebrew and other right-to-left
languages turn the whole page around. The English being *learned* (words, phrases, sentences) never changes;
only menus, meanings, tips and explanations do.

- English and Bangla are written by hand in the templates, as before.
- 12 more languages have the main screens written by hand in `world/locale/<code>.json`: Hindi, Urdu, Arabic,
  Spanish, French, Portuguese, Indonesian, Chinese, Russian, Turkish, Nepali and Vietnamese.
- Everything else is translated by the AI (the same `FE_AI_API_KEY` as the tutor). Until it is translated
  the text shows in English and is put in a queue. Add this **cron job** in cPanel (every 10 minutes):

  `*/10 * * * * cd ~/familyenglish && ~/virtualenv/familyenglish/3.13/bin/python manage.py translate_ui --pending --quiet`

  To translate a whole language at once: `python manage.py translate_ui --lang hi --all` (about 1,450 texts).
- Any translation can be corrected in **/admin → World → UI texts**. Corrected texts are marked "manual" and
  the AI never replaces them.

**Sign up with a code.** Sign-up asks for language, country and mobile number. Choosing the country fills in
the dial code (+880, +91, +44 …) and shows an example number, so people type only their own number. We send a
6-digit code to their **email** (and by **SMS** once an SMS provider is set up). The account works only after
the code is confirmed. People can also sign in with a code instead of a password (`/login/code/`). Codes are
stored hashed, last 10 minutes, allow 5 tries, and can be re-sent once a minute (5 an hour).

Email setup: in cPanel → Email Accounts create `noreply@familyenglish.global`, then set `FE_EMAIL_HOST`,
`FE_EMAIL_PORT` (465), `FE_EMAIL_USER`, `FE_EMAIL_PASSWORD` in `.env` (see `.env.example`). SMS: set
`FE_SMS_BACKEND=bulksmsbd` (Bangladesh) or `twilio` (worldwide) and its key, secret and sender.

**Paid everywhere, with SSLCommerz.** Families in every country use the same plans (phonics stays free).
Bangladesh pays in taka (৳299 / ৳1500 / ৳2500); other countries see US dollars ($3 / $15 / $25 — change
`PLAN_PRICES_USD` in `core/models.py`). The "Pay now" button opens SSLCommerz: card, bKash, Nagad, Rocket and
internet banking in Bangladesh, Visa/Mastercard/Amex in dollars abroad. The plan switches on by itself after we
check the payment with SSLCommerz's validation API (status VALID, same transaction, same amount and currency).
No manual approval: access starts the moment the payment is validated. Payments SSLCommerz marks as
high risk also get access, with a note in /admin → Payment requests for you to review. The manual bKash/Nagad Send Money form stays for
Bangladesh.

SSLCommerz setup:
1. Test first: create a sandbox store at developer.sslcommerz.com, put its store ID and password in
   `FE_SSLC_STORE_ID` / `FE_SSLC_STORE_PASSWORD`, keep `FE_SSLC_SANDBOX=1`, and pay with their test cards.
2. Go live: apply for a merchant account at sslcommerz.com (trade licence, bank account, website with
   pricing, refund, privacy and terms pages). Ask them to enable **USD / international cards**.
3. Put the live store ID and password in `.env`, set `FE_SSLC_SANDBOX=0`, and in the merchant panel → My Store →
   IPN Settings set `https://familyenglish.global/pay/sslcommerz/ipn/`. The switch
`FE_FREE_OUTSIDE_BD=1` can make families outside Bangladesh free later; it is off by default.

After uploading v15: `pip install -r requirements.txt` (adds Babel and phonenumbers), `python manage.py migrate`,
`python manage.py collectstatic --noinput`, add the email settings and the cron job, then restart the app.

## Run it on your computer

Needs Python 3.10 or newer.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate     Mac/Linux: source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_curriculum          # loads levels, 70 lessons and placement questions
python manage.py seed_practice            # loads 16 vocabulary decks and the 10 how-to guides
python manage.py seed_course              # loads the 75-lesson skill course
python manage.py createsuperuser          # for /admin
python manage.py runserver
```

Open http://127.0.0.1:8000. Sign up as an adult, add a learner, take the placement test, then make a plan.

Run the tests with `python manage.py test`.

## Adding content (in /admin)

- **Lessons → Videos.** Most videos come with a `search_query` and no `youtube_id`, so the lesson shows
  an "Open on the official channel" link. Find the right video on the **official** channel and paste its
  ID (the part after `watch?v=`) into `youtube_id`. The lesson then embeds it with youtube-nocookie.com.
  The *Lesson video* list lets you edit IDs in bulk. Two IDs are already set: Alphablocks
  "Alphabet Learn-A-Thon" (`wpoHQN2X8mM`) and "Learn to Read OW, OE, OA and O_E" (`VTNG-HglpU4`).
- **Practice items.** For a dictation lesson, `prompt` = the word the browser says and `answer` = what the
  learner types. For a quiz or tap lesson, `choices` = options separated by commas; `answer` must be one
  of them (a test checks this).
- **Payments.** Open *Payment requests*, select a pending payment, and choose
  *Confirm selected payments*. This extends the family's plan.
- To add a lot of content, edit the files in `learning/seed/` and run `python manage.py seed_curriculum`
  again. It is safe to re-run.

## Styling

The CSS is pre-built in `static/css/app.css` (Tailwind) plus `static/css/site.css`. It works offline;
fonts load from Google Fonts and fall back to system fonts. After you change classes in templates,
rebuild:

```bash
npx tailwindcss@3 -c tailwind.config.js -i static/css/tailwind.input.css -o static/css/app.css --minify
```

## Deploying (cPanel hosting)

The live site is **familyenglish.global**, hosted on ExonHost shared cPanel hosting (server
`bd27.exonhost.com`, IP `103.159.37.110`, nameservers `bdns1.exonhost.com` / `bdns2.exonhost.com`).
It runs through cPanel's **Setup Python App** (Phusion Passenger), which starts `passenger_wsgi.py`.
WhiteNoise serves the static files, so no web-server configuration is needed.

### Settings

In production, settings come from a `.env` file next to `manage.py` (see `.env.example`). Real
environment variables override it. Never upload your local `.env` or `db.sqlite3`.

| Variable | Value |
| --- | --- |
| `FE_SECRET_KEY` | A long random string: `python -c "import secrets; print(secrets.token_urlsafe(50))"` |
| `FE_DEBUG` | `0` |
| `FE_ALLOWED_HOSTS` | `familyenglish.global,www.familyenglish.global` |
| `FE_CSRF_TRUSTED_ORIGINS` | `https://familyenglish.global,https://www.familyenglish.global` |
| `FE_SSL_REDIRECT` | `1` (set it to `0` only until the SSL certificate is active) |
| `FE_DB_NAME`, `FE_DB_USER`, `FE_DB_PASSWORD` | The PostgreSQL database, user and password from cPanel |
| `FE_DB_HOST`, `FE_DB_PORT` | `localhost` and `5432` (the defaults) |

When `FE_DB_NAME` is set, the site uses PostgreSQL. When it is not set (for example on your own computer),
it uses SQLite (`db.sqlite3`).

### First deployment

1. **DNS.** At the domain registrar, set the nameservers to `bdns1.exonhost.com` and `bdns2.exonhost.com`.
   Make sure the domain is added in cPanel (main or addon domain).
2. **Upload.** Zip the project without `.venv/`, `__pycache__/`, `staticfiles/`, `db.sqlite3` and `.env`.
   In cPanel → File Manager, extract it to `/home/<cpaneluser>/familyenglish/`. Do not put it inside
   `public_html`.
3. **Create the app.** cPanel → Setup Python App → Create Application: Python 3.11 or 3.12,
   application root `familyenglish`, application URL `familyenglish.global`, startup file
   `passenger_wsgi.py`, entry point `application`.
4. **Create the database.** cPanel → PostgreSQL Databases: create a database (for example
   `familyenglish`), create a user with a strong password, then add the user to the database. cPanel puts
   your username in front of both names, for example `cpaneluser_familyenglish`.
5. **Create `.env`** in `/home/<cpaneluser>/familyenglish/` with the values above, using the full prefixed
   database and user names. Use `FE_SSL_REDIRECT=0` for now.
6. **Install and set up.** Copy the "Enter to the virtual environment" command from the app page, run
   it in cPanel → Terminal, then run:

   ```bash
   cd ~/familyenglish
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py seed_curriculum
   python manage.py seed_practice
   python manage.py seed_course
   python manage.py seed_wordlists
   python manage.py createsuperuser
   python manage.py collectstatic --noinput
   ```

   Click **Restart** on the app page. If Terminal is missing, ask ExonHost support to enable SSH or Terminal access.
7. **HTTPS.** cPanel → SSL/TLS Status → Run AutoSSL. When `https://familyenglish.global` opens, set
   `FE_SSL_REDIRECT=1` in `.env` and restart the app.

### Updating the live site

1. **Back up the database first** (see below) and keep a copy of `.env`.
2. Upload the new zip and extract it over `~/familyenglish/` (do not overwrite `.env`).
3. In the virtual environment:

   ```bash
   cd ~/familyenglish
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py seed_curriculum      # levels, family talks, talk topics
   python manage.py seed_practice
   python manage.py seed_course          # skill course + British pronunciation
   python manage.py seed_wordlists       # 3000 / 7000 word weeks
   python manage.py collectstatic --noinput
   ```

   All seed commands are safe to re-run; they keep what you added or changed in /admin.
4. Click **Restart** on the Python App page (or run `touch ~/familyenglish/tmp/restart.txt`).
5. Optional, once: `python manage.py fill_word_meanings --limit 8000` (needs `FE_AI_API_KEY`) and, daily
   until done, `python manage.py find_clips --limit 30` (needs `FE_YOUTUBE_API_KEY`).

### Database and backups

The live site uses PostgreSQL. Back it up regularly: cPanel → Backup → *Download a PostgreSQL Database
Backup*, or from Terminal:

```bash
pg_dump -h localhost -U cpaneluser_feuser cpaneluser_familyenglish > ~/fe-backup-$(date +%F).sql
```

To move existing data from SQLite into PostgreSQL, run `python manage.py dumpdata --natural-foreign
--natural-primary -e contenttypes -e auth.permission -e sessions --indent 2 > data.json` with SQLite, then
`migrate` and `python manage.py loaddata data.json` with PostgreSQL.

If the site shows an error page, check `~/familyenglish/stderr.log`, or the error log in cPanel → Metrics → Errors.

## Before going live

1. Follow **Deploying** above. Never run the live site with `FE_DEBUG=1`.
2. The bKash/Nagad number (01710503504) is set in `templates/core/pay.html`. Change it there if needed.
   Later, replace the manual flow with a payment gateway.
3. **Children's privacy and YouTube.** Most kids' videos are "made for kids". Google's API policy requires
   tracking to be off for those embeds. Keep lesson pages free of ad and analytics trackers. Check each
   video's `madeForKids` status and run a regular check for videos that were removed.
4. **Brands.** Follow the Jolly Phonics *order* only. Do not copy its images, songs, worksheets or audio.
   Do not suggest a partnership with Alphablocks, the British Council, the BBC or Oxford. Have
   `templates/core/privacy.html` reviewed by a lawyer, and check Bangladesh's rules on children's data.

## Next steps (not built yet)

- Record your own "How to use" videos and add their YouTube IDs in /admin.
- Server-side speech scoring for browsers without speech recognition (e.g. Whisper), and a speaking level check.
- Monthly re-test reminders, weekly Bangla SMS summaries for parents, and a school/NGO teacher dashboard.
- More lessons per level (planned: L0 48 · L1 40 · L2 40 · L3 60 · L4 72 · L5 84 · L6 96 · L7 108 · L8 120).

## Project layout

```
core/       family accounts, learner profiles, co-managers, payments, parent dashboard
learning/   levels, lessons, videos, practice, placement, planner, progress
  planner.py      rules-based study planner
  video.py        builds each lesson's short topic video
  stats.py        XP, skill progress, leaderboard
  placement.py    placement scoring
  seed/           curriculum data (levels, 42 sounds, Levels 1–8, placement questions)
practice/   level checks, skill practice, dictation, speaking, writing helper, AI tutor,
            flashcards, reports, refer & earn, tutorials, support
  ai.py           optional AI calls (standard library only), with a daily limit
  feedback.py     built-in writing checker, speaking score and tutor answers
  seed_data.py    vocabulary decks, speaking sentences, writing topics, tutorials
templates/  pages (Tailwind classes)
static/     built CSS and speech.js (browser text-to-speech; no audio files needed)
```
