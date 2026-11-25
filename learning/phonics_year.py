"""Turn the Phonics Year content (learning/seed/phonics_year.py) into lesson data.

For every day this builds:
  teacher   - the parents' guide: story to tell, timed steps in English and Bangla, words, sentences,
              tricky words and the reading text (shown in the parent view; the field keeps its old name)
  note_bn   - what the parent should know, in Bangla (parent view)
  home task - a 5-minute task for home
  items     - practice for the child: tap the picture, type the word, or choose the answer
"""

import random

from .seed.phonics import GROUPS
from .seed.phonics_year import BANK, CHECKS, STORIES, STORIES_BN, TEXTS, TRICKY, TRICKY_SENT, weeks, word

SOUNDS = {k: {"shown": shown, "action": action, "words": words, "tip": tip}
          for _, _, sounds in GROUPS for k, shown, _, action, words, tip in sounds}
ORDER = [k for _, _, sounds in GROUPS for k, *_ in sounds]
GRAPHEMES = {"ck": ["c", "k"], "oo_long": ["oo"], "oo_short": ["oo"], "th_voiced": ["th"], "th_unvoiced": ["th"]}
TRICKY_ORDER = [t for n in sorted(TRICKY) for t in TRICKY[n]]
REVIEW_WORDS = ["cat", "dog", "fish", "ship", "rain", "boat", "moon", "frog", "king", "chip", "sun", "bed"]

QUESTIONS = {
    "captions": [("A big red ___", "bus", "bus, bed, bag"), ("A cat on a ___", "mat", "mat, map, man"),
                 ("A dog in the ___", "sun", "sun, sit, sock")],
    "fold1": [("What does Tim have?", "a net", "a net, a hat, a kite"), ("Who is with Tim?", "Dad", "Dad, Mum, Mina"),
              ("How does Tim feel at the end?", "glad", "glad, sad, cross")],
    "fold2": [("What colour is the kite?", "red and green", "red and green, blue, pink"), ("Where does the kite get stuck?", "in the tree", "in the tree, on the roof, in the pond"),
              ("Who gets it down?", "Dad", "Dad, Mum, Mina")],
    "comp1": [("When do they go to the market?", "on Friday night", "on Friday night, on Monday, in the morning"),
              ("What does Dad buy?", "tea and peanuts", "tea and peanuts, a bird, a kite"),
              ("Why can't Mina have a bird?", "birds should fly free", "birds should fly free, it is too big, it costs too much")],
    "comp2": [("Where does Rafi put the pot?", "by the window", "by the window, in the bath, under the bed"),
              ("How many leaves come up?", "two", "two, ten, one"), ("How many pots are there at the end?", "four", "four, two, six")],
    "pigs": [("What did the first pig use?", "straw", "straw, bricks, sticks"), ("Which house did not fall down?", "the brick house", "the brick house, the straw house, the stick house"),
             ("What did the pigs give the wolf?", "some soup", "some soup, a brick, a house"),
             ("What did the wolf do at each house?", "huffed and puffed", "huffed and puffed, sang a song, knocked politely")],
}


def _graphemes_upto(sound_key):
    out = set()
    for k in ORDER[:ORDER.index(sound_key) + 1]:
        out.update(GRAPHEMES.get(k, [k]))
    return out


def _decodable(known, limit=6):
    """Bank words a child can read with the graphemes taught so far (greedy two-letter first)."""
    found = []
    for w in BANK:
        i, ok = 0, True
        while i < len(w):
            if w[i:i + 2] in known and len(w[i:i + 2]) == 2:
                i += 2
            elif w[i] in known:
                i += 1
            else:
                ok = False
                break
        if ok and len(w) >= 2:
            found.append(w)
    return found[:limit]


def _blank(s):
    return s.replace("___", "______")


# ------------------------------------------------------------------ teaching steps per kind

def S(t, t_bn, m, do, do_bn):
    return (t, t_bn, m, do, do_bn)


def _steps_sound(day, wk, d_index):
    keys = day["sounds"]
    steps = [S("Warm-up", "শুরু", 3, "Show the sound cards your child has learnt so far. Your child says each sound and does its action.",
               "এ পর্যন্ত শেখা sound-এর কার্ড দেখান। শিশু প্রতিটি sound বলবে আর action করবে।")]
    for k in keys:
        s = SOUNDS[k]
        shown = s["shown"]
        letter = shown.split(" ")[0]
        steps += [
            S(f"Story for /{shown}/", f"/{shown}/-এর গল্প", 4,
              "Tell the story in the box above. " + f"Then show the letter{'s' if len(letter) > 1 else ''} <{letter}> and say the sound /{shown}/ - the sound, not the letter name.",
              "ওপরের বক্সের গল্পটি বলুন। " + f"তারপর <{letter}> দেখিয়ে sound টা বলুন: /{shown}/ — অক্ষরের নাম নয়, sound।"),
            S("Action", "অ্যাকশন", 2, f"{s['action']}. Do it together, then ask your child to do it every time they see the card.",
              f"{s['action']}। একসাথে করুন; এরপর কার্ড দেখলেই শিশু action করবে।"),
            S("Write it", "লেখা", 5, f"Draw <{letter}> big in the air together, then on paper. Put a dot where the letter starts; "
              "your child traces it, then writes it alone. Praise a good start.",
              f"আগে বাতাসে বড় করে <{letter}> আঁকুন, তারপর কাগজে। অক্ষর যেখানে শুরু হয় সেখানে একটা বিন্দু দিন; শিশু উপর দিয়ে লিখবে, "
              "তারপর নিজে লিখবে। ঠিক জায়গা থেকে শুরু করলে প্রশংসা করুন।"),
            S("Hear it", "শোনা", 3, f"Say these words slowly: {', '.join(w for w, _, _ in s['words'])}. Your child gives a thumbs up on hearing /{shown}/. "
              "Add one word without the sound to keep it fun.",
              f"ধীরে ধীরে বলুন: {', '.join(w for w, _, _ in s['words'])}। /{shown}/ শুনলে শিশু বুড়ো আঙুল তুলবে। "
              "মজার জন্য মাঝে একটা শব্দ বলুন যাতে sound টা নেই।"),
        ]
    known = _graphemes_upto(keys[-1])
    words = _decodable(known)
    if day.get("auditory") or len(words) < 2:
        steps.append(S("Blend by ear", "শুনে জোড়া দেওয়া", 3, "Say a word in sounds, like s-u-n or s-i-t. Your child says the whole word. No reading yet.",
                       "শব্দটা ভেঙে বলুন, যেমন s-u-n, s-i-t। শিশু পুরো শব্দটা বলবে। এখনই পড়া নয়।"))
    else:
        steps.append(S("Blend and read", "জোড়া দিয়ে পড়া", 4, f"Point to each letter, say the sounds, then blend: {', '.join(words)}. "
                       "Read them together, then your child reads alone.",
                       f"প্রতিটি অক্ষরে আঙুল রেখে sound বলুন, তারপর জোড়া দিন: {', '.join(words)}। আগে একসাথে, তারপর শিশু একা পড়বে।"))
    steps.append(S("Practise", "অনুশীলন", 4, "Do today's practice in the app together.", "অ্যাপে আজকের অনুশীলন একসাথে করুন।"))
    return steps, words


def _steps(day, wk):
    kind, focus, words = day["kind"], day["focus"], day["words"]
    tricky = day.get("tricky", [])
    w = ", ".join(words)
    s = [S("Warm-up", "শুরু", 3, "Quick sound cards: every sound and spelling learnt so far. Your child says each one.",
           "দ্রুত sound কার্ড: এ পর্যন্ত শেখা সব sound আর বানান। শিশু প্রতিটি বলবে।")]
    if kind in ("assess1", "assess2"):
        part, part_bn = ("write", "লেখা") if kind == "assess1" else ("read", "পড়া")
        return [S("Before the check", "শুরুর আগে", 2, "Sit somewhere quiet. Say: 'This shows what you know. Just do your best.'",
                  "শান্ত জায়গায় বসুন। বলুন: 'এটা দেখায় তুমি কী জানো। শুধু চেষ্টা করো।'"),
                S(f"The check: {part}", f"মূল্যায়ন: {part_bn}", 15, "Your child does the check in the app alone. Don't tell the answers - "
                  "it shows what needs more practice. The score is saved on the Phonics Year page.",
                  "শিশু অ্যাপে একা মূল্যায়নটি করবে। উত্তর বলে দেবেন না — এতে বোঝা যাবে কোথায় আরও অনুশীলন দরকার। স্কোর ফনিক্স বছরের পাতায় থাকবে।"),
                S("After the check", "শেষে", 3, "Praise the effort. Look at what was missed and practise those sounds and words next week.",
                  "চেষ্টার প্রশংসা করুন। কোনগুলো ভুল হলো দেখুন, পরের সপ্তাহে সেগুলো আবার অনুশীলন করুন।")]
    if day.get("names"):
        letters = " ".join(day["names"])
        s.append(S("Letter names", "অক্ষরের নাম", 6, f"Say the names of {letters} together, like a song. Each letter has a name and a sound: "
                   "b is called 'bee' and says /b/.", f"{letters} — এই অক্ষরগুলোর নাম একসাথে ছড়ার মতো বলুন। প্রতিটি অক্ষরের একটি নাম আর একটি sound আছে: "
                   "b-এর নাম 'বি', sound /b/।"))
        if day["names"][0] == "n":
            s.append(S("Capital letters", "বড় হাতের অক্ষর", 6, "Write capital and small letters side by side (A a, B b …). Capitals start names and sentences.",
                       "বড় আর ছোট অক্ষর পাশাপাশি লিখুন (A a, B b …)। নাম আর বাক্য বড় হাতের অক্ষর দিয়ে শুরু হয়।"))
    if kind in ("spelling", "sort"):
        s.append(S("New spelling", "নতুন বানান", 6, f"Today: {focus}. Write it big on paper, say the sound it makes and stick it on the "
                   "spellings chart on the wall, next to the other ways to write the same sound.",
                   f"আজ: {focus}। কাগজে বড় করে লিখুন, sound টা বলুন, আর দেয়ালের বানান-চার্টে একই sound-এর অন্য বানানের পাশে লাগান।"))
        if day.get("pairs"):
            pairs = "; ".join(p.replace(" ", " → ") for p in day["pairs"])
            s.append(S("Watch it change", "বদলে যাওয়া দেখুন", 4, f"Write each pair and read both: {pairs}. Ask: what did the e at the end do?",
                       f"প্রতিটি জোড়া লিখে দুটোই পড়ুন: {pairs}। জিজ্ঞেস করুন: শেষের e কী করল?"))
    if kind == "blend":
        s.append(S("Blend", "জোড়া দেওয়া", 6, f"Today: {focus}. Say the two consonants quickly together, then blend the whole word: {w}.",
                   f"আজ: {focus}। দুটি ব্যঞ্জন দ্রুত একসাথে বলুন, তারপর পুরো শব্দ জোড়া দিন: {w}।"))
    if day.get("sort"):
        cols = " | ".join(f"{label}: {ws}" for label, ws in day["sort"])
        s.append(S("Sort", "ভাগ করা", 6, f"Write the words on small cards. Your child puts each card in the right group: {cols}.",
                   f"শব্দগুলো ছোট কার্ডে লিখুন। শিশু প্রতিটি কার্ড ঠিক দলে রাখবে: {cols}।"))
    if words and kind != "blend":
        s.append(S("Read the words", "শব্দ পড়া", 5, f"Read together, then your child reads alone: {w}. Say the sounds of any hard part.",
                   f"আগে একসাথে, তারপর শিশু একা পড়বে: {w}। কঠিন অংশ sound ভেঙে বলুন।"))
    if day.get("chart"):
        s.append(S("The spellings chart", "বানানের চার্ট", 8, "Make a chart on the wall: one row for each sound, with every spelling "
                   "learnt so far (e.g. /ai/: ai, ay, a_e). Your child adds one word for each spelling.",
                   "দেয়ালে একটি চার্ট বানান: প্রতিটি sound-এর জন্য এক সারি, তাতে এ পর্যন্ত শেখা সব বানান (যেমন /ai/: ai, ay, a_e)। "
                   "প্রতিটি বানানের জন্য শিশু একটি শব্দ লিখবে।"))
    for t in tricky:
        ex = TRICKY_SENT[t].replace("___", t)
        s.append(S(f"Tricky word '{t}'", f"Tricky word '{t}'", 5, f"Write '{t}'. Say it, say the letter names, and find the part that does not "
                   f"follow the rules. Look, say, cover, write, check. Read: \"{ex}\"",
                   f"'{t}' লিখুন। শব্দটা বলুন, অক্ষরের নাম বলুন, আর কোন অংশ নিয়ম মানে না তা খুঁজুন। দেখো, বলো, ঢাকো, লেখো, মিলাও। "
                   f"পড়ুন: \"{ex}\""))
    if day.get("text"):
        s.append(S("Read together", "একসাথে পড়া", 8, "Read the text below to your child, then read it together, one line each. "
                   "Point to each word as you read.", "নিচের লেখাটি শিশুকে পড়ে শোনান, তারপর একসাথে পড়ুন — এক লাইন আপনি, এক লাইন শিশু। "
                   "পড়ার সময় প্রতিটি শব্দে আঙুল রাখুন।"))
        s.append(S("Talk about it", "আলোচনা", 5, "Ask the questions in the app. Your child answers in a full sentence.",
                   "অ্যাপের প্রশ্নগুলো জিজ্ঞেস করুন। শিশু পুরো বাক্যে উত্তর দেবে।"))
    if day.get("review_tricky"):
        n = day["review_tricky"]
        s.append(S("Tricky word games", "Tricky word খেলা", 10, f"Write the {n} tricky words on cards. Spread them on the floor; "
                   "say a word and your child splats it with a hand. Then hide cards round the room to find and read.",
                   f"{n}টি tricky word কার্ডে লিখে মেঝেতে ছড়িয়ে দিন। আপনি একটা শব্দ বলবেন, শিশু হাত দিয়ে চাপড় দেবে। "
                   "তারপর ঘরে কার্ড লুকিয়ে রাখুন — শিশু খুঁজে পড়বে।"))
    if kind == "game":
        s.append(S("Games", "খেলা", 10, "Choose two: make words with letter cards, a word hunt round the house, "
                   "'I spy' with sounds, or words on paper fish to 'catch' and read.",
                   "দুটি বেছে নিন: অক্ষর কার্ড দিয়ে শব্দ বানানো, ঘরে শব্দ খোঁজা, sound দিয়ে 'আমি দেখি', "
                   "বা কাগজের মাছে শব্দ লিখে 'ধরা' আর পড়া।"))
    if kind == "dictation" or day.get("sentences"):
        sent = "; ".join(day.get("sentences", [])) or w
        s.append(S("Dictation", "শ্রুতিলিখন", 8, f"Say each one; your child says it back, counts the words on fingers, writes it, then checks: "
                   f"{sent}. Look for a capital letter, spaces between words and a full stop.",
                   f"প্রতিটি বলুন; শিশু আবার বলবে, আঙুলে শব্দ গুনবে, লিখবে, তারপর মিলিয়ে দেখবে: {sent}। "
                   "শুরুতে বড় হাতের অক্ষর, শব্দের মাঝে ফাঁক আর শেষে দাঁড়ি (.) আছে কিনা দেখুন।"))
    if kind == "celebrate":
        s.append(S("Celebrate", "উদযাপন", 10, "Your child reads a favourite word or sentence to the family. Print a certificate "
                   "(Progress → certificates) and put it on the wall.",
                   "শিশু পরিবারের সবাইকে প্রিয় শব্দ বা বাক্য পড়ে শোনাবে। একটি সনদ প্রিন্ট করুন (অগ্রগতি → সনদ) আর দেয়ালে লাগান।"))
    if kind == "review" and not words and not day.get("names"):
        s.append(S("Review", "পুনরাবৃত্তি", 10, "Read sounds and words from the last two weeks, then re-read a favourite little book.",
                   "গত দুই সপ্তাহের sound আর শব্দ পড়ুন, তারপর প্রিয় ছোট বইটি আবার পড়ুন।"))
    if kind in ("spelling", "blend", "review") and words and not day.get("sentences"):
        three = ", ".join(words[:3])
        s.append(S("Write it", "লেখা", 5, f"Say three of today's words: {three}. Your child says the sounds and writes each word. "
                   "Then show the right spelling.", f"আজকের তিনটি শব্দ বলুন: {three}। শিশু sound বলে প্রতিটি শব্দ লিখবে। তারপর ঠিক বানান দেখান।"))
    s.append(S("Practise", "অনুশীলন", 4, "Do today's practice in the app together.", "অ্যাপে আজকের অনুশীলন একসাথে করুন।"))
    return s


# ------------------------------------------------------------------ parent notes (Bangla)

def _note_bn(day):
    k = day["kind"]
    if k == "sound":
        parts = []
        for key in day["sounds"]:
            s = SOUNDS[key]
            parts.append(f"আজকের sound: **/{s['shown']}/**। Action: {s['action']}।" + (f"\n\n**টিপ:** {s['tip']}" if s["tip"] else ""))
        return ("\n\n".join(parts) + "\n\nশিশুকে letter-এর নাম নয়, sound শেখান (s = 'স্‌স্‌', 'এস' নয়)। "
                "গল্পটি শুনিয়ে action করুন, তারপর অ্যাপের practice একসাথে করুন। খেলার মতো রাখুন, বকবেন না।")
    if k in ("assess1", "assess2"):
        return ("আজ ছোট একটি মূল্যায়ন। শিশুকে একা করতে দিন, উত্তর বলে দেবেন না — এতে বোঝা যাবে কোথায় আরও অনুশীলন দরকার। "
                "শেষে স্কোর অগ্রগতি পাতায় দেখা যাবে। কম হলে চিন্তা করবেন না; পরের সপ্তাহে ওই অংশ আবার করুন।")
    if k == "celebrate":
        return "আজ উদযাপনের দিন! শিশু যা শিখেছে তা আপনাকে পড়ে শোনাবে। খুব প্রশংসা করুন — এই আনন্দই পরের ধাপে উৎসাহ দেয়।"
    lines = []
    if day.get("tricky"):
        ts = ", ".join(f"**{t}**" for t in day["tricky"])
        lines.append(f"আজকের tricky word: {ts}। এগুলো নিয়ম মেনে পড়া যায় না, তাই দেখে মনে রাখতে হয়। "
                     "'দেখো, বলো, ঢাকো, লেখো, মিলাও' — এভাবে ৩ বার লিখুন।")
    if k in ("spelling", "sort"):
        lines.append(f"আজকের বানান: **{day['focus']}**। একই sound বিভিন্ন বানানে লেখা যায় — শিশুকে দেখান কোন শব্দে কোন বানান।")
    if k == "blend":
        lines.append(f"আজ: **{day['focus']}**। দুটি ব্যঞ্জন একসাথে দ্রুত বলে পুরো শব্দ জোড়া দিন (s-t-o-p → stop)।")
    if day.get("text"):
        lines.append("আজ একটি ছোট লেখা পড়া হবে। শিশুর সাথে বসে পড়ুন, আঙুল দিয়ে প্রতিটি শব্দ দেখান, তারপর প্রশ্নগুলো জিজ্ঞেস করুন।")
    if k == "dictation" or day.get("sentences"):
        lines.append("শ্রুতিলিখন: আপনি বাক্যটি বলবেন, শিশু আঙুলে শব্দ গুনে লিখবে। বাক্যের শুরুতে বড় হাতের অক্ষর আর শেষে দাঁড়ি (.) দেখে নিন।")
    if day.get("names"):
        lines.append("আজ অক্ষরের **নাম** (a = 'এই', b = 'বি')। মনে করিয়ে দিন: নাম আর sound আলাদা।")
    if k in ("game", "review") and not lines:
        lines.append("আজ পুনরাবৃত্তি আর খেলা। শব্দ কার্ড বানিয়ে লুকিয়ে রাখুন, শিশু খুঁজে পড়বে।")
    return "\n\n".join(lines) or "আজ অ্যাপের practice শিশুর সাথে একসাথে করুন।"


def _home_bn(day, words):
    k = day["kind"]
    if k == "sound":
        ws = ", ".join(w for key in day["sounds"] for w, _, _ in SOUNDS[key]["words"])
        return f"বাসায় ৩টি জিনিস খুঁজুন যার নামে আজকের sound আছে (যেমন: {ws})। শিশু জিনিসটা ধরে sound আর action করবে।"
    if day.get("tricky"):
        return f"tricky word ({', '.join(day['tricky'])}) কাগজে লিখে ফ্রিজে বা দরজায় লাগান। প্রতিবার পাশ দিয়ে গেলে শিশু পড়বে।"
    if day.get("text"):
        return "আজকের লেখাটি রাতে আবার পড়ুন। শিশু আপনাকে গল্পটা নিজের ভাষায় বলবে।"
    if k in ("assess1", "assess2"):
        return "আজ বাসায় কোনো কাজ নেই — শুধু শিশুকে বলুন সে কত ভালো চেষ্টা করেছে।"
    if words:
        return f"এই শব্দগুলো ছোট কাগজে লিখে লুকিয়ে রাখুন: {', '.join(words[:5])}। শিশু খুঁজে পেলে জোরে পড়বে।"
    return "আজ ঘুমানোর আগে ৫ মিনিট একসাথে একটি ছোট বই পড়ুন।"


# ------------------------------------------------------------------ practice items

def _items(day, rng, taught_tricky, words):
    """Return (activity, [(prompt, answer, choices, picture, meaning_bn)])."""
    k = day["kind"]
    if k == "sound":
        pool = [w for key in ORDER for w in SOUNDS[key]["words"]]
        out = []
        for key in day["sounds"]:
            for w, e, bn in SOUNDS[key]["words"]:
                others = rng.sample([x for x in pool if x[0] not in {y[0] for y in SOUNDS[key]["words"]}], 2)
                opts = [f"{e} {w}"] + [f"{x[1]} {x[0]}" for x in others]
                rng.shuffle(opts)
                out.append((w, f"{e} {w}", ", ".join(opts), e, bn))
        return "sound_tap", out
    if k == "assess2":
        return "quiz", [(_blank(q), a, c, "", "") for q, a, c in CHECKS[day["check"]]["read"]]
    if k == "assess1":
        out = []
        for x in CHECKS[day["check"]]["write"]:
            if " " in x:
                out.append((x, x, "", "✍️", ""))
            elif len(x) > 2:
                w, e, bn = word(x)
                out.append((w, w, "", e, bn))
        return "dictation", out
    if day.get("names"):
        names = {"a": "ay", "b": "bee", "c": "see", "d": "dee", "e": "ee", "f": "ef", "g": "jee", "h": "aitch", "i": "eye",
                 "j": "jay", "k": "kay", "l": "el", "m": "em", "n": "en", "o": "oh", "p": "pee", "q": "cue", "r": "ar",
                 "s": "ess", "t": "tee", "u": "you", "v": "vee", "w": "double-you", "x": "ex", "y": "why", "z": "zed"}
        out = []
        for ch in day["names"][:8]:
            others = rng.sample([v for kk, v in names.items() if kk != ch], 2)
            opts = [names[ch]] + others
            rng.shuffle(opts)
            out.append((f"What is the name of the letter {ch.upper()} {ch}?", names[ch], ", ".join(opts), "🔤", ""))
        return "quiz", out
    if day.get("text") and day["text"] in QUESTIONS:
        return "quiz", [(_blank(q), a, c, "📖", "") for q, a, c in QUESTIONS[day["text"]]]
    if day.get("sort"):
        labels = [lab for lab, _ in day["sort"]]
        out = []
        for lab, ws in day["sort"]:
            for w in ws.split()[:2]:
                _, e, bn = word(w)
                out.append((f"{e} {w}: which group?".strip(), lab, ", ".join(labels), e, bn))
        rng.shuffle(out)
        return "quiz", out
    if day.get("tricky") or day.get("review_tricky"):
        pool = list(day.get("tricky") or rng.sample(taught_tricky[-day["review_tricky"]:], 6))
        earlier = [t for t in taught_tricky if t not in pool]
        pool += rng.sample(earlier, min(len(earlier), 3 - len(pool))) if len(pool) < 3 else []
        out = []
        for t in pool:
            others = [x for x in taught_tricky if x.lower() != t.lower()]
            others += [x for x in ("a", "it", "is", "and", "in") if x not in others and x != t][:max(0, 2 - len(others))]
            wrong = rng.sample(others, 2)
            opts = [t] + wrong
            rng.shuffle(opts)
            out.append((_blank(TRICKY_SENT[t]), t, ", ".join(opts), "⭐", ""))
        for w in words:   # top up with "which word is this picture?"
            if len(out) >= 4:
                break
            w, e, bn = word(w)
            if e:
                wrong = rng.sample([x for x in REVIEW_WORDS if x != w], 2)
                opts = [w] + wrong
                rng.shuffle(opts)
                out.append((f"Which word is {e}?", w, ", ".join(opts), e, bn))
        return "quiz", out
    out = [(w, w, "", e, bn) for w, e, bn in (word(x) for x in words)]
    out += [(s, s, "", "✍️", "") for s in day.get("sentences", [])]
    for extra in rng.sample(REVIEW_WORDS, 5):   # at least 4 items, topped up with review words
        if len(out) >= 4:
            break
        if all(extra != o[1] for o in out):
            out.append(word(extra))
            out[-1] = (out[-1][0], out[-1][0], "", out[-1][1], out[-1][2])
    return "dictation", out


# ------------------------------------------------------------------ the whole year

PREPARE = [
    ("Sound cards: write each sound learnt so far big on a piece of card.", "Sound কার্ড: এ পর্যন্ত শেখা প্রতিটি sound মোটা কাগজে বড় করে লিখুন।"),
    ("Paper and a pencil, or a slate, for writing and dictation.", "লেখা ও শ্রুতিলিখনের জন্য কাগজ-পেনসিল বা স্লেট।"),
    ("15–25 quiet minutes a day, at the same time if you can.", "প্রতিদিন ১৫–২৫ মিনিট শান্ত সময়, সম্ভব হলে একই সময়ে।"),
]


def build():
    """Yield (week, [day lessons]) for all 36 weeks."""
    rng = random.Random(2026)
    taught = []
    for wk in weeks():
        days = []
        prepare = list(PREPARE)
        if wk["term"] == 1 and wk["n"] <= 7:
            prepare.append(("A writing sheet: write the week's letters with a dot where each one starts.", "লেখার পাতা: সপ্তাহের অক্ষরগুলো লিখুন, প্রতিটির শুরুর জায়গায় একটা বিন্দু দিন।"))
        if any(d.get("text") for d in wk["days"]):
            prepare.append(("The reading text: print the week or show it on the phone.", "পড়ার লেখা: সপ্তাহটি প্রিন্ট করুন বা ফোনে দেখান।"))
        if any(d["kind"].startswith("assess") for d in wk["days"]):
            prepare.append(("A phone or tablet for this week's check.", "এই সপ্তাহের মূল্যায়নের জন্য একটি ফোন বা ট্যাবলেট।"))
        if wk["n"] in (21, 27, 34):
            prepare.append(("A big sheet of paper for the spellings chart on the wall.", "দেয়ালের বানান-চার্টের জন্য একটি বড় কাগজ।"))
        for i, day in enumerate(wk["days"]):
            if day["kind"] == "sound":
                steps, words = _steps_sound(day, wk, i)
                focus = day["focus"]
                action = " · ".join(SOUNDS[k]["action"] for k in day["sounds"])
                story = " ".join(STORIES[k] for k in day["sounds"])
                story_bn = " ".join(STORIES_BN[k] for k in day["sounds"])
                note_en = " ".join(f"Say the sound /{SOUNDS[k]['shown']}/ and do the action: {SOUNDS[k]['action']}." for k in day["sounds"])
            else:
                steps, words = _steps(day, wk), day["words"]
                focus, action, story, story_bn = day["focus"], "", "", ""
                note_en = f"Today: {day['title']}."
                if day.get("tricky"):
                    note_en += " Tricky words: " + ", ".join(day["tricky"]) + "."
            taught += [t for t in day.get("tricky", []) if t not in taught]
            activity, items = _items(day, rng, taught or TRICKY_ORDER[:3], words)
            text = TEXTS.get(day.get("text", ""))
            if isinstance(text, list):
                text = ("Captions", text)
            days.append({
                "title": day["title"], "focus": focus[:60], "action_hint": action[:200], "note_en": note_en,
                "note_bn": _note_bn(day), "home_task_bn": _home_bn(day, words),
                "home_task_en": "Practise for 5 minutes at home today.", "activity": activity,
                "minutes": 30 if day["kind"].startswith("assess") else 25, "items": items,
                "kind": day["kind"], "check": day.get("check"),
                "teacher": {"day": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"][i], "story": story, "story_bn": story_bn,
                            "steps": [{"t": t, "t_bn": tb, "min": m, "do": d, "do_bn": db} for t, tb, m, d, db in steps], "words": words,
                            "sentences": day.get("sentences", []), "tricky": day.get("tricky", []),
                            "text": {"title": text[0], "lines": text[1]} if text else None, "kind": day["kind"]},
            })
        yield wk, prepare, days
