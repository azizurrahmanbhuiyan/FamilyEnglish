"""Family talk for Levels 1-8. Order in every list: Sister, Brother, Mamma, Daddy, Grandma, Grandpa.
Each entry: (Me says, family member says, Bangla for Me, Bangla for the family member).
Each pair practises the lesson's pattern or topic in everyday home English."""

LEVELS = {
    # ------------------------------------------------------------------ Level 1: blending
    "Blend a-words: s-a-t": [
        ("The cat sat on my hat!", "Sad hat! Get the cat off.", "বিড়ালটা আমার টুপির ওপর বসেছে!", "বেচারা টুপি! বিড়ালটাকে সরাও।"),
        ("Can I have the red bag?", "Yes. It has a map in it.", "লাল ব্যাগটা কি নিতে পারি?", "হ্যাঁ। ওটার ভেতরে একটা মানচিত্র আছে।"),
        ("Mamma, I can tap the pan.", "Tap, tap! Not too hard.", "আম্মু, আমি প্যানে টোকা দিতে পারি।", "টুক টুক! বেশি জোরে না।"),
        ("Daddy, a man has a van.", "Yes, a man and a big van.", "আব্বু, একজন লোকের একটা ভ্যান আছে।", "হ্যাঁ, একজন লোক আর বড় ভ্যান।"),
        ("Grandma, I had jam.", "Jam on a hot bun?", "দাদি, আমি জ্যাম খেয়েছি।", "গরম বানের ওপর জ্যাম?"),
        ("Grandpa, sit on the mat.", "I can sit on the mat.", "দাদা, মাদুরে বসো।", "আমি মাদুরে বসতে পারি।"),
    ],
    "Blend i- and o-words": [
        ("Is the fish in the pot?", "No, the fish is in the tin.", "মাছটা কি পাতিলে?", "না, মাছটা কৌটায়।"),
        ("Hop on the log!", "I can hop on the log.", "গাছের গুঁড়িতে লাফাও!", "আমি গুঁড়িতে লাফাতে পারি।"),
        ("Mamma, the dog is on my bed.", "Get the dog off the bed.", "আম্মু, কুকুরটা আমার বিছানায়।", "কুকুরটাকে বিছানা থেকে নামাও।"),
        ("Daddy, it is hot.", "Sit in the shade.", "আব্বু, খুব গরম।", "ছায়ায় বসো।"),
        ("Grandma, I hid the pin.", "Is it in the box?", "দাদি, আমি পিনটা লুকিয়েছি।", "বাক্সের ভেতরে?"),
        ("Grandpa, I got six dots.", "Six! You win.", "দাদা, আমি ছয় পেয়েছি।", "ছয়! তুমি জিতেছ।"),
    ],
    "Blend e- and u-words": [
        ("The bug is on the bed!", "Get the bug! Quick!", "পোকাটা বিছানায়!", "পোকাটা ধরো! তাড়াতাড়ি!"),
        ("Run to the bus!", "Run fast! Get on!", "বাসের দিকে দৌড়াও!", "জোরে দৌড়াও! ওঠো!"),
        ("Mamma, I can get the cup.", "Get the red cup, please.", "আম্মু, আমি কাপটা আনতে পারি।", "লাল কাপটা আনো।"),
        ("Daddy, the hen is in the mud.", "Get her out of the mud!", "আব্বু, মুরগিটা কাদায়।", "ওকে কাদা থেকে তোলো!"),
        ("Grandma, let's have fun.", "Yes, fun in the sun!", "দাদি, চলো মজা করি।", "হ্যাঁ, রোদে মজা!"),
        ("Grandpa, I fed the pup.", "Good! The pup is fed.", "দাদা, আমি কুকুরছানাকে খাইয়েছি।", "ভালো! ছানাটা খেয়েছে।"),
    ],
    "Read sh, ch, th words": [
        ("Shh, let's read this book.", "Yes, this is a fun book.", "শশ, চলো এই বইটা পড়ি।", "হ্যাঁ, এটা মজার বই।"),
        ("I want fish and chips.", "Me too! With lots of chips.", "আমি মাছ আর চিপস খাব।", "আমিও! অনেক চিপস দিয়ে।"),
        ("Mamma, I shut the shop door.", "Thank you. That is good.", "আম্মু, দোকানের দরজা বন্ধ করেছি।", "ধন্যবাদ। ভালো করেছ।"),
        ("Daddy, the chick is on the path.", "Shoo it to the shed.", "আব্বু, ছানাটা রাস্তায়।", "ওকে তাড়িয়ে ঘরে নাও।"),
        ("Grandma, thank you for lunch.", "Thank you for helping.", "দাদি, দুপুরের খাবারের জন্য ধন্যবাদ।", "সাহায্য করার জন্য তোমাকেও ধন্যবাদ।"),
        ("Grandpa, sit on this chair.", "Thanks. This chair is soft.", "দাদা, এই চেয়ারে বসো।", "ধন্যবাদ। চেয়ারটা নরম।"),
    ],
    "Read ee, oa, ai words": [
        ("I see a goat in the rain.", "The goat needs a coat!", "বৃষ্টিতে একটা ছাগল দেখছি।", "ছাগলটার একটা কোট দরকার!"),
        ("Wait for me on the road.", "I will wait. Be quick.", "রাস্তায় আমার জন্য দাঁড়াও।", "দাঁড়াচ্ছি। তাড়াতাড়ি এসো।"),
        ("Mamma, I need soap for my feet.", "Here is the soap.", "আম্মু, পা ধোয়ার সাবান লাগবে।", "এই নাও সাবান।"),
        ("Daddy, let's sail a boat.", "A green boat on the stream.", "আব্বু, চলো নৌকা ভাসাই।", "খালে একটা সবুজ নৌকা।"),
        ("Grandma, we can feed the goat.", "Feed it some green leaves.", "দাদি, আমরা ছাগলকে খাওয়াতে পারি।", "কিছু সবুজ পাতা খাওয়াও।"),
        ("Grandpa, I see the train!", "Wave to the train.", "দাদা, ট্রেন দেখছি!", "ট্রেনকে হাত নাড়াও।"),
    ],
    "Tricky words: the, I, to, go, no": [
        ("I go to the park.", "I go to the park too.", "আমি পার্কে যাই।", "আমিও পার্কে যাই।"),
        ("No, no! The cat is mine!", "OK, the cat is yours.", "না, না! বিড়ালটা আমার!", "ঠিক আছে, বিড়ালটা তোমার।"),
        ("Mamma, I want to go to school.", "Yes, go and get your bag.", "আম্মু, আমি স্কুলে যেতে চাই।", "হ্যাঁ, যাও ব্যাগ নিয়ে এসো।"),
        ("Daddy, can I go to the shop?", "No, not alone. I will go too.", "আব্বু, দোকানে যেতে পারি?", "না, একা না। আমিও যাব।"),
        ("Grandma, I go to bed at nine.", "Good. Go to bed now.", "দাদি, আমি নয়টায় ঘুমাতে যাই।", "ভালো। এখন ঘুমাতে যাও।"),
        ("Grandpa, I like the book.", "I like the book too.", "দাদা, বইটা আমার ভালো লাগে।", "আমারও ভালো লাগে।"),
    ],
    "Read your first e-book": [
        ("I can read this page!", "Read it to me, please.", "আমি এই পাতাটা পড়তে পারি!", "আমাকে পড়ে শোনাও।"),
        ("Turn the page.", "OK, next page. What happens?", "পাতা উল্টাও।", "ঠিক আছে, পরের পাতা। কী হয়?"),
        ("Mamma, I read a whole book!", "A whole book! I am so proud.", "আম্মু, আমি পুরো একটা বই পড়েছি!", "পুরো বই! আমি খুব গর্বিত।"),
        ("Daddy, let's read at bedtime.", "Yes, one book every night.", "আব্বু, চলো ঘুমের আগে পড়ি।", "হ্যাঁ, প্রতি রাতে একটা বই।"),
        ("Grandma, can you hear me read?", "Yes, I am listening.", "দাদি, আমার পড়া শুনবে?", "হ্যাঁ, আমি শুনছি।"),
        ("Grandpa, the dog in the book is funny.", "Show me the funny dog.", "দাদা, বইয়ের কুকুরটা মজার।", "মজার কুকুরটা দেখাও।"),
    ],

    # ------------------------------------------------------------------ Level 2: blends and sentences
    "Blends: st, sp, tr, fr": [
        ("Stop! The frog is on the step.", "Step around the frog!", "থামো! ব্যাঙটা সিঁড়িতে।", "ব্যাঙটার পাশ দিয়ে যাও!"),
        ("Let's spin the top.", "Spin it fast!", "চলো লাটিম ঘোরাই।", "জোরে ঘোরাও!"),
        ("Mamma, I want fresh fruit.", "Fresh mangoes from the tree.", "আম্মু, তাজা ফল খাব।", "গাছের তাজা আম।"),
        ("Daddy, let's take the train.", "The train leaves at three.", "আব্বু, চলো ট্রেনে যাই।", "ট্রেন তিনটায় ছাড়বে।"),
        ("Grandma, my friend is here.", "Tell your friend to come in.", "দাদি, আমার বন্ধু এসেছে।", "বন্ধুকে ভেতরে আসতে বলো।"),
        ("Grandpa, tell me a story.", "Sit still, and I will start.", "দাদা, একটা গল্প বলো।", "চুপ করে বসো, আমি শুরু করছি।"),
    ],
    "Blends at the end: nd, st, mp": [
        ("Jump, jump! I am the best!", "You jump fast!", "লাফ, লাফ! আমি সেরা!", "তুমি দ্রুত লাফাও!"),
        ("My hand is in the sand.", "Find the shell in the sand.", "আমার হাত বালিতে।", "বালিতে ঝিনুকটা খোঁজো।"),
        ("Mamma, turn on the lamp.", "The lamp is on. Rest now.", "আম্মু, বাতিটা জ্বালাও।", "বাতি জ্বলছে। এখন বিশ্রাম নাও।"),
        ("Daddy, the wind is strong.", "Hold my hand.", "আব্বু, বাতাস খুব জোরে।", "আমার হাত ধরো।"),
        ("Grandma, you are my best friend.", "And you are my best friend.", "দাদি, তুমি আমার সবচেয়ে ভালো বন্ধু।", "আর তুমি আমার সবচেয়ে ভালো বন্ধু।"),
        ("Grandpa, I am first!", "You came first! Well done.", "দাদা, আমি প্রথম!", "তুমি প্রথম হয়েছ! সাবাশ।"),
    ],
    "Long o: ow, oe, oa, o_e": [
        ("Let's throw the ball.", "Throw it slow, please.", "চলো বল ছুড়ি।", "আস্তে ছোড়ো, প্লিজ।"),
        ("I hurt my toe.", "Oh no! Let me see your toe.", "আমার পায়ের আঙুলে ব্যথা।", "ওহ না! দেখি তোমার আঙুল।"),
        ("Mamma, I am going home.", "Go home slowly.", "আম্মু, আমি বাড়ি যাচ্ছি।", "আস্তে আস্তে বাড়ি যাও।"),
        ("Daddy, the window is open.", "Close it slowly, please.", "আব্বু, জানালা খোলা।", "আস্তে করে বন্ধ করো।"),
        ("Grandma, I wrote a note for you.", "Oh, a note! Read it to me.", "দাদি, তোমার জন্য একটা চিরকুট লিখেছি।", "ওহ, চিরকুট! পড়ে শোনাও।"),
        ("Grandpa, I know the way home.", "Show me the way.", "দাদা, আমি বাড়ির রাস্তা জানি।", "আমাকে রাস্তা দেখাও।"),
    ],
    "Magic e: a_e, i_e": [
        ("Let's bake a cake.", "Yes! I like cake.", "চলো একটা কেক বানাই।", "হ্যাঁ! আমার কেক ভালো লাগে।"),
        ("I can ride my bike.", "Ride it nice and slow.", "আমি সাইকেল চালাতে পারি।", "সুন্দর করে আস্তে চালাও।"),
        ("Mamma, what time is it?", "It is time to wake up.", "আম্মু, কয়টা বাজে?", "ঘুম থেকে ওঠার সময়।"),
        ("Daddy, let's fly a kite.", "Fine! Get the kite.", "আব্বু, চলো ঘুড়ি ওড়াই।", "ঠিক আছে! ঘুড়িটা আনো।"),
        ("Grandma, I made this for you.", "It is so nice. I like it.", "দাদি, এটা তোমার জন্য বানিয়েছি।", "খুব সুন্দর। আমার ভালো লেগেছে।"),
        ("Grandpa, smile for the photo!", "I will smile. Take it now.", "দাদা, ছবির জন্য হাসো!", "হাসছি। এখন তোলো।"),
    ],
    "Read short sentences": [
        ("The sun is hot today.", "Let's play in the shade.", "আজ রোদ খুব গরম।", "চলো ছায়ায় খেলি।"),
        ("I have a red ball.", "Can I play with it?", "আমার একটা লাল বল আছে।", "আমি কি খেলতে পারি?"),
        ("Mamma, I am hungry.", "Lunch is ready. Wash your hands.", "আম্মু, খিদে পেয়েছে।", "খাবার তৈরি। হাত ধোও।"),
        ("Daddy, the bus is late.", "Let's wait a little.", "আব্বু, বাস দেরি করছে।", "একটু অপেক্ষা করি।"),
        ("Grandma, I can read now.", "Read this line to me.", "দাদি, আমি এখন পড়তে পারি।", "এই লাইনটা পড়ে শোনাও।"),
        ("Grandpa, the cat is asleep.", "Let it sleep. Be quiet.", "দাদা, বিড়ালটা ঘুমাচ্ছে।", "ঘুমাতে দাও। চুপ থাকো।"),
    ],

    # ------------------------------------------------------------------ Level 3: first conversations
    "Hello! What's your name?": [
        ("Hi! What's your name?", "My name is Riya. Nice to meet you!", "হাই! তোমার নাম কী?", "আমার নাম রিয়া। তোমার সাথে দেখা হয়ে ভালো লাগল!"),
        ("Hello! How are you?", "I'm fine, thanks. And you?", "হ্যালো! কেমন আছো?", "ভালো আছি, ধন্যবাদ। তুমি?"),
        ("Good morning, Mamma!", "Good morning! Did you sleep well?", "শুভ সকাল, আম্মু!", "শুভ সকাল! ভালো ঘুম হয়েছে?"),
        ("Good evening, Daddy!", "Good evening! How was your day?", "শুভ সন্ধ্যা, আব্বু!", "শুভ সন্ধ্যা! দিন কেমন গেল?"),
        ("Hello, Grandma! How old are you?", "I'm seventy. How old are you?", "হ্যালো দাদি! তোমার বয়স কত?", "আমার সত্তর। তোমার বয়স কত?"),
        ("Goodbye, Grandpa!", "Goodbye! See you tomorrow.", "বিদায়, দাদা!", "বিদায়! কাল দেখা হবে।"),
    ],
    "My family": [
        ("You are my big sister.", "And you are my little brother.", "তুমি আমার বড় বোন।", "আর তুমি আমার ছোট ভাই।"),
        ("How many cousins do we have?", "We have five cousins.", "আমাদের কতজন কাজিন?", "আমাদের পাঁচজন কাজিন।"),
        ("Mamma, who is in this photo?", "That's your uncle and his wife.", "আম্মু, এই ছবিতে কে?", "ওটা তোমার মামা আর মামি।"),
        ("Daddy, is Aunt Lina your sister?", "Yes, she is my little sister.", "আব্বু, লীনা ফুপু কি তোমার বোন?", "হ্যাঁ, সে আমার ছোট বোন।"),
        ("Grandma, are you Daddy's mother?", "Yes, I am his mother.", "দাদি, তুমি কি আব্বুর মা?", "হ্যাঁ, আমি ওর মা।"),
        ("Grandpa, I love our big family.", "Me too. We are very lucky.", "দাদা, আমাদের বড় পরিবারটা আমার ভালো লাগে।", "আমারও। আমরা খুব ভাগ্যবান।"),
    ],
    "What's this? It's a …": [
        ("What's this?", "It's a pencil sharpener.", "এটা কী?", "এটা একটা পেন্সিল কাটার।"),
        ("What's that on the shelf?", "It's a clock.", "তাকের ওপর ওটা কী?", "ওটা একটা ঘড়ি।"),
        ("Mamma, what's this in the kitchen?", "It's a rice cooker.", "আম্মু, রান্নাঘরে এটা কী?", "এটা রাইস কুকার।"),
        ("Daddy, what's this button?", "It's the light switch.", "আব্বু, এই বোতামটা কী?", "এটা বাতির সুইচ।"),
        ("Grandma, what's this?", "It's my old radio.", "দাদি, এটা কী?", "এটা আমার পুরোনো রেডিও।"),
        ("Grandpa, is this your watch?", "Yes, it's my watch.", "দাদা, এটা কি তোমার ঘড়ি?", "হ্যাঁ, এটা আমার ঘড়ি।"),
    ],
    "Colours and numbers 1–20": [
        ("I have twelve crayons.", "And I have fifteen!", "আমার বারোটা রং-পেন্সিল আছে।", "আর আমার পনেরোটা!"),
        ("What colour is your shirt?", "It's orange.", "তোমার জামাটা কী রঙের?", "কমলা।"),
        ("Mamma, how many eggs do we need?", "We need eleven eggs.", "আম্মু, কয়টা ডিম লাগবে?", "এগারোটা ডিম লাগবে।"),
        ("Daddy, what colour is our car?", "It's silver.", "আব্বু, আমাদের গাড়ির রং কী?", "রুপালি।"),
        ("Grandma, I can count to twenty.", "Let me hear you count.", "দাদি, আমি বিশ পর্যন্ত গুনতে পারি।", "শুনি তোমার গোনা।"),
        ("Grandpa, your umbrella is purple!", "Yes, purple is my favourite colour.", "দাদা, তোমার ছাতা বেগুনি!", "হ্যাঁ, বেগুনি আমার প্রিয় রং।"),
    ],

    # ------------------------------------------------------------------ Level 4: daily life
    "Daily routine (present simple)": [
        ("What time do you get up?", "I get up at seven.", "তুমি কয়টায় ওঠো?", "আমি সাতটায় উঠি।"),
        ("Do you brush your teeth at night?", "Yes, I brush them every night.", "তুমি কি রাতে দাঁত মাজো?", "হ্যাঁ, প্রতি রাতে মাজি।"),
        ("Mamma, what do you do in the morning?", "I make breakfast and then I pray.", "আম্মু, সকালে তুমি কী করো?", "নাস্তা বানাই, তারপর নামাজ পড়ি।"),
        ("Daddy, how do you go to work?", "I take the bus every day.", "আব্বু, তুমি অফিসে কীভাবে যাও?", "প্রতিদিন বাসে যাই।"),
        ("Grandma, when do you go to bed?", "I usually go to bed at ten.", "দাদি, তুমি কখন ঘুমাতে যাও?", "সাধারণত দশটায়।"),
        ("Grandpa, do you walk every day?", "Yes, I walk after Fajr.", "দাদা, তুমি কি প্রতিদিন হাঁটো?", "হ্যাঁ, ফজরের পরে হাঁটি।"),
    ],
    "Can and can't": [
        ("Can you swim?", "Yes, I can. Can you?", "তুমি কি সাঁতার পারো?", "হ্যাঁ, পারি। তুমি পারো?"),
        ("I can't open this bottle.", "I can help you.", "আমি এই বোতলটা খুলতে পারছি না।", "আমি তোমাকে সাহায্য করতে পারি।"),
        ("Mamma, can I watch TV?", "You can watch after homework.", "আম্মু, টিভি দেখতে পারি?", "বাড়ির কাজের পরে দেখতে পারো।"),
        ("Daddy, can you ride a horse?", "No, I can't. But I can ride a bike.", "আব্বু, তুমি কি ঘোড়ায় চড়তে পারো?", "না, পারি না। কিন্তু সাইকেল চালাতে পারি।"),
        ("Grandma, can you sing for me?", "Yes, I can sing an old song.", "দাদি, আমাকে গান শোনাতে পারবে?", "হ্যাঁ, একটা পুরোনো গান গাইতে পারি।"),
        ("Grandpa, I can't find my shoes.", "They're under your bed.", "দাদা, আমি জুতা খুঁজে পাচ্ছি না।", "তোমার খাটের নিচে।"),
    ],
    "Places in town": [
        ("Where is the library?", "It's next to the post office.", "লাইব্রেরি কোথায়?", "পোস্ট অফিসের পাশে।"),
        ("Let's go to the park after school.", "OK, the park near the mosque.", "স্কুলের পরে চলো পার্কে যাই।", "ঠিক আছে, মসজিদের কাছের পার্কে।"),
        ("Mamma, are we going to the market?", "Yes, we need fish and vegetables.", "আম্মু, আমরা কি বাজারে যাচ্ছি?", "হ্যাঁ, মাছ আর সবজি লাগবে।"),
        ("Daddy, where is your bank?", "It's opposite the hospital.", "আব্বু, তোমার ব্যাংক কোথায়?", "হাসপাতালের উল্টো দিকে।"),
        ("Grandma, is the pharmacy open?", "Yes, it's open until ten.", "দাদি, ফার্মেসি কি খোলা?", "হ্যাঁ, দশটা পর্যন্ত খোলা।"),
        ("Grandpa, how far is the station?", "It's ten minutes by rickshaw.", "দাদা, স্টেশন কত দূর?", "রিকশায় দশ মিনিট।"),
    ],

    # ------------------------------------------------------------------ Level 5
    "Past simple: what happened?": [
        ("What did you do at school today?", "We painted pictures and played football.", "আজ স্কুলে কী করলে?", "ছবি আঁকলাম আর ফুটবল খেললাম।"),
        ("I lost my pencil yesterday.", "Did you look in your bag?", "কাল আমার পেন্সিল হারিয়েছি।", "ব্যাগে খুঁজেছিলে?"),
        ("Mamma, what did you cook?", "I cooked chicken curry.", "আম্মু, কী রান্না করেছ?", "মুরগির তরকারি রান্না করেছি।"),
        ("Daddy, where did you go last night?", "I went to Uncle's house.", "আব্বু, কাল রাতে কোথায় গিয়েছিলে?", "মামার বাসায় গিয়েছিলাম।"),
        ("Grandma, what did you do when you were young?", "I walked to school every day.", "দাদি, ছোটবেলায় তুমি কী করতে?", "প্রতিদিন হেঁটে স্কুলে যেতাম।"),
        ("Grandpa, did you watch the match?", "Yes! Bangladesh won.", "দাদা, খেলা দেখেছ?", "হ্যাঁ! বাংলাদেশ জিতেছে।"),
    ],
    "Tell a short story": [
        ("One day, a bird flew into our room.", "Then what happened?", "একদিন একটা পাখি আমাদের ঘরে ঢুকে পড়ল।", "তারপর কী হলো?"),
        ("First, I opened the window.", "And then the bird flew out!", "প্রথমে আমি জানালা খুললাম।", "আর তারপর পাখিটা উড়ে গেল!"),
        ("Mamma, can I tell you a story?", "Yes, start with 'Once upon a time'.", "আম্মু, তোমাকে একটা গল্প বলি?", "হ্যাঁ, 'অনেক দিন আগে' দিয়ে শুরু করো।"),
        ("Daddy, at the end, the boy found his cat.", "What a happy ending!", "আব্বু, শেষে ছেলেটা তার বিড়াল খুঁজে পেল।", "কী সুন্দর শেষ!"),
        ("Grandma, tell me a story from your village.", "Long ago, there was a big flood...", "দাদি, তোমার গ্রামের একটা গল্প বলো।", "অনেক আগে, একটা বড় বন্যা হয়েছিল..."),
        ("Grandpa, what happened next?", "Next, the boat came to save us.", "দাদা, তারপর কী হলো?", "তারপর আমাদের বাঁচাতে নৌকা এলো।"),
    ],
    "Bigger, faster, the best": [
        ("My kite is bigger than yours!", "But mine flies higher!", "আমার ঘুড়ি তোমারটার চেয়ে বড়!", "কিন্তু আমারটা বেশি উঁচুতে ওড়ে!"),
        ("Who is the fastest runner?", "You are faster than me.", "সবচেয়ে দ্রুত কে দৌড়ায়?", "তুমি আমার চেয়ে দ্রুত।"),
        ("Mamma, your biryani is the best!", "Thank you! It's better than last time.", "আম্মু, তোমার বিরিয়ানি সেরা!", "ধন্যবাদ! আগের বারের চেয়ে ভালো হয়েছে।"),
        ("Daddy, is Dhaka bigger than Khulna?", "Yes, Dhaka is much bigger.", "আব্বু, ঢাকা কি খুলনার চেয়ে বড়?", "হ্যাঁ, ঢাকা অনেক বড়।"),
        ("Grandma, you are the kindest person.", "And you are the sweetest child.", "দাদি, তুমি সবচেয়ে দয়ালু মানুষ।", "আর তুমি সবচেয়ে মিষ্টি বাচ্চা।"),
        ("Grandpa, which is the longest river?", "The Padma is one of the longest here.", "দাদা, সবচেয়ে লম্বা নদী কোনটা?", "পদ্মা এখানের সবচেয়ে লম্বা নদীগুলোর একটা।"),
    ],

    # ------------------------------------------------------------------ Level 6
    "Present perfect: experiences": [
        ("Have you ever seen the sea?", "Yes, I've been to Cox's Bazar.", "তুমি কি কখনো সমুদ্র দেখেছ?", "হ্যাঁ, আমি কক্সবাজার গেছি।"),
        ("I've finished my homework!", "Great! Have you checked it?", "আমার বাড়ির কাজ শেষ!", "দারুণ! মিলিয়ে দেখেছ?"),
        ("Mamma, have you seen my phone?", "Yes, I've put it on the table.", "আম্মু, আমার ফোন দেখেছ?", "হ্যাঁ, টেবিলে রেখেছি।"),
        ("Daddy, have you ever flown in a plane?", "Yes, I've flown to Sylhet twice.", "আব্বু, তুমি কি কখনো প্লেনে চড়েছ?", "হ্যাঁ, দুবার সিলেটে গেছি প্লেনে।"),
        ("Grandma, have you ever used a smartphone?", "Not yet, but I'd like to learn.", "দাদি, তুমি কি কখনো স্মার্টফোন ব্যবহার করেছ?", "এখনো না, কিন্তু শিখতে চাই।"),
        ("Grandpa, how long have you lived here?", "I've lived here for fifty years.", "দাদা, তুমি কত দিন ধরে এখানে থাকো?", "পঞ্চাশ বছর ধরে এখানে আছি।"),
    ],
    "Giving opinions": [
        ("I think cricket is more fun than football.", "Really? I think football is better.", "আমার মনে হয় ক্রিকেট ফুটবলের চেয়ে মজার।", "সত্যি? আমার মনে হয় ফুটবল ভালো।"),
        ("In my opinion, this film is great.", "I agree. The ending was amazing.", "আমার মতে, ছবিটা দারুণ।", "আমি একমত। শেষটা অসাধারণ ছিল।"),
        ("Mamma, what do you think of my drawing?", "I think it's beautiful. I love the colours.", "আম্মু, আমার আঁকা কেমন লাগল?", "খুব সুন্দর। রংগুলো খুব ভালো লেগেছে।"),
        ("Daddy, I think we should plant a tree.", "That's a good idea. Let's do it on Friday.", "আব্বু, আমার মনে হয় আমাদের একটা গাছ লাগানো উচিত।", "ভালো বুদ্ধি। চলো শুক্রবার লাগাই।"),
        ("Grandma, which season do you like best?", "I prefer winter because it's cool.", "দাদি, তোমার কোন ঋতু সবচেয়ে প্রিয়?", "আমার শীত বেশি পছন্দ, কারণ ঠান্ডা থাকে।"),
        ("Grandpa, do you think phones are good for kids?", "I think a little is fine, not too much.", "দাদা, তোমার কি মনে হয় ফোন বাচ্চাদের জন্য ভালো?", "অল্প ঠিক আছে, বেশি না।"),
    ],

    # ------------------------------------------------------------------ Level 7
    "Agreeing and disagreeing": [
        ("We should have pizza tonight.", "I'm not sure. How about rice?", "আজ রাতে পিৎজা খাওয়া উচিত।", "জানি না। ভাত খেলে কেমন হয়?"),
        ("I think homework is too long.", "I see your point, but it helps us learn.", "আমার মনে হয় বাড়ির কাজ খুব বেশি।", "বুঝলাম, কিন্তু এতে আমরা শিখি।"),
        ("Mamma, I think I can stay up late.", "I don't agree. You have school tomorrow.", "আম্মু, আমার মনে হয় আমি দেরি করে ঘুমাতে পারি।", "আমি একমত না। কাল তোমার স্কুল।"),
        ("Daddy, cycling is good exercise.", "I couldn't agree more!", "আব্বু, সাইকেল চালানো ভালো ব্যায়াম।", "আমি পুরোপুরি একমত!"),
        ("Grandma, life was harder in the past.", "That's true, but people were happy.", "দাদি, আগের দিনে জীবন কঠিন ছিল।", "সত্যি, কিন্তু মানুষ সুখী ছিল।"),
        ("Grandpa, I think we should visit the village.", "You're right. Let's go next month.", "দাদা, আমার মনে হয় আমাদের গ্রামে যাওয়া উচিত।", "তুমি ঠিক বলেছ। চলো আগামী মাসে যাই।"),
    ],
    "6 Minute English: listening": [
        ("Did you hear that news about the bridge?", "Yes, it opens next week.", "সেতুর খবরটা শুনেছ?", "হ্যাঁ, আগামী সপ্তাহে খুলবে।"),
        ("Can you play that part again?", "Sure. Listen for the numbers.", "ওই অংশটা আবার চালাবে?", "অবশ্যই। সংখ্যাগুলো খেয়াল করে শোনো।"),
        ("Mamma, what did the radio say?", "It said it will rain this afternoon.", "আম্মু, রেডিওতে কী বলল?", "বলল আজ বিকেলে বৃষ্টি হবে।"),
        ("Daddy, the speaker talks very fast.", "Listen for the key words, not every word.", "আব্বু, বক্তা খুব দ্রুত কথা বলে।", "প্রতিটা শব্দ না, মূল শব্দগুলো শোনো।"),
        ("Grandma, I'll tell you what I heard.", "Tell me the main idea first.", "দাদি, যা শুনলাম তোমাকে বলছি।", "আগে মূল কথাটা বলো।"),
        ("Grandpa, what does 'reduce' mean?", "It means to make something smaller.", "দাদা, 'reduce' মানে কী?", "কোনো কিছু কমানো।"),
    ],

    # ------------------------------------------------------------------ Level 8
    "Structure a short presentation": [
        ("Can I practise my talk with you?", "Of course. I'm your audience.", "আমার বক্তৃতাটা তোমার সাথে অনুশীলন করি?", "অবশ্যই। আমি তোমার শ্রোতা।"),
        ("Firstly, I'll talk about our school garden.", "Good start! What's your second point?", "প্রথমে, আমি আমাদের স্কুলের বাগান নিয়ে বলব।", "ভালো শুরু! তোমার দ্বিতীয় পয়েন্ট কী?"),
        ("Mamma, was my talk too long?", "It was good, but speak a little slower.", "আম্মু, আমার বক্তৃতা কি বেশি লম্বা ছিল?", "ভালো ছিল, তবে একটু আস্তে বলো।"),
        ("Daddy, how do I end my talk?", "Say 'To sum up' and thank the audience.", "আব্বু, বক্তৃতা কীভাবে শেষ করব?", "'To sum up' বলো আর শ্রোতাদের ধন্যবাদ দাও।"),
        ("Grandma, did you understand my talk?", "Yes, your main points were very clear.", "দাদি, আমার বক্তৃতা বুঝেছ?", "হ্যাঁ, তোমার মূল পয়েন্টগুলো খুব পরিষ্কার ছিল।"),
        ("Grandpa, do you have any questions?", "Yes. Why did you choose this topic?", "দাদা, কোনো প্রশ্ন আছে?", "হ্যাঁ। এই বিষয়টা কেন বেছে নিলে?"),
    ],
    "Bridge to IELTS": [
        ("Can you ask me a speaking question?", "Describe your favourite place in Dhaka.", "আমাকে একটা speaking প্রশ্ন করবে?", "ঢাকায় তোমার প্রিয় জায়গার বর্ণনা দাও।"),
        ("Let's time our writing practice.", "Twenty minutes. Ready, go!", "চলো লেখার অনুশীলনে সময় ধরি।", "বিশ মিনিট। রেডি, শুরু!"),
        ("Mamma, could you check my essay?", "Sure. Your ideas are good; check the tenses.", "আম্মু, আমার রচনাটা দেখে দেবে?", "অবশ্যই। ভাবনা ভালো; কালগুলো মিলিয়ে নাও।"),
        ("Daddy, what band score do I need?", "For most universities, around 6.5.", "আব্বু, আমার কত ব্যান্ড স্কোর লাগবে?", "বেশিরভাগ বিশ্ববিদ্যালয়ে প্রায় ৬.৫।"),
        ("Grandma, I'm nervous about the test.", "Prepare well and you will do fine.", "দাদি, পরীক্ষা নিয়ে ভয় লাগছে।", "ভালো করে প্রস্তুতি নাও, ভালো করবে।"),
        ("Grandpa, how do you stay calm?", "Breathe slowly and take one step at a time.", "দাদা, তুমি কীভাবে শান্ত থাকো?", "ধীরে শ্বাস নাও, এক এক করে এগোও।"),
    ],
}
