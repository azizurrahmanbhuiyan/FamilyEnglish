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
- **Curriculum.** 9 levels. Level 0 has all 42 sounds in 7 groups (Jolly Phonics teaching order) with
  Alphablocks videos. Levels 1–8 have starter modules using Alphablocks, British Council LearnEnglish Kids,
  Oxford Owl and BBC Learning English.
- **Pricing.** Free 14-day trial. After that, free accounts can open the first module of every level.
  Family plans cost ৳199/month, ৳999 for 6 months or ৳1,799 for 12 months. Payment is manual
  bKash/Nagad: the family submits a TrxID and an admin confirms it.

## Run it on your computer

Needs Python 3.10 or newer.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate     Mac/Linux: source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_curriculum          # loads levels, 70 lessons and placement questions
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
   python manage.py createsuperuser
   python manage.py collectstatic --noinput
   ```

   Click **Restart** on the app page. If Terminal is missing, ask ExonHost support to enable SSH or Terminal access.
7. **HTTPS.** cPanel → SSL/TLS Status → Run AutoSSL. When `https://familyenglish.global` opens, set
   `FE_SSL_REDIRECT=1` in `.env` and restart the app.

### Updating the live site

1. Upload the changed files (do not overwrite `.env`).
2. In the virtual environment: `cd ~/familyenglish`, then `pip install -r requirements.txt` (only if it
   changed), `python manage.py migrate` and `python manage.py collectstatic --noinput`.
3. Click **Restart** on the Python App page (or run `touch ~/familyenglish/tmp/restart.txt`).

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

- AI speaking check: record → speech-to-text (e.g. Whisper) → LLM rubric → one Bangla tip, metered per
  minute. Placement already stores a speaking level per learner, so it can plug in there.
- AI writing feedback for Levels 3 and up.
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
templates/  pages (Tailwind classes)
static/     built CSS and speech.js (browser text-to-speech; no audio files needed)
```
