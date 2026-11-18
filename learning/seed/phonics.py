"""Level 0: the 42 letter sounds, taught in the Jolly Phonics group order.

We follow the published teaching ORDER only. The actions, notes, word lists and
pictures below are FamilyEnglish's own; no Jolly Phonics images, songs or audio
are copied. Videos are linked from the official Alphablocks YouTube channel.
"""

# (key, shown, alphablocks search, our action idea, [(word, emoji, bangla), ...], extra Bangla tip)
GROUPS = [
    ("Group 1", "s a t i p n", [
        ("s", "s", "Alphablocks S", "Move your hand like a snake and hiss: sss",
         [("sun", "☀️", "সূর্য"), ("sock", "🧦", "মোজা"), ("six", "6️⃣", "ছয়")], ""),
        ("a", "a", "Alphablocks A", "Pretend ants run up your arm: a, a, a",
         [("ant", "🐜", "পিঁপড়া"), ("apple", "🍎", "আপেল"), ("bag", "👜", "ব্যাগ")],
         "'a' এখানে 'অ্যা' এর মতো ছোট শব্দ, 'এ' বা 'আ' নয়।"),
        ("t", "t", "Alphablocks T", "Turn your head left and right watching tennis: t, t, t",
         [("tap", "🚰", "কল"), ("ten", "🔟", "দশ"), ("cat", "🐱", "বিড়াল")],
         "ইংরেজি t জিভের ডগা দাঁতের পেছনের মাড়িতে লাগিয়ে বলে — বাংলা 'ত' নয়, 'ট' এর কাছাকাছি।"),
        ("i", "i", "Alphablocks I", "Wiggle your fingers like an insect: i, i, i",
         [("pin", "📌", "পিন"), ("insect", "🐛", "পোকা"), ("sit", "🪑", "বসা")], ""),
        ("p", "p", "Alphablocks P", "Puff out candles with your finger: p, p, p",
         [("pig", "🐷", "শূকর"), ("pan", "🍳", "কড়াই"), ("cup", "☕", "কাপ")],
         "p বলার সময় হালকা বাতাস বের হয় — হাতের তালু মুখের সামনে ধরে দেখুন।"),
        ("n", "n", "Alphablocks N", "Spread your arms like a plane: nnn",
         [("net", "🥅", "জাল"), ("nut", "🥜", "বাদাম"), ("nest", "🪺", "বাসা")], ""),
    ]),
    ("Group 2", "c/k e h r m d", [
        ("ck", "c / k", "Alphablocks C K", "Click two sticks (or fingers) together: c, c, c",
         [("cat", "🐱", "বিড়াল"), ("kite", "🪁", "ঘুড়ি"), ("cup", "☕", "কাপ")],
         "c আর k একই sound দেয় — /k/।"),
        ("e", "e", "Alphablocks E", "Crack an egg into a pan: e, e, e",
         [("egg", "🥚", "ডিম"), ("bed", "🛏️", "বিছানা"), ("hen", "🐔", "মুরগি")], ""),
        ("h", "h", "Alphablocks H", "Pant like you ran fast: h, h, h",
         [("hat", "👒", "টুপি"), ("hen", "🐔", "মুরগি"), ("hand", "✋", "হাত")], ""),
        ("r", "r", "Alphablocks R", "Shake your head like a puppy with a rag: rrr",
         [("red", "🔴", "লাল"), ("rat", "🐀", "ইঁদুর"), ("run", "🏃", "দৌড়ানো")],
         "ইংরেজি r এ জিভ মুখের ছাদে লাগে না — বাংলা 'র' এর মতো কম্পন হয় না।"),
        ("m", "m", "Alphablocks M", "Rub your tummy, food is tasty: mmm",
         [("man", "👨", "লোক"), ("map", "🗺️", "মানচিত্র"), ("mug", "🍵", "মগ")], ""),
        ("d", "d", "Alphablocks D", "Beat a drum with both hands: d, d, d",
         [("dog", "🐶", "কুকুর"), ("duck", "🦆", "হাঁস"), ("bed", "🛏️", "বিছানা")],
         "ইংরেজি d বাংলা 'ড' এর কাছাকাছি, 'দ' নয়।"),
    ]),
    ("Group 3", "g o u l f b", [
        ("g", "g", "Alphablocks G", "Gulp water from a glass: g, g, g",
         [("goat", "🐐", "ছাগল"), ("bag", "👜", "ব্যাগ"), ("gift", "🎁", "উপহার")], ""),
        ("o", "o", "Alphablocks O", "Switch a light on and off: o, o, o",
         [("dog", "🐶", "কুকুর"), ("pot", "🍲", "হাঁড়ি"), ("box", "📦", "বাক্স")], ""),
        ("u", "u", "Alphablocks U", "Open an umbrella above your head: u, u, u",
         [("up", "⬆️", "উপরে"), ("bus", "🚌", "বাস"), ("sun", "☀️", "সূর্য")],
         "'u' এখানে ছোট 'আ' এর মতো (up = আপ), 'উ' নয়।"),
        ("l", "l", "Alphablocks L", "Lick a lollipop: lll",
         [("leg", "🦵", "পা"), ("lamp", "💡", "বাতি"), ("log", "🪵", "কাঠের গুঁড়ি")], ""),
        ("f", "f", "Alphablocks F", "Let air out of a balloon, top teeth on bottom lip: fff",
         [("fan", "🪭", "পাখা"), ("fish", "🐟", "মাছ"), ("frog", "🐸", "ব্যাঙ")],
         "f বলার সময় উপরের দাঁত নিচের ঠোঁটে লাগবে — 'ফ' এর মতো দুই ঠোঁট নয়।"),
        ("b", "b", "Alphablocks B", "Bounce a ball: b, b, b",
         [("bus", "🚌", "বাস"), ("bat", "🦇", "বাদুড়"), ("bed", "🛏️", "বিছানা")], ""),
    ]),
    ("Group 4", "ai j oa ie ee or", [
        ("ai", "ai", "Alphablocks AI", "Cup your hand to your ear: ai? (say it)",
         [("rain", "🌧️", "বৃষ্টি"), ("snail", "🐌", "শামুক"), ("train", "🚆", "ট্রেন")],
         "দুটি letter মিলে একটি sound — 'এই'।"),
        ("j", "j", "Alphablocks J", "Wobble like jelly on a plate: j, j, j",
         [("jam", "🍯", "জ্যাম"), ("jet", "✈️", "জেট বিমান"), ("jug", "🫖", "জগ")], ""),
        ("oa", "oa", "Alphablocks OA", "Cover your mouth: oh! (say it)",
         [("boat", "⛵", "নৌকা"), ("goat", "🐐", "ছাগল"), ("coat", "🧥", "কোট")], ""),
        ("ie", "ie", "Alphablocks IE", "Salute like a soldier: ie! (say it)",
         [("pie", "🥧", "পাই"), ("tie", "👔", "টাই"), ("lie", "🛌", "শোয়া")], ""),
        ("ee", "ee", "Alphablocks EE", "Make donkey ears with your hands: ee-or",
         [("bee", "🐝", "মৌমাছি"), ("tree", "🌳", "গাছ"), ("feet", "🦶", "পা")],
         "লম্বা 'ঈ' — ছোট i (sit) থেকে আলাদা।"),
        ("or", "or", "Alphablocks OR", "Same donkey ears: ee-OR",
         [("fork", "🍴", "কাঁটাচামচ"), ("corn", "🌽", "ভুট্টা"), ("horn", "📯", "শিং")], ""),
    ]),
    ("Group 5", "z w ng v oo oo", [
        ("z", "z", "Alphablocks Z", "Flap your arms like a buzzing bee: zzz",
         [("zip", "🤐", "চেইন"), ("zoo", "🦓", "চিড়িয়াখানা"), ("buzz", "🐝", "গুনগুন")],
         "z বাংলা 'জ' নয় — মৌমাছির মতো 'জ্‌জ্‌জ্‌' কাঁপা শব্দ।"),
        ("w", "w", "Alphablocks W", "Round your lips and blow wind: w, w, w",
         [("web", "🕸️", "জাল"), ("wet", "💧", "ভেজা"), ("wind", "🌬️", "বাতাস")],
         "w-তে ঠোঁট গোল হবে, দাঁত ঠোঁটে লাগবে না (v থেকে আলাদা)।"),
        ("ng", "ng", "Alphablocks NG", "Lift weights above your head: nnng",
         [("ring", "💍", "আংটি"), ("king", "🤴", "রাজা"), ("sing", "🎤", "গান গাওয়া")],
         "বাংলা 'ং' এর মতো — g আলাদা করে বলবেন না।"),
        ("v", "v", "Alphablocks V", "Drive a van with a steering wheel: vvv",
         [("van", "🚐", "ভ্যান"), ("vet", "🩺", "পশু ডাক্তার"), ("vest", "🦺", "জ্যাকেট")],
         "v-তে উপরের দাঁত নিচের ঠোঁটে লাগে এবং কণ্ঠ কাঁপে। 'ভ' নয়।"),
        ("oo_long", "oo (moon)", "Alphablocks OO", "Move your head like a cuckoo: OO",
         [("moon", "🌙", "চাঁদ"), ("food", "🍲", "খাবার"), ("spoon", "🥄", "চামচ")],
         "লম্বা 'উ' — moon।"),
        ("oo_short", "oo (book)", "Alphablocks OO book", "Same cuckoo, short: oo",
         [("book", "📖", "বই"), ("cook", "👩‍🍳", "রান্না"), ("foot", "🦶", "পা")],
         "ছোট 'উ' — book। একই oo দুইভাবে পড়া যায়।"),
    ]),
    ("Group 6", "y x ch sh th th", [
        ("y", "y", "Alphablocks Y", "Eat a yummy yoghurt with a spoon: y, y, y",
         [("yes", "✅", "হ্যাঁ"), ("yak", "🐃", "চমরী গাই"), ("yell", "📣", "চিৎকার")], ""),
        ("x", "x", "Alphablocks X", "Pretend to take an x-ray with a camera: ks, ks",
         [("box", "📦", "বাক্স"), ("fox", "🦊", "শিয়াল"), ("six", "6️⃣", "ছয়")],
         "x = 'ক্স' দুটি sound মিলে।"),
        ("ch", "ch", "Alphablocks CH", "Move your arms like a train: ch, ch, ch",
         [("chip", "🍟", "চিপস"), ("chick", "🐥", "মুরগির ছানা"), ("chin", "🧔", "থুতনি")], ""),
        ("sh", "sh", "Alphablocks SH", "Finger on lips, baby is sleeping: shh",
         [("ship", "🚢", "জাহাজ"), ("fish", "🐟", "মাছ"), ("shop", "🏪", "দোকান")],
         "'শ' এর মতো, কিন্তু ঠোঁট একটু সামনে আসে।"),
        ("th_voiced", "th (this)", "Alphablocks TH", "Tongue out a little, voice on: th (this)",
         [("this", "👉", "এটা"), ("that", "👈", "ওটা"), ("mother", "👩", "মা")],
         "জিভের ডগা দুই দাঁতের মাঝে রাখুন, কণ্ঠ কাঁপবে। 'দ' বা 'ড' নয়।"),
        ("th_unvoiced", "th (thin)", "Alphablocks TH thin", "Tongue out a little, just air: th (thin)",
         [("thumb", "👍", "বুড়ো আঙুল"), ("three", "3️⃣", "তিন"), ("thin", "📏", "পাতলা")],
         "জিভ দুই দাঁতের মাঝে, শুধু বাতাস — 'থ' বা 'ট' নয়।"),
    ]),
    ("Group 7", "qu ou oi ue er ar", [
        ("qu", "qu", "Alphablocks QU", "Quack like a duck with your hands: kw, kw",
         [("queen", "👸", "রানি"), ("quick", "⚡", "দ্রুত"), ("quilt", "🛏️", "কাঁথা")],
         "qu = 'কো' + 'w' মিলে 'কুয়'।"),
        ("ou", "ou", "Alphablocks OU", "Pretend your thumb got pricked: ou!",
         [("out", "🚪", "বাইরে"), ("cloud", "☁️", "মেঘ"), ("mouth", "👄", "মুখ")], ""),
        ("oi", "oi", "Alphablocks OI", "Cup hands round your mouth and call a ship: oi!",
         [("oil", "🛢️", "তেল"), ("coin", "🪙", "কয়েন"), ("boil", "♨️", "ফোটানো")], ""),
        ("ue", "ue", "Alphablocks UE", "Point to people around you: you, you",
         [("rescue", "🛟", "উদ্ধার"), ("statue", "🗽", "মূর্তি"), ("cue", "🎱", "সংকেত")], ""),
        ("er", "er", "Alphablocks ER", "Stir a pot with both hands: er, er",
         [("her", "👧", "তার (মেয়ে)"), ("sister", "👭", "বোন"), ("letter", "✉️", "চিঠি")],
         "শেষের r সাধারণত উচ্চারণ হয় না (British): sis-tuh।"),
        ("ar", "ar", "Alphablocks AR", "Open wide like at the doctor: ar",
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
