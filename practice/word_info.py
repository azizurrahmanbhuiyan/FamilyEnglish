"""Part of speech and a simple English definition for every flashcard word."""

N, V, A, ADV, NUM, PH, C = "noun", "verb", "adjective", "adverb", "number", "phrase", "linking word"

WORD_INFO = {
    # numbers
    "one": (NUM, "the number 1"), "two": (NUM, "the number 2"), "three": (NUM, "the number 3"),
    "four": (NUM, "the number 4"), "five": (NUM, "the number 5"), "six": (NUM, "the number 6"),
    "seven": (NUM, "the number 7"), "eight": (NUM, "the number 8"), "nine": (NUM, "the number 9"),
    "ten": (NUM, "the number 10"),
    # animals
    "cat": (N, "a small furry pet that says 'meow'"), "dog": (N, "a pet animal that barks"),
    "cow": (N, "a big farm animal that gives milk"), "goat": (N, "a farm animal with horns that eats grass"),
    "hen": (N, "a female chicken that lays eggs"), "duck": (N, "a bird that swims and says 'quack'"),
    "fish": (N, "an animal that lives and swims in water"), "bird": (N, "an animal with wings and feathers"),
    "tiger": (N, "a big wild cat with orange and black stripes"),
    "elephant": (N, "a very large grey animal with a long trunk"),
    # colours
    "red": (A, "the colour of blood"), "blue": (A, "the colour of a clear sky"),
    "green": (A, "the colour of grass and leaves"), "yellow": (A, "the colour of a ripe banana"),
    "black": (A, "the darkest colour, like the night"), "white": (A, "the colour of milk"),
    "orange": (A, "a colour between red and yellow"), "pink": (A, "a light red colour"),
    "brown": (A, "the colour of soil or wood"), "purple": (A, "a colour made of red and blue"),
    # body
    "head": (N, "the top part of your body, with your face and brain"), "eye": (N, "the part you see with"),
    "ear": (N, "the part you hear with"), "nose": (N, "the part you smell with"),
    "mouth": (N, "the part you eat and speak with"), "hand": (N, "the part at the end of your arm"),
    "foot": (N, "the part at the end of your leg that you stand on"), "tooth": (N, "one of the hard white parts in your mouth"),
    "hair": (N, "what grows on your head"), "leg": (N, "the part of your body you walk with"),
    # family
    "mother": (N, "your female parent"), "father": (N, "your male parent"),
    "brother": (N, "a boy or man with the same parents as you"), "sister": (N, "a girl or woman with the same parents as you"),
    "grandmother": (N, "the mother of your mother or father"), "grandfather": (N, "the father of your mother or father"),
    "uncle": (N, "the brother of your mother or father"), "aunt": (N, "the sister of your mother or father"),
    "cousin": (N, "the child of your uncle or aunt"), "baby": (N, "a very young child"),
    # home
    "door": (N, "what you open to go into a room"), "window": (N, "glass in a wall that lets in light"),
    "bed": (N, "what you sleep on"), "chair": (N, "a seat for one person"),
    "table": (N, "furniture with a flat top where you eat or work"), "fan": (N, "a machine that moves air to keep you cool"),
    "kitchen": (N, "the room where food is cooked"), "bathroom": (N, "the room where you wash"),
    "roof": (N, "the top cover of a building"), "light": (N, "what helps you see; a lamp"),
    # food
    "rice": (N, "small white grains we cook and eat"), "egg": (N, "the round thing a hen lays"),
    "milk": (N, "the white drink from cows"), "bread": (N, "food made from flour and baked"),
    "banana": (N, "a long yellow fruit"), "mango": (N, "a sweet yellow-orange summer fruit"),
    "water": (N, "the clear liquid we drink"), "tea": (N, "a hot drink made from leaves"),
    "lentils": (N, "small seeds cooked to make dal"),
    # school
    "book": (N, "pages with words that you read"), "pen": (N, "a tool for writing with ink"),
    "pencil": (N, "a tool for writing or drawing that you can rub out"), "bag": (N, "something you carry things in"),
    "teacher": (N, "a person who helps you learn"), "classroom": (N, "a room where students learn"),
    "friend": (N, "a person you like and trust"), "homework": (N, "school work you do at home"),
    "exam": (N, "an important test"), "ruler": (N, "a straight tool for drawing lines and measuring"),
    # routine
    "wake up": (V, "to stop sleeping"), "brush": (V, "to clean with a brush, e.g. your teeth"),
    "eat": (V, "to put food in your mouth and swallow it"), "go": (V, "to move from one place to another"),
    "study": (V, "to spend time learning"), "play": (V, "to have fun with a game or toy"),
    "pray": (V, "to speak to God"), "help": (V, "to make something easier for someone"),
    "watch": (V, "to look at something for some time"), "sleep": (V, "to rest with your eyes closed"),
    # places
    "market": (N, "a place where people buy and sell food and things"), "hospital": (N, "a place where sick people get care"),
    "mosque": (N, "a building where Muslims pray"), "bank": (N, "a place that keeps and lends money"),
    "park": (N, "a green public place to walk and play"), "shop": (N, "a place where you buy things"),
    "bus stop": (N, "a place where buses stop for people"), "post office": (N, "a place where you send letters"),
    "river": (N, "a long natural flow of water"), "bridge": (N, "something built over a river or road to cross it"),
    # weather
    "sunny": (A, "bright with sunshine"), "rainy": (A, "with a lot of rain"), "cloudy": (A, "with many clouds"),
    "windy": (A, "with a lot of wind"), "hot": (A, "very warm"), "cold": (A, "not warm; low temperature"),
    "summer": (N, "the hottest season of the year"), "winter": (N, "the coldest season of the year"),
    "monsoon": (N, "the rainy season"), "storm": (N, "very bad weather with strong wind and rain"),
    # feelings
    "happy": (A, "feeling good and pleased"), "sad": (A, "feeling unhappy"), "angry": (A, "feeling very annoyed"),
    "tired": (A, "needing rest or sleep"), "scared": (A, "afraid"), "excited": (A, "very happy about something coming"),
    "proud": (A, "pleased about something you or others did"), "bored": (A, "not interested; nothing to do"),
    "worried": (A, "thinking about problems that might happen"), "calm": (A, "quiet and not worried"),
    # jobs
    "doctor": (N, "a person who treats sick people"), "farmer": (N, "a person who grows crops or keeps animals"),
    "driver": (N, "a person who drives a car, bus or truck"), "banker": (N, "a person who works in a bank"),
    "engineer": (N, "a person who designs and builds machines, roads or buildings"),
    "cook": (N, "a person who makes food"), "police officer": (N, "a person who keeps people safe and the law"),
    "nurse": (N, "a person who cares for sick people"), "shopkeeper": (N, "a person who owns or runs a shop"),
    # linking
    "however": (C, "but; used to add a different idea"), "because": (C, "for the reason that"),
    "although": (C, "even though"), "therefore": (C, "so; for this reason"),
    "in my opinion": (PH, "what I think is"), "for example": (PH, "used to give an example"),
    "moreover": (C, "also; in addition"), "instead": (ADV, "in the place of something else"),
    "unless": (C, "except if"), "on the other hand": (PH, "used to give the opposite view"),
    # society
    "environment": (N, "the air, water and land around us"), "pollution": (N, "dirt or harmful things in air, water or land"),
    "traffic jam": (N, "a line of vehicles that cannot move"), "government": (N, "the group of people who run a country"),
    "economy": (N, "the money, jobs and trade of a country"), "flood": (N, "a lot of water covering land that is usually dry"),
    "education": (N, "teaching and learning, e.g. at school"), "technology": (N, "machines and science used in daily life"),
    "volunteer": (N, "a person who works for free to help others"), "community": (N, "the people living in one area"),
    # academic
    "significant": (A, "important or large enough to notice"), "consequence": (N, "a result of an action"),
    "evidence": (N, "facts that show something is true"), "approach": (N, "a way of doing something"),
    "benefit": (N, "a good effect; an advantage"), "challenge": (N, "something difficult to do"),
    "essential": (A, "very important; necessary"), "furthermore": (C, "also; in addition"),
    "contribute": (V, "to give or add to something"), "analyse": (V, "to study something closely"),
}
