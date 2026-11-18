"""Placement question bank.

phonics (Levels 0-2): the browser says the word; the child taps a picture or a word.
listening / reading / writing (Levels 3-8): one question per level.
Format: (skill, level, prompt, spoken, picture, "choice1, choice2, choice3", answer)
"""

PLACEMENT = [
    # Level 0 — letter sounds (tap the picture that starts with the sound)
    ("phonics", 0, "Listen. Tap the picture that starts with this sound.", "sss", "", "☀️ sun, 🐶 dog, 🍎 apple", "☀️ sun"),
    ("phonics", 0, "Listen. Tap the picture that starts with this sound.", "mmm", "", "🐸 frog, 🗺️ map, 🚌 bus", "🗺️ map"),
    ("phonics", 0, "Listen. Tap the picture that starts with this sound.", "p", "", "🐷 pig, 🐟 fish, 🥚 egg", "🐷 pig"),
    # Level 1 — blending simple words
    ("phonics", 1, "Listen to the sounds. Which word is it?", "c. a. t.", "", "cat, cut, cot", "cat"),
    ("phonics", 1, "Listen. Tap the word you hear.", "ship", "", "chip, ship, shop", "ship"),
    ("phonics", 1, "Listen. Tap the word you hear.", "dog", "", "dig, dog, dug", "dog"),
    # Level 2 — blends and long vowels
    ("phonics", 2, "Listen. Tap the word you hear.", "frog", "", "fog, frog, from", "frog"),
    ("phonics", 2, "Listen. Tap the word you hear.", "kite", "", "kit, kite, cat", "kite"),
    ("phonics", 2, "Listen. Tap the word you hear.", "boat", "", "bat, boot, boat", "boat"),

    # Listening, Levels 3-8 (the browser reads the sentence aloud)
    ("listening", 3, "What did you hear?", "It's a red apple.", "🍎", "a red apple, a green apple, a red ball", "a red apple"),
    ("listening", 4, "What time does Mina get up?", "Mina gets up at seven o'clock and goes to school at eight.", "⏰", "7 o'clock, 8 o'clock, 11 o'clock", "7 o'clock"),
    ("listening", 5, "Where did they go last Friday?", "Last Friday we didn't go to the park because it rained, so we visited my grandmother.", "", "the park, grandmother's house, the market", "grandmother's house"),
    ("listening", 6, "Why is the speaker late?", "Sorry I'm late. The bus broke down, so I had to walk the last two kilometres.", "", "The bus broke down., He woke up late., He forgot the time.", "The bus broke down."),
    ("listening", 7, "What is the speaker's main point?", "While online classes are convenient, they can't fully replace the motivation that comes from learning alongside classmates.", "", "Online classes can't fully replace classroom motivation., Online classes are always better., Classmates are not important.", "Online classes can't fully replace classroom motivation."),
    ("listening", 8, "What does the speaker imply?", "Had the council acted on the warnings sooner, the flooding might have been far less severe.", "", "The council acted too late., The council prevented the flooding., There were no warnings.", "The council acted too late."),

    # Reading, Levels 3-8
    ("reading", 3, "Read: 'This is my cat. It is black.' What colour is the cat?", "", "🐈‍⬛", "black, white, red", "black"),
    ("reading", 4, "Read: 'Rafi lives in Dhaka. He goes to school by rickshaw.' How does Rafi go to school?", "", "", "by rickshaw, by bus, on foot", "by rickshaw"),
    ("reading", 5, "Read: 'The shop was closed, so Nila bought bread from the market instead.' Where did Nila buy bread?", "", "", "at the market, at the shop, at home", "at the market"),
    ("reading", 6, "Read: 'Despite the heavy rain, the match went ahead as planned.' What happened to the match?", "", "", "It was played., It was cancelled., It was moved.", "It was played."),
    ("reading", 7, "Read: 'The new policy, although well-intentioned, has had several unintended consequences.' The writer thinks the policy …", "", "", "had some bad results it didn't expect, was a total success, was badly intended", "had some bad results it didn't expect"),
    ("reading", 8, "Read: 'Far from being a panacea, technology merely amplifies existing educational practices.' The writer believes technology …", "", "", "is not a cure for everything, solves all problems, is useless", "is not a cure for everything"),

    # Writing / grammar, Levels 3-8 (choose the correct word)
    ("writing", 3, "Choose the correct word: 'I ___ a boy.'", "", "", "am, is, are", "am"),
    ("writing", 4, "Choose the correct word: 'She ___ to school every day.'", "", "", "goes, go, going", "goes"),
    ("writing", 5, "Choose the correct word: 'Yesterday we ___ a film.'", "", "", "watched, watch, watching", "watched"),
    ("writing", 6, "Choose the correct word: 'I have lived here ___ ten years.'", "", "", "for, since, from", "for"),
    ("writing", 7, "Choose the correct word: 'If I ___ more time, I would learn French.'", "", "", "had, have, will have", "had"),
    ("writing", 8, "Choose the correct word: 'Not only ___ late, but he also forgot the tickets.'", "", "", "was he, he was, he is", "was he"),
]
