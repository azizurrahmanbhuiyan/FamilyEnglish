"""Level 0: the 42 letter sounds, taught in the Jolly Phonics group order.

We follow the published teaching ORDER only. The actions, notes, word lists and
pictures below are FamilyEnglish's own; no Jolly Phonics images, songs or audio
are copied. Videos are linked from the official Alphablocks YouTube channel.
"""

# (key, shown, alphablocks search, our action idea, [(word, emoji, bangla), ...], extra Bangla tip)
GROUPS = [
    ("Group 1", "s a t i p n", [
        ("s", "s", "Alphablocks S", "Air leaks from a bicycle tyre — move your hand down slowly: sss",
         [("sun", "☀️", "সূর্য"), ("sock", "🧦", "মোজা"), ("six", "6️⃣", "ছয়")], ""),
        ("a", "a", "Alphablocks A", "Bite a big apple with your mouth wide open: a, a, a",
         [("ant", "🐜", "পিঁপড়া"), ("apple", "🍎", "আপেল"), ("bag", "👜", "ব্যাগ")],
         "'a' এখানে 'অ্যা' এর মতো ছোট শব্দ, 'এ' বা 'আ' নয়।"),
        ("t", "t", "Alphablocks T", "Tap the table with one finger: t, t, t",
         [("tap", "🚰", "কল"), ("ten", "🔟", "দশ"), ("cat", "🐱", "বিড়াল")],
         "ইংরেজি t জিভের ডগা দাঁতের পেছনের মাড়িতে লাগিয়ে বলে — বাংলা 'ত' নয়, 'ট' এর কাছাকাছি।"),
        ("i", "i", "Alphablocks I", "Scratch an itchy arm: i, i, i",
         [("pin", "📌", "পিন"), ("insect", "🐛", "পোকা"), ("sit", "🪑", "বসা")], ""),
        ("p", "p", "Alphablocks P", "Pop a balloon with a clap: p!",
         [("pig", "🐷", "শূকর"), ("pan", "🍳", "কড়াই"), ("cup", "☕", "কাপ")],
         "p বলার সময় হালকা বাতাস বের হয় — হাতের তালু মুখের সামনে ধরে দেখুন।"),
        ("n", "n", "Alphablocks N", "Shake your head for 'no': nnn",
         [("net", "🥅", "জাল"), ("nut", "🥜", "বাদাম"), ("nest", "🪺", "বাসা")], ""),
    ]),
    ("Group 2", "c/k e h r m d", [
        ("ck", "c / k", "Alphablocks C K", "Knock on a door: k, k, k",
         [("cat", "🐱", "বিড়াল"), ("kite", "🪁", "ঘুড়ি"), ("cup", "☕", "কাপ")],
         "c আর k একই sound দেয় — /k/।"),
        ("e", "e", "Alphablocks E", "Tap your elbow: e, e, e",
         [("egg", "🥚", "ডিম"), ("bed", "🛏️", "বিছানা"), ("hen", "🐔", "মুরগি")], ""),
        ("h", "h", "Alphablocks H", "Fan your hot face with your hand: h, h, h",
         [("hat", "👒", "টুপি"), ("hen", "🐔", "মুরগি"), ("hand", "✋", "হাত")], ""),
        ("r", "r", "Alphablocks R", "Pedal a rickshaw with your hands: rrr",
         [("red", "🔴", "লাল"), ("rat", "🐀", "ইঁদুর"), ("run", "🏃", "দৌড়ানো")],
         "ইংরেজি r এ জিভ মুখের ছাদে লাগে না — বাংলা 'র' এর মতো কম্পন হয় না।"),
        ("m", "m", "Alphablocks M", "Hum with your lips closed, hand on your cheek: mmm",
         [("man", "👨", "লোক"), ("map", "🗺️", "মানচিত্র"), ("mug", "🍵", "মগ")], ""),
        ("d", "d", "Alphablocks D", "Dig in the sand with a spade: d, d, d",
         [("dog", "🐶", "কুকুর"), ("duck", "🦆", "হাঁস"), ("bed", "🛏️", "বিছানা")],
         "ইংরেজি d বাংলা 'ড' এর কাছাকাছি, 'দ' নয়।"),
    ]),
    ("Group 3", "g o u l f b", [
        ("g", "g", "Alphablocks G", "Gargle water, hand on your throat: g, g, g",
         [("goat", "🐐", "ছাগল"), ("bag", "👜", "ব্যাগ"), ("gift", "🎁", "উপহার")], ""),
        ("o", "o", "Alphablocks O", "Open and close a box lid: o, o, o",
         [("dog", "🐶", "কুকুর"), ("pot", "🍲", "হাঁড়ি"), ("box", "📦", "বাক্স")], ""),
        ("u", "u", "Alphablocks U", "Point up, up, up: u, u, u",
         [("up", "⬆️", "উপরে"), ("bus", "🚌", "বাস"), ("sun", "☀️", "সূর্য")],
         "'u' এখানে ছোট 'আ' এর মতো (up = আপ), 'উ' নয়।"),
        ("l", "l", "Alphablocks L", "Lift a little bag with both hands: lll",
         [("leg", "🦵", "পা"), ("lamp", "💡", "বাতি"), ("log", "🪵", "কাঠের গুঁড়ি")], ""),
        ("f", "f", "Alphablocks F", "Wave a hand fan at your face: fff",
         [("fan", "🪭", "পাখা"), ("fish", "🐟", "মাছ"), ("frog", "🐸", "ব্যাঙ")],
         "f বলার সময় উপরের দাঁত নিচের ঠোঁটে লাগবে — 'ফ' এর মতো দুই ঠোঁট নয়।"),
        ("b", "b", "Alphablocks B", "Bite a banana: b, b, b",
         [("bus", "🚌", "বাস"), ("bat", "🦇", "বাদুড়"), ("bed", "🛏️", "বিছানা")], ""),
    ]),
    ("Group 4", "ai j oa ie ee or", [
        ("ai", "ai", "Alphablocks AI", "Let rain fall from your fingers: ai",
         [("rain", "🌧️", "বৃষ্টি"), ("snail", "🐌", "শামুক"), ("train", "🚆", "ট্রেন")],
         "দুটি letter মিলে একটি sound — 'এই'।"),
        ("j", "j", "Alphablocks J", "Jump up and down: j, j, j",
         [("jam", "🍯", "জ্যাম"), ("jet", "✈️", "জেট বিমান"), ("jug", "🫖", "জগ")], ""),
        ("oa", "oa", "Alphablocks OA", "Row a boat with two oars: oa, oa",
         [("boat", "⛵", "নৌকা"), ("goat", "🐐", "ছাগল"), ("coat", "🧥", "কোট")], ""),
        ("ie", "ie", "Alphablocks IE", "Tie a shoelace and pull the bow tight: ie!",
         [("pie", "🥧", "পাই"), ("tie", "👔", "টাই"), ("lie", "🛌", "শোয়া")], ""),
        ("ee", "ee", "Alphablocks EE", "Show your teeth in a big smile: ee",
         [("bee", "🐝", "মৌমাছি"), ("tree", "🌳", "গাছ"), ("feet", "🦶", "পা")],
         "লম্বা 'ঈ' — ছোট i (sit) থেকে আলাদা।"),
        ("or", "or", "Alphablocks OR", "Point down to the floor: or",
         [("fork", "🍴", "কাঁটাচামচ"), ("corn", "🌽", "ভুট্টা"), ("horn", "📯", "শিং")], ""),
    ]),
    ("Group 5", "z w ng v oo oo", [
        ("z", "z", "Alphablocks Z", "Zip up a jacket: zzz",
         [("zip", "🤐", "চেইন"), ("zoo", "🦓", "চিড়িয়াখানা"), ("buzz", "🐝", "গুনগুন")],
         "z বাংলা 'জ' নয় — মৌমাছির মতো 'জ্‌জ্‌জ্‌' কাঁপা শব্দ।"),
        ("w", "w", "Alphablocks W", "Wave hello: w, w, w",
         [("web", "🕸️", "জাল"), ("wet", "💧", "ভেজা"), ("wind", "🌬️", "বাতাস")],
         "w-তে ঠোঁট গোল হবে, দাঁত ঠোঁটে লাগবে না (v থেকে আলাদা)।"),
        ("ng", "ng", "Alphablocks NG", "Swing a bell from side to side: ng, ng",
         [("ring", "💍", "আংটি"), ("king", "🤴", "রাজা"), ("sing", "🎤", "গান গাওয়া")],
         "বাংলা 'ং' এর মতো — g আলাদা করে বলবেন না।"),
        ("v", "v", "Alphablocks V", "Make a V with two fingers: vvv",
         [("van", "🚐", "ভ্যান"), ("vet", "🩺", "পশু ডাক্তার"), ("vest", "🦺", "জ্যাকেট")],
         "v-তে উপরের দাঁত নিচের ঠোঁটে লাগে এবং কণ্ঠ কাঁপে। 'ভ' নয়।"),
        ("oo_long", "oo (moon)", "Alphablocks OO", "Point up at the moon: oo",
         [("moon", "🌙", "চাঁদ"), ("food", "🍲", "খাবার"), ("spoon", "🥄", "চামচ")],
         "লম্বা 'উ' — moon।"),
        ("oo_short", "oo (book)", "Alphablocks OO book", "Open a book and look inside: oo",
         [("book", "📖", "বই"), ("cook", "👩‍🍳", "রান্না"), ("foot", "🦶", "পা")],
         "ছোট 'উ' — book। একই oo দুইভাবে পড়া যায়।"),
    ]),
    ("Group 6", "y x ch sh th th", [
        ("y", "y", "Alphablocks Y", "Nod your head for 'yes': y, y, y",
         [("yes", "✅", "হ্যাঁ"), ("yak", "🐃", "চমরী গাই"), ("yell", "📣", "চিৎকার")], ""),
        ("x", "x", "Alphablocks X", "Cross your arms in an X: ks, ks",
         [("box", "📦", "বাক্স"), ("fox", "🦊", "শিয়াল"), ("six", "6️⃣", "ছয়")],
         "x = 'ক্স' দুটি sound মিলে।"),
        ("ch", "ch", "Alphablocks CH", "Sneeze into your elbow: ch!",
         [("chip", "🍟", "চিপস"), ("chick", "🐥", "মুরগির ছানা"), ("chin", "🧔", "থুতনি")], ""),
        ("sh", "sh", "Alphablocks SH", "Move your arms like sea waves at the beach: shhh",
         [("ship", "🚢", "জাহাজ"), ("fish", "🐟", "মাছ"), ("shop", "🏪", "দোকান")],
         "'শ' এর মতো, কিন্তু ঠোঁট একটু সামনে আসে।"),
        ("th_voiced", "th (this)", "Alphablocks TH", "Point at that thing over there, tongue between your teeth: th",
         [("this", "👉", "এটা"), ("that", "👈", "ওটা"), ("mother", "👩", "মা")],
         "জিভের ডগা দুই দাঁতের মাঝে রাখুন, কণ্ঠ কাঁপবে। 'দ' বা 'ড' নয়।"),
        ("th_unvoiced", "th (thin)", "Alphablocks TH thin", "Show three fingers, tongue out a little, just air: th",
         [("thumb", "👍", "বুড়ো আঙুল"), ("three", "3️⃣", "তিন"), ("thin", "📏", "পাতলা")],
         "জিভ দুই দাঁতের মাঝে, শুধু বাতাস — 'থ' বা 'ট' নয়।"),
    ]),
    ("Group 7", "qu ou oi ue er ar", [
        ("qu", "qu", "Alphablocks QU", "Shiver quickly, hugging yourself: kw, kw",
         [("queen", "👸", "রানি"), ("quick", "⚡", "দ্রুত"), ("quilt", "🛏️", "কাঁথা")],
         "qu = 'কো' + 'w' মিলে 'কুয়'।"),
        ("ou", "ou", "Alphablocks OU", "Point out of the window: ou!",
         [("out", "🚪", "বাইরে"), ("cloud", "☁️", "মেঘ"), ("mouth", "👄", "মুখ")], ""),
        ("oi", "oi", "Alphablocks OI", "Hold up a shiny coin you found: oi!",
         [("oil", "🛢️", "তেল"), ("coin", "🪙", "কয়েন"), ("boil", "♨️", "ফোটানো")], ""),
        ("ue", "ue", "Alphablocks UE", "Draw a U shape in the air: ue",
         [("rescue", "🛟", "উদ্ধার"), ("statue", "🗽", "মূর্তি"), ("cue", "🎱", "সংকেত")], ""),
        ("er", "er", "Alphablocks ER", "Scratch your head, thinking: er…",
         [("her", "👧", "তার (মেয়ে)"), ("sister", "👭", "বোন"), ("letter", "✉️", "চিঠি")],
         "শেষের r সাধারণত উচ্চারণ হয় না (British): sis-tuh।"),
        ("ar", "ar", "Alphablocks AR", "Point to a star in the sky: ar",
         [("car", "🚗", "গাড়ি"), ("star", "⭐", "তারা"), ("jar", "🫙", "বয়াম")], ""),
    ]),
]


def note_bn(shown, tip):
    base = (
        f"আজকের sound: **/{shown}/**। শিশুকে letter-এর নাম নয়, sound টা শেখান — "
        f"যেমন s এর নাম 'এস' কিন্তু sound 'স্‌স্‌স্‌'।\n\n"
        "ভিডিওটি একসাথে দেখুন, তারপর action করে sound টা ৩ বার বলুন। "
        "শিশু ভুল বললে ঠিক করে দিন, কিন্তু বকবেন না — খেলার মতো রাখুন।"
    )
    if tip:
        base += f"\n\n**বাংলাভাষীদের জন্য টিপ:** {tip}"
    return base


def home_task_bn(words):
    w = ", ".join(x[0] for x in words)
    return (f"আজ বাসায় ৩টি জিনিস খুঁজুন যেগুলোর নামে এই sound আছে (যেমন: {w})। "
            "শিশু জিনিসটা ধরবে আর sound টা বলবে।")
