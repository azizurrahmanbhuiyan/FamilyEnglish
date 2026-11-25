"""Colourful printable student worksheets (A4) for the five phonics skills. All content FamilyEnglish/Claude's own."""
import random
from pdf_build import build  # reuse the PDF builder (adds the footer)
import pdf_build as make
make.FOOT = "FamilyEnglish phonics worksheets — free to print for your own children and class. Pictures and words chosen by FamilyEnglish."

make.CSS = """
@page { size: A4; }
* { box-sizing: border-box; }
body { font-family: 'Andika', 'Noto Color Emoji', 'Lohit Bengali', sans-serif; color: #1f2340; font-size: 14pt; margin: 0; }
.bn { font-family: 'Lohit Bengali', 'Mukti', sans-serif; }
.emo { font-family: 'Noto Color Emoji'; }
.banner { border-radius: 20px; padding: 14px 20px; color: #fff; margin-bottom: 10px; }
.banner h1 { margin: 0; font-size: 26pt; line-height: 1.1; }
.banner p { margin: 4px 0 0; font-size: 12pt; opacity: .95; }
.b1 { background: linear-gradient(135deg,#e8364a,#f59e0b); } .b2 { background: linear-gradient(135deg,#1d8fff,#2fe0b5); }
.b3 { background: linear-gradient(135deg,#16a86a,#9be15d); } .b4 { background: linear-gradient(135deg,#8b5cf6,#db2777); }
.b5 { background: linear-gradient(135deg,#0ea5b7,#1d8fff); }
h2 { font-size: 17pt; margin: 14px 0 6px; color: #2a2470; break-after: avoid; }
h2 .n { display: inline-block; padding: 1px 10px; border-radius: 999px; background: #2a2470; color: #fff; font-size: 12pt; margin-right: 8px; vertical-align: 2px; }
.parent { background: #fff7e0; border-radius: 12px; padding: 8px 12px; font-size: 10.5pt; margin: 6px 0 10px; border-left: 5px solid #f59e0b; }
.page { break-before: page; }
.name { font-size: 12pt; margin: 4px 0 8px; } .name span { display: inline-block; width: 230px; border-bottom: 2px solid #999; margin-right: 18px; }
.grid { display: grid; gap: 8px; }
.card { border: 2px solid #e3e5f2; border-radius: 14px; padding: 6px; text-align: center; break-inside: avoid; }
.card .e { font-family: 'Noto Color Emoji'; font-size: 30pt; line-height: 1.2; }
.card .w { font-size: 12pt; color: #555; }
.wbox { display: inline-block; width: 46px; height: 46px; border: 2.5px solid #2a2470; border-radius: 8px; margin: 2px; vertical-align: middle; }
.chip { display: inline-block; border-radius: 10px; color: #fff; font-weight: 700; padding: 2px 8px; margin: 2px; font-size: 16pt; }
.g1 { background:#e8364a } .g2 { background:#f59e0b } .g3 { background:#16a86a } .g4 { background:#1d8fff } .g5 { background:#8b5cf6 } .g6 { background:#db2777 } .g7 { background:#0ea5b7 }
.gt1 { color:#e8364a } .gt2 { color:#d97706 } .gt3 { color:#16a86a } .gt4 { color:#1d8fff } .gt5 { color:#8b5cf6 } .gt6 { color:#db2777 } .gt7 { color:#0ea5b7 }
table.chart { width: 100%; border-collapse: separate; border-spacing: 4px; }
table.chart td { border-radius: 10px; padding: 1px 3px; text-align: center; background: #f6f7fd; font-size: 9.5pt; line-height: 1.15; }
table.chart td .l { display: block; font-size: 16pt; font-weight: 700; }
table.chart td .e { font-family: 'Noto Color Emoji'; font-size: 13pt; }
.cut { display: grid; grid-template-columns: repeat(6, 1fr); gap: 0; border: 2px dashed #aaa; }
.cut div { border: 1px dashed #bbb; height: 96px; display: flex; align-items: center; justify-content: center; font-size: 38pt; font-weight: 700; }
.track { display: grid; grid-template-columns: repeat(7, 1fr); gap: 5px; }
.track div { border: 2px solid #ccd; border-radius: 50%; height: 62px; display: flex; align-items: center; justify-content: center; font-size: 17pt; font-weight: 700; color: #889; }
.sb { display: inline-block; margin: 0 1px; position: relative; padding-bottom: 12px; }
.sb.d::after { content: ''; position: absolute; left: 50%; bottom: 0; width: 8px; height: 8px; margin-left: -4px; border-radius: 50%; background: #e8364a; }
.sb.l::after { content: ''; position: absolute; left: 10%; right: 10%; bottom: 2px; height: 4px; border-radius: 2px; background: #1d8fff; }
.words { display: grid; grid-template-columns: repeat(4, 1fr); gap: 6px 10px; font-size: 22pt; }
.words div { background: #f6f7fd; border-radius: 12px; text-align: center; padding: 4px 0 2px; }
.tick { display: inline-block; width: 18px; height: 18px; border: 2px solid #999; border-radius: 4px; vertical-align: middle; margin-left: 6px; }
.match { display: grid; grid-template-columns: 1fr 120px 1fr; font-size: 22pt; }
.match .r { text-align: right; } .match div { padding: 8px 6px; }
.match .dot { display: inline-block; width: 12px; height: 12px; border-radius: 50%; background: #2a2470; vertical-align: middle; margin: 0 8px; }
.sent { font-size: 18pt; line-height: 1.8; } .sent .t { color: #8b5cf6; font-weight: 700; }
.write { border-bottom: 2px solid #9aa; height: 46px; margin: 4px 0; }
.boxes { display: grid; grid-template-columns: 1fr 1fr; gap: 10px 16px; }
.boxes > div { display: flex; align-items: center; gap: 8px; border: 2px solid #e3e5f2; border-radius: 14px; padding: 6px 10px; break-inside: avoid; }
.boxes .e { font-family: 'Noto Color Emoji'; font-size: 30pt; }
.count { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; }
.count > div { border: 2px solid #e3e5f2; border-radius: 14px; padding: 6px; text-align: center; }
.count .e { font-family: 'Noto Color Emoji'; font-size: 32pt; }
.count .o span { display: inline-block; width: 34px; height: 34px; border: 2px solid #8b5cf6; border-radius: 50%; line-height: 30px; margin: 0 4px; font-weight: 700; color: #8b5cf6; }
table.lscwc { width: 100%; border-collapse: collapse; font-size: 16pt; }
table.lscwc th { background: #0ea5b7; color: #fff; padding: 6px; font-size: 12pt; }
table.lscwc td { border: 2px solid #d9dcef; height: 50px; padding: 0 8px; }
table.lscwc td.w { font-size: 22pt; font-weight: 700; }
.tw b { color: #e8364a; }
.foot { margin-top: 12px; font-size: 8pt; color: #888; border-top: 1px solid #e3e5f2; padding-top: 4px; font-family: Arial, sans-serif; }
"""

GROUPS = [
    ["s", "a", "t", "i", "p", "n"], ["ck", "e", "h", "r", "m", "d"], ["g", "o", "u", "l", "f", "b"],
    ["ai", "j", "oa", "ie", "ee", "or"], ["z", "w", "ng", "v", "oo", "oo"], ["y", "x", "ch", "sh", "th", "th"],
    ["qu", "ou", "oi", "ue", "er", "ar"]]
PIC = {  # one FamilyEnglish picture word per sound (the sound is marked in capitals for the parent)
    "s": ("☀️", "sun"), "a": ("🍎", "apple"), "t": ("🐯", "tiger"), "i": ("🐞", "insect"), "p": ("🐷", "pig"), "n": ("👃", "nose"),
    "ck": ("🪁", "kite / duck"), "e": ("🥚", "egg"), "h": ("🎩", "hat"), "r": ("🐰", "rabbit"), "m": ("🌙", "moon"), "d": ("🐶", "dog"),
    "g": ("🐐", "goat"), "o": ("🐙", "octopus"), "u": ("☂️", "umbrella"), "l": ("🦁", "lion"), "f": ("🐟", "fish"), "b": ("⚽", "ball"),
    "ai": ("🌧️", "rain"), "j": ("🧃", "juice"), "oa": ("⛵", "boat"), "ie": ("🥧", "pie"), "ee": ("🌳", "tree"), "or": ("🍴", "fork"),
    "z": ("🦓", "zebra"), "w": ("⌚", "watch"), "ng": ("💍", "ring"), "v": ("🚐", "van"), "oo": ("🥄", "spoon"), "oo2": ("📖", "book"),
    "y": ("🪀", "yo-yo"), "x": ("📦", "box"), "ch": ("🧀", "cheese"), "sh": ("🚢", "ship"), "th": ("🪶", "feather"), "th2": ("👍", "thumb"),
    "qu": ("👸", "queen"), "ou": ("☁️", "cloud"), "oi": ("🪙", "coin"), "ue": ("🗽", "statue"), "er": ("🪜", "ladder"), "ar": ("🚗", "car")}

import re


def number_sheets(html, pack):
    """Label every activity 'Worksheet <pack>.<n>' in reading order."""
    n = iter(range(1, 100))
    return re.sub(r"<span class='n'>.*?</span>", lambda m: f"<span class='n'>Worksheet {pack}.{next(n)}</span>", html)


def key_of(g, i, s):
    if s == "oo" and i == 5: return "oo2"
    if s == "th" and i == 5: return "th2"
    return s

def head(cls, title, sub, parent_en, parent_bn):
    return (f"<div class='banner {cls}'><h1>{title}</h1><p>{sub}</p></div>"
            "<div class='name'>Name: <span></span> Date: <span style='width:140px'></span></div>"
            f"<div class='parent'><b>For parents:</b> {parent_en}<br><span class='bn'>অভিভাবকের জন্য: {parent_bn}</span></div>")

def sb(word):
    """Sound buttons: 'sh-i-p' → dots under single letters, a line under digraphs."""
    return "".join(f"<span class='sb {'l' if len(g) > 1 else 'd'}'>{g}</span>" for g in word.split("-"))

# ---------------------------------------------------------------- Pack 1: letter sounds
def pack1():
    h = head("b1", "My Letter Sounds 🔤", "Skill 1 · Learn the 42 sounds",
             "Say the <b>sound</b>, not the letter name: s is /sss/, not \"ess\". Keep sounds short — /t/, not \"tuh\". 5 minutes a day is enough.",
             "অক্ষরের নাম নয়, ধ্বনি বলান: s মানে /স্‌স্‌স্‌/, \"এস\" নয়। ধ্বনি ছোট রাখুন — /ট্‌/, \"টা\" নয়। প্রতিদিন ৫ মিনিটই যথেষ্ট।")
    rows = ""
    for gi, g in enumerate(GROUPS, 1):
        cells = "".join(f"<td><span class='l gt{gi}'>{s}</span><span class='e'>{PIC[key_of(g,i,s)][0]}</span><br>{PIC[key_of(g,i,s)][1]}</td>" for i, s in enumerate(g))
        rows += f"<tr><td style='background:none;font-weight:700'>Group {gi}</td>{cells}</tr>"
    h += f"<h2><span class='n'>1</span>My sound chart — say each sound and its picture word</h2><table class='chart'>{rows}</table>"
    h += "<p style='font-size:11pt'>Two sounds have two pictures: <b>oo</b> is long in <i>spoon</i>, short in <i>book</i>. <b>th</b> buzzes in <i>feather</i> and is quiet in <i>thumb</i>.</p>"
    first = [("🐟", "f"), ("🐶", "d"), ("☀️", "s"), ("🐷", "p"), ("🎩", "h"), ("🌙", "m"), ("🐐", "g"), ("🦁", "l"), ("🐰", "r"), ("🍎", "a"), ("🥚", "e"), ("☂️", "u"),
             ("🐯", "t"), ("🚐", "v"), ("🦓", "z"), ("🧃", "j")]
    cards = "".join(f"<div class='card'><div class='e'>{e}</div><span class='wbox'></span></div>" for e, _ in first)
    h += f"<div class='page'></div><h2><span class='n'>2</span>What sound does it start with? Write the letter.</h2><div class='grid' style='grid-template-columns:repeat(4,1fr)'>{cards}</div>"
    h += "<p style='font-size:10pt;color:#777'>Answers: fish f · dog d · sun s · pig p · hat h · moon m · goat g · lion l · rabbit r · apple a · egg e · umbrella u · tiger t · van v · zebra z · juice j</p>"
    cut = "".join(f"<div class='gt{gi}'>{s}</div>" for gi, g in enumerate(GROUPS, 1) for s in g)
    h += f"<div class='page'></div><h2><span class='n'>3</span>Sound cards ✂️ Cut them out. Flash them every day.</h2><div class='cut'>{cut}</div>"
    track = "".join(f"<div class='gt{gi}'>{s}</div>" for gi, g in enumerate(GROUPS, 1) for s in g)
    h += f"<div class='page'></div><h2><span class='n'>4</span>I know my sounds! Colour a circle when you know the sound.</h2><div class='track'>{track}</div>"
    h += "<h2><span class='n'>5</span>Sound hunt 🔎</h2><p>Find 3 things at home that start with each sound:</p>"
    for s in ["s", "m", "b", "c"]:
        h += f"<div style='display:flex;align-items:center;gap:10px'><span class='chip g4' style='min-width:44px;text-align:center'>{s}</span><div class='write' style='flex:1'></div></div>"
    return h

# ---------------------------------------------------------------- Pack 2: letter formation
def trace_row(letter, colour):
    W, H, base, mid, top, desc = 680, 84, 60, 35, 22, 76
    lines = (f"<line x1='0' x2='{W}' y1='{top}' y2='{top}' stroke='#cfd3ea' stroke-width='1'/>"
             f"<line x1='0' x2='{W}' y1='{mid}' y2='{mid}' stroke='#cfd3ea' stroke-width='1.2' stroke-dasharray='5 5'/>"
             f"<line x1='0' x2='{W}' y1='{base}' y2='{base}' stroke='#e8364a' stroke-width='1.6'/>"
             f"<line x1='0' x2='{W}' y1='{desc}' y2='{desc}' stroke='#cfd3ea' stroke-width='1'/>")
    txt = f"<text x='8' y='{base}' font-family='Andika' font-size='52' fill='{colour}'>{letter}</text>"
    step = max(60, 30 * len(letter) + 30)
    for i in range(1, (W - 8 - 30 * max(1, len(letter))) // step + 1):
        txt += f"<text x='{8 + i * step}' y='{base}' font-family='Andika' font-size='52' fill='none' stroke='#9aa3c7' stroke-width='1.3' stroke-dasharray='3 3'>{letter}</text>"
    return f"<svg width='{W}' height='{H}' viewBox='0 0 {W} {H}'>{lines}{txt}</svg>"

def blank_row():
    return trace_row("", "#fff").replace("<text x='8' y='60' font-family='Andika' font-size='52' fill='#fff'></text>", "")

def pack2():
    h = head("b2", "My Letter Shapes ✏️", "Skill 2 · Form each letter the right way",
             "Check three things: a gentle tripod grip, the right <b>starting point</b>, and saying the sound while writing. Neatness comes later.",
             "তিনটি জিনিস দেখুন: আলতো করে পেনসিল ধরা (তিন আঙুলে), ঠিক জায়গা থেকে <b>শুরু</b> করা, আর লেখার সময় ধ্বনিটি বলা। সুন্দর হাতের লেখা পরে আসবে।")
    h += ("<h2><span class='n'>1</span>Hold your pencil like this</h2><div class='grid' style='grid-template-columns:repeat(3,1fr)'>"
          "<div class='card'><div class='e'>🤏</div><b>Pinch</b><div class='w'>thumb + first finger</div></div>"
          "<div class='card'><div class='e'>✍️</div><b>Rest</b><div class='w'>on your middle finger</div></div>"
          "<div class='card'><div class='e'>😌</div><b>Relax</b><div class='w'>hold it gently</div></div></div>")
    fams = [("Round letters — start like a c 🔄", "#e8364a", list("cadgoqes")),
            ("Straight-down letters — start at the top ⬇️", "#1d8fff", list("litjuy")),
            ("Down, up and over 🌈", "#16a86a", list("rnmhbpk")),
            ("Zig-zag letters ⚡", "#8b5cf6", list("vwxz")),
            ("Last few", "#db2777", ["f"])]
    first = True
    for title, col, letters in fams:
        h += f"<h2{'' if first else ''}><span class='n'>✓</span>{title}</h2>"
        first = False
        for L in letters:
            h += trace_row(L, col)
    h += ("<div class='page'></div><h2><span class='n'>★</span>b or d? Remember the bed 🛏️</h2>"
          "<p><b>b</b> starts with the stick (down, up and over). <b>d</b> starts like a <b>c</b>, then the stick. In <b>bed</b>, the b and d are the two ends of the bed.</p>"
          + trace_row('bed', '#1d8fff') +
          trace_row('b', '#16a86a') + trace_row('d', '#e8364a') +
          "<h2><span class='n'>★</span>Write your name</h2>" + blank_row() + blank_row() +
          "<h2><span class='n'>★</span>Write a word you can read</h2>" + blank_row() + blank_row())
    return h

# ---------------------------------------------------------------- Pack 3: blending
def pack3():
    h = head("b3", "I Can Read Words! 📖", "Skill 3 · Blending: say the sounds, push them together",
             "Point under each sound. A <b>dot</b> = one letter, one sound. A <b>line</b> = two letters, one sound. Say the sounds, then faster, then the word. Wait before helping.",
             "প্রতিটি ধ্বনির নিচে আঙুল রাখুন। <b>বিন্দু</b> = এক অক্ষর, এক ধ্বনি। <b>দাগ</b> = দুই অক্ষর, এক ধ্বনি। ধ্বনিগুলো বলুন, তারপর দ্রুত, তারপর পুরো শব্দ। সাহায্যের আগে একটু অপেক্ষা করুন।")
    sets = [("Sounds s a t i p n", "a-t i-t i-n s-a-t t-a-p p-i-n n-a-p t-i-n s-i-t p-a-n t-i-p s-i-p"),
            ("Add c k e h r m d", "c-a-t h-e-n r-e-d m-a-n h-a-t k-i-d m-a-t n-e-t h-a-m r-a-t p-e-t d-i-m"),
            ("Add g o u l f b", "d-o-g s-u-n b-u-s l-o-g f-u-n c-u-p b-a-g b-i-g h-u-t l-e-g f-o-g m-u-d"),
            ("Two letters, one sound", "sh-i-p ch-i-p f-i-sh th-i-n r-ai-n b-oa-t s-ee f-ee-t p-ie f-or-k b-oo-k c-ar"),
            ("Four sounds", "s-t-o-p j-u-m-p f-r-o-g d-r-u-m t-e-n-t h-a-n-d s-n-a-p c-l-a-p b-e-l-t s-p-o-t f-l-a-g m-i-l-k")]
    for i, (title, ws) in enumerate(sets, 1):
        if i == 3: h += "<div class='page'></div>"
        cells = "".join(f"<div>{sb(w)}<span class='tick'></span></div>" for w in ws.split())
        h += f"<h2><span class='n'>{i}</span>{title}</h2><div class='words'>{cells}</div>"
    pairs = [("dog", "🐶"), ("sun", "☀️"), ("cat", "🐱"), ("bus", "🚌"), ("hat", "🎩"), ("pig", "🐷"), ("fish", "🐟"), ("ship", "🚢")]
    pics = pairs[:]; random.Random(7).shuffle(pics)
    rows = "".join(f"<div class='r'>{w}<span class='dot'></span></div><div></div><div><span class='dot'></span><span class='emo' style='font-size:30pt'>{p[1]}</span></div>" for (w, _), p in zip(pairs, pics))
    h += f"<div class='page'></div><h2><span class='n'>6</span>Read the word. Draw a line to its picture.</h2><div class='match'>{rows}</div>"
    sents = ["A cat sat on a mat.", "<span class='t'>The</span> dog is in <span class='t'>the</span> sun.", "Sam had a red hat.",
             "Pip can hop and run.", "<span class='t'>I</span> can see a fish.", "Mum got a big pot of jam."]
    h += "<h2><span class='n'>7</span>Read the sentences</h2><p style='font-size:11pt'><span style='color:#8b5cf6;font-weight:700'>Purple</span> words are tricky words — just say them.</p><div class='sent'>" + "".join(f"<div>{s}<span class='tick'></span></div>" for s in sents) + "</div>"
    return h

# ---------------------------------------------------------------- Pack 4: segmenting / spelling
def pack4():
    h = head("b4", "I Can Spell Words! 🧩", "Skill 4 · Hear the sounds, write the sounds",
             "Say the word slowly. Your child says its sounds, counts them on fingers, then writes <b>one sound in each box</b>. Praise every correct sound — \"bote\" for boat is a good try!",
             "শব্দটি ধীরে বলুন। শিশু ধ্বনিগুলো বলবে, আঙুলে গুনবে, তারপর <b>প্রতিটি ঘরে একটি ধ্বনি</b> লিখবে। প্রতিটি ঠিক ধ্বনির জন্য প্রশংসা করুন — boat-এর জায়গায় \"bote\" লেখাও ভালো চেষ্টা!")
    items = [("🐱", 3), ("🐶", 3), ("☀️", 3), ("🐷", 3), ("🚌", 3), ("🎩", 3), ("🐟", 3), ("🚢", 3), ("🦆", 3), ("⛵", 3), ("🌳", 3), ("🌙", 3), ("🐸", 4), ("🥁", 4), ("⛺", 4), ("✋", 4)]
    box = "<span class='wbox'></span>"
    cells = "".join(f"<div><span class='e'>{e}</span>{box * n}</div>" for e, n in items)
    h += f"<h2><span class='n'>1</span>Sound boxes: one sound in each box</h2><div class='boxes'>{cells}</div>"
    h += "<p style='font-size:10pt;color:#777'>Answers: c-a-t · d-o-g · s-u-n · p-i-g · b-u-s · h-a-t · f-i-sh · sh-i-p · d-u-ck · b-oa-t · t-r-ee · m-oo-n · f-r-o-g · d-r-u-m · t-e-n-t · h-a-n-d</p>"
    cnt = [("🥚", "egg"), ("🐝", "bee"), ("🐄", "cow"), ("🐜", "ant"), ("🎂", "cake"), ("⭐", "star"), ("🦀", "crab"), ("🐌", "snail"), ("🛏️", "bed")]
    cc = "".join(f"<div><div class='e'>{e}</div><div class='w'>{w}</div><div class='o'><span>2</span><span>3</span><span>4</span></div></div>" for e, w in cnt)
    h += f"<div class='page'></div><h2><span class='n'>2</span>How many sounds? Circle the number.</h2><div class='count'>{cc}</div>"
    h += "<p style='font-size:10pt;color:#777'>Answers: egg 2 · bee 2 · cow 2 · ant 3 · cake 3 · star 3 · crab 4 · snail 4 · bed 3</p>"
    h += ("<div class='page'></div><h2><span class='n'>3</span>Dictation 🎧 Listen, say the sounds, write the word</h2>"
          "<div class='parent'><b>Words to say:</b> sat · pin · dog · red · cup · fish · chip · rain · boat · jump &nbsp; <b>Sentence:</b> The dog is in the van.</div>")
    for i in range(1, 11):
        h += f"<div style='display:flex;align-items:end;gap:8px'><b style='width:26px'>{i}.</b><div class='write' style='flex:1'></div></div>"
    h += "<p><b>Sentence:</b></p><div class='write'></div>"
    h += ("<h2><span class='n'>4</span>Draw your favourite toy and write its name</h2>"
          "<div style='border:2px dashed #aab;border-radius:14px;height:110px'></div>")
    return h

# ---------------------------------------------------------------- Pack 5: tricky words
TRICKY = [["the", "I", "to", "was", "said", "you"], ["he", "she", "we", "me", "be", "my"],
          ["are", "all", "they", "there", "come", "some"], ["one", "two", "what", "who", "where", "here"]]
TRICKY_PART = {"the": "th<b>e</b>", "I": "<b>I</b>", "to": "t<b>o</b>", "was": "w<b>a</b>s", "said": "s<b>ai</b>d", "you": "y<b>ou</b>",
               "he": "h<b>e</b>", "she": "sh<b>e</b>", "we": "w<b>e</b>", "me": "m<b>e</b>", "be": "b<b>e</b>", "my": "m<b>y</b>",
               "are": "<b>are</b>", "all": "<b>a</b>ll", "they": "th<b>ey</b>", "there": "th<b>ere</b>", "come": "c<b>o</b>m<b>e</b>", "some": "s<b>o</b>m<b>e</b>",
               "one": "<b>one</b>", "two": "t<b>wo</b>", "what": "wh<b>a</b>t", "who": "<b>who</b>", "where": "wh<b>ere</b>", "here": "h<b>ere</b>"}

def pack5():
    h = head("b5", "Tricky Words ⭐", "Skill 5 · Words with a tricky part",
             "Most of each word can be sounded out — only the <b style='color:#e8364a'>red part</b> is tricky. Learn one set a week. Read them every day; spell them with Look, Say, Cover, Write, Check.",
             "প্রতিটি শব্দের বেশিরভাগ অংশ ধ্বনি দিয়ে পড়া যায় — শুধু <b style='color:#e8364a'>লাল অংশটি</b> কঠিন। সপ্তাহে একটি সেট শিখুন। প্রতিদিন পড়ুন; বানান শিখুন: দেখো, বলো, ঢাকো, লেখো, মিলাও।")
    for i, s in enumerate(TRICKY, 1):
        cells = "".join(f"<div class='tw'>{TRICKY_PART[w]}<span class='tick'></span></div>" for w in s)
        h += f"<h2><span class='n'>{i}</span>Set {i}</h2><div class='words' style='grid-template-columns:repeat(6,1fr)'>{cells}</div>"
    rows = "".join(f"<tr><td class='w'>{w}</td><td></td><td></td><td></td><td style='width:60px'></td></tr>" for w in ["the", "said", "was", "you", "they", "come", "one", "what"])
    h += ("<div class='page'></div><h2><span class='n'>★</span>Look · Say · Cover · Write · Check</h2>"
          "<p style='font-size:12pt'>👀 Look at the word and say it. ✋ Cover it. ✏️ Write it. ✅ Uncover and check. Do it 3 times.</p>"
          f"<table class='lscwc'><tr><th>Look &amp; say</th><th>Write 1</th><th>Write 2</th><th>Write 3</th><th>✅</th></tr>{rows}</table>")
    sents = ["<span class='t'>I</span> had a hot dog.", "<span class='t'>She was</span> in bed.", "<span class='t'>They</span> ran <span class='t'>to</span> the bus.",
             "<span class='t'>Come</span> and get <span class='t'>some</span> jam.", "<span class='t'>Who said</span> that?", "<span class='t'>We are all</span> here!"]
    h += "<h2><span class='n'>★</span>Read the sentences — spot the tricky words</h2><div class='sent'>" + "".join(f"<div>{s}<span class='tick'></span></div>" for s in sents) + "</div>"
    cut = "".join(f"<div style='font-size:30pt'>{w}</div>" for s in TRICKY for w in s)
    h += f"<div class='page'></div><h2><span class='n'>✂️</span>Tricky word cards — cut out, play snap or memory</h2><div class='cut'>{cut}</div>"
    return h

if __name__ == "__main__":
    out = "static/downloads/phonics/"
    for pack, (fn, name) in enumerate(((pack1, "1-Letter-Sounds"), (pack2, "2-Letter-Formation"), (pack3, "3-Blending-Reading"),
                     (pack4, "4-Segmenting-Spelling"), (pack5, "5-Tricky-Words")), 1):
        build(number_sheets(fn(), pack), f"{out}familyenglish-phonics-{name.lower()}.pdf")
        print("built", name)
