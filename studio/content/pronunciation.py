"""Pronunciation course: 22 lessons in the order people learn to speak clearly, written by FamilyEnglish.

Order: start here → consonants → vowels → word endings and spelling → rhythm and connected speech →
accent and fluency (then the shadowing stories in stories.py).

Each lesson is taught like a grammar lesson (hello, key symbols, the rule in English and Bangla, spoken examples,
practice) and has a "drill": words to repeat with the target sound marked, scored by speech recognition.
Practice items use the grammar format: ("fill", prompt, [accepted]), ("fix", wrong, [accepted]), ("say", text),
("make", task, regex).
Drill items: (text, sound code from sounds.py, Bangla meaning, British IPA).
All explanations, examples and word lists here are FamilyEnglish's own.
"""

STAGES = [
    ("start", "🌱", "Start here", "শুরু এখানে"),
    ("consonants", "👄", "Consonant sounds", "ব্যঞ্জনধ্বনি"),
    ("vowels", "🎵", "Vowel sounds", "স্বরধ্বনি"),
    ("endings", "🔚", "Endings and spelling", "শব্দের শেষ ও বানান"),
    ("flow", "🔗", "Rhythm and connected speech", "ছন্দ ও জোড়া লাগানো কথা"),
    ("accent", "👑", "British accent and fluency", "ব্রিটিশ উচ্চারণ ও সাবলীলতা"),
]


def P(slug, stage, icon, title, title_bn, sub, hello, formula, rule, examples, practice, drill):
    return {"slug": slug, "stage": stage, "icon": icon, "title": title, "title_bn": title_bn, "sub": sub,
            "hello": hello, "formula": formula, "rule": rule, "examples": examples, "practice": practice,
            "drill": drill, "level": "pron"}


LESSONS = [
    # ------------------------------------------------------------------ Start here
    P("pron-first-lesson", "start", "🌱", "Your first pronunciation lesson", "আপনার প্রথম উচ্চারণ পাঠ",
      "Sounds, stress and rhythm",
      ("Clear pronunciation helps people understand you — and helps you understand them. Let's see what we will practise!",
       "পরিষ্কার উচ্চারণে মানুষ আপনাকে বুঝবে — আপনিও তাদের বুঝবেন। চলুন দেখি কী কী অনুশীলন করব!"),
      [("sounds", "subj"), ("stress", "verb"), ("rhythm", "obj")],
      ("English pronunciation has three parts. 1) Sounds: about 44 — vowels and consonants. English spelling often "
       "does not show the sound, so we learn the sounds themselves. 2) Word stress: in longer words one part is "
       "stronger — po-TA-to, not PO-ta-to. 3) Rhythm: in a sentence the important words are strong and the small "
       "words are quick and soft. Practise a little every day: listen, copy, record yourself and compare.",
       "ইংরেজি উচ্চারণের তিনটি অংশ। ১) ধ্বনি: প্রায় ৪৪টি — স্বর ও ব্যঞ্জন। বানান দেখে সবসময় ধ্বনি বোঝা যায় না, "
       "তাই ধ্বনিগুলোই শিখব। ২) শব্দের ঝোঁক: বড় শব্দে একটি অংশ জোরে বলা হয় — po-TA-to। ৩) ছন্দ: বাক্যে "
       "গুরুত্বপূর্ণ শব্দ জোরে, ছোট শব্দ দ্রুত ও নরম। প্রতিদিন একটু করে: শুনুন, নকল করুন, রেকর্ড করে মিলিয়ে নিন।"),
      [("My brother lives near the river.", "আমার ভাই নদীর কাছে থাকে।"),
       ("Can I have a glass of water, please?", "আমি কি এক গ্লাস পানি পেতে পারি?"),
       ("We're going to the market tomorrow.", "আমরা কাল বাজারে যাচ্ছি।")],
      [("fill", "English has about ___ sounds.", ["44", "forty-four", "forty four"]),
       ("fill", "In 'potato' the strong part is ___ (po, ta or to).", ["ta"]),
       ("fill", "In a sentence, small words like 'to' and 'a' are usually ___ (strong or soft).", ["soft", "weak"]),
       ("say", "Good morning, how are you today?"),
       ("say", "I would like a cup of tea."),
       ("make", "Say one sentence about your family.", r"\w+\s+\w+\s+\w+")],
      [("water", "ɔː", "পানি", "ˈwɔːtə"), ("family", "æ", "পরিবার", "ˈfæməli"), ("think", "θ", "ভাবা", "θɪŋk"),
       ("very", "v", "খুব", "ˈveri"), ("school", "uː", "স্কুল", "skuːl"), ("mother", "ʌ", "মা", "ˈmʌðə"),
       ("yellow", "j", "হলুদ", "ˈjeləʊ"), ("seven", "e", "সাত", "ˈsevn")]),

    P("pron-phonemic-chart", "start", "🔣", "The phonemic chart", "ধ্বনি-চিহ্নের চার্ট", "One symbol = one sound",
      ("Each symbol on the phonemic chart is one sound. Learn the symbols and any dictionary can teach you any word!",
       "চার্টের প্রতিটি চিহ্ন একটি ধ্বনি। চিহ্নগুলো শিখলে যেকোনো ডিকশনারি থেকে যেকোনো শব্দের উচ্চারণ শিখতে পারবেন!"),
      [("single vowels", "subj"), ("diphthongs", "verb"), ("consonants", "obj")],
      ("The chart has three groups. Single vowels: short /ɪ e æ ʌ ɒ ʊ ə/ and long ones marked ː /iː ɑː ɔː uː ɜː/. "
       "Diphthongs: two vowels that glide together /eɪ aɪ ɔɪ əʊ aʊ ɪə eə ʊə/. Consonants: many come in pairs — "
       "voiceless /p t k f θ s ʃ tʃ/ and voiced /b d g v ð z ʒ dʒ/ — plus /m n ŋ h l r w j/. In a dictionary, "
       "the mark ˈ comes before the stressed part: /ˈmʌðə/.",
       "চার্টে তিনটি ভাগ। একক স্বর: ছোট /ɪ e æ ʌ ɒ ʊ ə/ আর লম্বা (ː চিহ্ন) /iː ɑː ɔː uː ɜː/। দ্বিস্বর: দুটি স্বর একসাথে "
       "গড়িয়ে যায় /eɪ aɪ ɔɪ əʊ aʊ ɪə eə ʊə/। ব্যঞ্জন: অনেকগুলো জোড়ায় — অঘোষ /p t k f θ s ʃ tʃ/ ও ঘোষ "
       "/b d g v ð z ʒ dʒ/ — আর /m n ŋ h l r w j/। ডিকশনারিতে ˈ চিহ্নের পরের অংশে জোর পড়ে।"),
      [("Ship, chip and sheep — one sound changes the word.", "Ship, chip, sheep — একটি ধ্বনি বদলালে শব্দ বদলে যায়।"),
       ("The word 'night' has five letters but only three sounds.", "'night' শব্দে পাঁচটি অক্ষর, কিন্তু ধ্বনি মাত্র তিনটি।"),
       ("Look for the stress mark before the strong part of a word.", "শব্দের জোরালো অংশের আগে ঝোঁক-চিহ্নটি খুঁজুন।")],
      [("fill", "The mark ː means the vowel is ___ (long or short).", ["long"]),
       ("fill", "Is /b/ voiced or voiceless? ___", ["voiced"]),
       ("fill", "'Knife' has five letters and ___ sounds.", ["3", "three"]),
       ("fill", "A vowel that glides from one sound to another is a ___ (diphthong or consonant).", ["diphthong"]),
       ("say", "Three free trees."),
       ("say", "Ship, sheep, chip, cheap.")],
      [("ship", "ɪ", "জাহাজ", "ʃɪp"), ("sheep", "iː", "ভেড়া", "ʃiːp"), ("cat", "æ", "বিড়াল", "kæt"),
       ("cut", "ʌ", "কাটা", "kʌt"), ("cart", "ɑː", "গাড়ি (ঠেলা)", "kɑːt"), ("cot", "ɒ", "শিশুর খাট", "kɒt"),
       ("caught", "ɔː", "ধরা পড়েছিল", "kɔːt"), ("coat", "əʊ", "কোট", "kəʊt")]),

    # ------------------------------------------------------------------ Consonants
    P("pron-voiced-voiceless", "consonants", "🫁", "Voiced and voiceless sounds", "ঘোষ ও অঘোষ ধ্বনি",
      "Feel the buzz in your throat",
      ("Put your fingers on your throat. Say 'zzzz', then 'ssss'. Can you feel the difference?",
       "গলায় আঙুল রাখুন। 'zzzz' বলুন, তারপর 'ssss'। পার্থক্যটা টের পাচ্ছেন?"),
      [("voiced = buzz", "verb"), ("voiceless = air", "obj")],
      ("Voiced sounds make your throat buzz: /b d g v ð z ʒ dʒ/ and every vowel. Voiceless sounds are only air: "
       "/p t k f θ s ʃ tʃ/. Each pair uses the same mouth shape — only the voice changes: /p/–/b/, /f/–/v/, /s/–/z/. "
       "Bangla speakers often use ফ for both /f/ and /p/, or ভ for both /v/ and /b/. In English these are four "
       "different sounds: /f/ and /v/ use the top teeth on the bottom lip; /p/ and /b/ use both lips.",
       "ঘোষ ধ্বনিতে গলা কাঁপে: /b d g v ð z ʒ dʒ/ ও সব স্বর। অঘোষ ধ্বনিতে শুধু বাতাস: /p t k f θ s ʃ tʃ/। "
       "জোড়ার দুটির মুখের আকার একই — শুধু গলার স্বর বদলায়। আমরা অনেক সময় /f/ ও /p/-এর জায়গায় 'ফ', /v/ ও "
       "/b/-এর জায়গায় 'ভ' বলি। ইংরেজিতে এগুলো চারটি আলাদা ধ্বনি: /f/ ও /v/-তে ওপরের দাঁত নিচের ঠোঁটে; "
       "/p/ ও /b/-তে দুই ঠোঁট।"),
      [("Please pass the peas.", "মটরশুঁটিগুলো একটু দিন।"),
       ("Five vans visited the village.", "পাঁচটি ভ্যান গ্রামে এল।"),
       ("A big pig sat in the bag.", "একটি বড় শূকর থলের মধ্যে বসে ছিল।")],
      [("fill", "/v/ is voiced. Its voiceless partner is /___/.", ["f"]),
       ("fill", "Does /s/ make your throat buzz? ___ (yes or no)", ["no"]),
       ("fill", "For /f/ and /v/, the top teeth touch the bottom ___.", ["lip"]),
       ("say", "The vet visited a very old fox."),
       ("say", "Pack the big blue bag."),
       ("say", "Fine wine and five vines.")],
      [("fan", "f", "পাখা", "fæn"), ("van", "v", "ভ্যান", "væn"), ("pear", "p", "নাশপাতি", "peə"),
       ("bear", "b", "ভালুক", "beə"), ("sip", "s", "চুমুক", "sɪp"), ("zip", "z", "চেইন", "zɪp"),
       ("few", "f", "কয়েকটি", "fjuː"), ("view", "v", "দৃশ্য", "vjuː")]),

    P("pron-word-endings", "consonants", "🔚", "Clear sounds at the end of words", "শব্দের শেষ ধ্বনি স্পষ্ট",
      "rip or rib? mat or mad?",
      ("In English the last sound can change the whole word. Is it 'rip' or 'rib'? Let's listen closely!",
       "ইংরেজিতে শেষ ধ্বনি বদলালে পুরো শব্দ বদলে যায়। 'rip' না 'rib'? মন দিয়ে শুনি!"),
      [("vowel", "subj"), ("final consonant", "obj")],
      ("Never drop or swallow the last consonant — say it clearly but lightly. Listen to the vowel too: before a "
       "voiced final sound (/b d g v z/) the vowel is a little longer — 'mad' is longer than 'mat'. Before a "
       "voiceless final sound (/p t k f s/) the vowel is short and clipped. Don't add an extra vowel at the end: "
       "'dog', not 'dogue'.",
       "শেষ ব্যঞ্জন কখনো বাদ দেবেন না — হালকা কিন্তু স্পষ্ট বলুন। স্বরের দৈর্ঘ্যও খেয়াল করুন: শেষে ঘোষ ধ্বনি "
       "(/b d g v z/) থাকলে স্বর একটু লম্বা — 'mad' লম্বা, 'mat' ছোট। অঘোষ ধ্বনির আগে স্বর ছোট। শেষে বাড়তি "
       "'আ/এ' যোগ করবেন না: 'dog', 'ডগে' নয়।"),
      [("Leave the leaf on the table.", "পাতাটা টেবিলের ওপর রেখে দাও।"),
       ("He rode home and wrote a letter.", "সে বাড়ি ফিরে একটা চিঠি লিখল।"),
       ("Put some ice near your eyes.", "চোখের কাছে একটু বরফ ধরো।")],
      [("fill", "The vowel in 'mad' is ___ than in 'mat' (longer or shorter).", ["longer"]),
       ("fill", "'Rip' ends with a ___ sound (voiced or voiceless).", ["voiceless"]),
       ("fill", "'Leaf' ends with /f/. 'Leave' ends with /___/.", ["v"]),
       ("say", "The dog sat on the dock."),
       ("say", "Leave the leaf there."),
       ("say", "His bag is in the back.")],
      [("rip", "p", "ছিঁড়ে ফেলা", "rɪp"), ("rib", "b", "পাঁজর", "rɪb"), ("mat", "t", "মাদুর", "mæt"),
       ("mad", "d", "রাগী/পাগল", "mæd"), ("dock", "k", "জাহাজঘাট", "dɒk"), ("dog", "g", "কুকুর", "dɒg"),
       ("leaf", "f", "পাতা", "liːf"), ("leave", "v", "চলে যাওয়া", "liːv")]),

    P("pron-th", "consonants", "👅", "The two 'th' sounds", "দুই রকম 'th' ধ্বনি", "/θ/ think · /ð/ mother",
      ("Ready for a famous English sound? Your tongue is going to peek out between your teeth!",
       "বিখ্যাত একটা ইংরেজি ধ্বনি শিখি? জিভ একটু দাঁতের ফাঁক দিয়ে বের হবে!"),
      [("/θ/ air only", "obj"), ("/ð/ with voice", "verb")],
      ("Put the tip of your tongue lightly between your top and bottom teeth and push air out. /θ/ is only air: "
       "think, three, mouth, birthday. /ð/ adds your voice (buzz): those, mother, with, together. It is not ত/থ or "
       "দ — the tongue must touch the teeth. /ð/ is in many small, common words (the, these, there, other), so "
       "it matters a lot!",
       "জিভের ডগা হালকা করে ওপরের ও নিচের দাঁতের মাঝে রাখুন, তারপর বাতাস ছাড়ুন। /θ/ — শুধু বাতাস: think, three। "
       "/ð/ — সাথে গলার স্বর: those, mother। এটা 'থ' বা 'দ' নয় — জিভ অবশ্যই দাঁত ছোঁবে। the, these, there-এর "
       "মতো অনেক ছোট শব্দে /ð/ আছে, তাই এটা খুব জরুরি!"),
      [("My mother and father went together.", "আমার মা আর বাবা একসাথে গেলেন।"),
       ("Thirty-three thousand people were there.", "সেখানে তেত্রিশ হাজার মানুষ ছিল।"),
       ("Their birthday is on Thursday.", "ওদের জন্মদিন বৃহস্পতিবার।")],
      [("fill", "For /θ/ and /ð/ the tongue touches the ___.", ["teeth", "top teeth"]),
       ("fill", "Is the 'th' in 'those' /θ/ or /ð/? ___", ["ð", "/ð/", "voiced"]),
       ("fill", "Is the 'th' in 'three' /θ/ or /ð/? ___", ["θ", "/θ/", "voiceless"]),
       ("say", "I think these are my brother's things."),
       ("say", "Both of them are healthy."),
       ("say", "Thank you, mother.")],
      [("think", "θ", "ভাবা", "θɪŋk"), ("thirty", "θ", "ত্রিশ", "ˈθɜːti"), ("mouth", "θ", "মুখ", "maʊθ"),
       ("birthday", "θ", "জন্মদিন", "ˈbɜːθdeɪ"), ("those", "ð", "ঐগুলো", "ðəʊz"), ("mother", "ð", "মা", "ˈmʌðə"),
       ("together", "ð", "একসাথে", "təˈɡeðə"), ("other", "ð", "অন্য", "ˈʌðə")]),

    P("pron-british-r", "consonants", "🇬🇧", "The British R", "ব্রিটিশ R", "Say it before a vowel only",
      ("British English has a special rule for the letter r. Once you know it, you will sound much more British!",
       "ব্রিটিশ ইংরেজিতে r-এর একটা বিশেষ নিয়ম আছে। জানলে আপনার উচ্চারণ অনেক বেশি ব্রিটিশ শোনাবে!"),
      [("r + vowel = say it", "verb"), ("vowel + r = silent", "obj")],
      ("British English (RP) is non-rhotic: we say /r/ only when a vowel sound comes after it — rice, carry, "
       "story. When r comes after a vowel and no vowel follows, it is silent: car /kɑː/, short /ʃɔːt/, nurse "
       "/nɜːs/, sister /ˈsɪstə/. American English is rhotic and says every r. To make /r/: curl the tongue tip "
       "back without touching the roof of the mouth and round your lips a little — no rolled or tapped r like "
       "র. Linking r: if the next word starts with a vowel, the r comes back — 'far away' → fa-raway.",
       "ব্রিটিশ (RP) উচ্চারণে r বলা হয় শুধু যখন এর পরে স্বরধ্বনি থাকে — rice, carry। স্বরের পরে r থাকলে আর পরে "
       "স্বর না থাকলে r বলা হয় না: car /kɑː/, short /ʃɔːt/, sister /ˈsɪstə/। আমেরিকানরা সব r বলে। /r/ বলতে "
       "জিভের ডগা পেছনে বাঁকান, মুখের ছাদ ছোঁবেন না, ঠোঁট একটু গোল — বাংলা 'র'-এর মতো কাঁপাবেন না। পরের শব্দ "
       "স্বর দিয়ে শুরু হলে r ফিরে আসে: far away → ফা-রাওয়ে।"),
      [("The river runs past our farm.", "নদীটা আমাদের খামারের পাশ দিয়ে বয়ে যায়।"),
       ("My sister's car is very old.", "আমার বোনের গাড়িটা খুব পুরোনো।"),
       ("Where are you from?", "তুমি কোথা থেকে এসেছ?")],
      [("fill", "In British English, is the r in 'park' said? ___ (yes or no)", ["no"]),
       ("fill", "Is the r in 'carry' said? ___ (yes or no)", ["yes"]),
       ("fill", "In 'far away' the r comes back because the next word starts with a ___.", ["vowel"]),
       ("say", "Her car is over there."),
       ("say", "Rita wrote a great story."),
       ("say", "The door is open.")],
      [("rice", "r", "ভাত", "raɪs"), ("story", "r", "গল্প", "ˈstɔːri"), ("carrot", "r", "গাজর", "ˈkærət"),
       ("park", "ɑː", "পার্ক", "pɑːk"), ("short", "ɔː", "ছোট/খাটো", "ʃɔːt"), ("nurse", "ɜː", "নার্স", "nɜːs"),
       ("sister", "ə", "বোন", "ˈsɪstə"), ("far away", "r", "অনেক দূরে", "ˌfɑːr əˈweɪ")]),

    # ------------------------------------------------------------------ Vowels
    P("pron-short-long-i", "vowels", "🐑", "Short /ɪ/ and long /iː/", "ছোট /ɪ/ ও লম্বা /iː/", "live or leave?",
      ("'Sick' or 'seek'? 'Rich' or 'reach'? One small vowel changes everything. Let's practise!",
       "'sick' না 'seek'? 'rich' না 'reach'? একটা ছোট স্বর সব বদলে দেয়। চলুন অনুশীলন করি!"),
      [("/ɪ/ short, relaxed", "subj"), ("/iː/ long, smile", "obj")],
      ("/ɪ/ is short and relaxed: mouth slightly open, tongue high but loose — sit, big, fish, busy. /iː/ is long "
       "and tense: spread your lips like a smile and hold the sound — green, piece, she, people. Getting it wrong "
       "changes the meaning: sick/seek, rich/reach, lip/leap. Spelling help: ee, ea, ie and a final e often give "
       "/iː/; a single i between consonants often gives /ɪ/.",
       "/ɪ/ ছোট ও আলগা: মুখ সামান্য খোলা — sit, big, fish। /iː/ লম্বা ও টানটান: হাসির মতো ঠোঁট ছড়িয়ে ধ্বনিটা "
       "ধরে রাখুন — green, piece, she। ভুল হলে অর্থ বদলে যায়: sick/seek, rich/reach। বানানে ee, ea, ie প্রায়ই "
       "/iː/; দুই ব্যঞ্জনের মাঝে একটা i প্রায়ই /ɪ/।"),
      [("Read the list at least twice.", "তালিকাটা অন্তত দুবার পড়ো।"),
       ("The rich man couldn't reach the shelf.", "ধনী লোকটি তাকের নাগাল পেল না।"),
       ("His feet are too big for these thin shoes.", "এই পাতলা জুতোর জন্য ওর পা বেশি বড়।")],
      [("fill", "'Green' has the ___ vowel (short or long).", ["long"]),
       ("fill", "Which word has the long sound: hit or heat? ___", ["heat"]),
       ("fill", "For /iː/, spread your lips like a ___.", ["smile"]),
       ("say", "Six big fish swim in the lake."),
       ("say", "Keep the green beans for me."),
       ("say", "Is this the list he needs?")],
      [("list", "ɪ", "তালিকা", "lɪst"), ("least", "iː", "সবচেয়ে কম", "liːst"), ("hit", "ɪ", "আঘাত করা", "hɪt"),
       ("heat", "iː", "তাপ", "hiːt"), ("sick", "ɪ", "অসুস্থ", "sɪk"), ("seek", "iː", "খোঁজা", "siːk"),
       ("rich", "ɪ", "ধনী", "rɪtʃ"), ("reach", "iː", "নাগাল পাওয়া", "riːtʃ")]),

    P("pron-ae-e", "vowels", "😮", "/æ/ and /e/ — sat or set?", "/æ/ ও /e/ — sat না set?", "Open your mouth wider",
      ("Many learners say 'sat' and 'set' the same way. Today you'll make them different!",
       "অনেকে 'sat' আর 'set' একইভাবে বলেন। আজ দুটোকে আলাদা করে বলতে শিখবেন!"),
      [("/æ/ wide open", "subj"), ("/e/ half open", "obj")],
      ("/æ/: drop your jaw, open your mouth wide, tongue low and forward — cat, hand, map, bag. It is between "
       "the 'e' in 'bed' and the 'a' in 'car'. /e/: mouth only half open, jaw higher — red, bread, friend, said. "
       "Bangla speakers often use one 'এ/অ্যা' sound for both. Use a mirror: for /æ/ you should see a much bigger "
       "jaw drop.",
       "/æ/: চোয়াল নামান, মুখ বড় করে খুলুন, জিভ নিচে ও সামনে — cat, hand, map। এটা 'bed'-এর e আর 'car'-এর a-এর "
       "মাঝামাঝি। /e/: মুখ অর্ধেক খোলা — red, bread, friend। আমরা অনেক সময় দুটোর জন্য একই 'এ/অ্যা' বলি। "
       "আয়নায় দেখুন: /æ/-তে চোয়াল অনেক বেশি নামবে।"),
      [("Pat has a pet cat.", "প্যাটের একটা পোষা বিড়াল আছে।"),
       ("I guess the gas is off.", "মনে হয় গ্যাস বন্ধ।"),
       ("We sat down and set the table.", "আমরা বসলাম আর টেবিল সাজালাম।")],
      [("fill", "For /æ/ the mouth is ___ than for /e/ (wider or smaller).", ["wider"]),
       ("fill", "Which word has /e/: pat or pet? ___", ["pet"]),
       ("fill", "Which word has /æ/: sat or set? ___", ["sat"]),
       ("say", "Pat's grey hat is on the mat."),
       ("say", "Ten red pegs are on the shelf."),
       ("say", "Jack has a fat cat.")],
      [("pat", "æ", "আলতো চাপড়", "pæt"), ("pet", "e", "পোষা প্রাণী", "pet"), ("gas", "æ", "গ্যাস", "ɡæs"),
       ("guess", "e", "অনুমান করা", "ɡes"), ("sat", "æ", "বসেছিল", "sæt"), ("set", "e", "সাজানো", "set"),
       ("tan", "æ", "রোদে পোড়া রং", "tæn"), ("ten", "e", "দশ", "ten")]),

    P("pron-british-vowels", "vowels", "🎶", "Long and short British vowels", "ব্রিটিশ লম্বা ও ছোট স্বর",
      "cut/cart · cot/caught · full/fool",
      ("British English has twelve single vowels. Let's hear the long ones next to the short ones.",
       "ব্রিটিশ ইংরেজিতে বারোটি একক স্বর। লম্বাগুলো ছোটগুলোর পাশে রেখে শুনি।"),
      [("short", "subj"), ("long ː", "obj")],
      ("Short vowels: /ɪ/ sit, /e/ bed, /æ/ cat, /ʌ/ cup, /ɒ/ hot, /ʊ/ book, /ə/ the weak schwa. Long vowels "
       "(hold them longer): /iː/ see, /ɑː/ car, /ɔː/ door, /uː/ blue, /ɜː/ bird. Typical British features: /ɑː/ "
       "in words like bath, glass, fast, last; a short rounded /ɒ/ in hot, stop, want (not 'aa'); and no r after "
       "the long vowels. Pairs to practise: /ʌ/–/ɑː/ cut/cart, /ɒ/–/ɔː/ cot/caught, /ʊ/–/uː/ full/fool.",
       "ছোট স্বর: /ɪ/ sit, /e/ bed, /æ/ cat, /ʌ/ cup, /ɒ/ hot, /ʊ/ book, /ə/। লম্বা স্বর (বেশি সময় ধরে): /iː/ see, "
       "/ɑː/ car, /ɔː/ door, /uː/ blue, /ɜː/ bird। ব্রিটিশ বৈশিষ্ট্য: bath, glass, fast-এ লম্বা /ɑː/; hot, stop-এ ছোট "
       "গোল /ɒ/; লম্বা স্বরের পরে r নেই। জোড়া অনুশীলন: cut/cart, cot/caught, full/fool।"),
      [("We walked past the large park after lunch.", "দুপুরের খাবারের পর আমরা বড় পার্কটা পেরিয়ে হাঁটলাম।"),
       ("Put the book on the blue stool.", "বইটা নীল টুলের ওপর রাখো।"),
       ("The dog was hot, so we stopped.", "কুকুরটার গরম লাগছিল, তাই আমরা থামলাম।")],
      [("fill", "In British English, 'bath' has the ___ vowel as 'car' (same or different).", ["same"]),
       ("fill", "Which is long: 'full' or 'fool'? ___", ["fool"]),
       ("fill", "Which is long: 'cot' or 'caught'? ___", ["caught"]),
       ("say", "Pass me the glass, please."),
       ("say", "Our first nurse works on Thursday."),
       ("say", "Look at the moon.")],
      [("cut", "ʌ", "কাটা", "kʌt"), ("cart", "ɑː", "ঠেলাগাড়ি", "kɑːt"), ("cot", "ɒ", "শিশুর খাট", "kɒt"),
       ("caught", "ɔː", "ধরা পড়েছিল", "kɔːt"), ("full", "ʊ", "ভর্তি", "fʊl"), ("fool", "uː", "বোকা", "fuːl"),
       ("glass", "ɑː", "গ্লাস", "ɡlɑːs"), ("bird", "ɜː", "পাখি", "bɜːd")]),

    P("pron-schwa", "vowels", "😌", "The schwa /ə/", "শোয়া /ə/", "The most common sound in English",
      ("Here's a secret: the most common sound in English isn't written with one letter. It's the lazy little schwa!",
       "একটা গোপন কথা: ইংরেজির সবচেয়ে বেশি ব্যবহৃত ধ্বনির নিজস্ব কোনো অক্ষর নেই। এটা অলস ছোট্ট 'শোয়া'!"),
      [("strong", "verb"), ("ə weak", "obj")],
      ("The schwa /ə/ is short, soft and relaxed — mouth slightly open, tongue resting in the middle, like a tiny "
       "'uh' (a quick অ). It is never stressed. Many spellings make it: a in 'Saturday', e in 'happen', o in "
       "'today', u in 'suggest', er in 'letter', or in 'sailor'. Small words also become schwa in sentences: "
       "to /tə/, for /fə/, a /ə/, of /əv/, and /ən/. Using the schwa makes your English sound natural and less tiring.",
       "শোয়া /ə/ ছোট, নরম ও আলগা — মুখ সামান্য খোলা, জিভ মাঝখানে আরামে, যেন খুব ছোট একটা 'অ'। এতে কখনো জোর পড়ে "
       "না। নানা বানানে আসে: Saturday-র a, happen-এর e, today-র o, suggest-এর u, letter-এর er। বাক্যে ছোট শব্দও "
       "শোয়া হয়: to /tə/, for /fə/, a /ə/, of /əv/। শোয়া ব্যবহার করলে কথা স্বাভাবিক শোনায়।"),
      [("A cup of tea for my sister.", "আমার বোনের জন্য এক কাপ চা।"),
       ("Today is Saturday.", "আজ শনিবার।"),
       ("Lemon cake is my favourite.", "লেবুর কেক আমার সবচেয়ে প্রিয়।")],
      [("fill", "The schwa is ___ stressed (always or never).", ["never"]),
       ("fill", "Which part of 'today' is the schwa: to or day? ___", ["to"]),
       ("fill", "In 'a cup of tea', the word 'of' sounds like ___ (ov or əv).", ["əv", "uv", "ev"]),
       ("say", "My mother's sister is a sailor."),
       ("say", "Give it to Amina on Saturday."),
       ("say", "Take a photo with the camera.")],
      [("today", "ə", "আজ", "təˈdeɪ"), ("Saturday", "ə", "শনিবার", "ˈsætədeɪ"), ("lemon", "ə", "লেবু", "ˈlemən"),
       ("London", "ə", "লন্ডন", "ˈlʌndən"), ("camera", "ə", "ক্যামেরা", "ˈkæmərə"), ("police", "ə", "পুলিশ", "pəˈliːs"),
       ("letter", "ə", "চিঠি", "ˈletə"), ("suggest", "ə", "পরামর্শ দেওয়া", "səˈdʒest")]),

    P("pron-diphthongs", "vowels", "🔥", "Diphthongs and triphthongs", "দ্বিস্বর ও ত্রিস্বর", "Gliding vowels",
      ("Some English vowels move! Your mouth glides from one shape to another. Let's glide together.",
       "কিছু ইংরেজি স্বর নড়াচড়া করে! মুখ এক আকার থেকে আরেক আকারে গড়িয়ে যায়। চলুন একসাথে গড়াই।"),
      [("vowel 1", "subj"), ("→ vowel 2", "verb"), ("(→ ə)", "obj")],
      ("A diphthong glides from one vowel to another inside one syllable: /eɪ/ day, /aɪ/ my, /ɔɪ/ boy, /əʊ/ go, "
       "/aʊ/ now, /ɪə/ near, /eə/ chair (many people now say /ʊə/ as /ɔː/: sure). Make the first part longer and "
       "stronger, then glide. A triphthong glides through three: a diphthong + schwa: /aɪə/ fire, quiet; /aʊə/ "
       "shower; /eɪə/ greyer; /əʊə/ mower; /ɔɪə/ destroyer. In fast British speech the middle can almost "
       "disappear (fire → 'fah'), but as a learner glide clearly first.",
       "দ্বিস্বর এক সিলেবলের মধ্যে এক স্বর থেকে আরেক স্বরে গড়িয়ে যায়: /eɪ/ day, /aɪ/ my, /ɔɪ/ boy, /əʊ/ go, "
       "/aʊ/ now, /ɪə/ near, /eə/ chair। প্রথম অংশ লম্বা ও জোরালো, তারপর গড়ান। ত্রিস্বর তিনটি ধ্বনি জুড়ে: "
       "দ্বিস্বর + শোয়া: /aɪə/ fire, quiet; /aʊə/ shower; /ɔɪə/ destroyer। দ্রুত কথায় মাঝের অংশ প্রায় হারিয়ে যায়, "
       "তবে শুরুতে স্পষ্ট করে বলুন।"),
      [("Our music club is very quiet.", "আমাদের গানের ক্লাবটা খুব শান্ত।"),
       ("I write in my diary every night.", "আমি প্রতি রাতে ডায়েরিতে লিখি।"),
       ("Take a towel after your shower.", "গোসলের পরে একটা তোয়ালে নাও।")],
      [("fill", "'Day', 'my' and 'boy' each have a ___ (diphthong or triphthong).", ["diphthong"]),
       ("fill", "How many vowel sounds glide in 'quiet' — two or three? ___", ["3", "three"]),
       ("fill", "A triphthong is a diphthong plus a ___.", ["schwa", "ə"]),
       ("say", "Sit quietly by the fire."),
       ("say", "Take a towel after your shower."),
       ("say", "I'm tired, so I'll go home now.")],
      [("wait", "eɪ", "অপেক্ষা করা", "weɪt"), ("time", "aɪ", "সময়", "taɪm"), ("coin", "ɔɪ", "মুদ্রা", "kɔɪn"),
       ("road", "əʊ", "রাস্তা", "rəʊd"), ("cloud", "aʊ", "মেঘ", "klaʊd"), ("near", "ɪə", "কাছে", "nɪə"),
       ("quiet", "aɪ", "শান্ত", "ˈkwaɪət"), ("shower", "aʊ", "গোসল/ঝরনা", "ˈʃaʊə")]),

    # ------------------------------------------------------------------ Endings and spelling
    P("pron-ed-endings", "endings", "✅", "How to say -ed", "-ed কীভাবে বলবেন", "/t/, /d/ or /ɪd/",
      ("Past tense words end in -ed — but it has three different sounds! Let's learn the simple rule.",
       "অতীত কালের শব্দ -ed দিয়ে শেষ হয় — কিন্তু এর তিনটি আলাদা উচ্চারণ! সহজ নিয়মটা শিখি।"),
      [("/ɪd/ after t, d", "subj"), ("/t/ after voiceless", "verb"), ("/d/ after voiced", "obj")],
      ("-ed has three sounds. 1) /ɪd/ — an extra syllable — ONLY after /t/ or /d/: wait → waited, land → landed. "
       "2) /t/ after voiceless sounds /p k f s ʃ tʃ θ/: cook → cooked /kʊkt/, wash → washed /wɒʃt/. 3) /d/ after "
       "voiced sounds and vowels: stay → stayed, clean → cleaned. The most common mistake is adding an extra "
       "syllable: 'cooked' is ONE syllable, not 'cook-ed'.",
       "-ed-এর তিন উচ্চারণ। ১) /ɪd/ — একটা বাড়তি সিলেবল — শুধু /t/ বা /d/-এর পরে: waited, landed। ২) /t/ — "
       "অঘোষ ধ্বনির পরে: cooked /kʊkt/, washed। ৩) /d/ — ঘোষ ধ্বনি ও স্বরের পরে: stayed, cleaned। সবচেয়ে বড় "
       "ভুল বাড়তি সিলেবল যোগ করা: 'cooked' এক সিলেবল, 'কুকড্‌', 'কুকেড' নয়।"),
      [("She cooked rice and washed the dishes.", "সে ভাত রান্না করল আর থালা-বাসন ধুল।"),
       ("They stayed home and cleaned the room.", "ওরা বাসায় থাকল আর ঘর পরিষ্কার করল।"),
       ("Grandma visited us and baked a cake.", "দাদি আমাদের বাসায় এলেন আর একটা কেক বানালেন।")],
      [("fill", "'Cooked' ends with the sound /___/.", ["t"]),
       ("fill", "'Stayed' ends with the sound /___/.", ["d"]),
       ("fill", "'Visited' ends with the sound /___/.", ["id", "ɪd", "/ɪd/"]),
       ("fill", "How many syllables are in 'washed'? ___", ["1", "one"]),
       ("say", "I washed my hands and cleaned the table."),
       ("say", "We started early and finished late.")],
      [("waited", "d", "অপেক্ষা করেছিল", "ˈweɪtɪd"), ("landed", "d", "অবতরণ করেছিল", "ˈlændɪd"),
       ("cooked", "t", "রান্না করেছিল", "kʊkt"), ("washed", "t", "ধুয়েছিল", "wɒʃt"),
       ("laughed", "t", "হেসেছিল", "lɑːft"), ("stayed", "d", "থেকেছিল", "steɪd"),
       ("cleaned", "d", "পরিষ্কার করেছিল", "kliːnd"), ("rained", "d", "বৃষ্টি হয়েছিল", "reɪnd")]),

    P("pron-suffixes", "endings", "🧩", "Saying word endings (suffixes)", "শব্দের শেষাংশ (সাফিক্স)",
      "-ly · -able · -ible · -tion · -ful · -less",
      ("Endings like -tion and -ful are everywhere. Say them the British way: short and soft!",
       "-tion, -ful-এর মতো শেষাংশ সব জায়গায়। ব্রিটিশভাবে বলুন: ছোট আর নরম!"),
      [("word", "subj"), ("+ weak ending", "obj")],
      ("Suffixes are endings that change a word, and they are almost never stressed. -ly /li/ makes adverbs: "
       "gentle → gently. -able and -ible both sound /əbl/ — weak, never 'AY-bel': enjoyable, visible. -tion is "
       "/ʃn/ ('shn'), and the stress falls on the syllable just before it: e-du-CA-tion, STA-tion. -ful is /fl/ or "
       "/fʊl/, not a strong 'full': helpful, peaceful. -less is /ləs/ with a schwa: homeless, endless.",
       "সাফিক্স হলো শব্দের শেষে যোগ হওয়া অংশ, এতে প্রায় কখনো জোর পড়ে না। -ly /li/: gently। -able ও -ible দুটোই "
       "/əbl/ — দুর্বল, 'এইবেল' নয়: enjoyable, visible। -tion হলো /ʃn/ ('শন্‌'), আর ঠিক আগের সিলেবলে জোর: "
       "e-du-CA-tion। -ful হলো /fl/, জোরালো 'ফুল' নয়: helpful। -less হলো /ləs/: homeless।"),
      [("The station was quiet and peaceful.", "স্টেশনটা শান্ত আর নিরিবিলি ছিল।"),
       ("He answered politely and was very helpful.", "সে ভদ্রভাবে উত্তর দিল আর খুব সাহায্য করল।"),
       ("The mark on this shirt is hardly visible.", "এই শার্টের দাগটা প্রায় দেখাই যায় না।")],
      [("fill", "-tion sounds like ___ (shn or tee-on).", ["shn", "shun", "ʃn", "ʃən"]),
       ("fill", "Is the ending in 'helpful' stressed? ___ (yes or no)", ["no"]),
       ("fill", "In 'education', the stress is on ___ (e, du, ca or tion).", ["ca"]),
       ("say", "The nurse was gentle and helpful."),
       ("say", "Education is valuable."),
       ("say", "The trip was enjoyable but endless.")],
      [("gently", "l", "আলতো করে", "ˈdʒentli"), ("enjoyable", "ə", "উপভোগ্য", "ɪnˈdʒɔɪəbl"),
       ("visible", "ə", "দৃশ্যমান", "ˈvɪzəbl"), ("station", "ʃ", "স্টেশন", "ˈsteɪʃn"),
       ("education", "ʃ", "শিক্ষা", "ˌedʒuˈkeɪʃn"), ("helpful", "f", "সহায়ক", "ˈhelpfl"),
       ("peaceful", "f", "শান্তিপূর্ণ", "ˈpiːsfl"), ("homeless", "ə", "গৃহহীন", "ˈhəʊmləs")]),

    P("pron-silent-letters", "endings", "🤫", "Silent letters", "নীরব অক্ষর", "Letters we write but don't say",
      ("English keeps some letters that nobody says any more. Let's find the hidden silent letters!",
       "ইংরেজিতে কিছু অক্ষর লেখা হয়, কিন্তু আর কেউ বলে না। চলুন লুকোনো নীরব অক্ষরগুলো খুঁজি!"),
      [("write it", "verb"), ("don't say it", "obj")],
      ("Many words keep old spellings from how English sounded hundreds of years ago, or from other languages. "
       "Common patterns: kn → /n/ (knock), wr → /r/ (wrap), final mb → /m/ (lamb, plumber), stle and sten → /s/ "
       "(whistle, fasten), sw → /s/ (sword), sc before e/i → /s/ (scene), l in -lk can be silent (yolk), and h is "
       "silent after r (rhyme, rhythm). Learn these words by their sound, not by their spelling.",
       "অনেক শব্দে শত বছর আগের উচ্চারণ বা অন্য ভাষা থেকে আসা বানান রয়ে গেছে। সাধারণ নিয়ম: kn → /n/ (knock), "
       "wr → /r/ (wrap), শেষের mb → /m/ (lamb), stle/sten → /s/ (whistle, fasten), sw → /s/ (sword), sc → /s/ "
       "(scene), rh-তে h নীরব (rhyme)। এই শব্দগুলো বানান দেখে নয়, শুনে শিখুন।"),
      [("Knock on the door before you come in.", "ভেতরে আসার আগে দরজায় টোকা দাও।"),
       ("Please fasten your seat belt.", "দয়া করে সিট বেল্ট বেঁধে নিন।"),
       ("The plumber fixed the tap.", "মিস্ত্রি কলটা ঠিক করে দিলেন।")],
      [("fill", "In 'knock' the letter ___ is silent.", ["k"]),
       ("fill", "In 'lamb' the letter ___ is silent.", ["b"]),
       ("fill", "In 'fasten' the letter ___ is silent.", ["t"]),
       ("say", "Wrap the gift and fasten the ribbon."),
       ("say", "Whistle a song that rhymes."),
       ("say", "The little lamb in this scene is asleep.")],
      [("knock", "n", "টোকা দেওয়া", "nɒk"), ("wrap", "r", "মোড়ানো", "ræp"), ("lamb", "m", "ভেড়ার ছানা", "læm"),
       ("plumber", "m", "কলমিস্ত্রি", "ˈplʌmə"), ("whistle", "s", "বাঁশি/শিস", "ˈwɪsl"),
       ("fasten", "s", "বাঁধা", "ˈfɑːsn"), ("sword", "s", "তলোয়ার", "sɔːd"), ("rhyme", "r", "ছন্দমিল", "raɪm")]),

    P("pron-tricky-words", "endings", "⚠️", "Words almost everyone mispronounces", "যে শব্দগুলো প্রায় সবাই ভুল বলে",
      "Hidden syllables, strange vowels, moving stress",
      ("Some words trick almost every learner. After this lesson, they won't trick you!",
       "কিছু শব্দ প্রায় সব শিক্ষার্থীকে ঠকায়। এই পাঠের পরে আপনাকে আর ঠকাবে না!"),
      [("spelling", "subj"), ("≠", "verb"), ("sound", "obj")],
      ("Three traps cause most mistakes. 1) Hidden syllables: some written syllables disappear — interesting is "
       "IN-tres-ting (3 syllables), temperature is TEM-pre-cher, sandwich is SAN-wich, breakfast is BREK-fust. "
       "2) Strange vowels: busy and minute (60 seconds) both have /ɪ/; mountain ends in a weak /tən/. 3) Moving stress: "
       "PHO-to, but pho-TO-gra-pher; ho-TEL (stress at the end). When a word looks long, check the dictionary "
       "for the stress mark ˈ.",
       "তিনটি ফাঁদেই বেশিরভাগ ভুল হয়। ১) লুকোনো সিলেবল: কিছু লেখা সিলেবল বলা হয় না — interesting হলো IN-tres-ting "
       "(৩ সিলেবল), temperature হলো TEM-pre-cher, breakfast হলো BREK-fust। ২) অদ্ভুত স্বর: busy আর minute দুটোতেই /ɪ/। "
       "৩) ঝোঁক সরে যায়: PHO-to, কিন্তু pho-TO-gra-pher; ho-TEL। বড় শব্দে ডিকশনারির ˈ চিহ্ন দেখে নিন।"),
      [("The café is busy in the morning.", "সকালে ক্যাফেতে ভিড় থাকে।"),
       ("What's the temperature in the mountains?", "পাহাড়ে তাপমাত্রা কত?"),
       ("Those girls had breakfast at the hotel.", "ঐ মেয়েরা হোটেলে নাশতা করল।")],
      [("fill", "How many syllables does 'interesting' have when spoken? ___", ["3", "three"]),
       ("fill", "'Busy' sounds like ___ (bizzy or boozy).", ["bizzy"]),
       ("fill", "In 'photographer' the stress is on ___ (pho, to, gra or pher).", ["to"]),
       ("say", "This interesting sandwich has egg in it."),
       ("say", "Wait a minute, I'm busy."),
       ("say", "The photographer stayed at our hotel.")],
      [("interesting", "ɪ", "আকর্ষণীয়", "ˈɪntrəstɪŋ"), ("temperature", "ə", "তাপমাত্রা", "ˈtemprətʃə"),
       ("sandwich", "æ", "স্যান্ডউইচ", "ˈsænwɪtʃ"), ("breakfast", "e", "নাশতা", "ˈbrekfəst"),
       ("busy", "ɪ", "ব্যস্ত", "ˈbɪzi"), ("minute", "ɪ", "মিনিট", "ˈmɪnɪt"),
       ("photographer", "ɒ", "আলোকচিত্রী", "fəˈtɒɡrəfə"), ("hotel", "e", "হোটেল", "həʊˈtel")]),

    # ------------------------------------------------------------------ Rhythm and connected speech
    P("pron-weak-forms", "flow", "🪶", "Weak forms of small words", "ছোট শব্দের দুর্বল রূপ", "Why English sounds fast",
      ("Why does English seem so quick? Because small words become tiny and quick. Let's learn their 'weak' forms.",
       "ইংরেজি এত দ্রুত শোনায় কেন? কারণ ছোট শব্দগুলো ছোট্ট আর দ্রুত হয়ে যায়। চলুন এদের 'দুর্বল রূপ' শিখি।"),
      [("CONTENT words strong", "verb"), ("function words weak", "obj")],
      ("English is stress-timed: content words (nouns, main verbs, adjectives, adverbs) are strong, and the "
       "small function words between them are squeezed. Function words usually use a weak form with schwa: "
       "to /tə/, for /fə/, of /əv/, and /ən/, can /kən/, was /wəz/, were /wə/, have /əv/, them /ðəm/, from /frəm/. "
       "Use the STRONG form when the word is at the end of a sentence, said alone, or stressed for meaning: "
       "'Who is it for?' /fɔː/, 'Yes, I can.' /kæn/.",
       "ইংরেজি ঝোঁক-ভিত্তিক ছন্দের ভাষা: বিশেষ্য, মূল ক্রিয়া, বিশেষণের মতো অর্থবহ শব্দ জোরালো; মাঝের ছোট শব্দগুলো "
       "চেপে যায়। এরা সাধারণত শোয়া দিয়ে দুর্বল রূপে বলা হয়: to /tə/, for /fə/, of /əv/, and /ən/, can /kən/, "
       "was /wəz/। বাক্যের শেষে, একা বা অর্থের জন্য জোর দিলে জোরালো রূপ: 'Yes, I can.' /kæn/।"),
      [("I can swim, but I can't dive.", "আমি সাঁতার কাটতে পারি, কিন্তু ডুব দিতে পারি না।"),
       ("It was a gift for my mum.", "এটা আমার মায়ের জন্য একটা উপহার ছিল।"),
       ("Tell them to wait for us.", "ওদের বলো আমাদের জন্য অপেক্ষা করতে।")],
      [("fill", "In 'bread and butter', is 'and' weak or strong? ___", ["weak"]),
       ("fill", "At the end of 'Yes, I can.', is 'can' weak or strong? ___", ["strong"]),
       ("fill", "The weak form of 'for' is /f___/.", ["ə", "uh"]),
       ("say", "I was waiting for the bus."),
       ("say", "Some of them can come at two."),
       ("say", "Where are you from?")],
      [("a cup of tea", "ə", "এক কাপ চা", "ə ˈkʌp əv ˈtiː"), ("fish and chips", "ə", "মাছ আর চিপস", "ˌfɪʃ ən ˈtʃɪps"),
       ("time to go", "ə", "যাওয়ার সময়", "ˈtaɪm tə ˈɡəʊ"), ("I can help", "ə", "আমি সাহায্য করতে পারি", "aɪ kən ˈhelp"),
       ("it was late", "ə", "দেরি হয়ে গিয়েছিল", "ɪt wəz ˈleɪt"), ("tell them", "ə", "ওদের বলো", "ˈtel ðəm"),
       ("a gift for you", "ə", "তোমার জন্য উপহার", "ə ˈɡɪft fə ˈjuː"), ("from Dhaka", "ə", "ঢাকা থেকে", "frəm ˈdɑːkə")]),

    P("pron-contractions", "flow", "🗜️", "Contractions and reductions", "সংক্ষিপ্ত রূপ ও কথ্য রূপ",
      "I'm, don't · gonna, wanna",
      ("In real conversation people join words together. Some joins are fine everywhere; some only in chat!",
       "আসল কথোপকথনে মানুষ শব্দ জুড়ে বলে। কিছু জোড়া সব জায়গায় চলে; কিছু শুধু আড্ডায়!"),
      [("contraction ✓ speech + writing", "verb"), ("reduction = casual speech only", "obj")],
      ("Contractions join two words and are normal in speech and friendly writing: I am → I'm, do not → don't, "
       "they have → they've, we will → we'll, she would → she'd. Full forms in speech can sound very formal or "
       "angry. Reductions are only for casual speaking — don't write them in exams: going to → gonna, want to → "
       "wanna, got to → gotta, kind of → kinda, give me → gimme. Note: should've, could've, would've mean should "
       "HAVE — never write 'should of'.",
       "কন্ট্রাকশন দুটি শব্দ জোড়ে — কথায় ও সাধারণ লেখায় স্বাভাবিক: I'm, don't, they've, we'll। কথায় পূর্ণ রূপ "
       "খুব আনুষ্ঠানিক বা রাগী শোনাতে পারে। রিডাকশন শুধু ঘরোয়া কথায় — পরীক্ষায় লিখবেন না: gonna (going to), "
       "wanna (want to), gotta (got to), kinda (kind of)। should've মানে should have — কখনো 'should of' লিখবেন না।"),
      [("I'm tired, so I'll go to bed.", "আমি ক্লান্ত, তাই ঘুমাতে যাব।"),
       ("We're gonna watch a film tonight.", "আজ রাতে আমরা একটা সিনেমা দেখব।"),
       ("You should've told me earlier.", "তোমার আগে আমাকে বলা উচিত ছিল।")],
      [("fill", "The short form of 'they have' is ___.", ["they've"]),
       ("fill", "'Wanna' means ___ (want to or want a).", ["want to"]),
       ("fix", "I should of called you.", ["i should have called you.", "i should've called you."]),
       ("fill", "Is 'gonna' OK in an exam essay? ___ (yes or no)", ["no"]),
       ("say", "Don't worry, we'll be there soon."),
       ("say", "I've gotta finish my homework.")],
      [("I'm", "aɪ", "আমি (হই)", "aɪm"), ("don't", "əʊ", "করো না", "dəʊnt"), ("they've", "eɪ", "তারা (করেছে)", "ðeɪv"),
       ("we'll", "iː", "আমরা (করব)", "wiːl"), ("she'd", "iː", "সে (করত)", "ʃiːd"), ("gonna", "ə", "যাচ্ছি (কথ্য)", "ˈɡənə"),
       ("wanna", "ɒ", "চাই (কথ্য)", "ˈwɒnə"), ("should've", "ə", "উচিত ছিল", "ˈʃʊdəv")]),

    P("pron-linking", "flow", "🔗", "Linking words together", "শব্দ জুড়ে বলা", "pick‿it‿up · go‿w‿out",
      ("Native speakers don't stop between words — they link them. Let's make your English flow!",
       "ইংরেজিভাষীরা শব্দের মাঝে থামেন না — জুড়ে বলেন। চলুন আপনার কথাকে প্রবাহিত করি!"),
      [("word‿", "subj"), ("‿word", "obj")],
      ("1) Consonant + vowel: the last consonant moves onto the next word — 'pick it up' → pi-ki-tup, 'an apple' "
       "→ a-napple. 2) Vowel + vowel: we add a tiny joining sound. After /uː əʊ aʊ/ add /w/: 'go out' → go-w-out, "
       "'do it' → do-w-it. After /iː eɪ aɪ ɔɪ/ add /j/ (y): 'I am' → I-y-am, 'she is' → she-y-is. In British "
       "English after /ə ɑː ɔː ɜː/ add /r/: linking r in 'far away', and even where there is no r in the spelling "
       "(intrusive r): 'India and China' → India-r-and China. 3) Same consonant twice: say it once, a little "
       "longer — 'bus stop', 'big game'.",
       "১) ব্যঞ্জন + স্বর: শেষ ব্যঞ্জন পরের শব্দে চলে যায় — 'pick it up' → পি-কি-টাপ। ২) স্বর + স্বর: ছোট একটা "
       "জোড়-ধ্বনি যোগ হয় — /uː əʊ aʊ/-এর পরে /w/: go-w-out; /iː eɪ aɪ/-এর পরে /j/: I-y-am; ব্রিটিশ ইংরেজিতে /ə ɑː ɔː/-"
       "এর পরে /r/: far away, এমনকি বানানে r না থাকলেও (India-r-and China)। ৩) একই ব্যঞ্জন দুবার: একবার, একটু লম্বা "
       "করে — bus stop।"),
      [("Pick it up and put it on.", "এটা তুলে পরে নাও।"),
       ("Go out and see if he is in.", "বাইরে গিয়ে দেখো সে ভেতরে আছে কি না।"),
       ("Is the bus stop far away?", "বাসস্টপ কি অনেক দূরে?")],
      [("fill", "'Go out' is joined with a small /___/ sound.", ["w"]),
       ("fill", "'She is' is joined with a small /___/ sound.", ["j", "y"]),
       ("fill", "In 'an apple', the n moves to the word ___.", ["apple"]),
       ("say", "Turn it off at eleven."),
       ("say", "Do it again, Anna."),
       ("say", "Put it in a bag.")],
      [("pick it up", "k", "এটা তোলো", "ˌpɪk ɪt ˈʌp"), ("an apple", "n", "একটা আপেল", "ən ˈæpl"),
       ("turn it off", "n", "বন্ধ করো", "ˌtɜːn ɪt ˈɒf"), ("go out", "w", "বাইরে যাও", "ˌɡəʊ ˈwaʊt"),
       ("do it", "w", "করে ফেলো", "ˈduː wɪt"), ("I am", "j", "আমি", "aɪ jæm"),
       ("far away", "r", "অনেক দূরে", "ˌfɑːr əˈweɪ"), ("bus stop", "s", "বাসস্টপ", "ˈbʌs stɒp")]),

    P("pron-assimilation", "flow", "🌀", "Sounds that change and disappear", "যে ধ্বনি বদলায় ও হারিয়ে যায়",
      "would you → 'wudju' · next door → 'nex door'",
      ("In fast speech some sounds change shape or vanish. Knowing this helps you understand native speakers!",
       "দ্রুত কথায় কিছু ধ্বনি বদলে যায় বা হারিয়ে যায়। এটা জানলে ইংরেজিভাষীদের কথা সহজে বুঝবেন!"),
      [("sound", "subj"), ("→ changes", "verb"), ("next sound", "obj")],
      ("Assimilation: a sound becomes more like the next sound, so speech is smoother. /n/ → /m/ before /p b m/: "
       "'ten bikes' → tem bikes; /n/ → /ŋ/ before /k g/: 'in case' → ing case; /t/ → /p/ before /p b m/: 'that "
       "boy' → thap boy. /d/ + /j/ → /dʒ/: 'would you' → wu-ju; /t/ + /j/ → /tʃ/: 'don't you' → don-chu. Elision: "
       "/t/ and /d/ often disappear between two consonants: 'next door' → nex door, 'old man' → ole man. You "
       "don't have to do all of these, but you must be able to hear them.",
       "অ্যাসিমিলেশন: একটি ধ্বনি পরের ধ্বনির মতো হয়ে যায়, তাই কথা মসৃণ হয়। /p b m/-এর আগে /n/ → /m/: 'ten bikes' "
       "→ tem bikes; /k g/-এর আগে /n/ → /ŋ/: in case → ing case। /d/+/j/ → /dʒ/: would you → উডজু; /t/+/j/ → /tʃ/: "
       "don't you → ডোনচু। এলিশন: দুই ব্যঞ্জনের মাঝে /t/, /d/ হারিয়ে যায়: next door → নেক্স ডোর। সব আপনাকে বলতে "
       "হবে না, তবে শুনে বুঝতে হবে।"),
      [("Would you like ten bananas?", "তুমি কি দশটা কলা নেবে?"),
       ("Did you see that bird?", "তুমি কি ঐ পাখিটা দেখেছ?"),
       ("Our next door neighbour is kind.", "আমাদের পাশের বাড়ির প্রতিবেশী দয়ালু।")],
      [("fill", "In fast speech, 'ten bikes' can sound like 'te___ bikes'.", ["m"]),
       ("fill", "'Would you' often sounds like 'wu-___'.", ["ju", "joo", "dʒu"]),
       ("fill", "In 'next door', the sound /___/ often disappears.", ["t"]),
       ("say", "Did you meet him in Cox's Bazar?"),
       ("say", "Don't you want some?"),
       ("say", "Would you open the window?")],
      [("would you", "dʒ", "তুমি কি…", "ˈwʊdʒu"), ("did you", "dʒ", "তুমি কি করেছিলে", "ˈdɪdʒu"),
       ("don't you", "tʃ", "তুমি কি না…", "ˈdəʊntʃu"), ("ten bikes", "m", "দশটা সাইকেল", "ˌtem ˈbaɪks"),
       ("in case", "ŋ", "যদি দরকার হয়", "ɪŋ ˈkeɪs"), ("that boy", "p", "ঐ ছেলেটি", "ˌðæp ˈbɔɪ"),
       ("next door", "s", "পাশের বাড়ি", "ˌneks ˈdɔː"), ("old man", "l", "বুড়ো লোক", "ˌəʊl ˈmæn")]),

    P("pron-intonation", "flow", "🎶", "Intonation: the music of English", "ইন্টোনেশন: ইংরেজির সুর",
      "Falling ↘ · rising ↗ · fall-rise ↘↗",
      ("The same words can be a question, a statement, happy or annoyed — it all depends on the tune of your voice!",
       "একই কথা প্রশ্ন, বিবৃতি, খুশি বা বিরক্তি — সব নির্ভর করে গলার সুরের ওপর!"),
      [("↘ fall = finished", "verb"), ("↗ rise = open", "obj")],
      ("Intonation is your voice going up and down to show meaning and feeling. Falling ↘ for statements, "
       "orders and wh-questions: 'I live in Dhaka↘.' 'Where do you work↘?' Rising ↗ for yes/no questions and "
       "when you are unsure: 'Are you ready↗?' Fall-rise ↘↗ for polite doubt or 'there's more': 'It's nice, "
       "but…↘↗'. Lists rise on each item and fall on the last: 'rice↗, eggs↗ and oil↘'. Question tags fall when "
       "you expect 'yes' and rise when you really ask: 'It's hot, isn't it↘?' The most important word gets the "
       "biggest movement.",
       "ইন্টোনেশন হলো অর্থ ও অনুভূতি বোঝাতে গলার স্বর ওঠা-নামা। নামা সুর ↘: বিবৃতি, আদেশ ও wh-প্রশ্নে। ওঠা সুর ↗: "
       "হ্যাঁ/না প্রশ্নে ও অনিশ্চয়তায়। নেমে-ওঠা ↘↗: ভদ্র সন্দেহ বা 'আরও কিছু আছে'। তালিকায় প্রতিটিতে ওঠে, শেষটায় "
       "নামে। প্রশ্ন-ট্যাগ: উত্তর জানা থাকলে নামে, সত্যিই জানতে চাইলে ওঠে। সবচেয়ে গুরুত্বপূর্ণ শব্দে সুর সবচেয়ে বেশি বদলায়।"),
      [("Where are you going?", "তুমি কোথায় যাচ্ছ?"),
       ("Are you coming with us?", "তুমি কি আমাদের সাথে আসছ?"),
       ("I need rice, eggs, onions and oil.", "আমার চাল, ডিম, পেঁয়াজ আর তেল লাগবে।"),
       ("It's a lovely day, isn't it?", "দিনটা সুন্দর, তাই না?")],
      [("fill", "Wh-questions usually ___ at the end (rise or fall).", ["fall"]),
       ("fill", "Yes/no questions usually ___ at the end (rise or fall).", ["rise"]),
       ("fill", "In a list, the voice falls on the ___ item (first or last).", ["last"]),
       ("say", "What time does the class start?"),
       ("say", "Would you like tea or coffee?"),
       ("say", "You're from Sylhet, aren't you?")],
      [("Really?", "stress", "সত্যি?", "ˈrɪəli ↗"), ("Thank you.", "stress", "ধন্যবাদ।", "ˈθæŋk juː ↘"),
       ("Are you OK?", "stress", "তুমি ঠিক আছ?", "ɑː juː əʊˈkeɪ ↗"), ("Where's my bag?", "stress", "আমার ব্যাগ কোথায়?", "weəz maɪ ˈbæɡ ↘"),
       ("Maybe…", "stress", "হয়তো…", "ˈmeɪbi ↘↗"), ("Come here!", "stress", "এখানে এসো!", "kʌm ˈhɪə ↘"),
       ("Is it far?", "stress", "এটা কি দূরে?", "ɪz ɪt ˈfɑː ↗"), ("Good news!", "stress", "ভালো খবর!", "ɡʊd ˈnjuːz ↘")]),

    # ------------------------------------------------------------------ Accent and fluency
    P("pron-british-accent", "accent", "👑", "A modern British accent", "আধুনিক ব্রিটিশ উচ্চারণ",
      "Classic RP and Modern RP",
      ("Which British accent will you learn? Let's compare classic RP with the modern British accent we teach.",
       "কোন ব্রিটিশ উচ্চারণ শিখবেন? পুরোনো RP আর আমরা যে আধুনিক ব্রিটিশ উচ্চারণ শেখাই — দুটো মিলিয়ে দেখি।"),
      [("classic RP", "subj"), ("→ Modern RP", "obj")],
      ("RP (Received Pronunciation) is the classic accent of old BBC news and dictionaries. Modern RP is how many "
       "educated Britons speak today — clear, neutral and easy to understand, so it's what FamilyEnglish teaches. "
       "Changes from classic RP: 'sure', 'tour' now mostly use /ɔː/; the /æ/ in 'cat' is more open; the end of "
       "'happy' is a short bright /i/. Three quick steps to sound British: 1) no r after a vowel (car, water), "
       "2) /ɑː/ in words like bath, last, after, 3) the glide /əʊ/ in go, home, road — not a flat 'o'. In "
       "casual speech many Britons swallow /t/ between vowels (wa'er), but in exams say a clear /t/.",
       "RP হলো পুরোনো BBC খবর ও ডিকশনারির ক্লাসিক উচ্চারণ। Modern RP হলো আজকের অনেক শিক্ষিত ব্রিটিশের উচ্চারণ — "
       "পরিষ্কার, নিরপেক্ষ, সহজে বোঝা যায়; তাই আমরা এটাই শেখাই। পরিবর্তন: sure, tour-এ এখন বেশিরভাগ /ɔː/; cat-এর "
       "/æ/ আরও খোলা; happy-র শেষে ছোট /i/। ব্রিটিশ শোনাতে তিন ধাপ: ১) স্বরের পরে r নয়, ২) bath, last, after-এ /ɑː/, "
       "৩) go, home-এ গড়ানো /əʊ/। ঘরোয়া কথায় অনেকে /t/ গিলে ফেলেন, তবে পরীক্ষায় /t/ স্পষ্ট বলুন।"),
      [("I'm sure the tour starts at half past.", "আমি নিশ্চিত ট্যুরটা সাড়ে কোনো সময়ে শুরু হবে।"),
       ("Let's go home after the last class.", "শেষ ক্লাসের পরে চলো বাড়ি যাই।"),
       ("My cousin is happy with her new car.", "আমার কাজিন তার নতুন গাড়ি নিয়ে খুশি।")],
      [("fill", "Modern RP usually says 'sure' with ___ (ɔː or ʊə).", ["ɔː", "or", "aw"]),
       ("fill", "In British English, 'last' has the vowel in ___ (car or cat).", ["car"]),
       ("fill", "Is the r in 'water' said in British English? ___ (yes or no)", ["no"]),
       ("say", "Let's go home after class."),
       ("say", "Can you pass the water, please?"),
       ("say", "I'm sure it's half past four.")],
      [("bath", "ɑː", "গোসল", "bɑːθ"), ("after", "ɑː", "পরে", "ˈɑːftə"), ("home", "əʊ", "বাড়ি", "həʊm"),
       ("road", "əʊ", "রাস্তা", "rəʊd"), ("sure", "ɔː", "নিশ্চিত", "ʃɔː"), ("happy", "æ", "খুশি", "ˈhæpi"),
       ("water", "ɔː", "পানি", "ˈwɔːtə"), ("better", "t", "আরও ভালো", "ˈbetə")]),

    P("pron-shadowing", "accent", "🗣️", "Shadowing: copy a speaker", "শ্যাডোয়িং: বক্তাকে নকল করুন",
      "The fastest way to sound natural",
      ("Want to sound natural fast? Become the speaker's shadow — copy their voice, not just their words!",
       "দ্রুত স্বাভাবিক শোনাতে চান? বক্তার ছায়া হয়ে যান — শুধু শব্দ নয়, তাঁর কণ্ঠ নকল করুন!"),
      [("listen", "subj"), ("copy", "verb"), ("compare", "obj")],
      ("Shadowing means listening to a speaker and copying them straight after (or at the same time), like a "
       "shadow. Copy everything: sounds, stress, rhythm, linking and the tune of the voice. Five steps: 1) Listen "
       "once while reading. 2) Listen again and notice the links and strong words. 3) Repeat after each "
       "sentence. 4) Speak together with the voice. 5) Record yourself and compare. Five minutes every day "
       "works better than one long hour once a week. Our stories are made for shadowing!",
       "শ্যাডোয়িং মানে বক্তার কথা শুনে সাথে সাথে (বা একসাথে) ছায়ার মতো নকল করা। সব নকল করুন: ধ্বনি, ঝোঁক, ছন্দ, "
       "জোড়া লাগানো ও সুর। পাঁচ ধাপ: ১) পড়তে পড়তে একবার শুনুন। ২) আবার শুনে জোড়া ও জোরালো শব্দ খেয়াল করুন। "
       "৩) প্রতিটি বাক্যের পরে বলুন। ৪) কণ্ঠের সাথে একসাথে বলুন। ৫) রেকর্ড করে মিলিয়ে নিন। প্রতিদিন পাঁচ মিনিট, "
       "সপ্তাহে একদিন এক ঘণ্টার চেয়ে ভালো। আমাদের গল্পগুলো শ্যাডোয়িংয়ের জন্যই বানানো!"),
      [("Every morning, Rumi walks to school with her grandfather.", "প্রতিদিন সকালে রুমি দাদার সাথে হেঁটে স্কুলে যায়।"),
       ("They stop at a little tea stall on the corner.", "তারা মোড়ের ছোট্ট চায়ের দোকানে থামে।"),
       ("Grandfather tells her a new story every day.", "দাদা তাকে প্রতিদিন একটা নতুন গল্প বলেন।")],
      [("fill", "Shadowing means copying the speaker's sounds, rhythm and ___ (tune or spelling).", ["tune"]),
       ("fill", "Which is better: five minutes every day or one hour once a week? ___", ["five minutes every day", "five minutes", "every day"]),
       ("say", "Every morning, Rumi walks to school with her grandfather."),
       ("say", "They stop at a little tea stall on the corner."),
       ("say", "Grandfather tells her a new story every day.")],
      [("every morning", "stress", "প্রতিদিন সকালে", "ˌevri ˈmɔːnɪŋ"), ("walks to school", "ə", "হেঁটে স্কুলে যায়", "ˈwɔːks tə ˈskuːl"),
       ("with her grandfather", "ə", "দাদার সাথে", "wɪð ə ˈɡrænfɑːðə"), ("a little tea stall", "stress", "ছোট্ট চায়ের দোকান", "ə ˌlɪtl ˈtiː stɔːl"),
       ("on the corner", "ə", "মোড়ে", "ɒn ðə ˈkɔːnə"), ("tells her a story", "ə", "তাকে একটা গল্প বলেন", "ˈtelz ər ə ˈstɔːri"),
       ("every day", "stress", "প্রতিদিন", "ˌevri ˈdeɪ"), ("a new one", "w", "নতুন একটা", "ə ˈnjuː wʌn")]),
]

BY_SLUG = {p["slug"]: p for p in LESSONS}
FREE = {"pron-first-lesson", "pron-phonemic-chart"}


def by_stage(stage):
    return [p for p in LESSONS if p["stage"] == stage]


def key(slug):
    return f"pron:{slug}"


def drill_key(slug):
    return f"pron-drill:{slug}"
