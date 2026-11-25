"""British English sounds that Bangla speakers most often find hard, with a short tip in English and Bangla.

Used by "Repeat after me": the target letters of a word are underlined and, when the learner's try is
not recognised, the tip for that sound is shown.
"""

SOUNDS = {
    "æ": ("Open your mouth wide, tongue low and forward — between 'e' in 'bed' and 'a' in 'father'. Not 'এ'.",
          "মুখ বড় করে খুলুন, জিভ নিচে ও সামনে রাখুন — 'এ' আর 'আ'-এর মাঝামাঝি, যেমন cat, man।"),
    "e": ("Short 'e' as in 'bed', 'ten', 'friend' — mouth half open. Not a long 'এ্যা'.",
          "ছোট 'এ', যেমন bed, ten — মুখ অর্ধেক খোলা।"),
    "ɑː": ("A long, open 'aa' from the back of the mouth, as in 'car' — the 'r' is silent in British English.",
           "মুখের পেছন থেকে লম্বা 'আ', যেমন car — ব্রিটিশ উচ্চারণে r বলবেন না।"),
    "ʌ": ("A short, relaxed 'a' as in 'cup', 'mother' — not 'o' and not 'আ'.",
          "ছোট, আলগা 'অ্যা/আ' — cup, mother; 'ও' বলবেন না।"),
    "ɒ": ("Short 'o' with rounded lips, as in 'hot', 'dog' — British, not American 'aa'.",
          "ঠোঁট গোল করে ছোট 'অ', যেমন hot, dog।"),
    "ɔː": ("Long 'aw' with round lips, as in 'door', 'four', 'water'.",
           "ঠোঁট গোল করে লম্বা 'অ:', যেমন door, four।"),
    "ɜː": ("Long sound with relaxed lips, as in 'bird', 'work', 'learn' — no 'r'.",
           "ঠোঁট ঢিলে রেখে লম্বা 'আ:'-এর মতো, যেমন bird, work — r নেই।"),
    "ə": ("The weak 'uh' sound in unstressed syllables: 'a-bout', 'doc-tor', 'sis-ter'. Keep it short and soft.",
          "চাপহীন অংশে খুব ছোট নরম 'অ্যা' — about, doctor, sister।"),
    "iː": ("Long 'ee' with spread lips, as in 'see', 'teacher'. Hold it a little longer than 'ɪ'.",
           "ঠোঁট ছড়িয়ে লম্বা 'ঈ', যেমন see, teacher।"),
    "ɪ": ("Short, relaxed 'i' as in 'sit', 'busy' — shorter than 'ee'.",
          "ছোট, আলগা 'ই', যেমন sit — 'ঈ'-এর চেয়ে ছোট।"),
    "uː": ("Long 'oo' with rounded lips, as in 'food', 'school'.",
           "ঠোঁট গোল করে লম্বা 'ঊ', যেমন food, school।"),
    "ʊ": ("Short, relaxed 'u' as in 'book', 'good', 'put'.",
          "ছোট, আলগা 'উ', যেমন book, good।"),
    "eɪ": ("Glide from 'e' to 'i': 'day', 'name', 'train'. Not a flat 'এ'.",
           "'এ' থেকে 'ই'-তে গড়িয়ে যান: day, name — শুধু 'এ' নয়।"),
    "əʊ": ("British 'o' glides from 'uh' to 'oo': 'go', 'home', 'phone'. Not a flat 'ও'.",
           "'অ্যা' থেকে 'উ'-তে গড়িয়ে: go, home — শুধু 'ও' নয়।"),
    "aɪ": ("Glide from 'a' to 'i': 'my', 'time', 'rice'.", "'আ' থেকে 'ই'-তে: my, time।"),
    "aʊ": ("Glide from 'a' to 'oo': 'now', 'house', 'town'.", "'আ' থেকে 'উ'-তে: now, house।"),
    "ɔɪ": ("Start with a round 'aw' as in 'door', then glide to a short 'i': boy, coin, enjoy.",
           "গোল 'অ' দিয়ে শুরু করে ছোট 'ই'-তে গড়িয়ে যান: boy, coin, enjoy — 'বয়', 'কয়েন'।"),
    "b": ("Close both lips, then open them with your voice on — not 'ভ'.", "দুই ঠোঁট বন্ধ করে গলার স্বরসহ খুলুন — 'ভ' নয়, 'ব'।"),
    "g": ("The back of the tongue touches the soft roof of the mouth, with voice: go, bag.", "জিভের পেছন মুখের নরম ছাদ ছোঁয়, গলার স্বরসহ: go, bag।"),
    "k": ("Like /g/ but only air, with a small puff at the start of a word: cat, kite.", "/g/-এর মতো, কিন্তু শুধু বাতাস; শব্দের শুরুতে হালকা দমকা: cat।"),
    "m": ("Lips together, sound through the nose. Close your lips fully at the end of a word: climb → /klaɪm/.", "ঠোঁট বন্ধ, নাক দিয়ে ধ্বনি। শব্দের শেষে ঠোঁট পুরো বন্ধ করুন।"),
    "n": ("Tongue tip on the ridge behind the top teeth, sound through the nose: know, sun.", "জিভের ডগা ওপরের দাঁতের পেছনের উঁচু জায়গায়, নাক দিয়ে ধ্বনি।"),
    "eə": ("British 'air' sound: 'chair', 'where', 'there' — no 'r' at the end.",
           "chair, where — শেষে r বলবেন না।"),
    "ɪə": ("British 'ear' sound: 'here', 'near', 'idea' — no 'r' at the end.", "here, near — শেষে r নেই।"),
    "θ": ("Put your tongue lightly between your teeth and blow: 'think', 'three', 'bath'. Not 'থ' or 't'.",
          "জিভের ডগা দাঁতের মাঝে হালকা রেখে বাতাস ছাড়ুন: think, three — 'থ' নয়।"),
    "ð": ("Tongue between the teeth, with voice: 'this', 'mother', 'brother'. Not 'দ'.",
          "জিভ দাঁতের মাঝে রেখে গলায় শব্দ করুন: this, mother — 'দ' নয়।"),
    "v": ("Top teeth touch your bottom lip, with voice: 'very', 'van', 'seven'. Not 'ভ' and not 'w'.",
          "ওপরের দাঁত নিচের ঠোঁটে লাগিয়ে গলায় শব্দ: very, seven — 'ভ' বা 'w' নয়।"),
    "w": ("Round your lips like a kiss, then open: 'water', 'window'. Teeth do not touch the lip.",
          "ঠোঁট গোল করে তারপর খুলুন: water, window — দাঁত ঠোঁটে লাগবে না।"),
    "f": ("Top teeth on the bottom lip and blow: 'fish', 'phone', 'coffee'. Not 'ফ' with both lips.",
          "ওপরের দাঁত নিচের ঠোঁটে রেখে বাতাস: fish, phone — দুই ঠোঁটে 'ফ' নয়।"),
    "z": ("Like 's' but with a buzz in your throat: 'zoo', 'busy', 'dogs'. Not 'জ'.",
          "s-এর মতো, তবে গলায় গুনগুন: zoo, busy — 'জ' নয়।"),
    "ʒ": ("A soft buzzing 'sh': 'television', 'usually', 'measure'.", "গুনগুন করা নরম 'শ': television, usually।"),
    "ʃ": ("'sh' with rounded lips: 'shop', 'fish', 'station'. Keep it different from 's'.",
          "ঠোঁট একটু গোল করে 'শ': shop, fish — 'স' থেকে আলাদা।"),
    "s": ("A clean, sharp 's': 'sun', 'bus', 'school'. Not 'শ'.", "পরিষ্কার 'স': sun, school — 'শ' নয়।"),
    "tʃ": ("'ch' as in 'chair', 'teacher', 'watch' — a quick 't' + 'sh'.", "'চ' — chair, teacher।"),
    "dʒ": ("'j' as in 'jam', 'orange', 'bridge' — a quick 'd' + buzzing 'sh'.", "'জ' — jam, orange।"),
    "r": ("British 'r' is only said before a vowel: 'red', 'very'. In 'car', 'water', 'teacher' it is silent.",
          "ব্রিটিশ উচ্চারণে r শুধু স্বরবর্ণের আগে: red, very। car, water-এ r বলবেন না।"),
    "l": ("Tongue tip touches behind the top teeth: 'light', 'milk', 'ball'.", "জিভের ডগা ওপরের দাঁতের পেছনে: light, milk।"),
    "p": ("A strong puff of air at the start: 'pen', 'paper' — not a soft 'প'.",
          "শুরুতে জোরে বাতাস: pen, paper।"),
    "t": ("British 't' with the tongue tip behind the top teeth and a puff of air: 'tea', 'ten' — not 'ট'.",
          "জিভের ডগা দাঁতের পেছনে রেখে বাতাসসহ 't': tea, ten — 'ট' নয়।"),
    "d": ("Tongue tip behind the top teeth: 'day', 'door' — lighter than 'ড'.", "day, door — 'ড'-এর চেয়ে হালকা।"),
    "ŋ": ("'ng' at the back of the mouth, no hard 'g' after it: 'sing', 'morning'.",
          "গলার পেছনে 'ঙ', শেষে g নয়: sing, morning।"),
    "h": ("A soft breath: 'house', 'happy'.", "নরম শ্বাস: house, happy।"),
    "j": ("'y' as in 'yes', 'year', 'university'.", "'ইয়' — yes, year।"),
    "stress": ("Say the strong syllable louder and longer: 'TEA-cher', 'to-MOR-row', 'pho-TO-gra-phy'.",
               "জোরের অংশটি একটু জোরে ও লম্বা বলুন: TEA-cher, to-MOR-row।"),
}

SOUND_NAMES = {k: k for k in SOUNDS}


def tip(sound):
    return SOUNDS.get(sound) or SOUNDS["stress"]


def split_target(marked):
    """'f[a]mily' -> ('family', 'f', 'a', 'mily'). No brackets -> whole word, nothing underlined."""
    if "[" in marked and "]" in marked:
        a, rest = marked.split("[", 1)
        mid, b = rest.split("]", 1)
        return a + mid + b, a, mid, b
    return marked, marked, "", ""
