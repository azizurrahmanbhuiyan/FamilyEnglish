from ._h import C, L, T

SKILL = "reading"

LESSONS = [
    # ------------------------------------------------------------------ EASY
    L("rd-e1", "easy", 1, "Picture sentences", "ছবির বাক্য",
      "Read short sentences and match them with meaning.",
      "Read each word. Point with your finger. Small words matter: on, in, under, a, the.",
      "আঙুল দিয়ে প্রতিটি শব্দ ছুঁয়ে পড়ুন। ছোট শব্দগুলো (on, in, under) অর্থ বদলে দেয়।",
      "শিশুর সাথে একসাথে জোরে পড়ুন — আগে আপনি, পরে শিশু।",
      ["The cat is on the mat.", "The sun is hot.", "A big dog is in the box."],
      passage="The cat is on the mat. The dog is under the table. A red ball is in the box. "
              "The sun is big and hot. Mina has a hat.",
      passage_title="Read",
      video="Oxford Owl phonics reading simple sentences",
      practice=[
          C("Where is the cat?", "on the mat", "under the table", "in the box", qt="rd_detail",
            why="'The cat is on the mat.'"),
          C("What is in the box?", "a red ball", "the dog", "a hat", qt="rd_detail",
            why="'A red ball is in the box.'"),
          C("The sun is…", "big and hot", "small and cold", "red", qt="rd_detail", why="big and hot।"),
          T("Who has a hat? (one word)", "Mina", qt="rd_detail", why="'Mina has a hat.'"),
      ],
      test=[
          C("Where is the dog?", "under the table", "on the mat", "in the box", qt="rd_detail",
            why="under the table।"),
          C("What colour is the ball?", "red", "blue", "big", qt="rd_detail", why="a red ball।"),
          C("'under' means…", "নিচে", "উপরে", "ভেতরে", qt="rd_vocab", why="under = নিচে।"),
          C("Is the sun cold?", "no", "yes", qt="rd_detail", why="The sun is hot।"),
          C("What does Mina have?", "a hat", "a cat", "a ball", qt="rd_detail", why="a hat।"),
      ]),

    L("rd-e2", "easy", 2, "A note from Mum", "মায়ের চিরকুট",
      "Read a short note and find what to do.",
      "Notes are short. Look for the action words (buy, feed, call) and the times.",
      "চিরকুটে কাজের শব্দ (buy, feed, call) আর সময় খুঁজুন।",
      "", [],
      passage="Dear Rafi,\nI am at Aunt Lina's house. Please feed the cat at five o'clock. "
              "Do your homework before you watch TV. There is rice and dal in the kitchen. "
              "I will be home at seven.\nLove, Mum",
      passage_title="A note on the fridge",
      video="Oxford Owl reading notes for children",
      practice=[
          C("Where is Mum?", "at Aunt Lina's house", "at work", "in the kitchen", qt="rd_detail",
            why="'I am at Aunt Lina's house.'"),
          C("What must Rafi do at five?", "feed the cat", "watch TV", "eat dinner", qt="rd_detail",
            why="'feed the cat at five o'clock'।"),
          C("What should he do before TV?", "his homework", "cook rice", "call Mum", qt="rd_detail",
            why="'Do your homework before you watch TV.'"),
          T("What time will Mum come home? (number)", "7", accept=["seven", "7:00"], qt="rd_detail",
            why="'I will be home at seven.'"),
      ],
      test=[
          C("Who wrote the note?", "Mum", "Rafi", "Aunt Lina", qt="rd_gist", why="Love, Mum।"),
          C("What food is in the kitchen?", "rice and dal", "fish and rice", "bread", qt="rd_detail",
            why="rice and dal।"),
          C("Why did Mum write the note?", "to tell Rafi what to do", "to say happy birthday",
            "to buy food", qt="rd_gist", why="কাজের নির্দেশ দিতে।"),
          C("'feed' means…", "খাওয়ানো", "খেলা", "ঘুমানো", qt="rd_vocab", why="feed = খাওয়ানো।"),
          C("Can Rafi watch TV first?", "no", "yes", qt="rd_infer", why="আগে homework।"),
      ]),

    L("rd-e3", "easy", 3, "Signs around us", "আমাদের চারপাশের সাইন",
      "Understand common signs.",
      "Signs use few words: EXIT, NO PARKING, PUSH, PULL, KEEP LEFT, WET FLOOR. "
      "'NO' + action means you must not do it.",
      "সাইনে কম শব্দ: NO SMOKING = ধূমপান নিষেধ, PULL = টানুন, PUSH = ঠেলুন।",
      "দরজায় PUSH/PULL প্রায় সবাই গুলিয়ে ফেলে — PUSH = ঠেলুন।",
      ["EXIT", "WET FLOOR", "NO PARKING", "PULL"],
      video="British Council LearnEnglish signs",
      practice=[
          C("NO SMOKING means…", "Don't smoke here.", "You can smoke here.", "Buy cigarettes here.",
            qt="rd_vocab", why="NO + action = নিষেধ।"),
          C("You want to leave the building. Look for…", "EXIT", "ENTRANCE", "TOILETS", qt="rd_vocab",
            why="EXIT = বের হওয়ার পথ।"),
          C("WET FLOOR means…", "Be careful, you might slip.", "Wash the floor.", "Swim here.",
            qt="rd_infer", why="মেঝে ভেজা — সাবধান।"),
          C("A door says PUSH. You…", "push it away from you", "pull it towards you", "knock",
            qt="rd_vocab", why="PUSH = ঠেলুন।"),
      ],
      test=[
          C("NO PARKING means…", "Don't leave your car here.", "Park here.", "Cars for sale.",
            qt="rd_vocab", why="গাড়ি রাখা নিষেধ।"),
          C("Where do you see 'OPEN 9am–5pm'?", "on a shop door", "on a bus", "on a book",
            qt="rd_infer", why="দোকানের সময়।"),
          C("KEEP LEFT means…", "stay on the left side", "turn right", "stop", qt="rd_vocab",
            why="বাঁ দিকে থাকুন।"),
          C("A door says PULL. You…", "pull it towards you", "push it", "close it", qt="rd_vocab",
            why="PULL = টানুন।"),
          C("OUT OF ORDER means…", "it doesn't work", "it's new", "it's free", qt="rd_vocab",
            why="নষ্ট/চলছে না।"),
      ]),

    L("rd-e4", "easy", 4, "Lists and a menu", "তালিকা ও মেনু",
      "Find information in a list or menu quickly.",
      "You don't read a menu like a story. Move your eyes down the list and stop at what you need.",
      "মেনু গল্পের মতো পড়া হয় না — চোখ নিচে নামিয়ে দরকারি জিনিস খুঁজুন (scanning)।",
      "", [],
      passage="CAFE SHAPLA — MENU\nTea ........ 20 taka\nCoffee ........ 60 taka\nSamosa (2) ........ 30 taka\n"
              "Egg sandwich ........ 80 taka\nChicken soup ........ 120 taka\nMango juice ........ 70 taka\n"
              "Open every day 8am – 10pm",
      passage_title="A café menu",
      video="British Council LearnEnglish menu reading",
      practice=[
          T("How much is a cup of tea? (number)", "20", accept=["20 taka"], qt="rd_detail", why="Tea — 20 taka।"),
          C("Which is the most expensive?", "chicken soup", "coffee", "mango juice", qt="rd_detail",
            why="120 taka।"),
          C("How many samosas for 30 taka?", "two", "one", "three", qt="rd_detail", why="Samosa (2)।"),
          C("What time does the café open?", "8am", "10am", "8pm", qt="rd_detail", why="8am – 10pm।"),
      ],
      test=[
          T("How much is mango juice? (number)", "70", accept=["70 taka"], qt="rd_detail", why="70 taka।"),
          C("Tea and a samosa plate cost…", "50 taka", "40 taka", "60 taka", qt="rd_detail",
            why="20 + 30 = 50।"),
          C("Which is NOT on the menu?", "pizza", "egg sandwich", "coffee", qt="rd_detail",
            why="pizza নেই।"),
          C("What time does it close?", "10pm", "8pm", "9pm", qt="rd_detail", why="10pm।"),
          C("Is the café open on Friday?", "yes", "no", qt="rd_infer", why="Open every day।"),
      ]),

    L("rd-e5", "easy", 5, "A short story: The clever crow", "ছোট গল্প: বুদ্ধিমান কাক",
      "Read a short story and understand what happens.",
      "Stories have a beginning (who and where), a problem, and an end (how it is solved).",
      "গল্পে থাকে শুরু (কে, কোথায়), সমস্যা, আর শেষ (কীভাবে সমাধান)।",
      "গল্প পড়ার পর শিশুকে বাংলায় গল্পটা বলতে বলুন — বুঝেছে কি না বোঝা যাবে।",
      [],
      passage="It was a hot summer day. A crow was very thirsty. He flew everywhere to find water. "
              "At last he saw a pot under a tree. There was a little water at the bottom, but his beak "
              "could not reach it. The crow had an idea. He picked up small stones and dropped them into "
              "the pot, one by one. Slowly the water came up. The crow drank the water and flew away happily.",
      passage_title="The clever crow",
      video="Oxford Owl story time thirsty crow",
      practice=[
          C("What was the problem?", "The crow was thirsty.", "The crow was hungry.", "The crow was lost.",
            qt="rd_gist", why="'A crow was very thirsty.'"),
          C("Where was the pot?", "under a tree", "on a roof", "in a house", qt="rd_detail",
            why="'a pot under a tree'।"),
          C("Why couldn't he drink at first?", "The water was too low.", "The pot was broken.",
            "There was no water.", qt="rd_infer", why="'his beak could not reach it'।"),
          C("What did he drop into the pot?", "stones", "leaves", "sticks", qt="rd_detail", why="small stones।"),
      ],
      test=[
          C("What season was it?", "summer", "winter", "rainy season", qt="rd_detail", why="hot summer day।"),
          C("'thirsty' means…", "পিপাসার্ত", "ক্ষুধার্ত", "ক্লান্ত", qt="rd_vocab", why="thirsty = পিপাসার্ত।"),
          C("How did the crow feel at the end?", "happy", "sad", "angry", qt="rd_detail", why="flew away happily।"),
          C("What is the lesson of the story?", "Think and you can solve problems.", "Crows love stones.",
            "Summer is long.", qt="rd_infer", why="বুদ্ধি খাটালে সমাধান মেলে।"),
          C("'One by one' means…", "one after another", "all together", "very fast", qt="rd_vocab",
            why="একটা একটা করে।"),
      ]),

    # ------------------------------------------------------------------ MEDIUM
    L("rd-m1", "medium", 1, "A school notice", "স্কুলের নোটিশ",
      "Find dates, rules and actions in a notice.",
      "Notices give: what is happening, when, where, and what you must do. Underline dates and verbs "
      "like 'bring', 'must', 'should'.",
      "নোটিশে খুঁজুন: কী, কবে, কোথায়, আপনাকে কী করতে হবে। must = অবশ্যই।",
      "অভিভাবক হিসেবে স্কুলের ইংরেজি নোটিশ নিজে পড়ুন, তারপর সন্তানকে বুঝিয়ে দিন — দুজনেরই শেখা হবে।",
      [],
      passage="NOTICE — SPORTS DAY\nOur annual Sports Day will be held on Thursday 12 December at the "
              "school field. Students must come in their house colour T-shirt and bring a water bottle. "
              "Parents are welcome from 10am. The events will finish at 1pm, and prizes will be given at "
              "the end. If it rains, Sports Day will move to Sunday 15 December.\nThe Head Teacher",
      passage_title="Notice board",
      video="British Council LearnEnglish Teens reading notice",
      practice=[
          C("What is the notice about?", "Sports Day", "an exam", "a holiday", qt="rd_gist", why="SPORTS DAY।"),
          C("What must students bring?", "a water bottle", "lunch", "a book", qt="rd_detail",
            why="'bring a water bottle'।"),
          C("When can parents come?", "from 10am", "from 1pm", "at 9am", qt="rd_detail", why="from 10am।"),
          C("What happens if it rains?", "It moves to Sunday 15 December.", "It is cancelled.",
            "It happens inside.", qt="rd_detail", why="'move to Sunday 15 December'।"),
      ],
      test=[
          C("Where is Sports Day?", "the school field", "the stadium", "the park", qt="rd_detail",
            why="at the school field।"),
          C("What should students wear?", "house colour T-shirt", "school uniform", "any clothes",
            qt="rd_detail", why="house colour T-shirt।"),
          C("When are prizes given?", "at the end", "at 10am", "before the events", qt="rd_detail",
            why="'prizes will be given at the end'।"),
          C("'annual' means…", "every year", "every month", "once only", qt="rd_vocab", why="annual = বার্ষিক।"),
          C("Who wrote the notice?", "The Head Teacher", "a parent", "a student", qt="rd_detail",
            why="The Head Teacher।"),
      ]),

    L("rd-m2", "medium", 2, "An email from a friend", "বন্ধুর ইমেইল",
      "Understand news, plans and questions in an informal email.",
      "Informal emails start with 'Hi' and use short forms (I'm, can't). Friends share news, make "
      "plans and ask questions. Find the reason for writing.",
      "বন্ধুর ইমেইলে Hi, I'm, can't-এর মতো ছোট রূপ থাকে। কেন লিখেছে সেটা আগে খুঁজুন।",
      "", [],
      passage="Hi Tanvir,\nGuess what? I passed my driving test yesterday! I'm so happy. Dad says I can "
              "borrow his car at the weekend, so would you like to go to Cox's Bazar on Saturday? We can "
              "leave early, at 6am, and come back on Sunday evening. My cousin Nila wants to come too. "
              "Can you let me know by Thursday?\nSee you soon,\nSabbir",
      passage_title="Email",
      video="British Council LearnEnglish informal email reading",
      practice=[
          C("What is Sabbir's good news?", "He passed his driving test.", "He bought a car.",
            "He got a job.", qt="rd_gist", why="'I passed my driving test'।"),
          C("Where does he want to go?", "Cox's Bazar", "Sylhet", "Dhaka", qt="rd_detail", why="Cox's Bazar।"),
          C("Whose car will they use?", "Sabbir's dad's", "Tanvir's", "Nila's", qt="rd_detail",
            why="'borrow his (Dad's) car'।"),
          C("When must Tanvir reply?", "by Thursday", "on Saturday", "today", qt="rd_detail", why="by Thursday।"),
      ],
      test=[
          C("Why did Sabbir write?", "to invite Tanvir on a trip", "to say sorry", "to ask for money",
            qt="rd_gist", why="ভ্রমণে আমন্ত্রণ।"),
          C("Who else wants to come?", "Nila", "Dad", "Tanvir's sister", qt="rd_detail", why="cousin Nila।"),
          C("When will they come back?", "Sunday evening", "Saturday night", "Monday", qt="rd_detail",
            why="Sunday evening।"),
          C("How does Sabbir feel?", "happy", "nervous", "tired", qt="rd_infer", why="I'm so happy।"),
          C("'borrow' means…", "use something and give it back", "buy", "sell", qt="rd_vocab",
            why="ধার নেওয়া।"),
      ]),

    L("rd-m3", "medium", 3, "Reading a timetable", "সময়সূচি পড়া",
      "Find times and work out journeys from a timetable.",
      "Read across a row for one train, down a column for one station. Use the 24-hour clock: "
      "14:30 = 2:30 pm.",
      "সারি (row) ধরে একটি ট্রেন, কলাম ধরে একটি স্টেশন। 14:30 = দুপুর ২:৩০।",
      "", [],
      passage="DHAKA – CHATTOGRAM TRAINS\nTrain | Leaves Dhaka | Arrives Cumilla | Arrives Chattogram\n"
              "Subarna Express | 07:00 | — (no stop) | 12:15\nMahanagar | 07:45 | 10:30 | 14:20\n"
              "Turna (night) | 23:30 | 02:05 | 05:40",
      passage_title="Timetable",
      video="British Council LearnEnglish timetable reading",
      practice=[
          C("Which train is fastest to Chattogram?", "Subarna Express", "Mahanagar", "Turna", qt="rd_detail",
            why="7:00 → 12:15 = ৫ ঘণ্টা ১৫ মিনিট।"),
          C("Which train does NOT stop at Cumilla?", "Subarna Express", "Mahanagar", "Turna", qt="rd_detail",
            why="— (no stop)।"),
          T("When does Mahanagar arrive in Chattogram? (hh:mm)", "14:20", accept=["2:20", "2:20 pm"],
            qt="rd_detail", why="14:20 = 2:20 pm।"),
          C("Which train travels at night?", "Turna", "Mahanagar", "Subarna Express", qt="rd_detail",
            why="Turna (night)।"),
      ],
      test=[
          C("You must be in Cumilla before 11am. Take…", "Mahanagar", "Subarna Express", "Turna",
            qt="rd_infer", why="Mahanagar 10:30-এ Cumilla পৌঁছায়।"),
          C("14:20 is…", "2:20 pm", "4:20 pm", "2:20 am", qt="rd_vocab", why="14 − 12 = 2 pm।"),
          T("When does Turna leave Dhaka? (hh:mm)", "23:30", accept=["11:30 pm", "11:30"], qt="rd_detail",
            why="23:30।"),
          C("How long does Turna take to Chattogram?", "6 hours 10 minutes", "5 hours", "7 hours",
            qt="rd_infer", why="23:30 → 05:40।"),
          C("Which train leaves first in the morning?", "Subarna Express", "Mahanagar", "Turna",
            qt="rd_detail", why="07:00।"),
      ]),

    L("rd-m4", "medium", 4, "An article: Mangoes of Bangladesh", "প্রবন্ধ: বাংলাদেশের আম",
      "Find the main idea of each paragraph.",
      "Each paragraph usually has one main idea, often in the first sentence (the topic sentence). "
      "Read the first sentence of each paragraph before the details.",
      "প্রতিটি অনুচ্ছেদের প্রথম বাক্যে (topic sentence) সাধারণত মূল ভাবনা থাকে।",
      "পুরো লেখা পড়ার আগে প্রতিটি অনুচ্ছেদের প্রথম বাক্য পড়ুন — দ্রুত মূল বিষয় ধরা যায়।",
      [],
      passage="The mango is the national tree of Bangladesh, and its fruit is loved by almost everyone. "
              "The best-known mango areas are Rajshahi and Chapainawabganj in the north-west.\n\n"
              "There are many varieties. Himsagar is famous for its sweet taste, while Langra has a strong "
              "smell and thin skin. Fazli mangoes are very large and come late in the season.\n\n"
              "Mangoes are also important for farmers. Thousands of families earn money from mango gardens, "
              "and some mangoes are now sold abroad, for example to the UK and the Middle East.",
      passage_title="Mangoes of Bangladesh",
      video="BBC Learning English reading skimming",
      practice=[
          C("Paragraph 1 is mainly about…", "the mango as a national symbol and where it grows",
            "how to cook mango", "mango prices", qt="rd_gist", why="প্রথম অনুচ্ছেদ: national tree + এলাকা।"),
          C("Paragraph 2 is mainly about…", "different kinds of mango", "farmers", "exports",
            qt="rd_gist", why="There are many varieties।"),
          C("Which mango is very large?", "Fazli", "Himsagar", "Langra", qt="rd_detail", why="Fazli।"),
          C("Where are mangoes sold abroad?", "the UK and the Middle East", "India and China", "Japan",
            qt="rd_detail", why="UK and the Middle East।"),
      ],
      test=[
          C("Paragraph 3 is mainly about…", "why mangoes matter for farmers", "mango taste",
            "mango trees", qt="rd_gist", why="farmers + money।"),
          C("Which mango has a strong smell?", "Langra", "Fazli", "Himsagar", qt="rd_detail", why="Langra।"),
          C("Where are the best-known mango areas?", "the north-west", "the south", "the east",
            qt="rd_detail", why="north-west।"),
          C("'varieties' means…", "different types", "prices", "gardens", qt="rd_vocab", why="প্রকারভেদ।"),
          C("'abroad' means…", "in other countries", "in the market", "at home", qt="rd_vocab",
            why="বিদেশে।"),
      ]),

    L("rd-m5", "medium", 5, "Following a recipe", "রেসিপি অনুসরণ",
      "Follow instructions in the right order.",
      "Recipes have a list of ingredients and numbered steps. Imperatives (chop, add, stir) tell you "
      "what to do. Words like 'until' tell you when to stop.",
      "রেসিপিতে উপকরণ আর ধাপ থাকে। chop = কুচি, stir = নাড়ুন, until = যতক্ষণ না।",
      "", [],
      passage="EGG CURRY (serves 4)\nIngredients: 6 eggs, 2 onions, 2 tomatoes, 1 teaspoon turmeric, "
              "1 teaspoon chilli powder, salt, oil.\nSteps:\n1. Boil the eggs for 10 minutes, then peel them.\n"
              "2. Chop the onions and fry them in oil until golden.\n3. Add the tomatoes, turmeric, chilli and salt. "
              "Stir for 5 minutes.\n4. Add a cup of water and the eggs. Cook on low heat for 10 minutes.",
      passage_title="Recipe card",
      video="British Council LearnEnglish recipe instructions",
      practice=[
          C("How many eggs do you need?", "6", "4", "2", qt="rd_detail", why="6 eggs।"),
          C("What do you do first?", "boil the eggs", "chop the onions", "add water", qt="rd_detail",
            why="Step 1।"),
          C("Fry the onions until they are…", "golden", "black", "soft", qt="rd_detail", why="until golden।"),
          C("'serves 4' means…", "enough for 4 people", "4 steps", "4 minutes", qt="rd_vocab",
            why="৪ জনের জন্য।"),
      ],
      test=[
          C("When do you add the turmeric?", "step 3", "step 1", "step 4", qt="rd_detail", why="Step 3।"),
          C("How long do you cook at the end?", "10 minutes", "5 minutes", "20 minutes", qt="rd_detail",
            why="10 minutes on low heat।"),
          C("'peel' means…", "take off the skin", "cut into pieces", "cook", qt="rd_vocab", why="খোসা ছাড়ানো।"),
          C("What goes in with the water?", "the eggs", "the onions", "the salt", qt="rd_detail",
            why="'Add a cup of water and the eggs.'"),
          C("'Stir' means…", "mix with a spoon", "boil", "pour out", qt="rd_vocab", why="নাড়ুন।"),
      ]),

    # ------------------------------------------------------------------ ADVANCED
    L("rd-a1", "advanced", 1, "Skimming for the main idea", "স্কিমিং: মূল ভাবনা",
      "Read quickly to get the general idea.",
      "Skimming means reading fast for the gist: the title, first and last sentences, and repeated "
      "key words. You don't stop at difficult words.",
      "Skimming = দ্রুত পড়ে মূল ভাবনা ধরা: শিরোনাম, প্রথম ও শেষ বাক্য, বারবার আসা শব্দ।",
      "IELTS Reading-এ সময় কম — প্রথমে পুরো লেখা ৬০ সেকেন্ডে skim করুন, তারপর প্রশ্নে যান।",
      [],
      passage="Mobile banking has changed daily life in Bangladesh. Ten years ago, sending money to a "
              "village meant a long bus journey or an expensive agent. Today, millions of people send and "
              "receive money with a few taps on a basic phone. Garment workers support parents in rural "
              "areas, and small shopkeepers accept payments without cash. However, experts warn that users "
              "must protect their PIN numbers, because fraud calls are becoming more common. Overall, "
              "mobile banking has made money faster and cheaper to move, but safety awareness must grow too.",
      passage_title="Money in your pocket",
      video="BBC Learning English skimming and scanning",
      practice=[
          C("What is the text mainly about?", "how mobile banking changed life", "garment factories",
            "bus journeys", qt="rd_gist", why="প্রথম বাক্য: Mobile banking has changed daily life।"),
          C("Which sentences help most for skimming?", "the first and last", "only the middle",
            "every word", qt="rd_gist", why="প্রথম ও শেষ বাক্যে মূল ভাবনা।"),
          C("What is the writer's warning?", "protect your PIN", "don't use phones", "banks are closing",
            qt="rd_detail", why="'protect their PIN numbers'।"),
          C("'rural' means…", "in the countryside", "in the city", "abroad", qt="rd_vocab", why="গ্রামীণ।"),
      ],
      test=[
          C("Which title fits best?", "Mobile money: faster, but be careful", "Village life",
            "How to buy a phone", qt="rd_gist", why="সুবিধা + সতর্কতা।"),
          C("How did people send money ten years ago?", "by bus or an agent", "by email", "by post only",
            qt="rd_detail", why="bus journey or an expensive agent।"),
          C("'fraud' means…", "cheating to get money", "a new phone", "a bank", qt="rd_vocab", why="প্রতারণা।"),
          C("'However' in the text introduces…", "a problem", "an example", "a date", qt="rd_infer",
            why="However → সতর্কতা/সমস্যা।"),
          C("The writer's overall view is…", "positive, with a warning", "completely negative",
            "not clear", qt="rd_infer", why="Overall: faster and cheaper, but safety must grow।"),
      ]),

    L("rd-a2", "advanced", 2, "Scanning for facts", "স্ক্যানিং: নির্দিষ্ট তথ্য",
      "Find numbers, names and dates fast.",
      "Scanning means looking for one specific thing. Decide what it looks like (a number? a capital "
      "letter?) and move your eyes quickly until you find it.",
      "Scanning = নির্দিষ্ট তথ্য খোঁজা। আগে ঠিক করুন কী খুঁজছেন — সংখ্যা, নাম না তারিখ।",
      "", [],
      passage="The Sundarbans is the largest mangrove forest in the world. It covers about 10,000 square "
              "kilometres, and around 60 percent of it is in Bangladesh; the rest is in India. It became a "
              "UNESCO World Heritage Site in 1997. The forest is home to the Royal Bengal tiger; a 2018 "
              "survey counted 114 tigers on the Bangladesh side. It also protects coastal villages from "
              "cyclones such as Sidr, which hit in 2007.",
      passage_title="The Sundarbans: fact file",
      video="BBC Learning English reading for detail",
      practice=[
          T("What percentage is in Bangladesh? (number)", "60", accept=["60%", "60 percent"],
            qt="rd_detail", why="around 60 percent।"),
          T("When did it become a World Heritage Site? (year)", "1997", qt="rd_detail", why="1997।"),
          C("How many tigers were counted in 2018?", "114", "141", "1,140", qt="rd_detail", why="114।"),
          C("Which cyclone is named?", "Sidr", "Aila", "Amphan", qt="rd_detail", why="Sidr, 2007।"),
      ],
      test=[
          T("How big is the forest? (square km, number)", "10000", accept=["10,000", "10 000"],
            qt="rd_detail", why="about 10,000 square kilometres।"),
          C("Where is the rest of the forest?", "India", "Myanmar", "Nepal", qt="rd_detail", why="India।"),
          T("When did Sidr hit? (year)", "2007", qt="rd_detail", why="2007।"),
          C("Which animal is mentioned?", "Royal Bengal tiger", "elephant", "crocodile", qt="rd_detail",
            why="Royal Bengal tiger।"),
          C("What does the forest protect villages from?", "cyclones", "floods only", "tigers",
            qt="rd_detail", why="cyclones।"),
      ]),

    L("rd-a3", "advanced", 3, "Fact or opinion in a review", "রিভিউতে তথ্য না মতামত",
      "Separate facts from the writer's opinions.",
      "Reviews mix facts (price, place, time) with opinions (delicious, disappointing, I'd recommend). "
      "Adjectives of judgement and 'should' often show opinion.",
      "রিভিউতে তথ্য (দাম, জায়গা) ও মতামত (delicious, disappointing) মেশানো থাকে।",
      "অনলাইনে কেনাকাটার রিভিউ পড়ার সময়ও এই দক্ষতা কাজে লাগে।",
      [],
      passage="Green Leaf Restaurant opened last month on Road 27, Dhanmondi. The menu has twelve "
              "vegetarian dishes, and prices start at 250 taka. The vegetable biryani was absolutely "
              "delicious, but the service was disappointingly slow — we waited forty minutes. The "
              "restaurant is open until 11pm. Overall, I would recommend it for families, but go early.",
      passage_title="Restaurant review",
      video="British Council LearnEnglish fact and opinion",
      practice=[
          C("'The menu has twelve vegetarian dishes.' This is…", "a fact", "an opinion", qt="rd_infer",
            why="যাচাইযোগ্য — fact।"),
          C("'The vegetable biryani was absolutely delicious.' This is…", "an opinion", "a fact",
            qt="rd_infer", why="delicious = মতামত।"),
          C("What did the writer NOT like?", "slow service", "the price", "the food", qt="rd_detail",
            why="service was disappointingly slow।"),
          C("Where is the restaurant?", "Road 27, Dhanmondi", "Gulshan", "Road 7", qt="rd_detail",
            why="Road 27, Dhanmondi।"),
      ],
      test=[
          C("'The restaurant is open until 11pm.' This is…", "a fact", "an opinion", qt="rd_infer", why="fact।"),
          C("'I would recommend it for families.' This is…", "an opinion", "a fact", qt="rd_infer",
            why="recommend = মতামত।"),
          C("How long did they wait?", "forty minutes", "fourteen minutes", "four hours", qt="rd_detail",
            why="forty minutes।"),
          C("What advice does the writer give?", "go early", "go late", "don't go", qt="rd_detail",
            why="but go early।"),
          C("Which word shows opinion?", "disappointingly", "twelve", "Road", qt="rd_infer",
            why="disappointingly = বিচারমূলক শব্দ।"),
      ]),

    L("rd-a4", "advanced", 4, "Inference: reading between the lines", "ইঙ্গিত বোঝা",
      "Understand what the writer means but doesn't say directly.",
      "Writers often show, not tell. If 'she checked her watch for the third time', we infer she is "
      "impatient or worried. Use clues + your own knowledge.",
      "লেখক সবসময় সরাসরি বলেন না — clue থেকে অনুমান করতে হয় (inference)।",
      "উত্তর অবশ্যই লেখার clue দিয়ে প্রমাণ করা যাবে — শুধু নিজের ধারণা থেকে নয়।",
      [],
      passage="Rumana stood at the school gate, holding a small cake box. She checked her phone again: "
              "no messages. Most of the other parents had already left. The guard locked the side door and "
              "looked at her kindly. Then, at last, she saw a small figure running towards her with a "
              "medal swinging around his neck. Rumana's face broke into a wide smile.",
      passage_title="At the gate",
      video="BBC Learning English inference reading",
      practice=[
          C("How did Rumana probably feel before the end?", "worried", "angry", "sleepy", qt="rd_infer",
            why="বারবার ফোন দেখা, সবাই চলে গেছে — চিন্তিত।"),
          C("Who is the 'small figure' probably?", "her child", "the guard", "a teacher", qt="rd_infer",
            why="স্কুল গেট, মেডেল — তার সন্তান।"),
          C("Why might she have a cake?", "to celebrate", "to sell it", "for the guard", qt="rd_infer",
            why="মেডেল + কেক = উদযাপন।"),
          C("Was she one of the first parents to leave?", "no", "yes", qt="rd_infer",
            why="Most of the other parents had already left।"),
      ],
      test=[
          C("What did the child probably do?", "won something", "lost his bag", "got hurt", qt="rd_infer",
            why="medal = জয়।"),
          C("How did Rumana feel at the end?", "happy and relieved", "angry", "bored", qt="rd_infer",
            why="wide smile।"),
          C("Why did the guard look at her 'kindly'?", "he understood she was waiting", "he was angry",
            "she was late for work", qt="rd_infer", why="সবাই চলে গেছে, সে অপেক্ষা করছে।"),
          C("Inference means…", "understanding what is suggested", "copying words", "reading fast",
            qt="rd_infer", why="ইঙ্গিত থেকে বোঝা।"),
          C("Which clue shows time passing?", "Most of the other parents had already left.",
            "holding a small cake box", "a medal", qt="rd_infer", why="সময় পার হয়েছে।"),
      ]),

    L("rd-a5", "advanced", 5, "Words from context", "প্রসঙ্গ থেকে শব্দের অর্থ",
      "Guess the meaning of new words from the sentence around them.",
      "Don't stop at every new word. Look at: the word type (noun, verb, adjective), the words around "
      "it, examples, opposites (but, however) and definitions (which means, such as).",
      "অজানা শব্দে থামবেন না: পাশের শব্দ, উদাহরণ, বিপরীত (but) দেখে অর্থ অনুমান করুন।",
      "অভিধান পরে দেখুন — আগে অনুমান করুন, তারপর মিলিয়ে নিন। এতে শব্দ মনে থাকে।",
      [],
      passage="Many rivers in Bangladesh are polluted, which means they contain harmful waste. Factories "
              "sometimes discharge dirty water directly into them. This is detrimental to fish and to people "
              "who use the water; for example, children can get skin diseases. However, some communities "
              "have been resilient: they recovered quickly by building water filters and planting trees "
              "along the banks.",
      passage_title="Rivers in danger",
      video="BBC Learning English guessing meaning from context",
      practice=[
          C("'polluted' means…", "dirty and harmful", "very deep", "full of fish", qt="rd_vocab",
            why="'which means they contain harmful waste' — সংজ্ঞা দেওয়া আছে।"),
          C("'discharge' is a…", "verb", "noun", "adjective", qt="rd_vocab", why="Factories discharge… — কাজ।"),
          C("'discharge' probably means…", "send out", "clean", "buy", qt="rd_vocab", why="নির্গত করা।"),
          C("'detrimental' probably means…", "harmful", "helpful", "cheap", qt="rd_vocab",
            why="উদাহরণ: skin diseases → ক্ষতিকর।"),
      ],
      test=[
          C("'resilient' probably means…", "able to recover quickly", "very weak", "rich",
            qt="rd_vocab", why="'they recovered quickly' — ব্যাখ্যা আছে।"),
          C("Which phrase gave the meaning of 'polluted'?", "which means", "for example", "however",
            qt="rd_vocab", why="which means = সংজ্ঞা।"),
          C("Which phrase gave an example of harm?", "for example", "which means", "directly",
            qt="rd_vocab", why="for example।"),
          C("'However' in the text shows…", "a contrast", "a number", "a definition", qt="rd_infer",
            why="ভিন্ন দিক।"),
          C("What did communities do?", "built filters and planted trees", "closed factories",
            "moved away", qt="rd_detail", why="water filters + trees।"),
      ]),
]
