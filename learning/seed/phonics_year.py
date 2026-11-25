"""The Phonics Year: 36 weeks x 5 days, from the first letter sound to the end-of-year check.

Weeks 1-12 are Term 1 (Level 0), weeks 13-24 Term 2 (Level 1), weeks 25-36 Term 3 (Level 2).

The ORDER of sounds, spellings and tricky words follows a widely used synthetic-phonics sequence.
Everything else here - stories, actions, words, sentences, reading texts, assessments and
teaching steps - is written by FamilyEnglish. No stories, actions, songs, pictures or worksheets
from any published programme are copied.

Each day is turned into a Lesson by seed_curriculum: the parent view shows a step-by-step guide
(story, steps in Bangla and English), the Bangla note and home task, and the child practises in the app.
"""

from .phonics import GROUPS

# --------------------------------------------------------------------------------------------
# Our own one-minute story for every sound. Rafi (6) and his sister Mina (4) live in Dhaka.
STORIES = {
    "s": "Rafi's bicycle tyre has a tiny hole. The air comes out slowly - sss, sss. Rafi moves his hand down slowly, like the tyre going flat.",
    "a": "Mina finds a big red apple in the market basket. She opens her mouth wide and takes a bite: a, a, a!",
    "t": "Rafi waits for his lunch. He taps the table with one finger: t, t, t. 'Patience!' laughs Grandpa.",
    "i": "Grandma tickles Mina's arm with a soft feather. It itches! Mina scratches it and laughs: i, i, i.",
    "p": "At Rafi's birthday party, Mina claps a balloon between her hands. Pop! p!",
    "n": "Mina asks for a fourth sweet. Mum shakes her head: nnn, no!",
    "ck": "Grandpa comes to visit. He knocks on the door: k, k, k. Rafi runs to open it.",
    "e": "At dinner Mum says, 'Elbows off the table, please!' Rafi taps his elbow and smiles: e, e, e.",
    "h": "It is a hot afternoon in Dhaka. Mina fans her face with her hand and pants: h, h, h.",
    "r": "The family takes a rickshaw to Nani's house. Rafi pretends to pedal: rrr, rrr.",
    "m": "Mum makes mango pudding. Mina tastes it and rubs her cheek: mmm!",
    "d": "At Cox's Bazar, Rafi and Dad dig in the sand to build a sandcastle: d, d, d.",
    "g": "After brushing his teeth, Rafi gargles with water: g, g, g. Mina giggles.",
    "o": "Mina has a little box of beads. She opens the lid and closes it: o, o, o.",
    "u": "Rafi's kite goes up, up, up into the sky: u, u, u!",
    "l": "Mina helps Mum carry the shopping. She lifts a little bag of lentils: l, l, l.",
    "f": "The fan stops when the power goes off. Mina waves a hand fan: fff, fff.",
    "b": "Rafi peels a banana and takes a big bite: b, b, b.",
    "ai": "Rain falls on the tin roof. Mina lets her fingers fall like rain: ai, ai.",
    "j": "Rafi is so happy that he jumps up and down on the spot: j, j, j.",
    "oa": "On the river, the boatman rows the boat with two oars: oa, oa.",
    "ie": "Mina ties her shoelace and pulls the bow tight: ie!",
    "ee": "Grandma takes a photo. 'Smile!' Rafi shows all his teeth: ee!",
    "or": "Mina drops her pencil. 'Where is it?' Rafi points to the floor: or.",
    "z": "It is a cold morning. Rafi zips up his jacket: zzz.",
    "w": "Rafi sees his friend across the road and waves: w, w, w.",
    "ng": "The school bell swings and rings: ng, ng, ng. Time for class!",
    "v": "Rafi wins the race. He makes a V for victory with two fingers: vvv.",
    "oo_long": "At night, Mina points up at the round moon: oo!",
    "oo_short": "Rafi opens his new book and looks at the pictures: oo, oo.",
    "y": "'Do you want some yoghurt?' asks Dad. Mina nods: y, y, yes!",
    "x": "In the playground, Rafi crosses his arms in an X: ks, ks.",
    "ch": "Pepper tickles Mina's nose. She sneezes into her elbow: ch!",
    "sh": "At the beach, the waves come in and go out: shhh, shhh.",
    "th_voiced": "'Which kite is yours?' asks Mina. Rafi points: 'That one, over there!' th, th.",
    "th_unvoiced": "Rafi is three years older than Mina. He shows three fingers: th, th.",
    "qu": "Winter is here. Mina shivers and hugs herself quickly: kw, kw.",
    "ou": "A bird flies into the room! Rafi points out of the window: ou! Out you go!",
    "oi": "Rafi finds a shiny coin under the sofa. 'Oi! Look!' he says, and gives it to Mum: oi, oi.",
    "ue": "Rafi draws a big U in the air with his finger: ue, ue.",
    "er": "The teacher asks a hard question. Rafi scratches his head: er... er...",
    "ar": "From the window at night, Mina points to the brightest star: ar!",
}

# The same stories in Bangla, for parents who prefer to tell them in Bangla (the sound stays English)
STORIES_BN = {
    "s": "রাফির সাইকেলের চাকায় ছোট্ট একটা ছিদ্র। আস্তে আস্তে বাতাস বের হচ্ছে — sss, sss। রাফি চাকা চুপসে যাওয়ার মতো আস্তে হাত নামায়।",
    "a": "মিনা বাজারের ঝুড়িতে একটা বড় লাল আপেল পায়। মুখ বড় করে কামড় দেয়: a, a, a!",
    "t": "রাফি দুপুরের খাবারের অপেক্ষায়। এক আঙুলে টেবিলে টোকা দেয়: t, t, t। দাদা হেসে বলেন, 'ধৈর্য!'",
    "i": "দাদি নরম একটা পালক দিয়ে মিনার হাতে সুড়সুড়ি দেন। চুলকায়! মিনা চুলকায় আর হাসে: i, i, i।",
    "p": "রাফির জন্মদিনে মিনা দুই হাতে বেলুনে তালি দেয়। ফট! p!",
    "n": "মিনা চতুর্থ মিষ্টিটা চায়। আম্মু মাথা নাড়েন: nnn, না!",
    "ck": "দাদা বেড়াতে আসেন। দরজায় টোকা দেন: k, k, k। রাফি দৌড়ে দরজা খোলে।",
    "e": "রাতের খাবারে আম্মু বলেন, 'কনুই টেবিল থেকে নামাও!' রাফি কনুইতে টোকা দিয়ে হাসে: e, e, e।",
    "h": "ঢাকায় গরম দুপুর। মিনা হাত দিয়ে মুখে বাতাস করে আর হাঁপায়: h, h, h।",
    "r": "পরিবার রিকশায় নানুর বাড়ি যায়। রাফি প্যাডেল চালানোর ভান করে: rrr, rrr।",
    "m": "আম্মু আমের পুডিং বানান। মিনা চেখে গালে হাত বোলায়: mmm!",
    "d": "কক্সবাজারে রাফি আর আব্বু বালি খুঁড়ে বালির দুর্গ বানায়: d, d, d।",
    "g": "দাঁত ব্রাশের পর রাফি পানি দিয়ে গার্গল করে: g, g, g। মিনা হাসে।",
    "o": "মিনার একটা ছোট পুঁতির বাক্স আছে। সে ঢাকনা খোলে আর বন্ধ করে: o, o, o।",
    "u": "রাফির ঘুড়ি আকাশে উপরে, উপরে, উপরে ওঠে: u, u, u!",
    "l": "মিনা আম্মুকে বাজারের ব্যাগ বইতে সাহায্য করে। সে ছোট্ট এক ব্যাগ ডাল তোলে: l, l, l।",
    "f": "বিদ্যুৎ চলে গেলে পাখা থেমে যায়। মিনা হাতপাখা নাড়ে: fff, fff।",
    "b": "রাফি কলার খোসা ছাড়িয়ে বড় কামড় দেয়: b, b, b।",
    "ai": "টিনের চালে বৃষ্টি পড়ছে। মিনা আঙুলগুলো বৃষ্টির মতো ঝরায়: ai, ai।",
    "j": "রাফি এত খুশি যে এক জায়গায় লাফাতে থাকে: j, j, j।",
    "oa": "নদীতে মাঝি দুই বৈঠা দিয়ে নৌকা বায়: oa, oa।",
    "ie": "মিনা জুতার ফিতা বাঁধে আর গিঁট শক্ত করে টানে: ie!",
    "ee": "দাদি ছবি তুলবেন। 'হাসো!' রাফি সব দাঁত দেখিয়ে হাসে: ee!",
    "or": "মিনার পেনসিল পড়ে যায়। 'কোথায়?' রাফি মেঝের দিকে দেখায়: or।",
    "z": "শীতের সকাল। রাফি জ্যাকেটের চেইন টানে: zzz।",
    "w": "রাস্তার ওপারে বন্ধুকে দেখে রাফি হাত নাড়ে: w, w, w।",
    "ng": "স্কুলের ঘণ্টা দুলে দুলে বাজে: ng, ng, ng। ক্লাসের সময়!",
    "v": "রাফি দৌড়ে জেতে। দুই আঙুলে বিজয়ের V দেখায়: vvv।",
    "oo_long": "রাতে মিনা আকাশের গোল চাঁদের দিকে দেখায়: oo!",
    "oo_short": "রাফি নতুন বই খুলে ছবি দেখে: oo, oo।",
    "y": "'দই খাবে?' আব্বু জিজ্ঞেস করেন। মিনা মাথা নাড়ে: y, y, হ্যাঁ!",
    "x": "খেলার মাঠে রাফি দুই হাত ক্রস করে X বানায়: ks, ks।",
    "ch": "গোলমরিচে মিনার নাকে সুড়সুড়ি লাগে। সে কনুইয়ে মুখ ঢেকে হাঁচি দেয়: ch!",
    "sh": "সমুদ্রের ধারে ঢেউ আসে আর যায়: shhh, shhh।",
    "th_voiced": "'কোন ঘুড়িটা তোমার?' মিনা জিজ্ঞেস করে। রাফি দেখায়: 'ওইটা, ওখানে!' th, th।",
    "th_unvoiced": "রাফি মিনার চেয়ে তিন বছরের বড়। সে তিন আঙুল দেখায়: th, th।",
    "qu": "শীত এসেছে। মিনা কাঁপতে কাঁপতে দ্রুত নিজেকে জড়িয়ে ধরে: kw, kw।",
    "ou": "ঘরে একটা পাখি ঢুকেছে! রাফি জানালার বাইরে দেখায়: ou! বাইরে যাও!",
    "oi": "রাফি সোফার নিচে একটা চকচকে পয়সা পায়। 'Oi! দেখো!' বলে আম্মুকে দিয়ে দেয়: oi, oi।",
    "ue": "রাফি আঙুল দিয়ে বাতাসে বড় একটা U আঁকে: ue, ue।",
    "er": "শিক্ষক কঠিন প্রশ্ন করেন। রাফি মাথা চুলকায়: er... er...",
    "ar": "রাতে জানালা দিয়ে মিনা সবচেয়ে উজ্জ্বল তারার দিকে দেখায়: ar!",
}

# --------------------------------------------------------------------------------------------
# Word bank: word, emoji, Bangla. Used for pictures and meanings in practice.
_BANK = """
sun ☀️ সূর্য|sat 🪑 বসেছিল|at 📍 -এ|tin 🥫 টিন|pan 🍳 কড়াই|pin 📌 পিন|pit 🕳️ গর্ত|tap 🚰 কল|tip 💡 টিপ|nap 😴 ছোট ঘুম
ant 🐜 পিঁপড়া|nip 🤏 চিমটি|it 👉 এটা|sit 🪑 বসা|cat 🐱 বিড়াল|cap 🧢 টুপি|kit 🎒 সরঞ্জাম|net 🥅 জাল|pen 🖊️ কলম|ten 🔟 দশ
hen 🐔 মুরগি|hat 👒 টুপি|red 🔴 লাল|rat 🐀 ইঁদুর|man 👨 লোক|map 🗺️ মানচিত্র|mat 🧘 মাদুর|dad 👨 বাবা|dig ⛏️ খোঁড়া|den 🏠 গুহা
got ✋ পেল|dog 🐶 কুকুর|pot 🍲 হাঁড়ি|hot 🔥 গরম|mug 🍵 মগ|bus 🚌 বাস|cup ☕ কাপ|leg 🦵 পা|log 🪵 গুঁড়ি|fan 🪭 পাখা
fig 🟣 ডুমুর|bed 🛏️ বিছানা|bat 🦇 বাদুড়|big 🐘 বড়|bag 👜 ব্যাগ|rain 🌧️ বৃষ্টি|tail 🐒 লেজ|jam 🍯 জ্যাম|jet ✈️ জেট|goat 🐐 ছাগল
boat ⛵ নৌকা|coat 🧥 কোট|pie 🥧 পিঠা|tie 👔 টাই|bee 🐝 মৌমাছি|tree 🌳 গাছ|feet 🦶 পা|fork 🍴 কাঁটাচামচ|corn 🌽 ভুট্টা|zip 🤐 চেইন
web 🕸️ জাল|wet 💧 ভেজা|ring 💍 আংটি|king 🤴 রাজা|van 🚐 ভ্যান|moon 🌙 চাঁদ|book 📕 বই|food 🍛 খাবার|cook 👩‍🍳 রান্না|yes ✅ হ্যাঁ
box 📦 বাক্স|fox 🦊 শিয়াল|six 6️⃣ ছয়|chip 🍟 চিপস|ship 🚢 জাহাজ|fish 🐟 মাছ|shop 🏪 দোকান|chin 🧔 থুতনি|this 👇 এটা|thin 📏 পাতলা
queen 👸 রানি|out 🚪 বাইরে|cloud ☁️ মেঘ|coin 🪙 মুদ্রা|oil 🛢️ তেল|her 👧 তার|car 🚗 গাড়ি|star ⭐ তারা|farm 🚜 খামার|jar 🫙 বয়াম
stop 🛑 থামো|spot 🔵 দাগ|snap 📸 ছবি তোলা|slip 🧦 পিছলানো|clap 👏 হাততালি|flag 🚩 পতাকা|blue 🔵 নীল|grab ✊ ধরা|tram 🚋 ট্রাম|drum 🥁 ড্রাম
nest 🪺 বাসা|hand ✋ হাত|lamp 💡 বাতি|milk 🥛 দুধ|desk 🗄️ ডেস্ক|frog 🐸 ব্যাঙ|hill ⛰️ পাহাড়|bell 🔔 ঘণ্টা|puff 💨 ফুঁ|kiss 😘 চুমু
sing 🎤 গান|fishing 🎣 মাছ ধরা|duck 🦆 হাঁস|jump 🦘 লাফ|sock 🧦 মোজা|sunset 🌇 সূর্যাস্ত|picnic 🧺 পিকনিক|rabbit 🐇 খরগোশ|lemon 🍋 লেবু|robot 🤖 রোবট
happy 😊 খুশি|funny 😂 মজার|sunny 🌞 রোদেলা|baby 👶 শিশু|my 👤 আমার|fly 🪰 মাছি|sky 🌌 আকাশ|cry 😢 কান্না|lady 👩 মহিলা|cake 🎂 কেক
gate 🚪 গেট|name 🏷️ নাম|game 🎲 খেলা|these 👇 এগুলো|kite 🪁 ঘুড়ি|bike 🚲 সাইকেল|five 5️⃣ পাঁচ|home 🏠 বাড়ি|nose 👃 নাক|rope 🪢 দড়ি
cube 🧊 ঘনক|tube 🧪 নল|flute 🪈 বাঁশি|day 📅 দিন|play 🎮 খেলা|tray 🍽️ ট্রে|boy 👦 ছেলে|toy 🧸 খেলনা|tea 🍵 চা|leaf 🍃 পাতা
sea 🌊 সমুদ্র|night 🌃 রাত|light 💡 আলো|high ⬆️ উঁচু|snow ❄️ তুষার|bow 🎀 ফিতা|cow 🐄 গরু|owl 🦉 পেঁচা|town 🏙️ শহর|bird 🐦 পাখি
girl 👧 মেয়ে|shirt 👕 শার্ট|nurse 👩‍⚕️ নার্স|turn 🔄 ঘোরা|purse 👛 পার্স|new 🆕 নতুন|grew 🌱 বড় হলো|stew 🍲 স্টু|saw 🪚 করাত|paw 🐾 থাবা
draw ✏️ আঁকা|straw 🥤 স্ট্র|sauce 🥫 সস|launch 🚀 উৎক্ষেপণ|chalk 🖍️ চক|walk 🚶 হাঁটা|ball ⚽ বল|chair 🪑 চেয়ার|hair 💇 চুল|fair 🎡 মেলা
ear 👂 কান|hear 👂 শোনা|year 📆 বছর|bear 🐻 ভালুক|pear 🍐 নাশপাতি|square ⬛ বর্গ|share 🤝 ভাগ করা|phone 📱 ফোন|photo 📷 ছবি|elephant 🐘 হাতি
city 🏙️ শহর|ice 🧊 বরফ|face 😊 মুখ|rice 🍚 ভাত|cycle 🚲 সাইকেল|pencil ✏️ পেনসিল|gem 💎 রত্ন|giant 🧌 দানব|gym 🏋️ জিম|cage 🦜 খাঁচা
page 📄 পাতা|orange 🍊 কমলা|pig 🐷 শূকর|house 🏠 বাড়ি|wolf 🐺 নেকড়ে|straw 🌾 খড়|sticks 🥢 লাঠি|bricks 🧱 ইট|soup 🥣 স্যুপ|chimney 🏭 চিমনি
"""
BANK = {}
for _row in _BANK.replace("\n", "|").split("|"):
    _parts = _row.strip().split(" ", 2)
    if len(_parts) == 3:
        BANK.setdefault(_parts[0], (_parts[1], _parts[2]))


def word(w):
    """(word, emoji, bangla) for a word, with an empty picture if it is not in the bank."""
    e, bn = BANK.get(w, ("", ""))
    return (w, e, bn)


# --------------------------------------------------------------------------------------------
# The 60 tricky words, in the order they are taught (common English words, not owned by anyone)
TRICKY = {
    9: ["I", "the", "he"], 10: ["she", "me", "we"], 11: ["be", "was", "to"], 12: ["do", "are", "all"],
    13: ["you", "your", "come", "some"], 14: ["said", "here", "there", "they"], 15: ["go", "no", "so", "my"],
    19: ["by", "have"], 20: ["down", "like"], 21: ["old", "live"], 22: ["what", "give"], 23: ["one", "little"],
    24: ["only", "when"], 25: ["more", "who"], 26: ["were", "any"], 27: ["other", "where"], 28: ["want", "many"],
    29: ["why", "because"], 30: ["which", "before"], 33: ["put", "two", "could", "does"],
    34: ["their", "saw", "would", "four"], 35: ["right", "should", "made", "goes"],
}

# One of our own example sentences for each tricky word ("___" marks the gap)
TRICKY_SENT = {
    "I": "___ can see a red bus.", "the": "Pat ___ cat.", "he": "Rafi is sad, so ___ sits down.",
    "she": "Mina has a hat. ___ likes it.", "me": "Can you help ___?", "we": "Mum and I said, '___ are here!'",
    "be": "It will ___ hot.", "was": "The dog ___ wet.", "to": "Go ___ bed.", "do": "What can I ___?",
    "are": "We ___ at the shop.", "all": "We ___ clap.", "you": "Can ___ hop?", "your": "Is this ___ bag?",
    "come": "___ and sit here.", "some": "Can I have ___ jam?", "said": "'Stop!' ___ Dad.",
    "here": "Sit ___ with me.", "there": "The cat is over ___.", "they": "Rafi and Mina run. ___ are fast.",
    "go": "Let's ___ to the park.", "no": "Is it wet? ___, it is not.", "so": "It is ___ hot today!",
    "my": "This is ___ book.", "by": "Sit ___ the window.", "have": "I ___ a red kite.",
    "down": "Sit ___, please.", "like": "I ___ mangoes.", "old": "Grandpa is ___.", "live": "We ___ in Dhaka.",
    "what": "___ is your name?", "give": "Can you ___ me a pen?", "one": "I have ___ sister.",
    "little": "Mina is my ___ sister.", "only": "I have ___ one pencil.", "when": "___ is lunch?",
    "more": "Can I have ___ rice?", "who": "___ is at the door?", "were": "We ___ at home.",
    "any": "Is there ___ milk?", "other": "Where is my ___ sock?", "where": "___ is the cat?",
    "want": "I ___ a drink.", "many": "How ___ ducks can you see?", "why": "___ are you sad?",
    "because": "I am happy ___ it is Friday.", "which": "___ cup is yours?", "before": "Wash your hands ___ lunch.",
    "put": "___ the cup on the table.", "two": "I have ___ hands.", "could": "___ you help me?",
    "does": "Where ___ Mina sit?", "their": "The children took ___ bags.", "saw": "I ___ a big ship.",
    "would": "___ you like some tea?", "four": "A cat has ___ legs.", "right": "Turn ___ at the shop.",
    "should": "You ___ brush your teeth.", "made": "Mum ___ a cake.", "goes": "The bus ___ to school.",
}

# --------------------------------------------------------------------------------------------
# Our own short reading texts
TEXTS = {
    "captions": ["a big red bus", "a cat on a mat", "a dog in the sun", "ten hens in a pen"],
    "fold1": ("Tim and the Fish", [
        "Tim has a net.", "Tim and Dad sit by the pond.", "Dad holds Tim's hand. Tim dips the net in.",
        "Is it a fish? No, it is a red sock!", "Tim dips the net again.", "Yes! A big fish! Tim is so glad."]),
    "fold2": ("My Kite", [
        "I have a kite.", "It is red and green.", "My kite goes up, up, up.",
        "Oh no! It is in the tree.", "Dad gets the kite down.", "We go home in the rain."]),
    "comp1": ("The Night Market", [
        "On Friday night, Mina and Dad go to the night market.", "The lights are bright and the air smells of food.",
        "Dad buys hot tea and a bag of peanuts.", "Mina sees a man with a cage of green birds.",
        "'Can we take one home?' she asks. 'No,' says Dad. 'Birds should fly free.'", "They go home under the moon."]),
    "comp2": ("The Little Gardener", [
        "Rafi plants some seeds in a pot by the window.", "Each day he gives them water and puts them in the sun.",
        "After one week, two little green leaves come up.", "'Look, Mina!' he shouts. 'My plants are growing!'",
        "Mina wants to plant some seeds too.", "Now there are four pots on the window."]),
    "pigs": ("The Three Little Pigs", [
        "Once upon a time, three little pigs left home to build their own houses.",
        "The first pig was in a hurry. He built a house of straw.",
        "The second pig built a house of sticks. It was quick, and he went to play.",
        "The third pig worked hard all day. He built a strong house of bricks.",
        "A hungry wolf came to the straw house. He huffed and he puffed and the house fell down! The pig ran to his brother.",
        "The wolf came to the stick house. He huffed and he puffed and that house fell down too! Both pigs ran to the brick house.",
        "The wolf huffed and puffed at the brick house, but it did not fall.",
        "The wolf was tired and hungry, and he sat down outside. The pigs felt sorry for him and gave him some vegetable soup.",
        "'Thank you,' said the wolf. 'I am sorry. I will never blow down a house again.'",
        "From that day, the wolf and the three little pigs were friends, and the strong brick house was a happy home."]),
}


# --------------------------------------------------------------------------------------------
# The weeks. Day: (kind, title, focus, words, extra)
#   kind: sound | blend | tricky | spelling | sort | dictation | reading | game | review | assess1 | assess2 | celebrate
#   words: practice words (strings); extra: dict with sentences / tricky / text / sound keys / spellings
def D(kind, title, focus="", words="", **extra):
    return {"kind": kind, "title": title, "focus": focus, "words": words.split() if words else [], **extra}


def _sound_weeks():
    """Weeks 1-7: one group a week; Monday-Thursday one sound, Friday two sounds."""
    weeks = []
    for g, (g_name, g_sounds, sounds) in enumerate(GROUPS, 1):
        days = []
        for d, idx in enumerate([[0], [1], [2], [3], [4, 5]], 1):
            keys = [sounds[i][0] for i in idx]
            shown = " and ".join(f"/{sounds[i][1]}/" for i in idx)
            days.append(D("sound", f"The sound{'s' if len(idx) > 1 else ''} {shown}", shown, sounds=keys,
                          auditory=(g == 1 and d <= 2)))
        weeks.append({"title": f"{g_name}: {g_sounds}", "title_bn": f"{g_name} — {g_sounds}",
                      "goal": f"Children say, act and write the six sounds {g_sounds} and blend simple words with them.",
                      "days": days})
    return weeks


LATER = {
    8: ("Revision of Groups 1-4 and blends", "দল ১–৪ পুনরাবৃত্তি ও blend",
        "No new sounds. Children revise Groups 1-4 and blend words that start or end with two consonants.",
        [D("blend", "Blends at the start: st, sp, sn, sl", "st sp sn sl", "stop spot snap slip"),
         D("blend", "More start blends: cl, fl, gr, tr, dr", "cl fl gr tr dr", "clap flag grab drum"),
         D("blend", "Blends at the end: st, nd, mp, lk", "st nd mp lk", "nest hand lamp milk"),
         D("reading", "Reading captions", "captions", "bus cat dog hen", text="captions"),
         D("game", "Silent blending and games", "blending games", "frog desk jump stop")]),
    9: ("Revision of Groups 5-7 and first tricky words", "দল ৫–৭ পুনরাবৃত্তি ও প্রথম tricky word",
        "Children revise Groups 5-7, read words with double letters and meet the tricky words I, the and he.",
        [D("tricky", "Double letters and 'I'", "ll ss ff · I", "hill bell puff kiss", tricky=["I"]),
         D("blend", "Word families: -ing, -ish, -ack", "-ing -ish -ack", "ring sing fish fishing"),
         D("tricky", "Word families -ock, -uck, -ump and 'the'", "-ock -uck -ump · the", "sock duck jump", tricky=["the"]),
         D("blend", "Blending boxes", "sound boxes", "ship chip shop chin"),
         D("tricky", "Phrases and 'he'", "phrases · he", "fish ship", tricky=["he"])]),
    10: ("Letter names, capitals and long words", "অক্ষরের নাম, বড় হাতের অক্ষর ও লম্বা শব্দ",
         "Children learn the letter names and capitals, read two-part words and write words from dictation.",
         [D("tricky", "Letter names a-m and 'she'", "letter names a-m · she", "", tricky=["she"], names="abcdefghijklm"),
          D("review", "Letter names n-z and capital letters", "letter names n-z · capitals", "", names="nopqrstuvwxyz"),
          D("tricky", "Long words and 'me'", "two-part words · me", "sunset picnic rabbit lemon", tricky=["me"]),
          D("dictation", "Rhyme and dictation", "rhyme", "cat hat mat rat"),
          D("tricky", "Sentences and 'we'", "sentences · we", "", tricky=["we"], sentences=["we sat in the sun", "the cat is on the bed"])]),
    11: ("Catch-up: making words and games", "পিছিয়ে পড়া পূরণ: শব্দ বানানো ও খেলা",
         "A practice week: making words with letters, word puzzles and games before the end-of-term check.",
         [D("tricky", "Making words and 'be'", "make words · be", "pan pin pen pun", tricky=["be"]),
          D("game", "Anagrams: mixed-up letters", "anagrams", "pot top net ten"),
          D("tricky", "Code words and 'was'", "code words · was", "red bed fed", tricky=["was"]),
          D("dictation", "Sentences with tricky words", "sentences", "", sentences=["I was in bed", "he is in the van"]),
          D("tricky", "Game stations and 'to'", "games · to", "", tricky=["to"])]),
    12: ("End of Term 1: revision and check", "প্রথম টার্ম শেষ: পুনরাবৃত্তি ও মূল্যায়ন",
         "Children learn do, are and all, take dictation of words and sentences, and do the Term 1 check.",
         [D("tricky", "Dictating words and 'do'", "dictation · do", "ship chop moon king", tricky=["do"]),
          D("tricky", "Dictating sentences and 'are'", "sentences · are", "", tricky=["are"], sentences=["we are in the shop", "the fish are wet"]),
          D("assess1", "Term 1 check, part 1: write it", "check 1a", "", check=1),
          D("assess2", "Term 1 check, part 2: read it", "check 1b", "", check=1),
          D("tricky", "Celebration, review and 'all'", "celebrate · all", "", tricky=["all"])]),
    13: ("y as a vowel and tricky words", "স্বরবর্ণ হিসেবে y ও tricky word",
         "y says /ee/ at the end of longer words (happy) and /ie/ at the end of short words (my).",
         [D("tricky", "y says /ee/ and 'you'", "y = /ee/ · you", "happy funny sunny baby", tricky=["you"]),
          D("spelling", "y says /ie/", "y = /ie/", "my fly sky cry"),
          D("tricky", "Sorting y words and 'your'", "sort y · your", "", tricky=["your"], sort=[("/ee/", "happy funny baby lady"), ("/ie/", "my fly sky cry")]),
          D("tricky", "Reading captions and 'come'", "captions · come", "", tricky=["come"], text="captions"),
          D("tricky", "Reading groups and 'some'", "reading · some", "", tricky=["some"])]),
    14: ("Decodable words, a first book and dictation", "পড়ার মতো শব্দ, প্রথম বই ও শ্রুতিলিখন",
         "Children read word lists and their first little book, and write whole sentences from dictation.",
         [D("tricky", "Decodable words and 'said'", "word lists · said", "chip shed moon rain", tricky=["said"]),
          D("tricky", "Mixed word list and 'here'", "mixed words · here", "frog king coat bee", tricky=["here"]),
          D("tricky", "Reading a book: Tim and the Fish, and 'there'", "first book · there", "net boat fish", tricky=["there"], text="fold1"),
          D("tricky", "Dictated sentences and 'they'", "sentences · they", "", tricky=["they"], sentences=["the cat sat on the mat", "they had fish and chips"]),
          D("review", "Reading groups and review", "review", "rain boat feet moon")]),
    15: ("go, no, so, my and tricky word review", "go, no, so, my ও tricky word পুনরাবৃত্তি",
         "Children learn go, no, so and my, read a second little book and review all 24 tricky words so far.",
         [D("tricky", "'go'", "go", "", tricky=["go"]),
          D("tricky", "'no' and 'so'", "no · so", "", tricky=["no", "so"]),
          D("tricky", "Reading a book: My Kite, and 'my'", "second book · my", "kite tree rain", tricky=["my"], text="fold2"),
          D("dictation", "Dictated sentences", "sentences", "", sentences=["no, it is not my hat", "go to bed now"]),
          D("game", "Tricky word games and reading groups", "all 24 tricky words", "", review_tricky=24)]),
    16: ("Magic e: a_e and e_e", "ম্যাজিক e: a_e ও e_e",
         "An e at the end hops back over one letter and makes the vowel say its name: tap becomes tape.",
         [D("spelling", "What magic e does", "tap → tape", "cake gate name game", pairs=["tap tape", "pin pine", "hop hope"]),
          D("spelling", "a_e words", "a_e", "cake gate name game"),
          D("spelling", "e_e words", "e_e", "these", pairs=["pet Pete"]),
          D("review", "Practice with a_e and e_e", "practice", "cake name these game"),
          D("dictation", "Dictation and reading groups", "dictation", "cake gate", sentences=["the cake is on the plate"])]),
    17: ("Magic e: i_e, o_e, u_e", "ম্যাজিক e: i_e, o_e, u_e",
         "Children learn the other magic e spellings (kite, home, cube) and practise all five.",
         [D("spelling", "i_e", "i_e", "kite bike five", pairs=["kit kite", "pin pine"]),
          D("spelling", "o_e", "o_e", "home nose rope", pairs=["hop hope", "not note"]),
          D("spelling", "u_e", "u_e", "cube tube flute", pairs=["cub cube", "tub tube"]),
          D("sort", "All five magic e spellings", "a_e e_e i_e o_e u_e", "", sort=[("a_e", "cake gate"), ("i_e", "kite five"), ("o_e", "home rope"), ("u_e", "cube tube")]),
          D("dictation", "Dictation and reading groups", "dictation", "bike home cube", sentences=["I like my bike", "the rope is at home"])]),
    18: ("Revision and the half-term check", "পুনরাবৃত্তি ও মধ্য-টার্ম মূল্যায়ন",
         "Children revise magic e and y, then do the half-term check.",
         [D("review", "Revise a_e, i_e and y", "a_e i_e y", "cake kite happy fly"),
          D("review", "Revise o_e, u_e and e_e", "o_e u_e e_e", "home cube these"),
          D("assess1", "Half-term check, part 1: write it", "check 2a", "", check=2),
          D("assess2", "Half-term check, part 2: read it", "check 2b", "", check=2),
          D("review", "Reading groups and planning", "reading", "nose flute bike")]),
    19: ("Another way to write it: ay, oy, ea", "আরেক বানান: ay, oy, ea",
         "One sound can be written in more than one way: ay (day), oy (boy) and ea (sea).",
         [D("tricky", "ay says /ai/ and 'by'", "ay = /ai/ · by", "day play tray", tricky=["by"]),
          D("spelling", "oy says /oi/", "oy = /oi/", "boy toy"),
          D("spelling", "ea says /ee/", "ea = /ee/", "tea leaf sea"),
          D("tricky", "Sorting and 'have'", "sort · have", "", tricky=["have"], sort=[("ai", "rain tail"), ("ay", "day play")]),
          D("dictation", "Dictation and reading groups", "dictation", "play boy sea", sentences=["the boy can play in the sea"])]),
    20: ("Another way to write it: igh and ow", "আরেক বানান: igh ও ow",
         "igh says /ie/ (night), and ow has two sounds: /oa/ in snow and /ou/ in cow.",
         [D("spelling", "igh says /ie/", "igh", "night light high"),
          D("spelling", "ow says /oa/", "ow = /oa/", "snow bow"),
          D("tricky", "ow says /ou/ and 'down'", "ow = /ou/ · down", "cow owl town", tricky=["down"]),
          D("tricky", "Which ow? and 'like'", "which ow · like", "", tricky=["like"], sort=[("/oa/ as in snow", "snow bow"), ("/ou/ as in cow", "cow owl town")]),
          D("dictation", "Dictation and reading groups", "dictation", "night cow snow", sentences=["the owl flew at night"])]),
    21: ("The spellings chart, word families and dictation", "বানানের চার্ট, শব্দ-পরিবার ও শ্রুতিলিখন",
         "Children put all the spellings so far on one chart (/ai/ = ai, ay, a_e) and practise word families.",
         [D("tricky", "The spellings chart and 'old'", "chart · old", "rain day cake", tricky=["old"], chart=True),
          D("review", "Word families: -ay, -ight, -ake", "word families", "day play night light cake"),
          D("tricky", "Sentences and 'live'", "sentences · live", "", tricky=["live"], sentences=["we live in a big town"]),
          D("dictation", "Dictation", "dictation", "tray high snow", sentences=["it is a sunny day"]),
          D("game", "Games and reading groups", "games", "boat toy leaf")]),
    22: ("Another way to write it: ir and ur", "আরেক বানান: ir ও ur",
         "/er/ can be written er (her), ir (bird) and ur (turn).",
         [D("tricky", "ir and 'what'", "ir · what", "bird girl shirt", tricky=["what"]),
          D("spelling", "ur", "ur", "nurse turn purse"),
          D("sort", "Sorting er, ir, ur", "er ir ur", "", sort=[("er", "her sister"), ("ir", "bird girl"), ("ur", "turn nurse")]),
          D("tricky", "Dictation and 'give'", "dictation · give", "bird nurse", tricky=["give"], sentences=["the girl has a red shirt"]),
          D("review", "Reading groups", "reading", "shirt purse girl")]),
    23: ("Another way to write it: ew and aw", "আরেক বানান: ew ও aw",
         "ew says /ue/ (new) or /oo/ (grew); aw is another way to write /or/ (draw).",
         [D("spelling", "ew", "ew", "new grew stew"),
          D("spelling", "aw", "aw = /or/", "saw paw draw straw"),
          D("tricky", "Sorting and 'one'", "sort · one", "", tricky=["one"], sort=[("or", "fork corn"), ("aw", "paw draw")]),
          D("tricky", "Dictation and 'little'", "dictation · little", "new paw", tricky=["little"], sentences=["I can draw a little cat"]),
          D("game", "Word activities and reading groups", "word games", "straw stew grew")]),
    24: ("au, al and the end-of-term check", "au, al ও টার্ম শেষের মূল্যায়ন",
         "au and al are two more ways to write /or/ (sauce, chalk). Then the Term 2 check.",
         [D("spelling", "au says /or/", "au", "sauce launch"),
          D("tricky", "al says /or/ and 'only'", "al · only", "chalk walk ball", tricky=["only"]),
          D("assess1", "Term 2 check, part 1: write it", "check 3a", "", check=3),
          D("assess2", "Term 2 check, part 2: read it", "check 3b", "", check=3),
          D("tricky", "Celebration, review and 'when'", "celebrate · when", "", tricky=["when"])]),
    25: ("air and ear", "air ও ear",
         "Two new sounds: air (chair) and ear (hear). In a few words ear says /air/ (bear).",
         [D("spelling", "air", "air", "chair hair fair"),
          D("tricky", "ear and 'more'", "ear · more", "ear hear year", tricky=["more"]),
          D("tricky", "Sentences and 'who'", "sentences · who", "", tricky=["who"], sentences=["who has long hair"]),
          D("spelling", "ear can say /air/", "ear = /air/", "bear pear"),
          D("dictation", "Dictation and reading groups", "dictation", "chair year bear", sentences=["the bear sat on a chair"])]),
    26: ("are and ph", "are ও ph",
         "are is another way to write /air/ (share); ph is another way to write /f/ (phone).",
         [D("spelling", "are says /air/", "are", "square share"),
          D("spelling", "ph says /f/", "ph", "phone photo elephant"),
          D("tricky", "Sorting /air/ and 'were'", "sort · were", "", tricky=["were"], sort=[("air", "chair hair"), ("are", "share square"), ("ear", "bear pear")]),
          D("tricky", "Sentences and 'any'", "sentences · any", "", tricky=["any"], sentences=["is there any milk"]),
          D("dictation", "Dictation and reading groups", "dictation", "phone share", sentences=["I took a photo of an elephant"])]),
    27: ("The spellings chart, questions and dictation", "বানানের চার্ট, প্রশ্ন ও শ্রুতিলিখন",
         "Children add the newest spellings to the chart, read short texts and answer questions about them.",
         [D("tricky", "The chart and 'other'", "chart · other", "bird new draw chair", tricky=["other"], chart=True),
          D("reading", "Reading and answering questions", "reading for meaning", "", text="comp1"),
          D("tricky", "More questions and 'where'", "questions · where", "", tricky=["where"], text="comp1"),
          D("dictation", "Dictation", "dictation", "night share", sentences=["the moon is bright tonight"]),
          D("game", "Games and reading groups", "games", "phone sauce turn")]),
    28: ("Soft c", "নরম c",
         "Before e, i or y, c says /s/ (city, ice, cycle). Before other letters it says /k/ (cat).",
         [D("spelling", "c before e, i, y says /s/", "ce ci cy", "city cycle pencil"),
          D("spelling", "ce at the end", "-ce", "ice face rice"),
          D("tricky", "Word activities and 'want'", "soft c · want", "ice city", tricky=["want"]),
          D("tricky", "Hard or soft c? and 'many'", "hard or soft c · many", "", tricky=["many"], sort=[("/k/", "cat cup car"), ("/s/", "city ice face")]),
          D("dictation", "Dictation and reading groups", "dictation", "face rice", sentences=["I like rice and fish"])]),
    29: ("Soft g", "নরম g",
         "Before e, i or y, g often says /j/ (gem, giant, gym). Some words keep a hard g (get, girl).",
         [D("spelling", "g before e, i, y often says /j/", "ge gi gy", "gem giant gym"),
          D("spelling", "ge at the end", "-ge", "cage page orange"),
          D("tricky", "Hard or soft g? and 'why'", "hard or soft g · why", "", tricky=["why"], sort=[("/g/", "goat bag girl"), ("/j/", "gem giant cage")]),
          D("tricky", "Dictation and 'because'", "dictation · because", "page giant", tricky=["because"], sentences=["the giant is in a cage"]),
          D("review", "Reading groups", "reading", "orange gym gem")]),
    30: ("Revision and the half-term check", "পুনরাবৃত্তি ও মধ্য-টার্ম মূল্যায়ন",
         "Children learn which and before, revise air, ear, are, ph, soft c and g, then do the check.",
         [D("tricky", "Revise air, ear, are, ph and 'which'", "revise · which", "hair hear share phone", tricky=["which"]),
          D("tricky", "Revise soft c and g and 'before'", "revise · before", "city ice gem cage", tricky=["before"]),
          D("assess1", "Half-term check, part 1: write it", "check 4a", "", check=4),
          D("assess2", "Half-term check, part 2: read it", "check 4b", "", check=4),
          D("review", "Reading groups", "reading", "pear photo rice")]),
    31: ("The Three Little Pigs: reading and retelling", "তিনটি ছোট শূকর: পড়া ও আবার বলা",
         "Children hear and read the story, learn the characters, put the events in order and act it out.",
         [D("reading", "Telling the story", "the story", "pig house wolf", text="pigs"),
          D("reading", "The characters", "characters", "pig wolf", text="pigs"),
          D("reading", "Beginning, middle and end", "order", "straw sticks bricks", text="pigs"),
          D("reading", "Reading story sentences", "sentences", "house chimney soup", text="pigs"),
          D("game", "Acting out the story", "drama", "huff puff")]),
    32: ("The Three Little Pigs: writing and counting", "তিনটি ছোট শূকর: লেখা ও গোনা",
         "Children write labels, number sentences and a short retelling, and make a class book.",
         [D("dictation", "Labels", "labels", "pig wolf house straw sticks bricks"),
          D("game", "Cutting practice", "cut and stick", "pig house"),
          D("dictation", "Counting with the pigs", "counting", "", sentences=["three pigs", "one wolf", "three houses"]),
          D("dictation", "Writing a retelling", "retelling", "", sentences=["the wolf huffed and puffed", "the house fell down"]),
          D("reading", "Sharing and a class book", "class book", "", text="pigs")]),
    33: ("Comprehension, writing and tricky words", "বুঝে পড়া, লেখা ও tricky word",
         "Children read for meaning, write on their own and learn put, two, could and does.",
         [D("tricky", "'put' and 'two'", "put · two", "", tricky=["put", "two"]),
          D("reading", "Reading comprehension", "reading for meaning", "", text="comp2"),
          D("tricky", "Spot the difference and 'could'", "could", "", tricky=["could"]),
          D("tricky", "Writing on my own and 'does'", "writing · does", "", tricky=["does"], sentences=["my plant has two leaves"]),
          D("review", "Reading groups and review", "review", "")]),
    34: ("Whole-year spelling revision", "সারা বছরের বানান পুনরাবৃত্তি",
         "Each day revisits one family of spellings from the chart, ready for the end-of-year check.",
         [D("tricky", "Long vowels and 'their'", "ai ee ie oa ue · their", "rain tree night boat cube", tricky=["their"]),
          D("tricky", "/oo/, /or/, /er/, /air/ and 'saw'", "oo or er air · saw", "moon fork bird chair", tricky=["saw"]),
          D("tricky", "Soft c, soft g, ph and 'would'", "c g ph · would", "city gem phone", tricky=["would"]),
          D("tricky", "Dictation and 'four'", "dictation · four", "", tricky=["four"], sentences=["a cat has four legs"]),
          D("game", "Phonics games", "games", "snow paw new")]),
    35: ("The last tricky words and review", "শেষ tricky word ও পুনরাবৃত্তি",
         "Children learn right, should, made and goes, then review all 60 tricky words.",
         [D("tricky", "'right' and 'should'", "right · should", "", tricky=["right", "should"]),
          D("tricky", "'made' and 'goes'", "made · goes", "", tricky=["made", "goes"]),
          D("game", "All 60 tricky words", "60 tricky words", "", review_tricky=60),
          D("dictation", "Practice dictation", "dictation", "", sentences=["the bus goes to town", "mum made a cake"]),
          D("reading", "Choosing a read-aloud book", "reading for fun", "book")]),
    36: ("End-of-year check and celebration", "বছর শেষের মূল্যায়ন ও উদযাপন",
         "Children do the end-of-year check of every sound, spelling and tricky word, then celebrate.",
         [D("assess1", "End-of-year check, part 1: write it", "check 5a", "", check=5),
          D("assess2", "End-of-year check, part 2: read it", "check 5b", "", check=5),
          D("review", "Finishing and looking back", "my year", ""),
          D("celebrate", "Reading celebration", "celebrate", "book"),
          D("celebrate", "Certificates and a party", "well done", "")]),
}

# Our own checks: part 1 = write (dictation), part 2 = read (choose the word)
CHECKS = {
    1: {"write": ["s", "m", "ch", "sh", "sat", "frog", "rain", "the cat is on the bed"],
        "read": [("Which word is 🐟?", "fish", "fish, fan, fun"), ("Which word is 🌙?", "moon", "moon, man, mop"),
                 ("Which word is 🦆?", "duck", "duck, deck, dog"), ("Which word is 👑 for a girl?", "queen", "queen, quit, green"),
                 ("Which is a tricky word?", "the", "the, sat, pin"), ("___ like my dog.", "I", "I, he, me")]},
    2: {"write": ["happy", "fly", "cake", "kite", "home", "cube", "my bike is red", "we ate the cake"],
        "read": [("Which word is 🪁?", "kite", "kite, kit, kick"), ("Which word is 🎂?", "cake", "cake, cat, cap"),
                 ("Which word is 🧊?", "cube", "cube, cub, cup"), ("Which word is 😊?", "happy", "happy, hop, hip"),
                 ("___ said, 'Go to bed.'", "they", "they, there, the"), ("Which word has magic e?", "rope", "rope, rob, rip")]},
    3: {"write": ["day", "boy", "sea", "night", "bird", "nurse", "new", "draw", "the girl saw a cow"],
        "read": [("Which word is 🌃?", "night", "night, nit, net"), ("Which word is 🐦?", "bird", "bird, bed, bud"),
                 ("Which word is 🐄?", "cow", "cow, cot, cap"), ("Which word is 🖍️?", "chalk", "chalk, check, chip"),
                 ("Which spelling is right?", "play", "play, plai, plae"), ("___ is your name?", "what", "what, want, when")]},
    4: {"write": ["chair", "ear", "share", "phone", "city", "face", "gem", "cage", "the bear has a pear"],
        "read": [("Which word is 📱?", "phone", "phone, fone, pone"), ("Which word is 🧊?", "ice", "ice, is, its"),
                 ("Which word is 💎?", "gem", "gem, gum, get"), ("Which word is 🪑?", "chair", "chair, chin, cheer"),
                 ("In 'city', c says…", "/s/", "/s/, /k/, /ch/"), ("___ are you sad?", "why", "why, who, what")]},
    5: {"write": ["thin", "queen", "light", "snow", "turn", "paw", "hair", "orange", "the wolf huffed and puffed", "two pigs ran to the house"],
        "read": [("Which word is 🐘?", "elephant", "elephant, elefant, eliphant"), ("Which word is 🦉?", "owl", "owl, oil, all"),
                 ("Which word is 🥤?", "straw", "straw, stray, stew"), ("Which word is 🍊?", "orange", "orange, oranj, orang"),
                 ("A cat has ___ legs.", "four", "four, for, fore"), ("___ you like some tea?", "would", "would, wood, could"),
                 ("Which word has soft g?", "giant", "giant, goat, girl"), ("Which word has ir?", "shirt", "shirt, short, shut")]},
}


def weeks():
    """All 36 weeks as dicts: number, term, title, title_bn, goal, tricky, days."""
    out = []
    for n, w in enumerate(_sound_weeks(), 1):
        out.append({"n": n, **w})
    for n in range(8, 37):
        t, t_bn, goal, days = LATER[n]
        out.append({"n": n, "title": t, "title_bn": t_bn, "goal": goal, "days": days})
    for w in out:
        w["term"] = 1 if w["n"] <= 12 else 2 if w["n"] <= 24 else 3
        w["tricky"] = TRICKY.get(w["n"], [])
        assert len(w["days"]) == 5, w["n"]
    return out
