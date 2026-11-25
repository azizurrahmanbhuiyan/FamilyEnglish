"""British pronunciation: 30 lessons on the sounds, stress, rhythm and intonation of standard
Southern British English (the accent of BBC newsreaders and most British teachers).

Written for Bangla speakers: every lesson says which Bangla habit to change. The browser reads the
examples with a British voice (en-GB) and the microphone checks the learner's sentence.
"""

from ._h import C, L, S

SKILL = "speaking"


def P(slug, band, order, title, title_bn, goal, note_en, note_bn, tip_bn, say, pair, quiz, video, errors=()):
    """say: 4 sentences to say; pair: (word heard, other word) minimal pair; quiz: (question, right, *wrong, why)."""
    q, right, *rest = quiz
    wrong, why = rest[:-1], rest[-1]
    heard, other = pair
    practice = [
        S(say[0], why=tip_bn, qt="spk_sounds" if band == "easy" else "spk_stress" if "stress" in title.lower() else "spk_sounds"),
        C("Listen. Which word do you hear?", heard, other, say=heard, qt="spk_sounds",
          why=f"'{heard}' আর '{other}' আলাদা শোনায়।"),
        S(say[1], qt="spk_sounds"),
        C(q, right, *wrong, qt="spk_sounds", why=why),
    ]
    test = [
        S(say[2], qt="spk_sounds"),
        C("Listen. Which word do you hear?", other, heard, say=other, qt="spk_sounds",
          why=f"এবার '{other}'।"),
        S(say[3], qt="spk_sounds"),
        C(q, right, *wrong, qt="spk_sounds", why=why),
        S(say[0], qt="spk_sounds"),
    ]
    return L(slug, band, order, title, title_bn, goal, note_en, note_bn, tip_bn,
             examples=say[:3], errors=errors, video=video, practice=practice, test=test, minutes=12)


LESSONS = [
    # ------------------------------------------------------------------ EASY: the sounds
    P("pr-e1", "easy", 101, "British English: the silent r", "ব্রিটিশ ইংরেজি: নীরব r",
      "Hear and say words like car, water and teacher the British way.",
      "In British English you do not say r at the end of a word or before a consonant: car /kɑː/, "
      "water /ˈwɔːtə/, teacher /ˈtiːtʃə/, bird /bɜːd/. Say r only before a vowel: red, very, carry.",
      "ব্রিটিশ উচ্চারণে শব্দের শেষে বা ব্যঞ্জনের আগে r বলা হয় না: car = 'কা:', water = 'ওয়া:টা'। "
      "r বলুন শুধু স্বরের আগে: red, very।",
      "বাংলায় 'র' সব সময় উচ্চারিত হয়; ব্রিটিশ ইংরেজিতে car, park, teacher-এ r চুপ থাকে।",
      ["My father has a car.", "The teacher drinks water.", "The bird is in the park.", "Her sister is very clever."],
      ("car", "cow"), ("In British English, 'car' ends with…", "a long 'ah' sound", "a strong r sound", "a k sound",
                       "car = /kɑː/ — শেষে লম্বা 'আ:', r নেই।"),
      "BBC Learning English British pronunciation silent r",
      errors=[("water = 'ওয়াটার' (strong r)", "water = /ˈwɔːtə/", "শেষের r বলবেন না।")]),
    P("pr-e2", "easy", 102, "Short vowels: cat, bed, cup", "ছোট স্বর: cat, bed, cup",
      "Tell apart /æ/ (cat), /e/ (bed) and /ʌ/ (cup).",
      "/æ/ in cat, bag, man: open your mouth wide. /e/ in bed, pen, ten: smaller, like a quick 'e'. "
      "/ʌ/ in cup, bus, mum: short and relaxed, in the middle of the mouth.",
      "cat-এ মুখ বেশি খুলুন (অ্যা), bed-এ ছোট 'এ', cup-এ ছোট 'আ'। bus-কে 'বাস' লম্বা করবেন না।",
      "বাংলা 'অ্যা' আর 'এ' কাছাকাছি; ইংরেজিতে man আর men আলাদা শব্দ।",
      ["The cat is on the bed.", "My mum has a red cup.", "Ten men ran to the bus.", "I have a black bag."],
      ("man", "men"), ("Which word has the same vowel as 'cup'?", "bus", "bag", "bed",
                       "cup আর bus — দুটোতেই /ʌ/।"),
      "British Council LearnEnglish Kids short vowel sounds"),
    P("pr-e3", "easy", 103, "Long and short: sheep and ship", "লম্বা ও ছোট: sheep ও ship",
      "Tell apart /iː/ (sheep, see) and /ɪ/ (ship, sit).",
      "/iː/ is long with a smile: see, tree, eat, sheep. /ɪ/ is short and relaxed: sit, ship, big, fish. "
      "The length changes the word: sheep/ship, seat/sit, leave/live.",
      "/iː/ লম্বা 'ঈ' — ঠোঁটে হাসি; /ɪ/ ছোট 'ই'। sheep (ভেড়া) আর ship (জাহাজ) আলাদা।",
      "বাংলায় ই আর ঈ প্রায় এক রকম বলা হয়; ইংরেজিতে দৈর্ঘ্য অর্থ বদলায়।",
      ["I can see a sheep on the ship.", "Please sit in this seat.", "We eat fish and chips.", "The tree is big and green."],
      ("ship", "sheep"), ("Which word has a LONG sound?", "seat", "sit", "fish", "seat = /siːt/ লম্বা।"),
      "BBC Learning English sheep ship pronunciation"),
    P("pr-e4", "easy", 104, "British o: hot and door", "ব্রিটিশ o: hot ও door",
      "Say /ɒ/ (hot, dog) and /ɔː/ (door, ball) the British way.",
      "/ɒ/ is short with round lips: hot, dog, box, shop. It is a British sound (Americans say 'haht'). "
      "/ɔː/ is long and round: door, ball, four, walk, water.",
      "hot, dog — ছোট গোল 'অ' (ঠোঁট গোল)। door, ball, four — লম্বা গোল 'অ:'।",
      "বাংলা 'অ'-এর কাছাকাছি, কিন্তু ঠোঁট গোল করুন। four-এ r বলবেন না: /fɔː/।",
      ["The dog is in the box.", "Four balls are by the door.", "We walk to the shop.", "It is hot in August."],
      ("cot", "caught"), ("'Four' sounds like…", "/fɔː/ with no r", "'four' with a strong r", "'far'",
                          "ব্রিটিশ: four = /fɔː/।"),
      "BBC Learning English short o long o British"),
    P("pr-e5", "easy", 105, "Book and moon", "book ও moon",
      "Tell apart /ʊ/ (book, good) and /uː/ (moon, food).",
      "/ʊ/ is short: book, good, look, put, foot. /uː/ is long with round lips: moon, food, school, blue.",
      "book, good — ছোট 'উ'; moon, food — লম্বা 'ঊ'। book-কে 'বুউক' লম্বা করবেন না।",
      "pull আর pool, full আর fool — দৈর্ঘ্যে অর্থ বদলায়।",
      ["Look at the good book.", "The moon is blue tonight.", "Put your foot on the floor.", "We have food at school."],
      ("full", "fool"), ("Which word has a SHORT sound?", "book", "moon", "food", "book = /bʊk/ ছোট।"),
      "British Council LearnEnglish oo sound book moon"),
    P("pr-e6", "easy", 106, "V and W are different", "V আর W আলাদা",
      "Say /v/ (very, van) and /w/ (wet, window) correctly.",
      "/v/: top teeth touch the bottom lip and buzz — very, van, seven, love. /w/: round your lips like "
      "a kiss, no teeth — wet, window, water, we. Never say 'bhery' for very.",
      "v: ওপরের দাঁত নিচের ঠোঁটে, কম্পন। w: ঠোঁট গোল, দাঁত লাগবে না। very-কে 'ভেরি' (ভ) নয়, 'অয়েরি' নয়।",
      "বাংলায় 'ভ' আর 'ও' মিলে যায়; v ও w আলাদা — আয়নায় দেখে বলুন।",
      ["We have a very big van.", "The window is wet.", "Seven women went west.", "I love warm water."],
      ("vest", "west"), ("For /v/, your top teeth touch…", "your bottom lip", "nothing", "your tongue",
                         "v = দাঁত ঠোঁটে।"),
      "BBC Learning English v and w sounds"),
    P("pr-e7", "easy", 107, "F is not P", "F আর P আলাদা",
      "Say /f/ (fan, coffee) with air through the teeth, not like ফ.",
      "/f/: top teeth on the bottom lip, push air out — fan, fish, coffee, phone. /p/: close both lips "
      "and pop — pan, pen. Bangla ফ is a puff of p; English f is a long hiss.",
      "f: দাঁত ঠোঁটে রেখে বাতাস (ফ্ফ্ফ্)। p: দুই ঠোঁট বন্ধ করে ছাড়ুন। fan আর pan আলাদা।",
      "বাংলা 'ফ' আসলে ঠোঁটের শব্দ; ইংরেজি f দাঁত-ঠোঁটের। phone-এর ph-ও f।",
      ["My father likes coffee.", "The fish is in the pan.", "Five friends phoned me.", "Put the pen on the floor."],
      ("fan", "pan"), ("Which word starts with the /f/ sound?", "phone", "pen", "pin", "ph = f: phone।"),
      "BBC Learning English f and p sounds"),
    P("pr-e8", "easy", 108, "S, Sh and Z", "S, Sh আর Z",
      "Tell apart /s/ (see), /ʃ/ (she) and /z/ (zoo).",
      "/s/ is a hiss: see, sun, bus. /ʃ/ has round lips: she, shop, fish. /z/ is a buzzing s: zoo, "
      "zero, is, his, rose. Say 'zoo', not 'jew'.",
      "s = 'স্স্' হিস; sh = 'শ' ঠোঁট গোল; z = মৌমাছির মতো 'জ্জ্' কম্পন — 'জ' (j) নয়।",
      "বাংলায় z নেই, তাই zoo-কে 'জু' বলা হয়; জিভ নিচে রেখে s-এর মতো, কিন্তু গলায় কম্পন।",
      ["She sells fish at the shop.", "The zoo is open on Sunday.", "His rose is pink.", "Six sheep sit in the sun."],
      ("sip", "ship"), ("Which word has the buzzing /z/?", "zoo", "Sue", "shoe", "zoo = /zuː/।"),
      "BBC Learning English s z sh sounds"),
    P("pr-e9", "easy", 109, "Endings: cats, dogs, buses", "শেষের -s: cats, dogs, buses",
      "Say the plural -s three ways: /s/, /z/ and /ɪz/.",
      "After p, t, k, f: /s/ — cats, books. After most other sounds: /z/ — dogs, bags, trees. "
      "After s, z, sh, ch, ge: an extra syllable /ɪz/ — buses, boxes, watches, oranges. Never drop the s.",
      "cats = 'ক্যাটস', dogs = 'ডগজ', buses = 'বাসিজ'। শেষের s বাদ দেবেন না।",
      "বাংলায় বহুবচনে শব্দের শেষে কিছু যোগ হয় না বলে আমরা s ভুলে যাই — জোরে বলুন।",
      ["I have two cats and three dogs.", "The buses are red.", "She washes the dishes.", "My books are in the boxes."],
      ("buses", "bus"), ("How many syllables in 'boxes'?", "two", "one", "three", "box-es = দুই সিলেবল।"),
      "British Council plural s pronunciation"),
    P("pr-e10", "easy", 110, "Clear ends of words", "শব্দের শেষ স্পষ্ট",
      "Finish every word: hand, desk, old, milk.",
      "English words often end in two consonants: hand, desk, old, milk, best, asked. Say both, "
      "and do not add a vowel after them ('desk', not 'deska').",
      "hand-এর d, desk-এর k বলুন; শেষে 'আ' বা 'ও' যোগ করবেন না।",
      "দ্রুত বললে শেষের ব্যঞ্জন হারিয়ে যায় — ধীরে, স্পষ্ট বলুন।",
      ["Hold my hand.", "The old desk is in the next room.", "I asked for cold milk.", "This is the best test."],
      ("cold", "coal"), ("'Desk' ends with…", "/sk/", "/s/", "/skə/", "desk = /desk/।"),
      "BBC Learning English final consonant clusters"),

    # ------------------------------------------------------------------ MEDIUM: words
    P("pr-m1", "medium", 111, "-ed endings: worked, played, wanted", "-ed: worked, played, wanted",
      "Say past -ed as /t/, /d/ or /ɪd/.",
      "After p, k, f, s, sh, ch: /t/ — worked /wɜːkt/, watched. After voiced sounds: /d/ — played, "
      "lived. After t or d only: an extra syllable /ɪd/ — wanted, needed. 'Worked' is one syllable.",
      "worked = 'ওয়ার্কট' (এক সিলেবল), played = 'প্লেইড', wanted = 'ওয়ান্টিড'। সব -ed-কে 'এড' বলবেন না।",
      "'ওয়ার্কেড' বলা খুব সাধারণ ভুল।",
      ["I worked and then I played.", "She wanted to go home.", "We watched a film and laughed.", "He needed help, so I helped him."],
      ("wanted", "want"), ("How many syllables in 'watched'?", "one", "two", "three", "watched = /wɒtʃt/।"),
      "BBC Learning English ed endings pronunciation"),
    P("pr-m2", "medium", 112, "The schwa /ə/", "স্কোয়া /ə/",
      "Find and say the most common English sound: the weak /ə/.",
      "/ə/ is a short, lazy 'uh'. It is in unstressed syllables: about /əˈbaʊt/, teacher /ˈtiːtʃə/, "
      "banana /bəˈnɑːnə/, today, doctor, London. Spelling does not show it — any vowel can be /ə/.",
      "/ə/ = আলসে ছোট 'আ'। banana = 'বানা:না' নয়, 'বা-না:-না' যেখানে প্রথম আর শেষটা দুর্বল।",
      "আমরা বানান দেখে প্রতিটি স্বর পুরো উচ্চারণ করি; ইংরেজিতে জোরহীন অংশ দুর্বল হয়।",
      ["The doctor is from London.", "Today is a sunny day.", "I want a banana, please.", "My teacher talked about water."],
      ("a", "the"), ("Where is the schwa in 'about'?", "the first sound", "the last sound", "there is none",
                     "about = /əˈbaʊt/ — শুরুর a দুর্বল।"),
      "BBC Learning English schwa sound"),
    P("pr-m3", "medium", 113, "Day, my, boy", "day, my, boy",
      "Glide in the diphthongs /eɪ/, /aɪ/ and /ɔɪ/.",
      "A diphthong moves from one vowel to another: /eɪ/ day, name, rain; /aɪ/ my, time, five; "
      "/ɔɪ/ boy, toy, noise. Glide — 'day' is not 'de'.",
      "day = 'ডেই' (এ থেকে ই-তে যান), my = 'মাই', boy = 'বয়'। name-কে 'নেম' বলবেন না, 'নেইম'।",
      "বাংলায় 'এ' আর 'ও' একক স্বর; ইংরেজিতে day, go দুই-স্বরের মিল।",
      ["My name is Jane.", "The boy has five toys.", "It is time to play in the rain.", "Make a cake today."],
      ("late", "let"), ("'Name' has the sound…", "/eɪ/", "/e/", "/iː/", "name = /neɪm/।"),
      "BBC Learning English diphthongs ei ai oi"),
    P("pr-m4", "medium", 114, "British 'go' and 'now'", "ব্রিটিশ go ও now",
      "Say /əʊ/ (go, home) the British way and /aʊ/ (now, house).",
      "British /əʊ/ starts in the middle of the mouth: go /ɡəʊ/, home, phone, boat — not 'gou' and not "
      "'gō'. /aʊ/ opens wide then rounds: now, house, cow, down.",
      "go = 'গ্যাউ'-এর মতো হালকা (মাঝখান থেকে উ-তে), 'গো' নয়। now = 'নাউ'।",
      "phone-কে 'ফোন' বললে বোঝা যায়, কিন্তু ব্রিটিশ শোনাতে মাঝখান থেকে শুরু করুন।",
      ["Go home now.", "The brown cow is near the house.", "I phoned my mum on the boat.", "Don't shout out loud."],
      ("coat", "caught"), ("British 'home' sounds like…", "/həʊm/", "/hɔːm/", "/huːm/", "home = /həʊm/।"),
      "BBC Learning English diphthong ou British"),
    P("pr-m5", "medium", 115, "Here, there, tour", "here, there, tour",
      "Say /ɪə/ (here), /eə/ (hair) — British sounds with no r.",
      "/ɪə/: here, near, ear, idea. /eə/: hair, there, where, chair, square. No r at the end in British "
      "English: there /ðeə/, near /nɪə/. Many people now say 'sure' and 'tour' with /ɔː/.",
      "here = 'হিআ', there = 'দেআ', chair = 'চেআ' — শেষের r বলবেন না।",
      "where-কে 'হোয়্যার' (জোরালো র) বললে আমেরিকান শোনায়।",
      ["Where is the chair?", "Come over here, near me.", "There is a bear in the square.", "That is a good idea."],
      ("hair", "here"), ("British 'there' ends with…", "/eə/ (no r)", "a strong r", "/iː/", "there = /ðeə/।"),
      "BBC Learning English diphthongs ia ea British"),
    P("pr-m6", "medium", 116, "No extra vowel: school, street", "বাড়তি স্বর নয়: school, street",
      "Start words like school, street and sport without an extra vowel.",
      "Say s + consonant together at the start: school /skuːl/, street /striːt/, sport, small, speak, "
      "station. Do not add a vowel before ('is-school') or between ('sa-treet').",
      "'ইস্কুল', 'ইস্টেশন' নয় — school, station সরাসরি s দিয়ে শুরু।",
      "এটি বাংলাভাষীদের সবচেয়ে চেনা ভুল। আগে 'স্স্স্' লম্বা করে তারপর বাকিটা বলুন।",
      ["I walk to school on this street.", "Speak slowly at the station.", "Small students play sport.", "Stop and stand still."],
      ("sport", "support"), ("Correct way to say 'school':", "/skuːl/", "/ɪsˈkuːl/", "/səˈkuːl/",
                              "school = /skuːl/, আগে 'ই' নয়।"),
      "BBC Learning English consonant clusters s"),
    P("pr-m7", "medium", 117, "Word stress: PREsent or preSENT", "শব্দের জোর: PREsent/preSENT",
      "Put the stress on the right syllable in two-syllable words.",
      "Most two-syllable nouns and adjectives stress the first syllable: TEAcher, HAPpy, PREsent (a gift). "
      "Many two-syllable verbs stress the second: beGIN, deCIDE, preSENT (to give). Wrong stress makes "
      "words hard to understand.",
      "নাম-শব্দে সাধারণত প্রথম অংশে জোর (PREsent = উপহার), ক্রিয়ায় দ্বিতীয়তে (preSENT = উপস্থাপন করা)।",
      "বাংলায় জোর প্রায় সব সময় শুরুতে; ইংরেজিতে জোরের জায়গা বদলায়।",
      ["Here is a present for you.", "She will present her project.", "The lesson begins at nine.", "My teacher is happy."],
      ("REcord", "reCORD"), ("Where is the stress in 'begin'?", "be-GIN", "BE-gin", "both", "verb: beGIN।"),
      "BBC Learning English word stress"),
    P("pr-m8", "medium", 118, "Stress in long words", "লম্বা শব্দের জোর",
      "Stress long words correctly: PHOtograph, phoTOgraphy, photoGRAPHic.",
      "Endings move the stress: PHOtograph → phoTOgraphy → photoGRAPHic. Words ending in -tion, -sion, "
      "-ic stress the syllable before: inforMAtion, deCIsion, ecoNOmic. Listen and copy the strong beat.",
      "-tion, -ic-এর আগের অংশে জোর: inforMAtion, ecoNOmic।",
      "জোরের অংশ জোরে, লম্বা আর একটু উঁচু সুরে; বাকিগুলো দুর্বল (/ə/)।",
      ["I need some information.", "Photography is my hobby.", "It was a difficult decision.", "The economy is important."],
      ("comPUter", "COMputer"), ("Where is the stress in 'information'?", "in-for-MA-tion", "IN-for-ma-tion",
                                  "in-for-ma-TION", "-tion-এর আগে: MA।"),
      "BBC Learning English word stress long words"),
    P("pr-m9", "medium", 119, "Weak words: to, for, of, can", "দুর্বল শব্দ: to, for, of, can",
      "Use the weak forms /tə/, /fə/, /əv/, /kən/ in sentences.",
      "Small grammar words are weak in normal speech: to /tə/, for /fə/, of /əv/, and /ən/, can /kən/, "
      "a /ə/, the /ðə/. 'I can swim' = /aɪ kən swɪm/. Use the strong form only alone or at the end: "
      "'Yes, I can /kæn/.'",
      "বাক্যের ভেতর to = 'টা', for = 'ফা', can = 'কান' (দুর্বল)। শুধু শেষে বা একা হলে পুরো শব্দ।",
      "প্রতিটি শব্দ পুরো জোরে বললে কথা রোবটের মতো শোনায়।",
      ["I want to go for a walk.", "A cup of tea and a piece of cake.", "I can swim. Yes, I can.", "This is for you and your mum."],
      ("can", "can't"), ("In 'I can swim', 'can' is usually…", "weak /kən/", "strong /kæn/", "silent",
                         "বাক্যের ভেতর দুর্বল।"),
      "BBC Learning English weak forms"),
    P("pr-m10", "medium", 120, "The British t", "ব্রিটিশ t",
      "Say a clear British t in water, better and little.",
      "In standard British English, t between vowels is a clear /t/: water /ˈwɔːtə/, better /ˈbetə/, "
      "city, little — not the American 'wader' or 'bedder'. In casual speech you will also hear a "
      "'glottal stop' (wa'er), but learners should use the clear t.",
      "water = 'ওয়া:টা' — t স্পষ্ট, 'ওয়াডার' নয়। better = 'বেটা'।",
      "ইংরেজি t জিভ দাঁতের পেছনের মাড়িতে — বাংলা 'ট'-এর চেয়ে একটু সামনে, আর বাতাসসহ।",
      ["A little bit of water, please.", "This city is better.", "Put the butter on the table.", "It's a beautiful letter."],
      ("writer", "rider"), ("Standard British 'better' sounds like…", "/ˈbetə/", "/ˈbedər/", "/ˈbeːr/",
                            "clear t, শেষে r নেই।"),
      "BBC Learning English British t sound"),

    # ------------------------------------------------------------------ ADVANCED: connected speech
    P("pr-a1", "advanced", 121, "Linking words: pick it up", "শব্দ জোড়া: pick it up",
      "Link a final consonant to the next vowel: an apple, pick it up.",
      "When a word ends in a consonant and the next starts with a vowel, join them: an_apple "
      "(/ə næpl/), pick_it_up (/pɪ kɪ tʌp/), turn_off, fill_in. It sounds smooth and natural.",
      "an apple = 'আ-ন্যাপল' — শব্দ আলাদা করে থামবেন না।",
      "প্রতিটি শব্দের পরে থামলে বলা ধীর ও কাটা কাটা শোনায়।",
      ["Pick it up and put it on.", "I'd like an apple and an orange.", "Turn off the light at eight.", "Fill in this form, please."],
      ("an ice", "a nice"), ("In 'turn off', the n…", "joins the next word", "is silent", "is said twice",
                            "turn_off = 'টা:-নফ'।"),
      "BBC Learning English linking consonant vowel"),
    P("pr-a2", "advanced", 122, "Linking r: far away", "সংযোগী r: far away",
      "Use the British linking r: far_away, here_and there, law and order.",
      "British English drops final r, but says it when the next word begins with a vowel: far /fɑː/ → "
      "far_away /fɑːr əˈweɪ/; here_and there; four_o'clock. Many speakers even add an r between vowels: "
      "law(r) and order, the idea(r) of.",
      "far একা 'ফা:', কিন্তু far away = 'ফা:-রা-ওয়েই' — পরের শব্দ স্বরে শুরু হলে r ফিরে আসে।",
      "এটাই ব্রিটিশ উচ্চারণের একটি পরিচিত বৈশিষ্ট্য।",
      ["My school is far away.", "Come here and sit down.", "It starts at four o'clock.", "Where are you from?"],
      ("far away", "far"), ("In 'four o'clock', the r is…", "said, to link the words", "silent", "rolled",
                            "পরে স্বর থাকলে r বলা হয়।"),
      "BBC Learning English linking r intrusive r"),
    P("pr-a3", "advanced", 123, "Sentence stress", "বাক্যের জোর",
      "Stress the content words in a sentence.",
      "In a sentence, stress the words that carry meaning — nouns, main verbs, adjectives, adverbs, "
      "question words, not: 'I WANT to BUY a NEW BAG.' Grammar words stay weak. Moving the stress changes "
      "the meaning: 'I didn't take your PEN' (I took something else).",
      "অর্থবহ শব্দে জোর দিন (WANT, BUY, NEW, BAG); to, a দুর্বল।",
      "সব শব্দে সমান জোর দিলে শ্রোতা মূল কথা ধরতে পারে না।",
      ["I want to buy a new bag.", "Where did you go on Friday?", "She doesn't like cold tea.", "I didn't take your pen."],
      ("WHERE are you going", "where ARE you going"), ("Which words are stressed in 'I want to buy a new bag'?",
                                                       "want, buy, new, bag", "I, to, a", "all of them",
                                                       "অর্থবহ শব্দে জোর।"),
      "BBC Learning English sentence stress"),
    P("pr-a4", "advanced", 124, "English rhythm", "ইংরেজির ছন্দ",
      "Keep a steady beat: stressed syllables come at regular times.",
      "English is stress-timed: the strong beats come at regular times and the weak syllables squeeze in "
      "between. 'CATS EAT FISH' and 'the CATS will have EATen the FISH' take almost the same time.",
      "জোরালো অংশগুলো তালের মতো সমান দূরত্বে আসে; মাঝের দুর্বল অংশ দ্রুত বলা হয়।",
      "বাংলা সিলেবল-ভিত্তিক — প্রতিটি সিলেবল সমান। ইংরেজিতে হাততালি দিয়ে জোরের তাল অনুশীলন করুন।",
      ["Cats eat fish.", "The cats will have eaten the fish.", "Buy some bread at the shop.", "I'm going to see my friends at the weekend."],
      ("CATS EAT FISH", "the CATS have EATen the FISH"),
      ("English rhythm is based on…", "stressed syllables", "every syllable equally", "the last word",
       "stress-timed: জোরের তাল।"),
      "BBC Learning English rhythm stress timed"),
    P("pr-a5", "advanced", 125, "Falling tune: statements", "নামা সুর: বিবৃতি",
      "Use a falling tune for statements and wh- questions.",
      "Statements and wh- questions usually fall at the end: 'I live in DHAka↘.' 'Where do you LIVE↘?' "
      "A fall sounds sure and finished.",
      "বিবৃতি আর what/where প্রশ্নে শেষে সুর নামে।",
      "শেষে সুর উঁচু রাখলে মনে হয় কথা শেষ হয়নি।",
      ["I live in Dhaka.", "Where do you live?", "What time is it?", "This is my brother."],
      ("Where do you live", "Do you live here"), ("'What's your name?' usually…", "falls at the end",
                                                 "rises at the end", "stays flat", "wh- প্রশ্ন: নামা সুর।"),
      "BBC Learning English intonation falling"),
    P("pr-a6", "advanced", 126, "Rising tune: yes/no questions", "ওঠা সুর: হ্যাঁ/না প্রশ্ন",
      "Use a rising tune for yes/no questions and polite checking.",
      "Yes/no questions usually rise: 'Are you READy↗?' 'Is this your BAG↗?' Question tags fall when you "
      "are sure ('It's cold, isn't it↘') and rise when you really ask ('You're coming, aren't you↗?').",
      "হ্যাঁ/না প্রশ্নে শেষে সুর ওঠে: Are you ready↗?",
      "Question tag: নিশ্চিত হলে নামা সুর, সত্যি জানতে চাইলে ওঠা সুর।",
      ["Are you ready?", "Is this your bag?", "It's cold today, isn't it?", "You're coming, aren't you?"],
      ("ready?", "ready."), ("'Are you hungry?' usually…", "rises at the end", "falls at the end", "has no tune",
                             "yes/no প্রশ্ন: ওঠা সুর।"),
      "BBC Learning English intonation questions"),
    P("pr-a7", "advanced", 127, "Contractions: I'm, don't, we'll", "সংক্ষেপ: I'm, don't, we'll",
      "Use contractions in speech, as British speakers do.",
      "In speech, say I'm, you're, it's, don't, can't /kɑːnt/, won't, we'll, I'd, should've. British can't "
      "has a long /ɑː/: /kɑːnt/. Full forms (I am, do not) sound formal or give emphasis.",
      "কথায় I am নয়, I'm; do not নয়, don't। ব্রিটিশ can't = 'কা:ন্ট' (লম্বা আ)।",
      "সব জায়গায় পুরো রূপ বললে কথা বইয়ের মতো শোনায়।",
      ["I'm sure it's fine.", "I can't come, but she'll be there.", "We don't know where they've gone.", "You should've told me."],
      ("can't", "can"), ("British 'can't' has the vowel…", "/ɑː/ as in car", "/æ/ as in cat", "/e/ as in bed",
                         "can't = /kɑːnt/।"),
      "BBC Learning English contractions pronunciation"),
    P("pr-a8", "advanced", 128, "Lost sounds: next door, last night", "হারানো ধ্বনি: next door",
      "Drop t and d between consonants in fast speech (elision).",
      "In natural speech t and d often disappear between consonants: next door /neks dɔː/, last night "
      "/lɑːs naɪt/, handbag /ˈhæmbæɡ/, sandwich /ˈsænwɪtʃ/, Christmas (no t). This helps you understand "
      "fast English.",
      "দ্রুত কথায় next door = 'নেক্স ডো:', last night = 'লা:স নাইট' — t হারিয়ে যায়।",
      "শুনে বোঝার জন্য এটি খুব জরুরি; নিজে বলার সময় ধীরে বললে t রাখতে পারেন।",
      ["My friend lives next door.", "I went out last night.", "I had a sandwich for lunch.", "She left her handbag."],
      ("next door", "nest door"), ("In fast speech 'last night' often sounds like…", "/lɑːs naɪt/",
                                   "/lɑːst ə naɪt/", "/læst naɪt/", "t বাদ পড়ে।"),
      "BBC Learning English elision"),
    P("pr-a9", "advanced", 129, "Sounds that change: would you", "বদলে যাওয়া ধ্বনি: would you",
      "Hear and use joined sounds like 'would you' /wʊdʒu/.",
      "Neighbouring sounds change each other (assimilation): would you → /wʊdʒu/, did you → /dɪdʒu/, "
      "meet you → /miːtʃu/, ten boys → /tem bɔɪz/, good girl → /ɡʊɡ ɡɜːl/.",
      "would you = 'উজু', did you = 'ডিজু', meet you = 'মিচু' — দ্রুত কথায় এভাবেই শোনায়।",
      "এগুলো জানলে স্থানীয়দের দ্রুত কথা বুঝতে সুবিধা হয়।",
      ["Would you like some tea?", "Did you see that?", "Nice to meet you.", "Could you help me, please?"],
      ("would you", "wood you"), ("'Did you' in fast speech often sounds like…", "/dɪdʒu/", "/dɪd juː/ with a pause",
                                  "/daɪ juː/", "d + y = /dʒ/।"),
      "BBC Learning English assimilation connected speech"),
    P("pr-a10", "advanced", 130, "Speaking at length: chunks and pauses", "লম্বা কথা: খণ্ড ও বিরতি",
      "Speak for a minute clearly: pause between ideas, not inside them (IELTS Speaking).",
      "Divide speech into chunks of meaning and pause between them: 'In my free time | I usually play "
      "cricket | with my friends | near our house.' Stress one key word in each chunk, fall at the end of "
      "an idea, and keep a steady pace. This is what examiners call fluency and pronunciation.",
      "অর্থের খণ্ডে খণ্ডে বলুন, খণ্ডের মাঝখানে নয়, খণ্ডের পরে থামুন।",
      "IELTS-এ উচ্চারণ মানে নিখুঁত অ্যাকসেন্ট নয় — স্পষ্ট, সঠিক জোর ও সুরে বোঝা যায় এমন কথা।",
      ["In my free time, I usually play cricket with my friends.", "My favourite place in Dhaka is the park near our house.",
       "I think learning English is important because it opens many doors.", "Last year, I visited my grandparents in the village."],
      ("in my FREE time", "IN my free TIME"), ("Where should you pause?", "between chunks of meaning",
                                             "after every word", "never", "অর্থের খণ্ডের পরে।"),
      "IELTS Speaking pronunciation chunking British Council"),
]
