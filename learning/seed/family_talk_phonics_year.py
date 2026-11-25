"""'Talk at home' for the Phonics Year weeks 8-36 (weeks 1-7 use the sound talks in family_talk_phonics).

Each week's five lessons share one set. A string means: reuse the set of that existing lesson title.
Order in every list: Sister, Brother, Mamma, Daddy, Grandma, Grandpa. (Me says, they say, Bangla, Bangla)
"""

NEW = {
    "y as a vowel": [
        ("I am so happy today!", "Why are you happy?", "আজ আমি খুব খুশি!", "তুমি খুশি কেন?"),
        ("Look, a fly in the sky!", "Shoo, fly, shoo!", "দেখো, আকাশে মাছি!", "যাও মাছি, যাও!"),
        ("Mamma, the baby is crying.", "Let me pick her up.", "আম্মু, বাবুটা কাঁদছে।", "দাও, আমি কোলে নিই।"),
        ("Daddy, it is a sunny day.", "Let's go to the park.", "আব্বু, আজ রোদেলা দিন।", "চলো পার্কে যাই।"),
        ("Grandma, that is so funny!", "You make me laugh too.", "দাদি, এটা খুব মজার!", "তুমিও আমাকে হাসাও।"),
        ("Grandpa, why is the sky blue?", "Good question! Let's find out.", "দাদা, আকাশ নীল কেন?", "ভালো প্রশ্ন! চলো জেনে নিই।"),
    ],
    "ir and ur": [
        ("Look at that little bird!", "It is a brown bird.", "ওই ছোট্ট পাখিটা দেখো!", "এটা বাদামি পাখি।"),
        ("It is my turn now.", "OK, your turn.", "এখন আমার পালা।", "ঠিক আছে, তোমার পালা।"),
        ("Mamma, my shirt is dirty.", "Put it in the wash.", "আম্মু, আমার শার্ট ময়লা।", "ধোয়ার জন্য রেখে দাও।"),
        ("Daddy, I want to be a nurse.", "You will be a kind nurse.", "আব্বু, আমি নার্স হতে চাই।", "তুমি দয়ালু নার্স হবে।"),
        ("Grandma, I was first in the race!", "First! Well done, girl!", "দাদি, আমি দৌড়ে প্রথম হয়েছি!", "প্রথম! খুব ভালো!"),
        ("Grandpa, where is your purse?", "It is on the shelf.", "দাদা, তোমার মানিব্যাগ কোথায়?", "তাকের ওপর।"),
    ],
    "ew and aw": [
        ("Look, I have new shoes!", "They are very nice.", "দেখো, আমার নতুন জুতা!", "খুব সুন্দর।"),
        ("Can I draw on your paper?", "Yes, draw a cat.", "তোমার কাগজে আঁকতে পারি?", "হ্যাঁ, একটা বিড়াল আঁকো।"),
        ("Mamma, can I have a straw?", "Here is a straw for your juice.", "আম্মু, একটা স্ট্র দেবে?", "এই নাও জুসের স্ট্র।"),
        ("Daddy, my plant grew!", "It grew so tall.", "আব্বু, আমার গাছ বড় হয়েছে!", "কত লম্বা হয়েছে।"),
        ("Grandma, I saw a big dog.", "Did it have big paws?", "দাদি, আমি একটা বড় কুকুর দেখেছি।", "ওর থাবা কি বড় ছিল?"),
        ("Grandpa, what is new today?", "A new book for you!", "দাদা, আজ নতুন কী?", "তোমার জন্য একটা নতুন বই!"),
    ],
    "au and al": [
        ("Let's walk to the shop.", "OK, let's walk.", "চলো দোকানে হেঁটে যাই।", "ঠিক আছে, চলো।"),
        ("Throw the ball to me!", "Catch the ball!", "বলটা আমার দিকে ছোড়ো!", "বলটা ধরো!"),
        ("Mamma, I like this sauce.", "It is tomato sauce.", "আম্মু, এই সসটা মজা।", "এটা টমেটো সস।"),
        ("Daddy, can I have chalk?", "Draw on the wall outside.", "আব্বু, আমাকে চক দেবে?", "বাইরের দেয়ালে আঁকো।"),
        ("Grandma, you are tall!", "And you are getting tall too.", "দাদি, তুমি লম্বা!", "আর তুমিও লম্বা হচ্ছ।"),
        ("Grandpa, let's talk.", "I always like to talk with you.", "দাদা, চলো গল্প করি।", "তোমার সাথে গল্প করতে সবসময় ভালো লাগে।"),
    ],
    "air and ear": [
        ("Sit on this chair.", "Thank you, it is near you.", "এই চেয়ারে বসো।", "ধন্যবাদ, তোমার কাছেই।"),
        ("Can you hear the rain?", "Yes, I can hear it.", "বৃষ্টির শব্দ শুনছ?", "হ্যাঁ, শুনছি।"),
        ("Mamma, brush my hair, please.", "Sit still, my dear.", "আম্মু, চুল আঁচড়ে দাও।", "চুপ করে বসো, সোনা।"),
        ("Daddy, can we go to the fair?", "Yes, next year.", "আব্বু, আমরা কি মেলায় যাব?", "হ্যাঁ, আগামী বছর।"),
        ("Grandma, I have a teddy bear.", "What is its name?", "দাদি, আমার একটা টেডি বিয়ার আছে।", "ওর নাম কী?"),
        ("Grandpa, I want a pear.", "Here is a sweet pear.", "দাদা, আমি একটা নাশপাতি খাব।", "এই নাও মিষ্টি নাশপাতি।"),
    ],
    "are and ph": [
        ("Let's share the cake.", "Half for you, half for me.", "চলো কেকটা ভাগ করি।", "অর্ধেক তোমার, অর্ধেক আমার।"),
        ("Can I see the photo?", "Here, look at us!", "ছবিটা দেখতে পারি?", "এই দেখো, আমরা!"),
        ("Mamma, your phone is ringing.", "Thank you, I will get it.", "আম্মু, তোমার ফোন বাজছে।", "ধন্যবাদ, আমি ধরছি।"),
        ("Daddy, I saw an elephant!", "At the zoo? How big was it?", "আব্বু, আমি একটা হাতি দেখেছি!", "চিড়িয়াখানায়? কত বড় ছিল?"),
        ("Grandma, please take care.", "I will, my dear.", "দাদি, সাবধানে থেকো।", "থাকব, সোনা।"),
        ("Grandpa, draw a square.", "One, two, three, four sides.", "দাদা, একটা বর্গ আঁকো।", "এক, দুই, তিন, চার বাহু।"),
    ],
    "soft c": [
        ("I can ride my cycle!", "You are fast!", "আমি সাইকেল চালাতে পারি!", "তুমি খুব জোরে চালাও!"),
        ("Can I have some ice?", "Here is some ice.", "একটু বরফ দেবে?", "এই নাও বরফ।"),
        ("Mamma, I like rice and fish.", "Good! Lunch is ready.", "আম্মু, আমার ভাত-মাছ পছন্দ।", "ভালো! দুপুরের খাবার তৈরি।"),
        ("Daddy, the city is so big.", "Yes, Dhaka is a big city.", "আব্বু, শহরটা অনেক বড়।", "হ্যাঁ, ঢাকা বড় শহর।"),
        ("Grandma, you have a nice face.", "What a nice thing to say!", "দাদি, তোমার মুখটা খুব সুন্দর।", "কী সুন্দর কথা!"),
        ("Grandpa, where is my pencil?", "It is in your pencil box.", "দাদা, আমার পেনসিল কোথায়?", "তোমার পেনসিল বক্সে।"),
    ],
    "soft g": [
        ("Look, a shiny gem!", "It is so pretty.", "দেখো, একটা চকচকে রত্ন!", "খুব সুন্দর।"),
        ("Turn the page, please.", "OK, next page.", "পাতাটা উল্টাও।", "ঠিক আছে, পরের পাতা।"),
        ("Mamma, can I have an orange?", "Here is a big orange.", "আম্মু, একটা কমলা খাব?", "এই নাও বড় কমলা।"),
        ("Daddy, are you a giant?", "Ho ho, a friendly giant!", "আব্বু, তুমি কি দানব?", "হো হো, বন্ধু দানব!"),
        ("Grandma, the bird is in a cage.", "Birds like to fly free.", "দাদি, পাখিটা খাঁচায়।", "পাখিরা মুক্তভাবে উড়তে ভালোবাসে।"),
        ("Grandpa, how old is this house?", "It is very, very old.", "দাদা, বাড়িটা কত পুরনো?", "অনেক, অনেক পুরনো।"),
    ],
    "three little pigs": [
        ("Let's play three little pigs!", "I will be the wolf!", "চলো তিনটি ছোট শূকর খেলি!", "আমি নেকড়ে হব!"),
        ("Help, the wolf is coming!", "Run to the brick house!", "বাঁচাও, নেকড়ে আসছে!", "ইটের বাড়িতে দৌড়াও!"),
        ("Mamma, is our house made of bricks?", "Yes, it is strong.", "আম্মু, আমাদের বাড়ি কি ইটের?", "হ্যাঁ, খুব মজবুত।"),
        ("Daddy, huff and puff!", "Huff! Puff! It did not fall!", "আব্বু, ফুঁ দাও!", "ফুঁ! ফুঁ! পড়ল না!"),
        ("Grandma, tell me the pig story.", "Once upon a time…", "দাদি, শূকরের গল্পটা বলো।", "অনেক দিন আগে…"),
        ("Grandpa, which pig is the best?", "The one who worked hard.", "দাদা, কোন শূকর সবচেয়ে ভালো?", "যে কঠোর পরিশ্রম করেছিল।"),
    ],
}

WEEK_TALK = {
    8: "Blends: st, sp, tr, fr", 9: "Tricky words: the, I, to, go, no", 10: "Read short sentences",
    11: "Blend a-words: s-a-t", 12: "Blend e- and u-words", 13: "y as a vowel", 14: "Read your first e-book",
    15: "Tricky words: the, I, to, go, no", 16: "Magic e: a_e, i_e", 17: "Long o: ow, oe, oa, o_e",
    18: "Blend i- and o-words", 19: "Read ee, oa, ai words", 20: "Long o: ow, oe, oa, o_e", 21: "Read sh, ch, th words",
    22: "ir and ur", 23: "ew and aw", 24: "au and al", 25: "air and ear", 26: "are and ph", 27: "Read short sentences",
    28: "soft c", 29: "soft g", 30: "Blends at the end: nd, st, mp", 31: "three little pigs", 32: "three little pigs",
    33: "Read your first e-book", 34: "Read ee, oa, ai words", 35: "Tricky words: the, I, to, go, no", 36: "Read short sentences",
}
