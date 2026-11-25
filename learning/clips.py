"""Short, on-topic video clips for every lesson (like YouGlish: only the part that matches).

Rules
- 4 to 5 clips per lesson, each at most 5 minutes, all together at most 20 minutes.
- Single videos only: never playlists, live streams or very long videos (over 60 minutes).
- A video of 5 minutes or less is used whole. A longer video is used only if its own chapter list
  (timestamps in the description, e.g. "2:15 The s sound") has a part that matches the lesson; the
  player then starts and stops at that part.
- safeSearch=strict, embeddable videos only. Clips from TRUSTED_CHANNELS are shown at once; clips from
  other channels wait for an admin to approve them.

Needs a free YouTube Data API key in FE_YOUTUBE_API_KEY. Each lesson costs about 200-300 quota units
(the free daily quota is 10,000), so run `python manage.py find_clips --limit 30` once a day until done.
"""

import json
import re
import urllib.parse
import urllib.request

from django.conf import settings

MAX_CLIP = 5 * 60
MIN_CLIP = 30
MAX_TOTAL = 20 * 60
TARGET_CLIPS = 5
MIN_CLIPS = 4
MAX_SOURCE = 60 * 60

TRUSTED_CHANNELS = [
    "BBC Learning English", "British Council LearnEnglish Kids", "LearnEnglish Kids", "British Council",
    "LearnEnglish Teens", "Alphablocks", "Numberblocks", "Oxford Owl", "Oxford University Press ELT",
    "Jolly Learning", "Super Simple Songs", "Super Simple Learning", "Dream English Kids",
    "Jack Hartmann Kids Music Channel", "Scratch Garden", "Kids Learning Tube", "English Singsing",
    "Bounce Patrol - Kids Songs", "Maple Leaf Learning", "Peekaboo Kidz", "National Geographic Kids",
    "SciShow Kids", "Cambridge English",
]
BAD_WORDS = ["compilation", "full episode", "full movie", "livestream", "24/7", "hour", "hours", "marathon",
             "learn-a-thon", "playlist", "shorts", "reaction", "prank"]
STOP = {"the", "a", "an", "and", "of", "to", "in", "on", "for", "with", "your", "my", "at", "is", "it",
        "trip", "time", "sound", "lesson", "english", "kids", "learn", "learning"}


class ClipError(Exception):
    pass


def _api(endpoint, **params):
    key = getattr(settings, "YOUTUBE_API_KEY", "")
    if not key:
        raise ClipError("Set FE_YOUTUBE_API_KEY to find clips.")
    url = f"https://www.googleapis.com/youtube/v3/{endpoint}?" + urllib.parse.urlencode({**params, "key": key})
    try:
        with urllib.request.urlopen(url, timeout=20) as resp:
            return json.loads(resp.read().decode())
    except Exception as exc:  # network, quota, bad key
        raise ClipError(f"YouTube API error: {exc}") from exc


# ------------------------------------------------------------------ parsing helpers

def parse_duration(iso):
    """ISO 8601 'PT1H2M3S' -> seconds."""
    m = re.fullmatch(r"P(?:(\d+)D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", iso or "")
    if not m:
        return 0
    d, h, mi, s = (int(x or 0) for x in m.groups())
    return d * 86400 + h * 3600 + mi * 60 + s


def parse_time(text):
    """'1:02:03' / '2:15' / '135' -> seconds."""
    parts = [int(p) for p in str(text).strip().split(":") if p.strip().isdigit()]
    secs = 0
    for p in parts:
        secs = secs * 60 + p
    return secs


def fmt_time(secs):
    secs = int(secs or 0)
    return f"{secs // 3600}:{secs % 3600 // 60:02d}:{secs % 60:02d}" if secs >= 3600 else f"{secs // 60}:{secs % 60:02d}"


def chapters(description, duration):
    """Chapters from a video description: [(start, end, title)]."""
    rows = []
    for line in (description or "").splitlines():
        m = re.match(r"^\s*[\[(]?((?:\d{1,2}:)?\d{1,2}:\d{2})[\])]?\s*[-–—:|.]?\s*(.+)$", line)
        if m:
            rows.append((parse_time(m.group(1)), m.group(2).strip()))
    rows = sorted({s: t for s, t in rows}.items())
    if len(rows) < 2 or rows[0][0] != 0:
        return []  # YouTube chapters always start at 0:00
    out = []
    for i, (start, title) in enumerate(rows):
        end = rows[i + 1][0] if i + 1 < len(rows) else duration
        if end > start:
            out.append((start, end, title))
    return out


def youtube_id(text):
    """A video ID from an ID or any YouTube link. Playlist-only links return ''."""
    text = (text or "").strip()
    if re.fullmatch(r"[A-Za-z0-9_-]{11}", text):
        return text
    m = re.search(r"(?:v=|youtu\.be/|embed/|shorts/|live/)([A-Za-z0-9_-]{11})", text)
    return m.group(1) if m else ""


def keywords(*texts):
    words = []
    for t in texts:
        for w in re.findall(r"[A-Za-z]+", (t or "").lower()):
            if len(w) > 1 and w not in STOP and w not in words:
                words.append(w)
    return words


def relevance(text, kws):
    low = (text or "").lower()
    return sum(1 for k in kws if re.search(rf"(?<![a-z]){re.escape(k.lower())}(?![a-z])", low))


def trusted(channel):
    c = (channel or "").lower()
    return any(t.lower() == c or t.lower() in c for t in TRUSTED_CHANNELS)


# ------------------------------------------------------------------ what to search for

def plan_for(item):
    """(queries, keywords) for a kids lesson, a course lesson or a talk topic."""
    from course.models import CourseLesson
    from .models import Lesson, TalkTopic

    if isinstance(item, Lesson):
        level = item.module.level.number
        if item.skill == "phonics" and level == 0:
            sound = re.sub(r"\(.*?\)|[/]", " ", item.focus or item.title).strip()
            sound = sound.split()[0] if sound else item.title
            # Only titles/chapters about THIS sound count (e.g. "S sound", "Letter S"), not any phonics video.
            return ([f"{sound} sound phonics for kids", f"letter {sound} sound song"],
                    [f"{sound} sound", f"letter {sound}", f"sound {sound}", f"/{sound}/"])
        base = item.title if level >= 3 else f"{item.title} phonics reading"
        return ([f"{base} English for kids", f"{item.focus} {base}"], keywords(item.title, item.focus))
    if isinstance(item, CourseLesson):
        q = item.video_query or item.title
        return ([q, f"{item.title} English {item.get_skill_display().lower()} lesson"], keywords(item.title, item.goal))
    if isinstance(item, TalkTopic):
        words = " ".join(w["word"] for w in item.words[:4])
        return ([f"{item.title} for kids English vocabulary", f"{item.title} song for kids"],
                keywords(item.title, words))
    raise ValueError("Unknown lesson type")


# ------------------------------------------------------------------ choosing clips

def choose(candidates, kws, existing_secs=0, existing_count=0, have_ids=()):
    """Pick clips from candidate videos.

    candidates: [{"id", "title", "channel", "duration", "description", "made_for_kids", "embeddable"}]
    Returns [{"youtube_id", "start", "end", "title", "channel", "trusted", "part"}]
    """
    picks, total, used = [], existing_secs, set(have_ids)
    scored = []
    for v in candidates:
        if not v.get("embeddable", True) or v["id"] in used:
            continue
        title_low = v["title"].lower()
        if any(re.search(rf"\b{re.escape(b)}\b", title_low) for b in BAD_WORDS) or v["duration"] < MIN_CLIP or v["duration"] > MAX_SOURCE:
            continue
        score = relevance(v["title"], kws) * 3 + (4 if trusted(v["channel"]) else 0) + (1 if v.get("made_for_kids") else 0)
        if v["duration"] <= MAX_CLIP:
            if relevance(v["title"], kws) == 0:
                continue
            scored.append((score, v, 0, v["duration"], ""))
            continue
        best = None
        for start, end, part in chapters(v.get("description"), v["duration"]):
            r = relevance(part, kws)
            if r and (best is None or r > best[0]):
                best = (r, start, min(end, start + MAX_CLIP), part)
        if best and best[2] - best[1] >= MIN_CLIP:
            scored.append((score + best[0] * 3, v, best[1], best[2], best[3]))
    scored.sort(key=lambda x: -x[0])
    for score, v, start, end, part in scored:
        if existing_count + len(picks) >= TARGET_CLIPS:
            break
        if total + (end - start) > MAX_TOTAL:
            continue
        picks.append({"youtube_id": v["id"], "start": start, "end": end, "title": v["title"][:200],
                      "channel": v["channel"][:80], "trusted": trusted(v["channel"]), "part": part[:120]})
        total += end - start
    return picks


def search_videos(query, duration="any"):
    data = _api("search", part="snippet", q=query, type="video", maxResults=15, safeSearch="strict",
                videoEmbeddable="true", relevanceLanguage="en", videoDuration=duration)
    ids = [it["id"]["videoId"] for it in data.get("items", []) if it.get("id", {}).get("videoId")]
    if not ids:
        return []
    info = _api("videos", part="snippet,contentDetails,status", id=",".join(ids))
    out = []
    for v in info.get("items", []):
        sn, cd, st = v.get("snippet", {}), v.get("contentDetails", {}), v.get("status", {})
        if sn.get("liveBroadcastContent", "none") != "none":
            continue
        out.append({"id": v["id"], "title": sn.get("title", ""), "channel": sn.get("channelTitle", ""),
                    "description": sn.get("description", ""), "duration": parse_duration(cd.get("duration")),
                    "made_for_kids": st.get("madeForKids", False), "embeddable": st.get("embeddable", True)})
    return out


def find_for(item):
    """Search YouTube and save new clips for one lesson. Returns the number of clips added."""
    from .models import VideoClip

    have = VideoClip.objects.for_item(item).exclude(status=VideoClip.Status.REJECTED)
    count, secs = have.count(), sum(c.length for c in have)
    if count >= MIN_CLIPS:
        return 0
    queries, kws = plan_for(item)
    added = []
    for q in queries:
        for duration in ("short", "medium"):
            candidates = search_videos(q, duration)
            picks = choose(candidates, kws, secs, count + len(added),
                           list(have.values_list("youtube_id", flat=True)) + [p["youtube_id"] for p in added])
            for p in picks:
                added.append(p)
                secs += p["end"] - p["start"]
            if count + len(added) >= TARGET_CLIPS:
                break
        if count + len(added) >= MIN_CLIPS:
            break
    for order, p in enumerate(added, count + 1):
        VideoClip.objects.create(
            **VideoClip.target_kwargs(item), order=order, youtube_id=p["youtube_id"], start=p["start"],
            end=p["end"], title=p["title"], channel=p["channel"], part=p["part"], source="auto",
            status=VideoClip.Status.APPROVED if p["trusted"] else VideoClip.Status.PENDING)
    return len(added)


def short_search_url(query):
    """Fallback link: YouTube search limited to videos under 4 minutes."""
    return ("https://www.youtube.com/results?search_query=" + urllib.parse.quote_plus(query)
            + "&sp=EgIYAQ%253D%253D")


# ------------------------------------------------------------------ video links (always shown)

# One example word per phonics sound, used for the "hear it in real videos" (YouGlish) link.
SOUND_WORDS = {
    "/s/": "sun", "/a/": "ant", "/t/": "tap", "/i/": "insect", "/p/": "pen", "/n/": "net", "/c / k/": "cat",
    "/e/": "egg", "/h/": "hat", "/r/": "rat", "/m/": "map", "/d/": "dog", "/g/": "goat", "/o/": "orange",
    "/u/": "umbrella", "/l/": "lion", "/f/": "fish", "/b/": "bat", "/ai/": "rain", "/j/": "jam", "/oa/": "boat",
    "/ie/": "pie", "/ee/": "tree", "/or/": "fork", "/z/": "zip", "/w/": "web", "/ng/": "ring", "/v/": "van",
    "/oo (book)/": "book", "/oo (moon)/": "moon", "/y/": "yes", "/x/": "fox", "/ch/": "chip", "/sh/": "ship",
    "/th (thin)/": "thin", "/th (this)/": "this", "/qu/": "queen", "/ou/": "cloud", "/oi/": "coin",
    "/ue/": "blue", "/er/": "water", "/ar/": "car",
}


def youglish_url(phrase):
    """YouGlish: many real videos, each starting at the moment someone says this word or sentence."""
    return "https://youglish.com/pronounce/" + urllib.parse.quote(phrase) + "/english"


def _link(emoji, en, bn, query):
    return {"emoji": emoji, "en": en, "bn": bn, "query": query, "url": short_search_url(query), "kind": "youtube"}


def video_links(item):
    """At least 5 separate links for a lesson. Each one opens a page with several short videos on one angle
    of the topic (YouTube search filtered to under 4 minutes), plus a YouGlish link for a key word or sentence."""
    from course.models import CourseLesson
    from .models import Lesson, TalkTopic

    links, say = [], ""
    if isinstance(item, Lesson):
        level = item.module.level.number
        if item.skill == "phonics" and level == 0:
            sound = re.sub(r"\(.*?\)|[/]", " ", item.focus or item.title).strip().split()[0]
            links = [
                _link("🔤", f"The /{sound}/ sound", f"/{sound}/ ধ্বনি", f"{sound} sound phonics for kids"),
                _link("🎵", f"Letter {sound.upper()} song", f"{sound.upper()} অক্ষরের গান", f"letter {sound} song for kids"),
                _link("🖼️", f"Words with /{sound}/", f"/{sound}/ দিয়ে শব্দ", f"words that start with {sound} sound for kids"),
                _link("👄", f"How to say /{sound}/", f"/{sound}/ কীভাবে বলবেন", f"how to pronounce {sound} sound phonics mouth"),
                _link("🧩", f"Blend and read with /{sound}/", f"/{sound}/ দিয়ে মিলিয়ে পড়া", f"{sound} sound blending words for kids"),
            ]
            say = SOUND_WORDS.get(item.focus, "")
        elif item.skill in ("phonics", "reading") and level <= 2:
            focus = re.sub(r"^CVC with (.+)$", r"CVC words short \1", item.focus or item.title)
            links = [
                _link("🔤", f"{focus}: phonics lesson", f"{focus}: ফনিক্স পাঠ", f"{focus} phonics for kids"),
                _link("🎵", "Phonics song", "ফনিক্স গান", f"{focus} phonics song for kids"),
                _link("🧩", "Blend and read words", "মিলিয়ে শব্দ পড়া", f"{focus} words blending reading for kids"),
                _link("📖", "Read a little story", "ছোট গল্প পড়া", f"{focus} decodable reading for kids"),
                _link("👄", "Say it clearly", "স্পষ্ট করে বলা", f"{focus} pronunciation phonics for kids"),
            ]
            m = re.search(r":\s*(.+)$", item.title)
            if m:
                say = m.group(1).split(",")[0].strip().replace("-", "")
        else:
            topic = re.sub(r"\s*\(.*?\)", "", item.title).strip()
            focus = (item.focus or topic).replace("&", "and")
            links = [
                _link("📺", f"{topic}: lesson", f"{topic}: পাঠ", f"{topic} English for kids"),
                _link("🎵", "Song", "গান", f"{focus} song for kids"),
                _link("💡", f"Learn: {focus}", f"শিখি: {focus}", f"{focus} English lesson for kids"),
                _link("💬", "Conversation", "কথোপকথন", f"{focus} English conversation for kids"),
                _link("📖", "Story", "গল্প", f"{focus} story for kids English"),
            ]
            say = topic if len(topic.split()) <= 3 else ""
    elif isinstance(item, TalkTopic):
        t, words = item.title, [w["word"] for w in item.words]
        links = [
            _link("🔤", f"{t}: words", f"{item.title_bn}: শব্দ", f"{t} vocabulary for kids"),
            _link("🎵", "Song", "গান", f"{t} song for kids"),
            _link("📖", "Story", "গল্প", f"{t} story for kids English"),
            _link("💬", "Talk about it", "কথোপকথন", f"{t} English conversation for kids"),
            _link("🖼️", "Picture words", "ছবির শব্দ", f"{' '.join(words[:4])} flashcards for kids"),
        ]
        say = words[0] if words else ""
    elif isinstance(item, CourseLesson):
        t = item.title
        links = [
            _link("📺", f"{t}: lesson", f"{item.title_bn or t}: পাঠ", item.video_query or f"{t} English lesson"),
            _link("🇬🇧", "BBC Learning English", "বিবিসি লার্নিং ইংলিশ", f"BBC Learning English {t}"),
            _link("💡", "Examples", "উদাহরণ", f"{t} examples English"),
            _link("⚠️", "Common mistakes", "সাধারণ ভুল", f"{t} common mistakes English"),
            _link("✏️", "Practice", "অনুশীলন", f"{t} practice exercises English"),
        ]
        ex = next((e for e in item.examples if isinstance(e, str)), "")
        say = ex.rstrip(".?!") if ex and len(ex.split()) <= 8 else ""
    if say:
        links.append({"emoji": "🎧", "en": f"Hear “{say}” in real videos (YouGlish)",
                      "bn": f"আসল ভিডিওতে “{say}” শুনুন (YouGlish)", "query": say, "url": youglish_url(say),
                      "kind": "youglish"})
    return links


def clip_context(item, request=None):
    """What a lesson page needs: approved clips, total time and a short-video fallback link."""
    from .models import VideoClip

    clips = list(VideoClip.objects.for_item(item).visible())
    queries, _ = plan_for(item)
    total = sum(c.length for c in clips)
    return {"clips": clips, "clips_total": fmt_time(total), "clips_fallback": short_search_url(queries[0]),
            "video_links": video_links(item)}
