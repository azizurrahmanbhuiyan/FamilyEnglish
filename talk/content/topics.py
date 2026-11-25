"""Talk: the topics learners can choose, the daily-talk openers and the Read-and-talk library.

All text here is written by FamilyEnglish. Topic ideas are general (travel, food, science …);
the articles, questions and titles are our own words.

Each category has:
  openers  – three questions the tutor can start a daily talk with
  topics   – article ideas; the AI writes the article the first time someone opens it (then it is saved)
  seed     – one article we wrote ourselves, so Read and talk works even without AI
"""

LEVELS = [
    (1, "Beginner", "শুরু করছি", "I know a few words and simple phrases."),
    (2, "Elementary", "প্রাথমিক", "I can talk about myself and everyday things."),
    (3, "Intermediate", "মাঝারি", "I can have a simple conversation on familiar topics."),
    (4, "Upper intermediate", "উচ্চ-মাঝারি", "I can talk about most topics but make some mistakes."),
    (5, "Advanced", "উন্নত", "I speak fluently and want to sound more natural."),
]

REASONS = [
    ("career", "💼", "For my career", "চাকরি ও ক্যারিয়ারের জন্য"),
    ("study", "🎓", "For study or exams", "পড়াশোনা বা পরীক্ষার জন্য"),
    ("travel", "✈️", "To travel", "ভ্রমণের জন্য"),
    ("abroad", "🌍", "To live abroad", "বিদেশে থাকার জন্য"),
    ("family", "👨‍👩‍👧", "To help my children", "সন্তানদের সাহায্য করতে"),
    ("confidence", "💪", "To feel confident", "আত্মবিশ্বাসী হতে"),
    ("fun", "🎉", "Just for fun", "মজার জন্য"),
]

CHALLENGES = [
    ("speaking", "🗣️", "Speaking without freezing", "আটকে না গিয়ে কথা বলা"),
    ("pronunciation", "👄", "Pronunciation", "উচ্চারণ"),
    ("grammar", "🧩", "Grammar", "ব্যাকরণ"),
    ("vocabulary", "📖", "Finding the right words", "ঠিক শব্দ খুঁজে পাওয়া"),
    ("listening", "👂", "Understanding fast speakers", "দ্রুত কথা বোঝা"),
]

CORRECT = [
    ("always", "Correct me every time", "প্রতিবার ভুল ধরিয়ে দিন"),
    ("big", "Only big mistakes", "শুধু বড় ভুল"),
    ("end", "At the end, in my report", "শেষে, রিপোর্টে"),
]

VOICES = [
    ("classic", "Classic", "স্বাভাবিক", 1.0),
    ("warm", "Warm", "নরম", 0.85),
    ("casual", "Casual", "হালকা মেজাজ", 1.15),
]

SPEEDS = [(1.0, "1×"), (0.8, "0.8×"), (0.6, "0.6×")]

DAILY_GOALS = [5, 10, 15, 20]


def C(key, emoji, title, title_bn, openers, topics, seed):
    return {"key": key, "emoji": emoji, "title": title, "title_bn": title_bn,
            "openers": openers, "topics": topics, "seed": seed}


def A(slug, title, level, body, questions, words):
    """A hand-written article. body: paragraphs separated by blank lines. words: (word, meaning)."""
    return {"slug": slug, "title": title, "level": level, "body": body.strip(), "questions": questions, "words": words}


CATEGORIES = [
    C("travel", "✈️", "Travel", "ভ্রমণ",
      ["Where is the best place you have ever visited, and why?",
       "If you could take a free trip tomorrow, where would you go?",
       "Do you prefer the hills, the sea or a big city for a holiday?"],
      ["Slow travel: seeing more by doing less", "The world's most beautiful railway journeys",
       "How to pack light for a week away", "Travelling on a small budget",
       "Good manners when you visit another country", "Night markets around Asia",
       "Islands worth visiting once in your life", "Why some people travel alone"],
      A("travel-sajek", "Above the clouds in Sajek", 2, """
Sajek Valley is in the hills of Rangamati. Many visitors arrive in the afternoon after a long, bumpy ride in an open jeep. The road climbs higher and higher, and the air becomes cool.

The best time is early morning. People wake up before sunrise, wrap themselves in shawls and walk to the viewpoint. Below them, a white sea of clouds covers the valleys. When the sun comes up, the clouds turn pink and gold.

Visitors stay in small wooden cottages. In the evening they eat bamboo chicken and listen to the wind. There is little mobile signal, so many people say it is the perfect place to switch off their phones.
""", ["Would you like to wake up early to see the clouds? Why?",
      "How do you feel when there is no mobile signal?",
      "Tell me about a place in Bangladesh you want to visit."],
        [("bumpy", "not smooth; full of small jumps"), ("viewpoint", "a high place with a good view"),
         ("switch off", "stop using; turn off")])),

    C("food", "🍛", "Food", "খাবার",
      ["What is your favourite meal, and who cooks it best?",
       "Is there a food you hated as a child but love now?",
       "What would you cook for a guest from another country?"],
      ["Street food around the world", "Why spices travelled across oceans",
       "Rice: one grain, a thousand dishes", "Food myths: what is true and what is not",
       "How markets bring a town together", "Eating with the seasons",
       "Picnic food that travels well", "The story of bread"],
      A("food-fuchka", "The magic of fuchka", 2, """
In the evening, crowds gather around the fuchka stalls of Dhaka. The seller moves fast. He cracks a small, hollow shell with his thumb, fills it with spicy potato and chickpeas, and adds a little grated egg on top.

Then comes the best part: the sour tamarind water. You must eat each fuchka in one bite, or the water runs down your chin. Friends often have a contest to see who can eat the most.

Fuchka is cheap, but it is more than a snack. It is a reason to meet friends after school or work, to laugh and to talk. Many people who move abroad say it is the food they miss most.
""", ["Do you like spicy food? What is the spiciest thing you have eaten?",
      "Which snack reminds you of your friends?",
      "What food would you miss most if you lived abroad?"],
        [("hollow", "empty inside"), ("sour", "a taste like lemon"), ("contest", "a small competition")])),

    C("cooking", "🍳", "Cooking", "রান্না",
      ["Can you cook? What is the first dish you learned?",
       "Who taught you to cook, or who would you like to learn from?",
       "Describe how to make a cup of tea, step by step."],
      ["Cooking with leftovers", "Five meals you can make in fifteen minutes",
       "Kitchen tools that save time", "Planning a week of meals",
       "How to make plain rice perfect every time", "Baking without an oven",
       "Cooking with children safely", "Making food look beautiful on the plate"],
      A("cooking-khichuri", "Rainy-day khichuri", 2, """
When the first heavy rain of the monsoon falls, many families in Bangladesh cook khichuri. It is a simple dish of rice and lentils, cooked together with turmeric, ginger and a little ghee.

First, you wash the rice and the lentils. Next, you fry onions and spices in a big pot until they smell wonderful. Then you add the rice, the lentils and hot water, and let everything cook slowly. Some people add vegetables or a few pieces of beef or chicken.

Khichuri is usually served with fried egg, eggplant fritters and pickles. Eating it while the rain drums on the roof is one of life's small pleasures.
""", ["What do you like to eat on a rainy day?",
      "Can you explain how to cook a simple dish using first, next and then?",
      "What is one of life's small pleasures for you?"],
        [("lentils", "small dried seeds, like dal"), ("fritters", "pieces of food fried in batter"),
         ("drums", "makes a beating sound, like a drum")])),

    C("sports", "⚽", "Sports", "খেলাধুলা",
      ["Which sport do you enjoy watching or playing?",
       "Tell me about a match you will never forget.",
       "Do you think children should play a sport every day?"],
      ["Why fair play matters more than winning", "How running shoes changed over the years",
       "Women's football is growing fast", "What makes a great team captain",
       "Sport and the mind: staying calm under pressure", "Traditional games we should not forget",
       "Big sports events and the cities that host them", "Esports: is gaming a real sport?"],
      A("sports-cricket-street", "Cricket on the playground", 2, """
On Friday mornings, the school playground near Rafi's home becomes a cricket ground. The wicket is a plastic bucket, or three sticks tied together. The ball is often a tennis ball wrapped in tape so it moves faster.

There are special rules. If you hit the ball over the wall, you are out. If the ball goes into the school garden, the batter must ask the guard politely to get it. When the call to prayer begins, everyone stops and rests.

Many famous players started this way. They say playground cricket taught them quick reactions, teamwork and how to play in a small space. Most of all, it taught them to love the game.
""", ["Did you play games in a park or a field as a child?",
      "Which playground cricket rule do you think is the funniest?",
      "What can children learn from playing in a team?"],
        [("playground", "an open place where children play"), ("politely", "in a kind, respectful way"), ("reactions", "how quickly you move when something happens")])),

    C("music", "🎵", "Music", "সংগীত",
      ["What kind of music do you listen to when you are happy?",
       "Can you play an instrument, or which one would you like to learn?",
       "Is there a song that always brings back a memory?"],
      ["How music helps us remember", "Traditional instruments from around the world",
       "Should every child learn music?", "Singing together: why choirs make people happy",
       "From radio to streaming: how we listen now", "Music as a way to calm down",
       "Folk songs and the stories they keep", "Learning English through songs"],
      A("music-baul", "The wandering singers", 3, """
Bauls are wandering singers from Bangladesh and West Bengal. For hundreds of years they have travelled from village to village with simple instruments, such as the one-stringed ektara and a small drum.

Their songs are about love, life and the search for meaning. The words are simple, but the ideas are deep. Many songs ask the listener to look inside their own heart instead of following others blindly.

Today, baul music is played at festivals, on television and online. UNESCO has recognised baul songs as part of the world's cultural heritage. Young musicians now mix baul tunes with guitars and keyboards, so the old songs reach new ears.
""", ["Why do you think old songs are still popular today?",
      "Would you like to travel and perform like a baul? Why or why not?",
      "Do you prefer traditional music or modern music?"],
        [("wandering", "moving from place to place"), ("blindly", "without thinking"), ("heritage", "things from the past that we keep and value")])),

    C("movies", "🎬", "Movies", "চলচ্চিত্র",
      ["What is the last film you watched, and did you like it?",
       "Do you prefer watching films at the cinema or at home?",
       "Which film would you recommend to a friend, and why?"],
      ["How animated films are made", "Why we love stories about heroes",
       "Documentaries that changed how people think", "Film music: the sound of a story",
       "Coming-of-age films and growing up", "Special effects then and now",
       "Books that became films", "Why some films make us cry"],
      A("movies-animation", "Twenty-four pictures a second", 3, """
An animated film is really thousands of still pictures shown very quickly. When we see about twenty-four pictures every second, our brain joins them together and we see movement.

In the past, artists drew every picture by hand. A short film could take months, and a long film could take years and hundreds of artists. Today, most animation is made on computers, but the job is still slow and careful. Animators study how people walk, how hair moves in the wind and how a face changes when someone is surprised.

The best animated films are not only for children. They tell stories about friendship, fear and growing up that adults enjoy too.
""", ["What is your favourite animated film or cartoon?",
      "Why do you think animation takes so much time?",
      "Do you think cartoons are only for children?"],
        [("still", "not moving"), ("careful", "done slowly to avoid mistakes"), ("surprised", "feeling something unexpected")])),

    C("technology", "💻", "Technology", "প্রযুক্তি",
      ["Which app do you use most every day?",
       "How has technology changed your family's life?",
       "Would you like a robot to help at home? What would it do?"],
      ["Staying safe online", "How smartphones changed the way we shop",
       "Artificial intelligence in everyday life", "Smart homes: helpful or too much?",
       "3D printing and what it can make", "Mobile banking in Bangladesh",
       "How to take a break from screens", "The future of travel: trains, cars and more"],
      A("tech-mobile-money", "Money in your pocket", 3, """
Twenty years ago, sending money to your family in a village meant a long trip or a slow post office. Today, millions of people in Bangladesh send money in seconds using a mobile phone.

Mobile financial services let people pay bills, buy things in shops and receive their salary without a bank account. A rickshaw puller in Dhaka can send money to his mother in Kurigram at night, and she can collect it from a small shop the next morning.

There are risks too. Some people receive fake messages asking for their PIN. Experts give one simple rule: never share your PIN or one-time code with anyone, even if they say they are from the company.
""", ["Do you or your family use mobile banking? What for?",
      "What would you do if someone asked for your PIN on the phone?",
      "How has the mobile phone changed life in villages?"],
        [("salary", "money you get for your work"), ("fake", "not real"), ("risks", "chances that something bad may happen")])),

    C("science", "🔬", "Science", "বিজ্ঞান",
      ["Which science subject did you enjoy most at school?",
       "If you could ask a scientist one question, what would it be?",
       "What invention do you think is the most important?"],
      ["Why we dream", "The body clock: why we feel sleepy", "How bees make honey",
       "The science of rainbows", "Why the sea is salty", "How vaccines teach the body",
       "What makes a volcano erupt", "Spider silk: stronger than steel?"],
      A("science-sleep", "Why we need sleep", 3, """
Scientists once thought that sleep was simply a time when the body switched off. Now we know the brain is very busy at night.

While we sleep, the brain sorts the day's memories. It keeps the important ones and lets the rest fade. That is why students who sleep well after studying often remember more than students who stay up all night. Sleep also helps the body repair muscles and fight illness.

Most adults need seven to nine hours, and children need even more. Bright screens late at night can trick the brain into thinking it is still daytime, so experts suggest putting phones away an hour before bed.
""", ["How many hours do you usually sleep?",
      "Do you use your phone before bed? Could you stop?",
      "Do you remember things better after a good night's sleep?"],
        [("fade", "slowly disappear"), ("repair", "fix"), ("trick", "make someone believe something untrue")])),

    C("business", "📈", "Business", "ব্যবসা",
      ["If you started a small business, what would it sell?",
       "What makes a good boss or manager?",
       "Do you prefer shopping in markets or in big shops? Why?"],
      ["Why customers come back to a shop", "Managing a team that works from home",
       "How small shops use social media", "What makes a product different from the rest",
       "Good communication at work", "Social businesses that help people",
       "Changing direction when a business struggles", "Running a family business"],
      A("business-tea-stall", "The tea stall that grew", 3, """
Rashid opened a tiny tea stall near a bus stop with one kettle and six cups. At first, he sold tea like everyone else. Then he noticed something: office workers were always in a hurry, and they hated waiting.

So he changed his business. He started preparing tea in flasks before the morning rush. He learned his regular customers' names and how they liked their tea. He added ginger tea on cold days and lemon tea in summer.

Within two years, Rashid had three stalls and four workers. When people ask him for advice, he says, "Watch your customers. They will tell you what to do — not with words, but with their feet."
""", ["What did Rashid do differently from other tea sellers?",
      "What do you think he meant by 'with their feet'?",
      "Which small business near your home do you like, and why?"],
        [("rush", "a very busy time"), ("regular", "coming often"), ("advice", "a suggestion about what to do")])),

    C("career", "🧑‍💼", "Career", "ক্যারিয়ার",
      ["What job do you do, or what job would you like to do?",
       "What was your first job or your first day at work like?",
       "Which skills do you think every worker needs today?"],
      ["How to do well in a job interview", "Careers in banking and finance",
       "Learning new skills at any age", "Managing your time at work",
       "Finding a mentor", "Working from home: good and bad sides",
       "Writing a CV that stands out", "Dealing with stress at work"],
      A("career-interview", "The five-minute rule", 3, """
Many people get nervous before a job interview. One recruiter in Dhaka gives her candidates a simple tip: the first five minutes matter most.

Arrive ten minutes early. Smile, greet everyone politely, including the person at the front desk. When the interview starts, give a short, clear answer to "Tell me about yourself": who you are, what you have done and why you want this job. Practise it aloud at home until it sounds natural, not memorised.

At the end, always ask one good question, such as "What does success look like in this role after six months?" It shows you are thinking about the job, not only about getting it.
""", ["How would you answer 'Tell me about yourself'? Try it now.",
      "Why do you think the first five minutes matter so much?",
      "What question would you ask at the end of an interview?"],
        [("nervous", "worried and a little afraid"), ("candidates", "people trying to get a job"), ("memorised", "learned by heart, word for word")])),

    C("nature", "🌳", "Nature", "প্রকৃতি",
      ["Do you prefer forests, rivers or beaches?",
       "What is your favourite season, and why?",
       "What do you do to look after nature?"],
      ["Coral reefs: the gardens of the sea", "Forests and the climate", "Why we need bees",
       "Composting at home", "How tides shape the coast", "Walking in the forest to feel calm",
       "The science of storms", "Plants that eat insects"],
      A("nature-sundarbans", "The forest in the sea", 2, """
The Sundarbans is the largest mangrove forest in the world. It grows where the great rivers of Bangladesh meet the Bay of Bengal. Twice a day, the tide comes in and covers the roots of the trees with salty water.

Mangrove trees have special roots that stick up out of the mud, like fingers, so they can breathe. The forest is home to crocodiles, deer, monkeys, many birds and, of course, the Royal Bengal tiger.

The Sundarbans also protects people. When a cyclone comes from the sea, the trees slow down the wind and the waves. That is why protecting the forest means protecting the villages behind it.
""", ["Have you visited the Sundarbans, or would you like to?",
      "How does the forest protect people from cyclones?",
      "Which animal from the Sundarbans would you most like to see?"],
        [("mangrove", "a tree that grows in salty water"), ("mud", "wet, soft earth"), ("cyclone", "a very strong storm")])),

    C("pets", "🐾", "Pets", "পোষা প্রাণী",
      ["Do you have a pet, or would you like one?",
       "Are you a cat person or a dog person?",
       "What do pets teach children?"],
      ["Training a dog with kindness", "Caring for an old pet", "Talking parrots: how do they learn?",
       "Adopting animals from the street", "Pets and our health", "Making toys for pets at home",
       "Moving house with a pet", "Fish tanks and how they calm us"],
      A("pets-street-cat", "The cat who chose us", 1, """
One rainy evening, a small grey kitten sat outside our door. She was wet and hungry. My little brother gave her some milk and a piece of fish.

The next day she came back. And the next day. Soon she was sleeping on our doormat every night. We called her Megh, which means cloud, because of her soft grey fur.

Now Megh lives with us. She likes sunny windows and hates loud noises. She waits for my father every evening and follows him to the kitchen. My mother says we did not choose Megh — Megh chose us.
""", ["Why is the cat called Megh?",
      "Has an animal ever 'chosen' you or your family?",
      "What does your pet, or a pet you know, like and hate?"],
        [("kitten", "a baby cat"), ("doormat", "a mat in front of a door"), ("fur", "the soft hair of an animal")])),

    C("art", "🎨", "Art and design", "শিল্প ও নকশা",
      ["Do you like drawing or painting?",
       "What is the most beautiful building you have seen?",
       "Is there art on the walls of your home? Describe it."],
      ["Different ways to paint", "Paper cutting as an art", "Art that helps people feel better",
       "Pottery: making beautiful things from clay", "Using empty space in design",
       "Street art and murals", "Photography: telling a story in one picture", "How artists help the environment"],
      A("art-rickshaw", "Moving paintings", 2, """
Dhaka's rickshaws are like small art galleries on wheels. Their backs and hoods are covered with bright pictures: film stars, birds, flowers, buses and sometimes dreamy villages with rivers and boats.

Rickshaw painters work in small workshops. They use bold colours — red, green, pink and yellow — so the pictures can be seen from far away. A rickshaw owner often chooses the pictures, and some say a beautiful rickshaw gets more passengers.

In 2023, rickshaw painting in Dhaka was added to UNESCO's list of cultural heritage. Artists hope this will help young people learn the skill before it disappears.
""", ["What pictures would you paint on your own rickshaw?",
      "Why do you think rickshaw art uses bold colours?",
      "Which local art or craft should children learn about?"],
        [("galleries", "places to show art"), ("bold", "strong and bright"), ("disappears", "goes away and is not seen any more")])),

    C("books", "📚", "Books", "বই",
      ["What is the best book you have ever read?",
       "Do you prefer paper books or reading on a screen?",
       "Which book would you give to a child, and why?"],
      ["Why reading aloud to children matters", "Translating a book into another language",
       "Picture books that teach big ideas", "Old stories retold in new ways",
       "How to build a reading habit", "Libraries: more than books",
       "Writing your own short story", "Book fairs and why people love them"],
      A("books-ekushey", "A month of books", 2, """
Every February, Dhaka hosts the Ekushey Book Fair. It is one of the biggest book fairs in the region, and it lasts the whole month.

Hundreds of stalls sell new books by Bangladeshi writers: novels, poems, science books and stories for children. Writers sit at their publishers' stalls and sign books for readers. Families come after school and work, and the paths are full of people until late at night.

The fair is held in memory of the Language Movement of 1952, when people gave their lives for the right to speak Bangla. So for many visitors, buying a book in February is more than shopping. It is a way to celebrate their language.
""", ["Have you been to a book fair? What did you buy?",
      "Why is the book fair held in February?",
      "Which book would you like a writer to sign for you?"],
        [("region", "a large area of the world"), ("publishers", "companies that make and sell books"), ("celebrate", "do something special for a happy reason")])),

    C("education", "🏫", "Education", "শিক্ষা",
      ["What was your favourite subject at school?",
       "Who was your best teacher, and what made them special?",
       "Should children have homework every day?"],
      ["Learning outside the classroom", "Teaching children about money",
       "Critical thinking: asking good questions", "Parents as teachers at home",
       "School uniforms: for and against", "How teachers keep learning",
       "Classrooms where everyone belongs", "Phones and students: helpful or harmful?"],
      A("education-outdoor", "Lessons under the tree", 2, """
At a small primary school in Sirajganj, the best lesson of the week happens outside. Every Thursday, the teacher takes the children to the school garden.

They measure how much the bean plants have grown and write it in their notebooks. They count the leaves, draw insects and talk about why some plants need more water than others. In the rainy season they measure the rain in a jar.

The teacher says the children remember these lessons much better than lessons from the book. "When they touch the soil and see the plant grow, maths and science become real," she explains. "And they come to school happy."
""", ["Did you have lessons outside when you were at school?",
      "Why do children remember outdoor lessons better?",
      "If you were a teacher, what outdoor lesson would you give?"],
        [("measure", "find the size or amount of something"), ("insects", "small animals with six legs"), ("soil", "the earth that plants grow in")])),

    C("news", "📰", "News and society", "খবর ও সমাজ",
      ["How do you usually get the news?",
       "What good news have you heard recently?",
       "What would make your neighbourhood a better place?"],
      ["Plastic in our rivers and seas", "Working from anywhere", "Festivals that bring people together",
       "Clean energy from the sun and wind", "Keeping small languages alive",
       "Farming in a changing climate", "Volunteers who make a difference", "Cities built for walking"],
      A("news-solar", "Light for the char", 3, """
On the chars — the sandy river islands of northern Bangladesh — the electricity grid never arrived. For years, families used kerosene lamps that were smoky and expensive.

Then small solar panels began to appear on tin roofs. A panel the size of a door can charge a battery during the day. At night, the battery powers a few lights, a fan and a phone charger.

The change has been big. Children can study after dark, and shopkeepers keep their shops open longer. Mothers say the air inside the house is cleaner without kerosene. Bangladesh now has millions of these home solar systems, one of the largest numbers in the world.
""", ["How did solar panels change life on the chars?",
      "What would you do if you had no electricity for a week?",
      "Do you think more homes in cities should use solar power?"],
        [("grid", "the network of wires that carries electricity"), ("expensive", "costing a lot of money"), ("charge", "fill a battery with power")])),

    C("mindfulness", "🧘", "Mindfulness", "মনোযোগী জীবন",
      ["What helps you relax after a long day?",
       "What are three things you are thankful for today?",
       "How do you calm down when you feel stressed?"],
      ["Simple breathing exercises", "Listening fully to another person", "Keeping a gratitude jar",
       "Letting go of small worries", "Being kind to yourself", "Taking a mindful walk",
       "Mindful eating: slowing down", "Helping children name their feelings"],
      A("mind-breathing", "Four, four, four", 2, """
When we feel nervous, our breathing becomes fast and short. A simple exercise can help us calm down in less than a minute. Some teachers call it "box breathing".

Breathe in slowly through your nose while you count to four. Hold your breath and count to four. Breathe out slowly through your mouth and count to four. Then wait and count to four again. Repeat this three or four times.

You can do it anywhere: before an exam, before a speech, or in a traffic jam. Many people find that their shoulders relax and their thoughts become clearer. It is a small habit with a big effect.
""", ["When do you feel nervous?",
      "Let's try box breathing together. How do you feel now?",
      "What small habit makes a big difference in your life?"],
        [("exercise", "an activity to practise something"), ("repeat", "do again"), ("habit", "something you do often, almost without thinking")])),

    C("philosophy", "🤔", "Big questions", "বড় প্রশ্ন",
      ["What does a good life mean to you?",
       "Is it ever OK to tell a small lie?",
       "What makes something beautiful?"],
      ["What is happiness?", "Why do we laugh?", "Can we ever really know something?",
       "What is the purpose of school?", "Fate or choice: who decides our future?",
       "Why forgiving is hard", "Is a friend online a real friend?", "What makes a good leader?"],
      A("big-happiness", "Two kinds of happy", 4, """
Philosophers have argued about happiness for thousands of years. One useful idea is that there are two kinds of happiness.

The first is pleasure: the warm feeling of eating a good meal, winning a game or getting a gift. It is real and important, but it does not last long.

The second is meaning: the deeper feeling that your life matters. People often find it in helping others, learning something difficult or caring for their family. This kind of happiness can live alongside hard work and even sadness. A mother who stays up all night with a sick child is not having fun, but she may feel that this is exactly where she should be.
""", ["Which gives you more happiness: pleasure or meaning?",
      "Describe something hard you did that made you proud.",
      "Can a person be happy and sad at the same time?"],
        [("argued", "discussed with different opinions"), ("pleasure", "a feeling of enjoyment"), ("alongside", "together with")])),
]

BY_KEY = {c["key"]: c for c in CATEGORIES}
INTERESTS = [(c["key"], c["emoji"], c["title"], c["title_bn"]) for c in CATEGORIES]

# Seeds that free families can read (one from each of the first three categories)
FREE_SEEDS = {"travel-sajek", "food-fuchka", "pets-street-cat"}


def seed_articles():
    for c in CATEGORIES:
        yield c, c["seed"]


def seed(slug):
    for c in CATEGORIES:
        if c["seed"]["slug"] == slug:
            return c, c["seed"]
    return None, None


def topic_slug(cat_key, i):
    return f"{cat_key}-t{i + 1}"


def topic(slug):
    """'travel-t3' -> (category, title) for an AI-written article idea, or (None, None)."""
    key, _, n = slug.rpartition("-t")
    c = BY_KEY.get(key)
    if not c or not n.isdigit() or not 1 <= int(n) <= len(c["topics"]):
        return None, None
    return c, c["topics"][int(n) - 1]


# --------------------------------------------------------------------------------------------
# More article ideas, one list per category (our own titles). Topics not suitable for a family app
# - violence, crime, the supernatural, alcohol, politics, romance, religion debates, celebrity
# scandals, addiction and trauma - are left out on purpose. New ideas are appended, so the slugs of
# existing topics (travel-t1 …) never change.
MORE_TOPICS = {
    "books": [
        "Famous characters who live on outside their books", "When the film of a book disappoints",
        "How book prizes change what people read", "Book lovers who share reviews online",
        "Old myths inside today's stories", "Stories about the future: freedom and fear",
        "A touch of magic in everyday stories", "Unforgettable first lines of novels",
        "How novels show families and parents", "How pictures help children enjoy books",
        "Biographies: meeting remarkable people", "A reading challenge: try a new kind of book",
        "Fables and the big ideas they carry", "How to write a good book blurb",
        "Visiting places from famous books", "What if history had been different?",
    ],
    "education": [
        "Learning by doing projects", "Learning by asking questions", "Mixing art with science and maths",
        "Using technology to learn a new language", "Helping children understand other cultures",
        "Talking about feelings at school", "Calm minds in the classroom", "Teaching children to settle arguments kindly",
        "How teachers and students build trust", "How parents' support helps at school",
        "Caring for nature starts at school", "Films and games in the classroom: helpful or not?",
        "Music lessons and the growing brain", "Teachers need care too", "Never too old to learn",
    ],
    "science": [
        "How aeroplanes stay in the air", "Roller coasters: the science of loops and drops", "The science of sport",
        "The human genome: the body's instruction book", "Editing genes: what it can do and what we should ask",
        "How our genes shape who we are", "Why clean air matters for health", "Food and long-term health",
        "How exercise lowers stress", "How the body feels pain", "What motivates us?",
        "What really makes people happy?", "Nanotechnology: very tiny machines", "Plastics made from plants",
        "The science behind natural disasters", "How memories are made",
    ],
    "technology": [
        "Keeping your privacy online", "How machine learning works", "Gadgets we wear", "Computers that can see",
        "Big data and how it changes the world", "Green technology for a cleaner planet", "E-sports and gaming",
        "Quantum computers and secret codes", "Fingerprints and faces as passwords", "Technology in hospitals",
        "Technology and fashion", "Technology and buying a home", "How technology changes friendships",
        "From film to digital cameras", "Virtual and augmented reality", "Neural networks, explained simply",
        "Games that mix the real world and the online world",
    ],
    "career": [
        "Building a network of contacts", "Balancing work and family life", "When you feel you don't belong at work",
        "Understanding feelings at work", "Freelance and gig work", "Careers in healthcare", "Careers in teaching",
        "Careers in clean energy", "Careers in film, TV and music", "Starting your own business",
        "Getting on with everyone at the office", "Different people, stronger teams", "Learning something new every year",
        "Managing your energy, not just your time",
    ],
    "music": [
        "Music therapy: healing with sound", "Concerts you watch online", "K-pop around the world",
        "Album covers that became famous", "How music is recorded today", "Old classical music in new songs",
        "Women who changed music", "Musicians who started on the street", "Music awards and what they mean",
        "When musicians from different worlds work together", "Making music up on the spot",
        "Music that brings neighbours together", "Music at sports matches", "Music in paintings",
        "Bands that changed music history", "How music styles change over time",
    ],
    "news": [
        "New ideas for recycling", "Young people starting businesses", "Documentaries about real problems",
        "Super-fast trains and flying cars", "New ideas in schools", "Art today: what is modern art?",
        "Telling stories with photographs", "Helping athletes stay calm", "What makes a family strong?",
        "Shopping without plastic", "Growing older in good health",
    ],
    "pets": [
        "Can pets understand our feelings?", "Keeping a pet at a healthy weight", "How to tell when a pet is unwell",
        "Animals that comfort people", "Famous animals in history", "Pets that became famous online",
        "Pets and a healthy heart", "Can pets sense things? Fact or fiction", "Making a garden safe for your pet",
        "Cat cafés: tea with a furry friend", "Funny pets and why we love them", "Choosing a pet responsibly",
        "Teaching your pet new tricks",
    ],
    "nature": [
        "Bringing coral reefs back to life", "The Great Barrier Reef", "Heat from inside the Earth",
        "Natural hot springs", "The world's oldest forests", "Nature and the people who live close to it",
        "How the climate changes animal life", "Tides and coastlines", "Traditional farming",
        "Plants people use for health: what science says", "Nature as an artist's teacher",
        "Gardening for beginners", "A quiet walk in the forest",
    ],
    "movies": [
        "Why superhero films are so popular", "Parallel worlds in science fiction", "Old memories in new films",
        "Comedy in different kinds of films", "How social media sells films", "Big film series and why we love them",
        "Myths and folk tales in fantasy films", "Making dragons fly: visual effects", "Documentaries about true stories",
        "Films about traditional communities", "Films inspired by poems and books", "Different styles of animation",
        "Imagined future worlds in films",
    ],
    "philosophy": [
        "What is truth in art and stories?", "Should you trust your gut feeling?", "What is the mind?",
        "What is the meaning of life?", "How science finds answers", "Mind and body: how are they linked?",
        "Should we change human genes?", "What is beauty?", "What do dreams mean?", "Knowledge and reason",
        "What makes a fair society?", "Kindness in families",
    ],
    "mindfulness": [
        "A calm mind for creative ideas", "Listening to your inner voice", "Speaking up kindly",
        "Mindful use of social media", "Beating self-doubt", "Bouncing back from hard times",
        "Finding joy in everyday life", "Letting go of regrets", "Mindfulness and yoga", "Leading with a calm mind",
        "Relaxing from head to toe", "A clear and focused mind", "Mindfulness and memory",
        "Really listening to music", "Calm parents, calm children",
    ],
    "art": [
        "Art and digital technology", "The Bauhaus and modern design", "Sculpting with clay", "Designing packets and labels",
        "Designing with a grid", "Simple, quiet photographs", "Art in clothes and costumes", "Saving old paintings",
        "Street fashion and graphic design", "Making paper by hand", "Portrait photography",
        "Using empty space in a design", "Shape and form in sculpture", "Aboriginal art today", "The colours of pottery glazes",
        "Art that keeps a culture alive",
    ],
    "travel": [
        "The best places to watch the stars", "How social media changes travel", "Storytelling traditions around the world",
        "Local customs: dos and don'ts", "Snorkelling and diving among fish", "Old villages with cobbled streets",
        "Unforgettable road trips", "Crafts and souvenirs from around the world", "Lost cities of long ago",
        "Taking great travel photos", "Hopping from island to island", "Holidays for adventure lovers",
        "Safaris and national parks", "Visiting places from famous films", "Travelling on foot and by bicycle",
        "Travelling without harming nature", "Getting by when you don't speak the language",
    ],
    "cooking": [
        "Rolling sushi at home", "Cooking with seaweed", "Yoghurt from breakfast to dessert", "Cooking without wheat",
        "Bite-size snacks for a party", "New ways with cauliflower", "Taking beautiful food photos", "Mixing Asian flavours at home",
        "Cooking fish and prawns", "A plate of cheese and fruit", "Dumplings around the world", "Fruits you may never have tried",
        "Decorating a cake", "Cooking with tofu", "A brunch with no meat", "Popcorn three ways",
        "Keeping fruit and vegetables for later", "Five-minute breakfasts",
    ],
    "business": [
        "A company's name on social media", "Selling to people around the world", "Happy staff, better work",
        "Leaders who serve their team", "How goods travel from farm to shop", "Adverts made just for you",
        "Businesses that change quickly", "Managing time in a team", "Different people, new ideas",
        "Online adverts and shoppers", "Standing out from the competition", "Finding new customers and keeping them",
        "Why customers stay loyal", "Looking after a company's good name", "Virtual reality at work",
        "How new businesses help a country grow",
    ],
    "food": [
        "When two food cultures meet", "The long history of street food", "Food around the Mediterranean",
        "Eggs from breakfast to dessert", "Bringing back lost family recipes", "Making food look beautiful",
        "The joy of food markets", "A picnic in the park", "Herbs in the kitchen", "The story of sourdough bread",
        "Trying new flavours", "Swapping homemade food with neighbours", "A meal at a top restaurant",
        "Food and feelings", "Food and memories",
    ],
    "sports": [
        "Sport that cares for the planet", "Why companies sponsor sport", "Traditional sports around the world",
        "The skill behind darts", "Rugby around the world", "How fans celebrate", "Sport that helps communities",
        "Sport and a healthy country", "Athletes on social media", "Great teams through history",
        "Team tactics made simple", "Kabaddi and other games of Bangladesh",
    ],
}

for _key, _extra in MORE_TOPICS.items():
    BY_KEY[_key]["topics"].extend(t for t in _extra if t not in BY_KEY[_key]["topics"])
