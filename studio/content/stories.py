"""Short stories for shadowing (listen, copy, record), written by FamilyEnglish.

Two are our own retellings of old fables (Aesop, public domain); the rest are original FamilyEnglish stories.
Each line: (English, Bangla, note). The note shows what to copy: ‿ = link the words, (ə) = weak form,
CAPITALS = the strong word, ↗ ↘ = the tune.
vocab: (word, meaning in simple English, Bangla). quiz: fill-the-gap items in the grammar practice format.
"""


def S(slug, level, emoji, title, title_bn, lines, vocab, quiz, focus):
    return {"slug": slug, "level": level, "emoji": emoji, "title": title, "title_bn": title_bn,
            "lines": lines, "vocab": vocab, "quiz": quiz, "focus": focus}


STORIES = [
    S("lost-kite", "A1", "🪁", "The Lost Kite", "হারানো ঘুড়ি", [
        ("Tara has a red kite.", "তারার একটা লাল ঘুড়ি আছে।", "has‿a · RED KITE"),
        ("She flies it in the field every evening.", "সে প্রতি সন্ধ্যায় মাঠে ঘুড়ি ওড়ায়।", "flies‿it‿on · EVERY EVENING"),
        ("One day the wind is very strong.", "একদিন বাতাস খুব জোরালো।", "VERY STRONG ↘"),
        ("The string breaks and the kite flies away.", "সুতো ছিঁড়ে যায় আর ঘুড়িটা উড়ে চলে যায়।", "breaks‿and (ən) · flies‿away (j)"),
        ("Tara runs across the field and looks for it.", "তারা মাঠের ওপারে দৌড়ে গিয়ে ঘুড়িটা খোঁজে।", "runs‿across · looks‿for‿it (fə)"),
        ("A little boy is holding it in the garden.", "ছোট্ট একটা ছেলে বাগানে সেটা ধরে আছে।", "holding‿it‿in"),
        ("'Is this your kite?' he asks with a smile.", "'এটা কি তোমার ঘুড়ি?' সে হেসে জিজ্ঞেস করে।", "Is this your KITE ↗"),
        ("Now they fly it together.", "এখন তারা একসাথে ঘুড়ি ওড়ায়।", "fly‿it (j) · toGETHer"),
    ], [("kite", "a toy that flies in the wind on a string", "ঘুড়ি"), ("field", "a big open area of grass", "মাঠ"),
        ("string", "a long, thin thread", "সুতো"), ("across", "from one side to the other", "এপার থেকে ওপারে"),
        ("together", "with each other", "একসাথে")],
      [("fill", "Tara's kite is ___.", ["red"]), ("fill", "The ___ breaks and the kite flies away.", ["string"]),
       ("fill", "She flies the kite in the ___.", ["field"]), ("fill", "At the end they fly it ___.", ["together"])],
      "Linking: consonant + vowel"),

    S("tortoise-hare", "A2", "🐢", "The Tortoise and the Hare", "কচ্ছপ আর খরগোশ", [
        ("A hare liked to laugh at a slow tortoise.", "একটা খরগোশ ধীর এক কচ্ছপকে নিয়ে হাসাহাসি করতে ভালোবাসত।", "liked‿to (tə) · laugh‿at · SLOW"),
        ("'You are the slowest animal in the forest,' he said.", "'তুমি বনের সবচেয়ে ধীর প্রাণী,' সে বলল।", "slowest‿animal‿in · FOREST ↘"),
        ("The tortoise smiled and said, 'Let's have a race.'", "কচ্ছপ হেসে বলল, 'চলো দৌড় প্রতিযোগিতা করি।'", "smiled‿and (ən) · have‿a RACE"),
        ("The hare ran so fast that he was soon far ahead.", "খরগোশ এত জোরে দৌড়াল যে শিগগিরই অনেক এগিয়ে গেল।", "was (wəz) · far‿ahead (linking r)"),
        ("He felt so sure of winning that he lay down for a nap.", "জেতার ব্যাপারে এত নিশ্চিত ছিল যে সে একটু ঘুমিয়ে নিতে শুয়ে পড়ল।", "sure‿of (əv) · for‿a (fər‿ə)"),
        ("The tortoise kept walking, step by step.", "কচ্ছপ হাঁটতেই থাকল, এক পা এক পা করে।", "kept walking (t disappears) · STEP by STEP"),
        ("By the time the hare opened his eyes, the tortoise was crossing the finish line.", "খরগোশ যখন চোখ খুলল, কচ্ছপ তখন শেষ সীমা পার হচ্ছে।", "opened‿his (z‿ɪ) · his‿eyes · FINISH line"),
        ("Slow and steady wins the race.", "ধীরে কিন্তু অবিচলভাবে চললে জয় আসে।", "SLOW and (ən) STEADY ↘"),
    ], [("hare", "an animal like a big rabbit with long ears", "খরগোশ (বড়)"), ("tortoise", "a slow animal with a hard shell", "কচ্ছপ"),
        ("race", "a competition to see who is fastest", "দৌড় প্রতিযোগিতা"), ("nap", "a short sleep in the day", "ছোট ঘুম"),
        ("steady", "not changing; calm and regular", "অবিচল")],
      [("fill", "The ___ laughed at the tortoise.", ["hare"]), ("fill", "The hare lay down for a ___.", ["nap"]),
       ("fill", "The tortoise kept walking, step by ___.", ["step"]), ("fill", "Slow and ___ wins the race.", ["steady"])],
      "Weak forms and linking r"),

    S("rainy-bus-stop", "A2", "🌧️", "Rain at the Bus Stop", "বাসস্টপে বৃষ্টি", [
        ("It started to rain while Karim was waiting for the bus.", "করিম বাসের জন্য অপেক্ষা করার সময় বৃষ্টি শুরু হলো।", "started‿to (tə) · waiting‿for (fə)"),
        ("He didn't have an umbrella.", "তার কাছে ছাতা ছিল না।", "have‿an‿umbrella"),
        ("An old woman stood next to him under a small roof.", "এক বৃদ্ধা ছোট একটা ছাউনির নিচে তার পাশে দাঁড়িয়ে ছিলেন।", "An‿old · next to (t disappears)"),
        ("'Would you like to share my umbrella?' she asked.", "'আমার ছাতাটা ভাগাভাগি করবে?' তিনি জিজ্ঞেস করলেন।", "Would you (wudju) · share‿my ↗"),
        ("They talked about the weather and their families.", "তারা আবহাওয়া আর নিজেদের পরিবার নিয়ে কথা বলল।", "talked‿about · and their (ən ðeə)"),
        ("When the bus came, Karim helped her get on.", "বাস এলে করিম তাঁকে উঠতে সাহায্য করল।", "helped her (helpt‿ə) · get‿on"),
        ("A kind word can make a wet day warm.", "একটা দয়ালু কথা ভেজা দিনকেও উষ্ণ করে দিতে পারে।", "KIND word · WET day WARM ↘"),
    ], [("umbrella", "you hold it over your head in the rain", "ছাতা"), ("share", "use something together", "ভাগাভাগি করা"),
        ("weather", "rain, sun, wind, heat and cold", "আবহাওয়া"), ("wet", "covered with water", "ভেজা"),
        ("kind", "friendly and helpful", "দয়ালু")],
      [("fill", "Karim was waiting for the ___.", ["bus"]), ("fill", "He didn't have an ___.", ["umbrella"]),
       ("fill", "They talked about the ___ and their families.", ["weather"]), ("fill", "A ___ word can make a wet day warm.", ["kind"])],
      "Weak forms: to, for, and"),

    S("boy-who-cried-wolf", "A2", "🐺", "The Boy Who Cried Wolf", "যে ছেলেটি 'নেকড়ে' বলে চেঁচাত", [
        ("Long ago, a young shepherd took his sheep to the hills every day.", "অনেক দিন আগে এক তরুণ রাখাল প্রতিদিন তার ভেড়াগুলো পাহাড়ে নিয়ে যেত।", "Long‿ago · took‿his · to (tə) the HILLS"),
        ("He was bored, so he shouted, 'Wolf! Wolf!'", "তার একঘেয়ে লাগছিল, তাই সে চেঁচাল, 'নেকড়ে! নেকড়ে!'", "was (wəz) · WOLF ↘ WOLF ↘"),
        ("The villagers ran up the hill to help him.", "গ্রামবাসীরা তাকে বাঁচাতে পাহাড়ে দৌড়ে এল।", "ran‿up · to (tə) help‿him (help‿im)"),
        ("There was no wolf, and the boy laughed at them.", "কোনো নেকড়ে ছিল না, আর ছেলেটা তাদের দেখে হাসল।", "and (ən) · laughed‿at‿them (əm)"),
        ("He played the same trick again the next week.", "পরের সপ্তাহে সে আবার একই চালাকি করল।", "played the (d disappears) · trick‿again"),
        ("Then one evening a real wolf came out of the forest.", "তারপর এক সন্ধ্যায় সত্যিকারের এক নেকড়ে বন থেকে বেরিয়ে এল।", "came‿out‿of (əv) · REAL wolf"),
        ("He cried for help, but nobody believed him.", "সে সাহায্যের জন্য চেঁচাল, কিন্তু কেউ বিশ্বাস করল না।", "cried for (fə) · NObody beLIEVED him ↘"),
        ("If you tell lies, people won't trust you when you tell the truth.", "মিথ্যা বললে, সত্যি বললেও মানুষ তোমাকে বিশ্বাস করবে না।", "tell lies↗ · won't trust you (tʃu) ↘"),
    ], [("shepherd", "a person who looks after sheep", "রাখাল"), ("bored", "not interested; nothing to do", "একঘেয়েমিতে ক্লান্ত"),
        ("villager", "a person who lives in a village", "গ্রামবাসী"), ("trick", "something you do to fool people", "চালাকি"),
        ("trust", "believe that someone is honest", "বিশ্বাস করা")],
      [("fill", "The boy took his ___ to the hills.", ["sheep"]), ("fill", "He shouted '___!' but there was none.", ["wolf"]),
       ("fill", "Later, nobody ___ him.", ["believed"]), ("fill", "If you tell lies, people won't ___ you.", ["trust"])],
      "Weak forms and sounds that disappear"),

    S("mango-tree", "A2", "🥭", "Grandma's Mango Tree", "দাদির আমগাছ", [
        ("There is an old mango tree behind Grandma's house.", "দাদির বাড়ির পেছনে একটা পুরোনো আমগাছ আছে।", "There‿is (linking r) · an‿old"),
        ("Every summer it is full of sweet yellow mangoes.", "প্রতি গ্রীষ্মে গাছটা মিষ্টি হলুদ আমে ভরে যায়।", "full‿of (əv) · SWEET YELLOW"),
        ("Grandpa picks the ripe ones with a long pole, and the children catch them in a basket.", "দাদা লম্বা লাঠি দিয়ে পাকা আম পাড়েন, আর বাচ্চারা ঝুড়িতে ধরে।", "picks the · catch‿them · pick the RIPE ones"),
        ("Grandma makes pickles and sends them to the whole family.", "দাদি আচার বানান আর পুরো পরিবারে পাঠান।", "makes pickles · sends them (əm) to (tə)"),
        ("She planted the tree on the day my father was born.", "বাবা যেদিন জন্মেছিলেন, সেদিন দাদি গাছটা লাগিয়েছিলেন।", "planted the (ɪd) · was (wəz) BORN"),
        ("Now it is older than all of us, except Grandma!", "এখন গাছটা আমাদের সবার চেয়ে বড়, দাদি ছাড়া!", "older than (ðən) · all‿of‿us · exCEPT GRANDma ↘"),
    ], [("ripe", "ready to eat", "পাকা"), ("pickle", "fruit kept in oil, salt and spices", "আচার"),
        ("plant", "put a seed or young tree in the ground", "রোপণ করা"), ("whole", "all of it", "পুরো"),
        ("except", "but not", "ছাড়া")],
      [("fill", "The tree is behind ___'s house.", ["grandma", "grandma's"]), ("fill", "The children pick the ___ mangoes.", ["ripe"]),
       ("fill", "Grandma makes ___.", ["pickles"]), ("fill", "The tree is older than everyone ___ Grandma.", ["except"])],
      "-ed endings and silent letters"),

    S("secret-letter", "B1", "✉️", "The Secret Letter", "গোপন চিঠি", [
        ("While cleaning the cupboard, Nadia found an old envelope.", "আলমারি পরিষ্কার করতে গিয়ে নাদিয়া একটা পুরোনো খাম পেল।", "found‿an‿old · CUPboard (p silent)"),
        ("Inside was a letter her grandfather had written in 1971.", "ভেতরে একটা চিঠি ছিল, যা তার দাদা ১৯৭১ সালে লিখেছিলেন।", "Inside was‿a · had (əd) written"),
        ("The paper was yellow and the ink had faded.", "কাগজটা হলুদ হয়ে গিয়েছিল আর কালি ফিকে হয়ে গিয়েছিল।", "and the (ən ðə) · had faded (ɪd)"),
        ("He wrote about hope, courage and a family waiting for him.", "তিনি আশা, সাহস আর তাঁর অপেক্ষায় থাকা পরিবারের কথা লিখেছিলেন।", "HOPE↗ COURage↗ and a FAMily↘ · waiting for (fə)"),
        ("Nadia read it aloud to her mother.", "নাদিয়া মাকে চিঠিটা জোরে পড়ে শোনাল।", "read‿it‿aloud (d‿ɪ‿t‿ə) · to her (tə hə)"),
        ("Neither of them spoke for a long time.", "অনেকক্ষণ দুজনের কেউই কথা বলল না।", "Neither‿of (r‿əv) · for‿a LONG time"),
        ("Then her mother smiled and said, 'Now you know where your courage comes from.'", "তারপর মা হেসে বললেন, 'এখন তুমি জানো তোমার সাহস কোথা থেকে এসেছে।'", "smiled‿and · NOW you KNOW ↘"),
    ], [("envelope", "a paper cover for a letter", "খাম"), ("faded", "lost its colour", "ফিকে হয়ে যাওয়া"),
        ("courage", "being brave when something is hard", "সাহস"), ("aloud", "so others can hear", "জোরে (শুনিয়ে)"),
        ("neither", "not one and not the other", "দুজনের কেউই না")],
      [("fill", "Nadia found an old ___ in the cupboard.", ["envelope"]), ("fill", "The ink had ___.", ["faded"]),
       ("fill", "The letter was about hope, ___ and family.", ["courage"]), ("fill", "Nadia read it ___ to her mother.", ["aloud"])],
      "List intonation and weak forms"),

    S("night-train", "B1", "🚆", "The Night Train to Sylhet", "সিলেটের রাতের ট্রেন", [
        ("The night train to Sylhet was late, as usual.", "সিলেটগামী রাতের ট্রেনটা যথারীতি দেরি করল।", "to (tə) · late‿as‿usual"),
        ("Rafi bought a cup of tea and sat on his suitcase.", "রাফি এক কাপ চা কিনে নিজের স্যুটকেসের ওপর বসল।", "cup‿of (əv) · sat‿on‿his"),
        ("Next to him, a girl was trying to read a map of the tea gardens.", "তার পাশে একটা মেয়ে চা-বাগানের মানচিত্র পড়ার চেষ্টা করছিল।", "Next to (nex tə) · map‿of"),
        ("'Are you going to Srimangal too?' he asked.", "'তুমিও কি শ্রীমঙ্গল যাচ্ছ?' সে জিজ্ঞেস করল।", "Are you going to (gonna in fast speech) · TOO ↗"),
        ("It turned out they were both students of the same teacher.", "দেখা গেল তারা দুজনই একই শিক্ষকের ছাত্র।", "turned‿out · were (wə) · SAME"),
        ("By the time the train arrived, they had planned a trip together.", "ট্রেন আসতে আসতে তারা একসাথে একটা ভ্রমণের পরিকল্পনা করে ফেলেছিল।", "By the time · had (əd) planned‿a"),
        ("Sometimes a late train brings you exactly where you need to be.", "কখনো কখনো দেরি করা ট্রেনও তোমাকে ঠিক যেখানে থাকা দরকার সেখানে নিয়ে যায়।", "LATE train · EXactly · need to (tə) be ↘"),
    ], [("as usual", "in the normal way; like always", "যথারীতি"), ("suitcase", "a bag with a handle for travelling", "স্যুটকেস"),
        ("turn out", "become known in the end", "শেষে জানা যাওয়া"), ("plan", "decide what to do in the future", "পরিকল্পনা করা"),
        ("exactly", "completely correct", "ঠিক")],
      [("fill", "The train was late, as ___.", ["usual"]), ("fill", "Rafi sat on his ___.", ["suitcase"]),
       ("fill", "They were both students of the same ___.", ["teacher"]), ("fill", "They planned a ___ together.", ["trip"])],
      "Assimilation and reductions"),
]

BY_SLUG = {s["slug"]: s for s in STORIES}
FREE = {"lost-kite"}


def key(slug):
    return f"story:{slug}"


def quiz_key(slug):
    return f"story-quiz:{slug}"
