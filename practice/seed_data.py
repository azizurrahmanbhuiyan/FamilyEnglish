"""Seed content for practice tools. Edit here, then run: python manage.py seed_practice"""

# (slug, title, title_bn, emoji, level, [(word, emoji, bangla, example), ...])
DECKS = [
    ("numbers", "Numbers 1–10", "সংখ্যা ১–১০", "🔢", 0, [
        ("one", "1️⃣", "এক", "I have one nose."), ("two", "2️⃣", "দুই", "I have two eyes."),
        ("three", "3️⃣", "তিন", "Three cats."), ("four", "4️⃣", "চার", "A chair has four legs."),
        ("five", "5️⃣", "পাঁচ", "Five fingers on one hand."), ("six", "6️⃣", "ছয়", "Six eggs."),
        ("seven", "7️⃣", "সাত", "Seven days in a week."), ("eight", "8️⃣", "আট", "A spider has eight legs."),
        ("nine", "9️⃣", "নয়", "Nine balls."), ("ten", "🔟", "দশ", "Ten toes."),
    ]),
    ("animals", "Animals", "প্রাণী", "🐘", 1, [
        ("cat", "🐱", "বিড়াল", "The cat is sleeping."), ("dog", "🐶", "কুকুর", "The dog can run."),
        ("cow", "🐄", "গরু", "A cow gives milk."), ("goat", "🐐", "ছাগল", "The goat eats grass."),
        ("hen", "🐔", "মুরগি", "The hen lays eggs."), ("duck", "🦆", "হাঁস", "The duck can swim."),
        ("fish", "🐟", "মাছ", "Fish live in water."), ("bird", "🐦", "পাখি", "The bird can fly."),
        ("tiger", "🐯", "বাঘ", "The tiger lives in the Sundarbans."),
        ("elephant", "🐘", "হাতি", "An elephant is very big."),
    ]),
    ("colours", "Colours", "রং", "🎨", 1, [
        ("red", "🔴", "লাল", "A red apple."), ("blue", "🔵", "নীল", "The sky is blue."),
        ("green", "🟢", "সবুজ", "Green leaves."), ("yellow", "🟡", "হলুদ", "A yellow banana."),
        ("black", "⚫", "কালো", "A black bag."), ("white", "⚪", "সাদা", "White milk."),
        ("orange", "🟠", "কমলা", "An orange orange!"), ("pink", "🩷", "গোলাপি", "A pink flower."),
        ("brown", "🟤", "বাদামি", "A brown cow."), ("purple", "🟣", "বেগুনি", "A purple pen."),
    ]),
    ("body", "My body", "আমার শরীর", "🖐️", 2, [
        ("head", "🙂", "মাথা", "Touch your head."), ("eye", "👁️", "চোখ", "Close your eyes."),
        ("ear", "👂", "কান", "I hear with my ears."), ("nose", "👃", "নাক", "I smell with my nose."),
        ("mouth", "👄", "মুখ", "Open your mouth."), ("hand", "✋", "হাত", "Wash your hands."),
        ("foot", "🦶", "পা", "One foot, two feet."), ("tooth", "🦷", "দাঁত", "Brush your teeth."),
        ("hair", "💇", "চুল", "She has long hair."), ("leg", "🦵", "পা (পুরো)", "A bird has two legs."),
    ]),
    ("family", "Family", "পরিবার", "👪", 3, [
        ("mother", "👩", "মা", "My mother cooks rice."), ("father", "👨", "বাবা", "My father works in a bank."),
        ("brother", "👦", "ভাই", "My brother is seven."), ("sister", "👧", "বোন", "My sister reads books."),
        ("grandmother", "👵", "দাদি / নানি", "My grandmother tells stories."),
        ("grandfather", "👴", "দাদা / নানা", "My grandfather walks every morning."),
        ("uncle", "🧔", "চাচা / মামা", "My uncle lives in Sylhet."),
        ("aunt", "👩‍🦱", "চাচি / খালা / ফুফু", "My aunt is a teacher."),
        ("cousin", "🧒", "চাচাতো/মামাতো ভাই-বোন", "My cousin plays football."),
        ("baby", "👶", "শিশু", "The baby is sleeping."),
    ]),
    ("home", "At home", "বাড়িতে", "🏠", 3, [
        ("door", "🚪", "দরজা", "Close the door, please."), ("window", "🪟", "জানালা", "Open the window."),
        ("bed", "🛏️", "বিছানা", "Go to bed."), ("chair", "🪑", "চেয়ার", "Sit on the chair."),
        ("table", "🍽️", "টেবিল", "Food is on the table."), ("fan", "🪭", "পাখা", "Turn on the fan."),
        ("kitchen", "🍳", "রান্নাঘর", "Mother is in the kitchen."),
        ("bathroom", "🚿", "গোসলখানা", "Wash your hands in the bathroom."),
        ("roof", "🏠", "ছাদ", "We fly kites on the roof."), ("light", "💡", "বাতি", "Switch off the light."),
    ]),
    ("food", "Food", "খাবার", "🍚", 3, [
        ("rice", "🍚", "ভাত", "We eat rice every day."), ("fish", "🐟", "মাছ", "Fish curry is tasty."),
        ("egg", "🥚", "ডিম", "I eat an egg for breakfast."), ("milk", "🥛", "দুধ", "Drink your milk."),
        ("bread", "🍞", "রুটি", "Bread and butter."), ("banana", "🍌", "কলা", "A banana is yellow."),
        ("mango", "🥭", "আম", "Mangoes come in summer."), ("water", "💧", "পানি", "Drink water."),
        ("tea", "🍵", "চা", "Grandfather drinks tea."), ("lentils", "🥣", "ডাল", "Rice and lentils."),
    ]),
    ("school", "School", "স্কুল", "🏫", 3, [
        ("book", "📕", "বই", "Open your book."), ("pen", "🖊️", "কলম", "Write with a pen."),
        ("pencil", "✏️", "পেন্সিল", "A sharp pencil."), ("bag", "🎒", "ব্যাগ", "My school bag is heavy."),
        ("teacher", "🧑‍🏫", "শিক্ষক", "Our teacher is kind."), ("classroom", "🏫", "শ্রেণিকক্ষ", "Our classroom is big."),
        ("friend", "🧑‍🤝‍🧑", "বন্ধু", "She is my best friend."), ("homework", "📝", "বাড়ির কাজ", "I finish my homework."),
        ("exam", "📄", "পরীক্ষা", "I take my exam on Sunday."), ("ruler", "📏", "রুলার", "Draw a line with a ruler."),
    ]),
    ("routine", "My day (verbs)", "আমার দিন (ক্রিয়া)", "⏰", 4, [
        ("wake up", "⏰", "ঘুম থেকে ওঠা", "I wake up at six."), ("brush", "🪥", "দাঁত মাজা", "I brush my teeth."),
        ("eat", "🍽️", "খাওয়া", "We eat breakfast together."), ("go", "🚶", "যাওয়া", "I go to school by rickshaw."),
        ("study", "📚", "পড়াশোনা করা", "I study in the evening."), ("play", "⚽", "খেলা", "We play in the field."),
        ("pray", "🤲", "প্রার্থনা করা", "Father prays five times a day."),
        ("help", "🤝", "সাহায্য করা", "I help my mother."), ("watch", "📺", "দেখা", "We watch TV at night."),
        ("sleep", "😴", "ঘুমানো", "I sleep at ten."),
    ]),
    ("places", "Places in town", "শহরের জায়গা", "🏙️", 4, [
        ("market", "🛒", "বাজার", "Father goes to the market."), ("hospital", "🏥", "হাসপাতাল", "Doctors work in a hospital."),
        ("mosque", "🕌", "মসজিদ", "The mosque is near our house."), ("bank", "🏦", "ব্যাংক", "Mother works in a bank."),
        ("park", "🌳", "পার্ক", "We play in the park."), ("shop", "🏪", "দোকান", "The shop is open."),
        ("bus stop", "🚏", "বাস স্ট্যান্ড", "Wait at the bus stop."), ("post office", "🏤", "ডাকঘর", "Send a letter from the post office."),
        ("river", "🏞️", "নদী", "Boats sail on the river."), ("bridge", "🌉", "সেতু", "We crossed the bridge."),
    ]),
    ("weather", "Weather and seasons", "আবহাওয়া ও ঋতু", "🌦️", 4, [
        ("sunny", "☀️", "রোদ", "It is sunny today."), ("rainy", "🌧️", "বৃষ্টি", "It is rainy in July."),
        ("cloudy", "☁️", "মেঘলা", "The sky is cloudy."), ("windy", "🌬️", "বাতাস", "It is windy on the roof."),
        ("hot", "🥵", "গরম", "Summer is very hot."), ("cold", "🥶", "ঠান্ডা", "Winter mornings are cold."),
        ("summer", "🌞", "গ্রীষ্ম", "Mangoes come in summer."), ("winter", "❄️", "শীত", "We eat pitha in winter."),
        ("monsoon", "⛈️", "বর্ষা", "The monsoon brings heavy rain."), ("storm", "🌪️", "ঝড়", "Stay inside during a storm."),
    ]),
    ("feelings", "Feelings", "অনুভূতি", "😊", 5, [
        ("happy", "😊", "খুশি", "I am happy today."), ("sad", "😢", "দুঃখিত", "She looks sad."),
        ("angry", "😠", "রাগান্বিত", "Don't be angry."), ("tired", "😴", "ক্লান্ত", "I am tired after school."),
        ("scared", "😨", "ভীত", "The baby is scared of thunder."), ("excited", "🤩", "উত্তেজিত", "We are excited about Eid."),
        ("proud", "🥲", "গর্বিত", "My parents are proud of me."), ("bored", "🥱", "বিরক্ত", "I feel bored at home."),
        ("worried", "😟", "চিন্তিত", "Mother is worried about the exam."), ("calm", "😌", "শান্ত", "Take a breath and stay calm."),
    ]),
    ("jobs", "Jobs", "পেশা", "🧑‍⚕️", 5, [
        ("doctor", "🧑‍⚕️", "ডাক্তার", "A doctor helps sick people."), ("teacher", "🧑‍🏫", "শিক্ষক", "A teacher works in a school."),
        ("farmer", "🧑‍🌾", "কৃষক", "A farmer grows rice."), ("driver", "🚗", "চালক", "The driver drives a bus."),
        ("banker", "🏦", "ব্যাংকার", "A banker works in a bank."), ("engineer", "👷", "প্রকৌশলী", "An engineer builds bridges."),
        ("cook", "👩‍🍳", "রাঁধুনি", "The cook makes biryani."), ("police officer", "👮", "পুলিশ", "A police officer keeps us safe."),
        ("nurse", "🧑‍⚕️", "নার্স", "The nurse gave me medicine."), ("shopkeeper", "🏪", "দোকানদার", "The shopkeeper sells rice."),
    ]),
    ("linking", "Opinions and linking words", "মতামত ও সংযোজক শব্দ", "🔗", 6, [
        ("however", "↔️", "তবে / তবুও", "It was raining. However, we went out."),
        ("because", "❓", "কারণ", "I stayed home because I was ill."),
        ("although", "🔀", "যদিও", "Although it was late, she kept reading."),
        ("therefore", "➡️", "সুতরাং", "He practised daily; therefore, he improved."),
        ("in my opinion", "💭", "আমার মতে", "In my opinion, reading is important."),
        ("for example", "👉", "উদাহরণস্বরূপ", "Some fruits, for example mangoes, are seasonal."),
        ("moreover", "➕", "তাছাড়া", "The park is clean. Moreover, it is safe."),
        ("instead", "🔄", "পরিবর্তে", "We walked instead of taking a rickshaw."),
        ("unless", "🚫", "যদি না", "We will go unless it rains."),
        ("on the other hand", "⚖️", "অন্যদিকে", "Cities are busy. On the other hand, villages are quiet."),
    ]),
    ("society", "News and society", "খবর ও সমাজ", "📰", 7, [
        ("environment", "🌍", "পরিবেশ", "We must protect the environment."),
        ("pollution", "🏭", "দূষণ", "Air pollution is high in Dhaka."),
        ("traffic jam", "🚗", "যানজট", "The traffic jam made us late."),
        ("government", "🏛️", "সরকার", "The government built a new road."),
        ("economy", "📈", "অর্থনীতি", "The economy is growing."),
        ("flood", "🌊", "বন্যা", "The flood damaged many homes."),
        ("education", "🎓", "শিক্ষা", "Education opens doors."),
        ("technology", "💻", "প্রযুক্তি", "Technology changes how we learn."),
        ("volunteer", "🙋", "স্বেচ্ছাসেবক", "She volunteers at a school."),
        ("community", "🏘️", "সম্প্রদায় / সমাজ", "Our community helped after the storm."),
    ]),
    ("academic", "Formal and academic words", "আনুষ্ঠানিক শব্দ", "🎓", 8, [
        ("significant", "📌", "গুরুত্বপূর্ণ", "There was a significant increase."),
        ("consequence", "⛓️", "পরিণতি", "Every action has a consequence."),
        ("evidence", "🔎", "প্রমাণ", "There is clear evidence."),
        ("approach", "🧭", "পদ্ধতি", "We need a new approach."),
        ("benefit", "🎁", "উপকার", "Exercise has many benefits."),
        ("challenge", "🧗", "চ্যালেঞ্জ", "Learning English is a challenge."),
        ("essential", "⭐", "অপরিহার্য", "Sleep is essential for children."),
        ("furthermore", "➕", "অধিকন্তু", "Furthermore, it saves time."),
        ("contribute", "🤲", "অবদান রাখা", "Everyone can contribute."),
        ("analyse", "🧪", "বিশ্লেষণ করা", "Let's analyse the results."),
    ]),
]

# Speaking practice. "repeat": say the sentence; "answer": answer the question in your own words.
SPEAKING = {
    0: ("repeat", ["sun", "cat", "pig", "fish", "ship", "three", "very", "water"]),
    1: ("repeat", ["a red hat", "the dog can run", "a big ship", "I can see a fish", "this is my bag"]),
    2: ("repeat", ["The frog can jump.", "I like cake.", "The boat is on the river.",
                   "My kite is blue.", "Five green trees."]),
    3: ("repeat", ["My name is Rafi.", "This is my mother.", "I am seven years old.",
                   "It's a chair.", "I like rice and fish."]),
    4: ("repeat", ["I get up at six o'clock.", "She goes to school by rickshaw.",
                   "I can swim, but I can't fly.", "The market is next to the mosque.",
                   "We eat dinner at nine."]),
    5: ("answer", ["What did you do yesterday?", "Who is your best friend? Why?",
                   "What is your favourite season? Why?", "Tell me about your family.",
                   "What do you want to be when you grow up?"]),
    6: ("answer", ["Have you ever been to Cox's Bazar? Tell me about it.",
                   "Do you think children should have mobile phones? Why?",
                   "What is the best way to learn English?",
                   "Describe your favourite festival."]),
    7: ("answer", ["What are the advantages and disadvantages of living in a big city?",
                   "How has technology changed the way families spend time together?",
                   "Should school start later in the morning? Give your reasons."]),
    8: ("answer", ["To what extent should the government pay for higher education?",
                   "Is it better to learn from experience or from books? Discuss.",
                   "How can communities prepare better for floods?"]),
}

WRITING_PROMPTS = {
    "young": ["Write 3 things you can see in your room.", "Write about your favourite animal.",
              "Write the names of your family members."],
    "mid": ["Write about your day yesterday (5 sentences).", "Describe your best friend.",
            "Write a short letter to your grandmother."],
    "high": ["Do you think homework is useful? Give two reasons.",
             "Describe a place in Bangladesh you would like to visit, and why.",
             "Write an email to your teacher asking for one day of leave."],
}

# The 10 "How to use FamilyEnglish" tutorials — the same topics as IELTSly's series,
# with FamilyEnglish examples. (order, title, title_bn, group, summary, steps_bn, minutes, link_name)
TUTORIALS = [
    (1, "Create your family account", "ফ্যামিলি অ্যাকাউন্ট খুলুন", "Getting started",
     "Any adult — parent, grandparent or elder — opens one account for the whole family.",
     "হোম পেজে 'Start free' চাপুন।\nআপনার নাম, ইমেইল ও পাসওয়ার্ড দিন।\nপরিবারের নাম লিখুন (যেমন: Bhuiyan family)।\n"
     "'Create account' চাপুন — ১৪ দিনের ফ্রি ট্রায়াল শুরু হবে।", 2, "core:signup"),
    (2, "Add learners and set the goal", "শিক্ষার্থী যোগ করুন ও লক্ষ্য ঠিক করুন", "Getting started",
     "Add up to 6 learners, take the level test and choose the full course (1, 2 or 3 years).",
     "'Add learner' চাপুন, নাম ও জন্মসাল দিন।\nছোট শিশুর জন্য চাইলে ৪ সংখ্যার গোপন কোড দিন।\n"
     "প্লেসমেন্ট টেস্ট দিন — লেভেল বের হবে।\n'Make my study plan' এ শেষ লেভেল ও মাস বেছে নিন।", 3, "core:learner_add"),
    (3, "Dashboard, placement test and lessons tour", "ড্যাশবোর্ড, প্লেসমেন্ট টেস্ট ও লেসন", "Getting started",
     "Today's mission, the calendar, the lesson library and topic videos.",
     "Dashboard-এ 'Today's mission' থেকে আজকের লেসন শুরু করুন।\nপ্রতিটি লেসনে: ভিডিও → নোট → অনুশীলন → বাসার কাজ।\n"
     "Study plan-এ ক্যালেন্ডার দেখুন; শুক্রবার Family English day।\n'All lessons' থেকে যেকোনো লেসন খুলতে পারবেন।", 4, "learning:today"),
    (4, "Level checks and skill practice", "লেভেল চেক ও স্কিল অনুশীলন", "Practice & tests",
     "Re-check one skill every month, and drill Listening, Reading or Writing in 10-question rounds.",
     "'Level checks' খুলুন, একটি skill বেছে নিন।\nপ্রশ্ন ধীরে ধীরে কঠিন হয় — জানা না থাকলে অনুমান করুন।\n"
     "ফলাফলে নতুন লেভেল দেখাবে।\n'Skill practice' এ প্রতিদিন ১০ প্রশ্নের ছোট রাউন্ড দিন।", 3, "practice:checks"),
    (5, "Ask the AI tutor", "এআই টিউটরকে প্রশ্ন করুন", "AI tools",
     "Ask how to say a sound, when to use 'an', or how to change your plan — in English or Bangla.",
     "'Ask tutor' খুলুন।\nইংরেজি বা বাংলায় প্রশ্ন লিখুন।\nউত্তর সহজ ইংরেজিতে, সাথে বাংলা ব্যাখ্যা।\n"
     "বাবা-মা Family পেজ থেকে শিশুর প্রশ্নোত্তর দেখতে পারেন।", 2, "practice:tutor"),
    (6, "Practise speaking", "কথা বলার অনুশীলন", "AI tools",
     "Say words and sentences into the microphone and see which words were heard.",
     "'Speaking practice' খুলুন, মাইক্রোফোনের অনুমতি দিন (Chrome ভালো কাজ করে)।\n▶ চেপে বাক্যটি শুনুন।\n"
     "🎤 চেপে বাক্যটি বলুন।\nকোন শব্দ বোঝা যায়নি তা দেখে আবার চেষ্টা করুন।", 4, "practice:speaking"),
    (7, "Writing helper", "লেখার সহায়ক", "AI tools",
     "Write a few sentences and get them corrected, with a Bangla note for every fix.",
     "'Writing helper' খুলুন।\nএকটি বিষয় বেছে নিন বা নিজের মতো লিখুন।\n'Check my writing' চাপুন।\n"
     "সংশোধিত লেখা ও বাংলায় কারণ দেখুন, তারপর নিজে আবার লিখুন।", 3, "practice:writing"),
    (8, "Vocabulary flashcards", "শব্দের ফ্ল্যাশকার্ড", "Learning",
     "Picture cards with Bangla meanings. Cards you know come back less often.",
     "'Vocabulary' খুলুন, একটি ডেক বেছে নিন।\nছবি দেখে শব্দটি বলুন, তারপর কার্ড উল্টান।\n"
     "'I knew it' বা 'Again' চাপুন।\n'Due for review' কার্ডগুলো প্রতিদিন একবার দেখুন।", 3, "practice:vocab"),
    (9, "Track progress: reports and streaks", "অগ্রগতি: রিপোর্ট ও স্ট্রিক", "Reports",
     "See level checks, speaking and writing history, words learned, XP and your streak.",
     "'My reports' খুলুন।\nপ্রতিটি skill-এর লেভেল কীভাবে বদলেছে দেখুন।\n"
     "প্রতিদিন একটি লেসন শেষ করলে 🔥 streak বাড়ে।\nFamily leaderboard-এ এই সপ্তাহের XP দেখুন।", 2, "practice:reports"),
    (10, "Refer and earn", "রেফার করুন, ফ্রি দিন পান", "Refer & earn",
     "Share your family code. They get 7 extra trial days; you get 30 free days when they first pay.",
     "'Refer & earn' খুলুন।\nআপনার কোড বা লিংক কপি করুন।\nআত্মীয় বা বন্ধুকে পাঠান।\n"
     "তারা প্রথমবার টাকা দিলে আপনার পরিবার ৩০ দিন ফ্রি পাবে।", 2, "practice:refer"),
]


# Typing speed texts (our own sentences). Easy: short words; Medium: everyday sentences;
# Hard: longer words and punctuation, close to exam typing.
TYPING_TEXTS = {
    "easy": [
        "the sun is hot and the sky is blue. we can play in the park and then go home for rice and dal.",
        "my cat likes milk. my dog likes to run. we have a red ball and a big box in the yard.",
        "i get up at six. i wash my face and eat bread. then i go to school with my sister.",
    ],
    "medium": [
        "Every Friday our family visits Grandma. She tells us stories about her village, and we help her cook lunch.",
        "The market is busy in the morning. People buy fish, vegetables and fruit before it gets too hot.",
        "Reading for ten minutes a day can make a big difference. Choose a short story and read it aloud.",
    ],
    "hard": [
        "Although mobile phones are useful for learning, children should balance screen time with outdoor play, "
        "reading and conversation; otherwise, their sleep and concentration may suffer.",
        "In many districts, solar panels have replaced kerosene lamps, which means families save money and "
        "students can study safely after dark. However, old batteries must be recycled properly.",
        "The chart shows that the number of families using mobile banking rose steadily between 2016 and 2024, "
        "while those relying only on bank branches fell from 60% to 25%.",
    ],
}
