"""Lessons from the FamilyEnglish Pronunciation Handbook (Lessons 01-23, written for FamilyEnglish).

The handbook PDFs are downloads (course/handouts.py). These app lessons cover the handbook topics
that the 30 British pronunciation lessons did not have yet, so school students and IELTS learners
meet them in their course plan. Topics already in the course (schwa, -ed, weak forms …) link to
their handbook PDF instead of being repeated.
"""

from ._h import C, L, O, S, T
from .pronunciation import P

SKILL = "speaking"

LESSONS = [
    P("pr-h01", "easy", 99, "Pronunciation basics: sounds, symbols and stress", "উচ্চারণের ভিত্তি: ধ্বনি, চিহ্ন ও জোর",
      "Know the three building blocks: vowels, consonants, and stress and rhythm.",
      "English has about 44 sounds but only 26 letters, so we use phonemic symbols between slashes: "
      "shop /ʃɒp/, home /həʊm/. Vowels are monophthongs (one mouth position: /ɒ/ in shop), diphthongs "
      "(a glide: /aʊ/ in house) or triphthongs (/aʊə/ in flower). The mark ː means long: /ɑː/ in garden is "
      "longer than /æ/ in hand. In a sentence, important words are stressed and the small words become weak.",
      "ইংরেজিতে ২৬টি অক্ষর কিন্তু প্রায় ৪৪টি ধ্বনি, তাই / / চিহ্নের ভেতরে ধ্বনি লেখা হয়। ː মানে লম্বা স্বর। "
      "বাক্যে দরকারি শব্দে জোর পড়ে, ছোট শব্দগুলো দুর্বল হয়।",
      "বানান দেখে উচ্চারণ করবেন না — ধ্বনির চিহ্ন দেখে শিখুন।",
      ["Grandma drinks tea every morning.", "The children play in the garden.", "Our house is near the park.",
       "My brother rides his bike to school."],
      ("hand", "garden"), ("What does ː mean in /ɑː/?", "a long sound", "a silent letter", "a stressed word",
                           "ː = লম্বা স্বর, যেমন garden-এর /ɑː/।"),
      "FamilyEnglish pronunciation basics phonemic symbols"),
    P("pr-h02", "easy", 100, "The phonemic chart", "ধ্বনির চার্ট",
      "Read the 44 symbols of British English and say a word for each.",
      "The chart groups the sounds: 12 monophthongs (sea, milk, foot, blue, egg, sofa, girl, four, apple, cup, "
      "star, box), 8 diphthongs (ear, rain, pure, coin, snow, pear, kite, owl) and 24 consonants, most in "
      "voiceless/voiced pairs: /p/–/b/, /t/–/d/, /f/–/v/, /s/–/z/, /θ/–/ð/. Extra symbols: /i/ city, the glottal "
      "stop [ʔ] in button and the dark L [ɫ] in bell. Game: point to a symbol, everyone says a new word with it.",
      "চার্টে ১২টি একক স্বর, ৮টি দ্বিস্বর আর ২৪টি ব্যঞ্জন। বেশিরভাগ ব্যঞ্জন জোড়ায়: কণ্ঠস্বরহীন /p/ আর কণ্ঠস্বরযুক্ত /b/। "
      "চার্টটি পড়ার টেবিলের পাশে লাগিয়ে রাখুন।",
      "গলায় হাত রেখে /s/ আর /z/ বলুন — /z/-তে কম্পন টের পাবেন।",
      ["A girl with a blue cup.", "Three feathers on a yellow chair.", "The mouse ran past the treasure.",
       "Snow is falling on the kite."],
      ("zip", "sip"), ("Which pair is voiceless / voiced?", "/s/ and /z/", "/m/ and /n/", "/l/ and /r/",
                       "/s/ কণ্ঠস্বরহীন, /z/ কণ্ঠস্বরযুক্ত।"),
      "British English phonemic chart 44 sounds"),
    P("pr-h08", "easy", 131, "TH /ð/ or D /d/: there or dare", "TH /ð/ নাকি D /d/: there না dare",
      "Say the, this and there with /ð/ — not with /d/.",
      "For /ð/ put the tip of your tongue lightly between or just behind your top teeth and let the air flow "
      "with your voice on — you can hold it: ðððð. For /d/ the tongue presses the ridge behind the teeth and "
      "the air pops out — you can't hold it. Pairs: there/dare, those/doze, than/Dan, other/udder, worthy/wordy.",
      "/ð/: জিভের ডগা দাঁতের মাঝে, বাতাস চলতে থাকে, গলা কাঁপে (the, this)। /d/: জিভ দাঁতের পেছনের মাড়িতে, "
      "বাতাস হঠাৎ বের হয়। 'দ্য' বা 'ডিস' নয়।",
      "বাংলায় /ð/ নেই, তাই আমরা 'দ' বা 'ড' বলি — জিভ দাঁতের মাঝে রাখার অভ্যাস করুন।",
      ["These are my father's shoes.", "There's a feather on the floor.", "We had bread for dinner.",
       "Those birds fly together every winter."],
      ("there", "dare"), ("Which word starts with /ð/?", "those", "doze", "dinner",
                          "those = /ðəʊz/; doze = /dəʊz/।"),
      "TH sound vs D sound British pronunciation", errors=[("dis", "this", "জিভ দাঁতের মাঝে: /ðɪs/")]),
    P("pr-h13", "easy", 132, "Silent letters: knee, lamb, half", "নীরব অক্ষর: knee, lamb, half",
      "Know the common silent letters and why they are there.",
      "Many letters are written but not said, because pronunciation changed and spelling did not. "
      "kn → /n/: knee, knock, knowledge. wr → /r/: wrap, wrong. mb → /m/: lamb, plumber. l in half, calm, "
      "salmon, could, would. w in answer, sword. t in whistle, fasten, Christmas. c in scissors, science. "
      "h in honour. g in design. b in debt. cupboard = /ˈkʌb.əd/, biscuit = /ˈbɪs.kɪt/.",
      "বানানে আছে কিন্তু উচ্চারণে নেই: knee = 'নী', lamb = 'ল্যাম', half = 'হা:ফ', answer = 'আ:নসা', "
      "cupboard = 'কাবাড'।",
      "বাংলায় যা লেখা তা-ই পড়া হয়, তাই আমরা নীরব অক্ষরও বলে ফেলি।",
      ["Please knock before you come in.", "Cut the apple in half.", "Would you like a biscuit?",
       "The cups are in the cupboard."],
      ("knows", "nose"), ("Which letter is silent in 'answer'?", "w", "a", "r",
                          "answer = /ˈɑːn.sə/ — w নীরব।"),
      "common words with silent letters British English",
      errors=[("cup-board", "cupboard /ˈkʌb.əd/", "p নীরব"), ("k-nife", "knife /naɪf/", "k নীরব")]),
    P("pr-h07", "medium", 133, "Triphthongs: fire, flower, player", "ত্রিস্বর: fire, flower, player",
      "Glide through three vowel sounds: /aɪə/ fire, /aʊə/ flower, /eɪə/ player, /əʊə/ mower, /ɔɪə/ soya.",
      "A triphthong is usually a diphthong + schwa in one smooth movement: /aɪ/ + /ə/ = /aɪə/ (fire, tired, "
      "quiet), /aʊə/ (shower, flower, towel), /eɪə/ (player, greyer), /əʊə/ (mower, lower), /ɔɪə/ (soya, "
      "employer). The r is silent in British English. In fast speech they are often 'smoothed': tyre can sound "
      "like tar.",
      "তিনটি স্বর এক টানে: fire = 'ফাইয়া', flower = 'ফ্লাউয়া', player = 'প্লেইয়া'। শেষে r বলবেন না।",
      "fire-কে 'ফায়ার' বললে r আর দুই সিলেবল হয় — হালকা 'ফাইয়া' বলুন।",
      ["Let's sit by the window.", "I take a shower every morning.", "She picked a flower from the garden.",
       "The library is very quiet."],
      ("flower", "flour"), ("Which word has /aɪə/?", "quiet", "quite", "quit",
                            "quiet = /ˈkwaɪ.ət/; quite = /kwaɪt/।"),
      "how to pronounce triphthongs British English"),
    P("pr-h12", "medium", 134, "Suffixes: -ly, -able, -tion, -ful, -less", "প্রত্যয়: -ly, -able, -tion, -ful, -less",
      "Say suffixes weakly and stress the right syllable.",
      "Suffixes are almost never stressed, so their vowel is weak: -ly /li/ (softly), -able and -ible /ə.bəl/ "
      "(washable, visible — they sound the same), -tion /ʃən/ (information — the stress falls just before "
      "-tion: inforMAtion, eduCAtion), -ful /fəl/ (helpful, peaceful — one l!), -less /ləs/ (careless, endless).",
      "প্রত্যয়ে জোর পড়ে না: helpful = 'হেল্পফ্‌ল', careless = 'কেয়ালাস'। -tion-এর আগের সিলেবলে জোর: "
      "inforMAtion।",
      "'-ফুল', '-লেস', '-শন' পুরো জোরে বলবেন না; দুর্বল রাখুন।",
      ["Grandma speaks softly to the baby.", "This jacket is machine washable.",
       "The information is on the school website.", "My brother is always helpful in the kitchen."],
      ("useful", "useless"), ("Where is the stress in 'education'?", "eduCAtion", "EDucation", "educaTION",
                              "-tion-এর ঠিক আগের সিলেবলে জোর।"),
      "how to pronounce suffixes in English able tion ful less"),
    P("pr-h14", "medium", 135, "Words people often say wrong", "যে শব্দগুলো প্রায় সবাই ভুল বলে",
      "Check yourself on 30 words like queue, sixth, temperature and squirrel.",
      "A pronunciation check-up: say the word, then check. queue /kjuː/, sixth /sɪksθ/, temperature "
      "/ˈtem.prə.tʃə/ (three syllables), specific /spəˈsɪf.ɪk/ (not 'pacific'), mischievous /ˈmɪs.tʃɪ.vəs/ "
      "(not 'mis-chee-vee-ous'), squirrel /ˈskwɪr.əl/, comfortable /ˈkʌmf.tə.bəl/, vegetable /ˈvedʒ.tə.bəl/, "
      "Wednesday /ˈwenz.deɪ/. Tick the ones you got wrong and practise them again tomorrow.",
      "নিজেকে যাচাই করুন: আগে বলুন, তারপর মিলিয়ে দেখুন। Wednesday = 'ওয়েনজডেই', comfortable = 'কামফটাবল', "
      "vegetable = 'ভেজটাবল'।",
      "বানান অনুযায়ী সব অক্ষর বললে এই শব্দগুলো ভুল হয়ে যায়।",
      ["There was a long queue at the bakery.", "It's my sister's sixth birthday.",
       "We eat our vegetables every day.", "This sofa is very comfortable."],
      ("specific", "pacific"), ("How many syllables in 'Wednesday' (British)?", "two", "three", "one",
                                "Wednesday = /ˈwenz.deɪ/ — দুই সিলেবল।"),
      "30 commonly mispronounced English words British",
      errors=[("Wed-nes-day", "Wednesday /ˈwenz.deɪ/", "মাঝের d আর e নীরব"),
              ("pacific (for specific)", "specific /spəˈsɪf.ɪk/", "শুরুতে sp")]),
    P("pr-h18", "advanced", 136, "A British accent: the R, the vowels and the T", "ব্রিটিশ উচ্চারণ: R, স্বর ও T",
      "Know the three biggest differences between British RP and General American.",
      "1) The R: British RP is non-rhotic — no r before a consonant or at the end: star /stɑː/, teacher, north. "
      "2) The vowels: hot /hɒt/ and coffee /ˈkɒf.i/ keep a rounded /ɒ/; in the south bath, dance, ask use long "
      "/ɑː/ (the north uses /æ/ — both are British). 3) The T: no American flap — butter is /ˈbʌt.ə/, not "
      "'budder'; in Modern RP a t before a consonant can be a glottal stop: football [ˈfʊʔ.bɔːl]. Only a small "
      "share of British people speak RP — clarity matters more than any accent.",
      "তিনটি ধাপ: (১) শেষের r নীরব (star = 'স্টা:'), (২) hot = 'হট' গোল ঠোঁটে, bath = 'বা:থ', (৩) butter-এ "
      "স্পষ্ট t, 'বাডার' নয়।",
      "আমেরিকান সিনেমা দেখে আমরা r আর flap T মিশিয়ে ফেলি — একটি উচ্চারণ বেছে নিয়ে মেনে চলুন।",
      ["My sister is a teacher.", "Would you like a hot coffee?", "We had a bath after the dance.",
       "Put some butter on the bread."],
      ("cot", "cut"), ("In British RP, 'car' ends with…", "no r sound", "a strong r", "a t sound",
                       "British RP non-rhotic: car = /kɑː/।"),
      "RP and Modern RP British accent R vowels T"),
    L("pr-h19", "advanced", 137, "Shadowing a story: The New Puppy", "গল্প ছায়ার মতো বলা: The New Puppy",
      "Use the shadowing technique to copy sounds, stress and rhythm.",
      "Shadowing: listen to a sentence and say it at the same time, like a shadow — or pause and repeat. Copy "
      "the stress, the rhythm and the tune, not just the words. Notice the weak forms: has a /həz ə/, and /ən/, "
      "to /tə/, and the linking r: after a /ˈɑːftər ə/, under a /ˈʌndər ə/.",
      "শ্যাডোয়িং: শুনুন আর সাথে সাথে একই সুরে বলুন। শুধু শব্দ নয়, জোর, ছন্দ আর সুর নকল করুন।",
      "প্রথমে প্রতিটি বাক্যের পরে থেমে বলুন, তারপর একসাথে বলার চেষ্টা করুন।",
      examples=["Sam's family has a new puppy.", "Then they play in the garden.", "Biscuit loves to run after a red ball."],
      passage=("Sam's family has a new puppy. His name is Biscuit. He is small and brown, with big soft ears. "
               "Every morning, Sam gives him food and fresh water. Then they play in the garden. Biscuit loves to "
               "run after a red ball. One day, the ball went under a bush. Biscuit looked and looked, but he could "
               "not find it. Sam laughed and helped him. Now they are best friends."),
      passage_title="The New Puppy",
      video="shadowing technique English pronunciation practice",
      practice=[S("Sam's family has a new puppy.", why="has a = /həz ə/ — দুর্বল।", qt="spk_sentence"),
                S("Every morning, Sam gives him food and fresh water.", why="gives him = /ɡɪvz ɪm/ — h পড়ে যায়।"),
                C("In 'after a red ball', after a sounds like…", "/ˈɑːftər ə/", "/ˈæftə eɪ/", "/ˈɑːf ə/",
                  why="শব্দের শেষে r আর পরের শব্দ স্বর দিয়ে শুরু হলে r ফিরে আসে (linking r)।", qt="spk_sounds"),
                S("Sam laughed and helped him.", why="laughed = /lɑːft/, helped = /helpt/ — এক সিলেবল।")],
      test=[S("His name is Biscuit."), S("Then they play in the garden."), S("Now they are best friends."),
            C("Which word in 'Biscuit loves to run' is weak?", "to", "loves", "run",
              why="to = /tə/।", qt="spk_sounds"),
            S("One day, the ball went under a bush.", why="under a = /ˈʌndər ə/ — linking r।")],
      minutes=15),
    L("pr-h20", "advanced", 138, "Reading a phonemic transcription: The Lion and the Mouse",
      "ধ্বনিলিপি পড়া: The Lion and the Mouse",
      "Read a whole story in phonemic symbols and hear weak forms, linking r and dropped h.",
      "A transcription shows how we really speak. In the fable: and = /ən/, to = /tə/, of = /əv/, was = /wəz/; "
      "his and him lose the h after another word (his paw /ɪz pɔː/, woke him up /wəʊk ɪm ʌp/); a linking r "
      "appears between vowels (creature ever /ˈkriːtʃər ˈevə/). ‖ marks the end of a sentence.",
      "ধ্বনিলিপিতে দেখা যায় আমরা আসলে কীভাবে বলি: and = /ən/, to = /tə/, his-এর h পড়ে যায়।",
      "প্রথমে সাধারণ লেখা পড়ুন, তারপর ধ্বনিলিপি দেখে আবার পড়ুন।",
      examples=["A little mouse ran across his paw.", "Please let me go.", "Even a mouse can help a lion."],
      passage=("One hot afternoon, a lion was sleeping in the shade of a tree. A little mouse ran across his paw "
               "and woke him up. The lion was cross, and he caught the mouse in his big paw. \"Please let me go,\" "
               "said the mouse. \"One day, I might be able to help you.\" The lion laughed, but he let the mouse go. "
               "A few days later, the lion was caught in a net. The mouse heard him and came running. She chewed "
               "through the ropes until the lion was free. \"You laughed at me,\" said the mouse, \"but now you know "
               "that even a mouse can help a lion.\"\n\n"
               "/wʌn hɒt ˌɑːftəˈnuːn ə ˈlaɪən wəz ˈsliːpɪŋ ɪn ðə ʃeɪd əv ə triː ‖ ə ˈlɪtəl maʊs ræn əˈkrɒs ɪz pɔːr "
               "ən wəʊk ɪm ʌp ‖/"),
      passage_title="The Lion and the Mouse",
      video="phonemic transcription reading practice British English",
      practice=[C("In the transcription, 'and' is written…", "/ən/", "/ænd/", "/end/", why="দুর্বল রূপ /ən/।", qt="spk_sounds"),
                C("'woke him up' is said…", "/wəʊk ɪm ʌp/", "/wəʊk hɪm ʌp/", "/wɒk hɪm ʌp/",
                  why="him-এর h পড়ে যায় আর শব্দগুলো জুড়ে যায়।", qt="spk_sounds"),
                S("A little mouse ran across his paw."), S("Please let me go.")],
      test=[S("Even a mouse can help a lion."),
            C("Which symbol marks the end of a sentence?", "‖", "ː", "ˈ", why="‖ = বড় বিরতি।", qt="spk_sounds"),
            S("The lion laughed, but he let the mouse go."),
            C("In 'creature ever', the r is…", "said, to link the two vowels", "always silent", "said as /d/",
              why="linking r: /ˈkriːtʃər ˈevə/।", qt="spk_sounds"),
            S("She chewed through the ropes until the lion was free.")],
      minutes=15),
    L("pr-h21", "advanced", 139, "Connected speech: The North Wind and the Sun", "জোড়া কথা: The North Wind and the Sun",
      "Find catenation, elision, assimilation, intrusion and the glottal stop in a real text.",
      "Five features of fast, natural speech: catenation (came‿along), elision — a /t/ or /d/ between consonants "
      "disappears (firs(t) succeeded), assimilation — a sound copies its neighbour (in making → /ɪm ˈmeɪkɪŋ/), "
      "intrusion — an extra /r/, /w/ or /j/ between vowels (blew‿w‿as, the‿j‿other), and the glottal stop "
      "(tha[ʔ] the). H-dropping in weak pronouns: take his /teɪk‿ɪz/.",
      "দ্রুত কথায় শব্দ জোড়া লাগে, কিছু ধ্বনি হারায় বা বদলায়, আর স্বরের মাঝে /r/, /w/, /j/ ঢুকে পড়ে।",
      "পুরো গল্পটি একবার স্বাভাবিকভাবে পড়ুন, তারপর চিহ্নগুলো দেখে আবার পড়ুন।",
      examples=["A traveller came along wrapped in a warm cloak.", "The North Wind blew as hard as he could.",
                "The traveller took off his cloak."],
      passage=("The North Wind and the Sun were disputing which was the stronger, when a traveller came along "
               "wrapped in a warm cloak. They agreed that the one who first succeeded in making the traveller take "
               "his cloak off should be considered stronger than the other. Then the North Wind blew as hard as he "
               "could, but the more he blew, the more closely did the traveller fold his cloak around him; and at "
               "last the North Wind gave up the attempt. Then the Sun shone out warmly, and immediately the traveller "
               "took off his cloak. And so the North Wind was obliged to confess that the Sun was the stronger of the two."),
      passage_title="The North Wind and the Sun (Aesop)",
      video="connected speech elision assimilation linking British English",
      practice=[C("'came along' joins as /keɪm‿əˈlɒŋ/. This is…", "catenation", "elision", "assimilation",
                  why="শেষের ব্যঞ্জন পরের শব্দের স্বরে জুড়ে যায়।", qt="spk_sounds"),
                C("'in making' → /ɪm ˈmeɪkɪŋ/. This is…", "assimilation", "intrusion", "catenation",
                  why="n পাশের m-এর মতো হয়ে যায়।", qt="spk_sounds"),
                C("'blew as' → /bluː‿wəz/. The extra /w/ is…", "intrusion", "elision", "a glottal stop",
                  why="দুই স্বরের মাঝে /w/ ঢোকে।", qt="spk_sounds"),
                S("A traveller came along wrapped in a warm cloak.")],
      test=[S("The North Wind blew as hard as he could."),
            C("'first succeeded' → /fɜːs səkˈsiːdɪd/. The /t/ is lost by…", "elision", "intrusion", "assimilation",
              why="দুই ব্যঞ্জনের মাঝে /t/ হারায়।", qt="spk_sounds"),
            S("The Sun shone out warmly."),
            C("'the other' → /ði‿jʌðə/. The extra /j/ is…", "intrusion", "elision", "catenation",
              why="the-এর /i/ আর other-এর স্বরের মাঝে /j/।", qt="spk_sounds"),
            S("They agreed that the one who first succeeded should be considered stronger.")],
      minutes=18),
]

# Lessons that belong to other skills
EXTRA = [
    ("grammar", L("gr-all-tenses", "medium", 140, "All the tenses A1–B2: a map", "সব কাল A1–B2: এক নজরে",
     "See the ten key tenses side by side and choose the right one.",
     "Present continuous: now (Grandma is watering the plants). Present simple: habits and facts (She walks to "
     "school). Past simple: finished past (We visited Sylhet last year). Past continuous: in progress in the past "
     "(I was cooking when you called). Present perfect: past with a link to now (I've lost my keys). Past perfect: "
     "earlier past (The film had started when we arrived). Past perfect continuous: how long before a past moment "
     "(She had been waiting for an hour). Will: decisions now and predictions. Going to: plans and evidence. "
     "Present tenses for the future: timetables (The bus leaves at six) and arrangements (I'm meeting Rina tomorrow).",
     "দশটি কাল একসাথে: এখন = present continuous, অভ্যাস = present simple, শেষ হওয়া অতীত = past simple, "
     "অতীতে চলছিল = past continuous, অতীত যার ফল এখন আছে = present perfect, অতীতেরও আগে = past perfect, "
     "ভবিষ্যৎ = will / going to / present।",
     "উচ্চারণ টিপ: past -ed তিনভাবে: worked /t/, played /d/, wanted /ɪd/।",
     examples=["Grandma is watering the plants.", "I've lost my keys.", "The bus leaves at six."],
     video="all English tenses A1 B2 explained",
     practice=[C("Right now, Dad ___ dinner.", "is cooking", "cooks", "cooked", why="এখন চলছে = present continuous।", qt="gr_tense"),
               C("We ___ Sylhet last year.", "visited", "have visited", "visit", why="last year = past simple।", qt="gr_tense"),
               C("I ___ my keys — I can't open the door.", "have lost", "lost", "was losing",
                 why="অতীতের কাজ, ফল এখন = present perfect।", qt="gr_tense"),
               T("The film ___ (start) when we arrived.", "had started", why="আগের অতীত = past perfect।", qt="gr_tense")],
     test=[C("Look at those clouds! It ___ rain.", "is going to", "will", "rains", why="দেখে বোঝা যায় = going to।", qt="gr_tense"),
           C("I ___ when you called.", "was cooking", "cooked", "am cooking", why="অতীতে চলছিল।", qt="gr_tense"),
           C("The train ___ at 6 tomorrow.", "leaves", "is leaving to", "left", why="সময়সূচি = present simple।", qt="gr_tense"),
           T("She ___ (wait) for an hour before the bus came.", "had been waiting", why="past perfect continuous।", qt="gr_tense"),
           C("I think it ___ sunny tomorrow.", "will be", "is being", "was", why="মতামত/ভবিষ্যদ্বাণী = will।", qt="gr_tense")],
     minutes=20)),
    ("reading", L("rd-family-qa", "advanced", 141, "Reading: learning English as a family (B2+ words)",
     "পড়া: পরিবারে ইংরেজি শেখা (B2+ শব্দ)",
     "Read a Q&A and learn 20 useful B2+ words like consistent, reluctant and milestone.",
     "Key words: compile (collect and organise), routine, immersion, spontaneous, accent, consistent, milestone, "
     "strategy, overwhelmed, bilingual, mimic, reluctant, feedback, fluency, misconception, identity, heritage, "
     "clarity, hypothetical, gradually.",
     "B2+ শব্দ: consistent = নিয়মিত একইভাবে, reluctant = অনিচ্ছুক, milestone = গুরুত্বপূর্ণ ধাপ, "
     "overwhelmed = অনেক চাপে দিশেহারা, mimic = নকল করা।",
     "নতুন শব্দ পড়ে জোরে বলুন, তারপর নিজের বাক্যে ব্যবহার করুন।",
     passage=("Q: Why did you start FamilyEnglish?\nA: As a teacher, I noticed that many of my students had excellent "
              "grammar but felt overwhelmed when they had to speak. Their biggest problem was pronunciation. I wanted "
              "to compile clear, simple lessons that whole families could use at home.\n\n"
              "Q: What's the best way for parents to help their children?\nA: Be consistent. Ten minutes every day is "
              "better than two hours once a month. Build English into your routine - songs in the car, a bedtime "
              "story, naming things while you cook. Children love to mimic, so let them copy you, and give "
              "encouraging feedback rather than correcting every mistake.\n\n"
              "Q: My teenager is reluctant to speak. What should I do?\nA: Don't force it. Let them listen first - "
              "immersion through films and music builds confidence gradually. Celebrate every milestone, however "
              "small. Spontaneous conversations often come when there's no pressure.\n\n"
              "Q: Should we try to sound British or American?\nA: It's a common misconception that you need a "
              "'perfect' native accent. Your accent is part of your identity and your heritage. Aim for clarity and "
              "fluency, not perfection.\n\n"
              "Q: What if a family has only five minutes a day?\nA: In that hypothetical situation, my strategy would "
              "be one minute of listening, two minutes of shadowing and two minutes of talking about your day."),
     passage_title="A FamilyEnglish Q&A",
     practice=[C("'Consistent' means…", "always doing something in the same way", "very fast", "not planned",
                 why="consistent = নিয়মিত, একইভাবে।", qt="rd_vocab"),
               C("Why was FamilyEnglish started?", "Students had good grammar but people couldn't understand them",
                 "Grammar lessons were too short", "Families didn't want to learn together",
                 why="প্রথম উত্তরে বলা আছে।", qt="rd_detail"),
               C("What is the main advice for parents?", "Practise a little every day", "Correct every mistake",
                 "Study two hours a month", why="Ten minutes every day…", qt="rd_detail"),
               T("A word that means 'not wanting to do something': r_______", "reluctant", qt="rd_vocab")],
     test=[C("What does the writer suggest for a reluctant teenager?", "Let them listen first",
             "Make them speak in front of guests", "Stop English", why="Don't force it…", qt="rd_detail"),
           C("The writer's view on accents:", "Clarity matters more than a native accent", "Everyone should sound British",
             "Accents stop communication", why="Aim for clarity and fluency.", qt="rd_detail"),
           C("'Spontaneous' means…", "not planned", "very loud", "difficult", why="spontaneous = হঠাৎ, পরিকল্পনা ছাড়া।", qt="rd_vocab"),
           C("How should five minutes be used?", "Listening, shadowing and talking", "Only grammar", "Only films",
             why="শেষ উত্তরে।", qt="rd_detail"),
           T("A word that means 'to copy the way someone speaks': m____", "mimic", qt="rd_vocab")],
     minutes=20)),
]
