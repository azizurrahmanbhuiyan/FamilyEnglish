"""Simple English-to-English definitions for the word lists (run once by the developer).

Source: Open English WordNet (CC BY 4.0, derived from Princeton WordNet), the most common sense of the
word's main part of speech, plus FamilyEnglish's own definitions for small grammar words (the, of, and…)
that a dictionary of meanings does not cover. American spellings in definitions are changed to British.

Usage:  git clone --depth 1 https://github.com/globalwordnet/english-wordnet /tmp/oewn
        python tools/build_definitions.py /tmp/oewn/src/yaml
Output: practice/data/en_definitions.tsv  (word, definition, example)
"""

import csv
import glob
import re
import sys
from pathlib import Path

import yaml

DATA = Path(__file__).resolve().parent.parent / "practice" / "data"
POS_CODE = {"noun": ["n"], "verb": ["v"], "adjective": ["a", "s"], "adverb": ["r"]}

OWN = {
    "the": ("used before a noun when we know which one we mean", "The sun is hot."),
    "a": ("one; used before a singular noun that starts with a consonant sound", "I have a cat."),
    "an": ("one; used before a singular noun that starts with a vowel sound", "She ate an apple."),
    "to": ("towards a place; also used before a verb", "I go to school. I want to play."),
    "and": ("joins two words or ideas together", "bread and butter"),
    "of": ("belonging to or part of something", "a cup of tea"),
    "in": ("inside something, or during a time", "The cat is in the box."),
    "on": ("touching the top of something; on a day", "The book is on the table."),
    "at": ("in a particular place or time", "See you at six."),
    "with": ("together with someone or something", "I walk with my dad."),
    "for": ("given to someone; used to show a purpose or a length of time", "This gift is for you."),
    "from": ("showing where something starts or comes from", "I am from Dhaka."),
    "by": ("near; or showing who did something", "Sit by the window."),
    "about": ("on the subject of; also nearly", "a book about animals"),
    "into": ("moving to the inside of something", "Jump into the water."),
    "over": ("above something; also finished", "The bird flew over the house."),
    "under": ("below something", "The ball is under the bed."),
    "after": ("later than something", "We play after school."),
    "before": ("earlier than something", "Wash your hands before lunch."),
    "between": ("in the space in the middle of two things", "I sit between my brothers."),
    "through": ("from one side to the other side", "We walked through the park."),
    "up": ("towards a higher place", "Look up at the sky."),
    "down": ("towards a lower place", "Sit down, please."),
    "out": ("away from the inside", "Let's go out."),
    "off": ("away from a place; not working", "Turn off the light."),
    "but": ("used before something different or surprising", "I am tired but happy."),
    "or": ("used to show a choice", "Tea or milk?"),
    "so": ("for that reason; also very", "It was raining, so we stayed home."),
    "because": ("for the reason that", "I am happy because it is Friday."),
    "if": ("used to say that one thing depends on another", "If it rains, we will stay in."),
    "when": ("at what time; at the time that", "When is your birthday?"),
    "while": ("during the time that", "Mum cooks while I read."),
    "than": ("used when comparing two things", "My brother is taller than me."),
    "as": ("in the same way; in the role of", "She works as a teacher."),
    "that": ("the one there; also used to join sentences", "That is my bag."),
    "this": ("the one here, near you", "This is my book."),
    "these": ("the ones here, near you", "These are my pens."),
    "those": ("the ones there, not near you", "Those birds are big."),
    "I": ("the person who is speaking", "I like mangoes."),
    "you": ("the person or people you are speaking to", "You are kind."),
    "he": ("a boy or man already talked about", "He is my brother."),
    "she": ("a girl or woman already talked about", "She is my sister."),
    "it": ("a thing or animal already talked about", "It is a red ball."),
    "we": ("the speaker and other people", "We are a family."),
    "they": ("people or things already talked about", "They are my friends."),
    "me": ("the person speaking (after a verb or preposition)", "Give it to me."),
    "him": ("a boy or man (after a verb or preposition)", "I called him."),
    "her": ("a girl or woman; belonging to her", "This is her bag."),
    "us": ("the speaker and others (after a verb or preposition)", "Come with us."),
    "them": ("people or things (after a verb or preposition)", "I like them."),
    "my": ("belonging to me", "my mother"),
    "your": ("belonging to you", "your school"),
    "his": ("belonging to him", "his bike"),
    "its": ("belonging to it", "The dog wags its tail."),
    "our": ("belonging to us", "our house"),
    "their": ("belonging to them", "their garden"),
    "who": ("which person", "Who is that?"),
    "what": ("which thing", "What is your name?"),
    "which": ("used to ask about one of a group", "Which colour do you like?"),
    "where": ("in or to what place", "Where do you live?"),
    "why": ("for what reason", "Why are you sad?"),
    "how": ("in what way", "How do you say this?"),
    "some": ("a number or amount of something", "Some milk, please."),
    "any": ("one, some or all, it does not matter which", "Have you got any pencils?"),
    "all": ("every one; the whole amount", "All the children are here."),
    "every": ("each one of a group", "I read every day."),
    "each": ("every one, thought about separately", "Each child has a book."),
    "both": ("the two together", "Both my sisters sing."),
    "many": ("a large number of", "There are many stars."),
    "much": ("a large amount of", "Not much water is left."),
    "more": ("a larger number or amount", "Can I have more rice?"),
    "most": ("the largest number or amount", "Most children like sweets."),
    "few": ("a small number of", "I have a few friends here."),
    "no": ("not any; also the opposite of yes", "No, thank you."),
    "not": ("used to make a sentence negative", "I am not hungry."),
    "yes": ("used to agree or say something is true", "Yes, please."),
    "please": ("a polite word used when asking for something", "Water, please."),
    "be": ("to exist; used to describe someone or something", "I want to be a doctor."),
    "have": ("to own or hold something", "I have two brothers."),
    "do": ("to perform an action", "Do your homework."),
    "will": ("used to talk about the future", "I will call you tomorrow."),
    "would": ("used to talk about something imagined, or to ask politely", "Would you like some tea?"),
    "can": ("to be able to do something", "I can swim."),
    "could": ("was able to; also used to ask politely", "Could you help me?"),
    "should": ("used to say what is the right thing to do", "You should drink water."),
    "may": ("used to say something is possible, or to ask politely", "May I come in?"),
    "might": ("used to say something is possible", "It might rain."),
    "must": ("used to say something is necessary", "You must wear a seat belt."),
    "shall": ("used to offer or suggest something", "Shall we go?"),
    "very": ("to a great degree", "It is very cold."),
    "too": ("also; or more than is good", "Me too! It is too hot."),
    "also": ("as well", "She also plays cricket."),
    "just": ("exactly; or a very short time ago", "I have just eaten."),
    "only": ("no more than; no one else", "I have only one pen."),
    "here": ("in or to this place", "Come here."),
    "there": ("in or to that place", "Put it there."),
    "now": ("at this time", "Let's go now."),
    "then": ("at that time; next", "First wash, then eat."),
    "today": ("this day", "Today is Monday."),
    "tomorrow": ("the day after today", "See you tomorrow."),
    "yesterday": ("the day before today", "I was ill yesterday."),
    "again": ("one more time", "Say it again."),
    "always": ("every time", "I always brush my teeth."),
    "never": ("not ever", "I never eat in class."),
    "often": ("many times", "We often visit Grandma."),
    "sometimes": ("on some occasions", "Sometimes I walk to school."),
    "still": ("continuing until now", "She is still asleep."),
    "already": ("before now", "I have already finished."),
    "yet": ("until now (in questions and negatives)", "Have you eaten yet?"),
    "hello": ("a word you say when you meet someone", "Hello, Grandpa!"),
    "goodbye": ("a word you say when you leave", "Goodbye, see you soon."),
    "thanks": ("thank you", "Thanks for your help."),
    "sorry": ("a word you say when you have done something wrong", "Sorry I'm late."),
    "okay": ("all right; agreed", "Okay, let's start."),
    "oh": ("a sound showing surprise", "Oh, it's you!"),
    "hi": ("hello (friendly)", "Hi, Mum!"),
    "wow": ("a word showing great surprise", "Wow, what a big cake!"),
    "per": ("for each", "100 taka per kilo"),
    "via": ("travelling through a place", "We flew to London via Dubai."),
    "anymore": ("not now as before", "I don't live there anymore."),
    "however": ("but; despite this", "It was cold. However, we went out."),
    "though": ("although; but", "It was late, though we stayed."),
    "although": ("in spite of the fact that", "Although it rained, we played."),
    "unless": ("except if", "Don't go unless I call you."),
    "until": ("up to a time", "Wait until six."),
    "since": ("from a time in the past until now", "I have lived here since 2020."),
    "whether": ("if (used when there are two choices)", "I don't know whether to go."),
    "either": ("one or the other of two", "You can have either cake."),
    "towards": ("in the direction of", "Walk towards the gate."),
    "upon": ("on (formal)", "Once upon a time…"),
    "within": ("inside a time or place", "Finish within an hour."),
    "without": ("not having or using", "Tea without sugar."),
    "against": ("touching; or opposing", "Lean against the wall."),
    "during": ("all through a period of time", "Don't talk during the lesson."),
    "among": ("in the middle of a group", "a house among the trees"),
    "behind": ("at the back of", "The cat is behind the door."),
    "near": ("not far from", "The shop is near my house."),
    "across": ("from one side to the other", "Walk across the road carefully."),
    "along": ("following the length of", "We walked along the river."),
    "around": ("on every side of; in a circle", "Run around the field."),
    "above": ("higher than", "The lamp is above the table."),
    "below": ("lower than", "Write your name below the line."),
    "inside": ("in the inner part of", "Come inside, it's raining."),
    "outside": ("not inside", "Let's play outside."),
    "myself": ("me (when I do something to me)", "I hurt myself."),
    "yourself": ("you (when you do something to you)", "Help yourself."),
    "himself": ("him (when he does something to him)", "He made it himself."),
    "itself": ("it (when it does something to it)", "The door opened by itself."),
    "themselves": ("them (when they do something to them)", "They enjoyed themselves."),
    "someone": ("a person, but we don't know who", "Someone is at the door."),
    "something": ("a thing, but we don't know what", "I want something to eat."),
    "anything": ("any thing at all", "Do you need anything?"),
    "nothing": ("not anything", "There is nothing in the box."),
    "everything": ("all things", "Everything is ready."),
    "everyone": ("all people", "Everyone is here."),
    "anyone": ("any person", "Is anyone home?"),
    "nobody": ("no person", "Nobody was there."),
    "another": ("one more; a different one", "Can I have another?"),
    "other": ("different; the rest", "the other boys"),
    "such": ("so great; of this kind", "It was such a nice day."),
    "same": ("not different", "We have the same bag."),
    "Monday": ("the day after Sunday", "School starts on Monday."),
    "Friday": ("the day after Thursday", "We pray together on Friday."),
    "English": ("the language of England, spoken all over the world", "We learn English."),
    "British": ("from the United Kingdom", "a British accent"),
    "England": ("a country in the United Kingdom", "London is in England."),
    "London": ("the capital city of England and the UK", "Big Ben is in London."),
    "Britain": ("England, Scotland and Wales together", "It often rains in Britain."),
    "else": ("other; different", "Anything else?"),
    "whose": ("belonging to which person", "Whose bag is this?"),
    "whom": ("which person (formal, after a verb or preposition)", "To whom did you write?"),
    "whoever": ("any person who", "Whoever comes first wins."),
    "whenever": ("every time that", "Call me whenever you like."),
    "everybody": ("every person", "Everybody likes holidays."),
    "anybody": ("any person", "Can anybody help?"),
    "herself": ("her (when she does something to her)", "She dressed herself."),
    "ourselves": ("us (when we do something to us)", "We made it ourselves."),
    "yours": ("belonging to you", "Is this pen yours?"),
    "nor": ("and not (after neither or not)", "Neither he nor I went."),
    "onto": ("moving to a position on something", "The cat jumped onto the table."),
    "ah": ("a sound showing that you understand or are pleased", "Ah, now I see!"),
    "media": ("newspapers, television, radio and the internet", "The news was in the media."),
    "mister": ("Mr; a polite word for a man", "Excuse me, mister."),
}
# Children's first words: our own very simple definitions (the dictionary ones are written for adults).
SIMPLE = {k: (v, "") for k, v in {
    "mother": "your female parent; your mum", "father": "your male parent; your dad", "mum": "mother (British, informal)",
    "dad": "father (informal)", "baby": "a very young child", "brother": "a boy or man who has the same parents as you",
    "sister": "a girl or woman who has the same parents as you", "grandma": "the mother of your mother or father",
    "grandpa": "the father of your mother or father", "family": "a group of people related to each other, like parents and children",
    "friend": "a person you know and like", "boy": "a male child", "girl": "a female child", "man": "an adult male person",
    "woman": "an adult female person", "child": "a young person who is not yet an adult", "teacher": "a person whose job is to teach",
    "school": "a place where children go to learn", "book": "pages with writing or pictures, joined together to read",
    "pen": "a thing you write with in ink", "pencil": "a thing you write or draw with; it has grey lead inside",
    "bag": "a container you carry things in", "desk": "a table you write or study at", "chair": "a seat for one person, with a back",
    "table": "furniture with a flat top on legs", "door": "you open it to go into or out of a room",
    "window": "an opening in a wall, with glass, to let light in", "house": "a building where people live",
    "home": "the place where you live", "room": "a part of a building with walls, like a bedroom",
    "bed": "furniture you sleep on", "kitchen": "the room where food is cooked", "bathroom": "the room where you wash",
    "garden": "land near a house where flowers or vegetables grow", "tree": "a tall plant with a trunk, branches and leaves",
    "flower": "the coloured part of a plant", "sun": "the bright star that gives us light and heat in the day",
    "moon": "the round thing that shines in the sky at night", "star": "a small bright light in the sky at night",
    "sky": "the space above the earth where you see clouds and the sun", "rain": "water that falls from clouds",
    "water": "the clear liquid in rivers and rain that we drink", "fire": "the heat, flames and light when something burns",
    "cloud": "a white or grey shape in the sky, made of water", "wind": "air that moves", "sea": "the large area of salt water",
    "river": "a long line of water that flows to the sea", "beach": "the sand or stones next to the sea",
    "cat": "a small animal with soft fur that people keep as a pet", "dog": "an animal that barks, often kept as a pet",
    "cow": "a large farm animal that gives milk", "goat": "a farm animal with horns that gives milk",
    "hen": "a female chicken; it lays eggs", "duck": "a water bird with a flat beak", "fish": "an animal that lives and swims in water",
    "bird": "an animal with feathers and wings; most birds can fly", "horse": "a large animal people ride",
    "elephant": "a very big grey animal with a long nose called a trunk", "tiger": "a big wild cat with orange fur and black stripes",
    "lion": "a big wild cat; the male has long hair round its head", "monkey": "a clever animal that climbs trees",
    "snake": "a long animal with no legs", "frog": "a small green animal that jumps and lives near water",
    "rabbit": "a small animal with long ears", "bee": "an insect that makes honey", "ant": "a very small insect that lives in big groups",
    "red": "the colour of blood", "blue": "the colour of the sky on a sunny day", "green": "the colour of grass and leaves",
    "yellow": "the colour of a banana", "orange": "the colour between red and yellow; also a round fruit",
    "pink": "a light red colour", "purple": "the colour you get when you mix red and blue", "black": "the darkest colour",
    "white": "the colour of milk or snow", "brown": "the colour of chocolate or soil", "colour": "red, blue, green and so on",
    "number": "a word or sign like one, two, 3 or 4", "head": "the top part of your body, with your eyes and mouth",
    "hair": "what grows on your head", "eye": "the part of your body you see with", "ear": "the part of your body you hear with",
    "nose": "the part of your face you smell and breathe with", "mouth": "the part of your face you eat and speak with",
    "tooth": "one of the hard white things in your mouth", "face": "the front of your head",
    "hand": "the part at the end of your arm, with fingers", "arm": "the part of your body between your shoulder and hand",
    "leg": "the part of your body you walk on", "foot": "the part at the end of your leg that you stand on",
    "finger": "one of the five long parts of your hand", "apple": "a round fruit with red or green skin",
    "banana": "a long yellow fruit", "rice": "small white grains we cook and eat", "bread": "food made from flour and baked",
    "egg": "an oval thing laid by a hen; we eat it", "milk": "the white drink that comes from cows",
    "tea": "a hot drink made with leaves", "juice": "the drink you get from fruit", "cake": "a sweet food baked for parties",
    "sweet": "tasting of sugar; also a small sugary food", "fruit": "the sweet part of a plant we eat, like a mango",
    "vegetable": "a plant we cook or eat, like a potato", "food": "what people and animals eat",
    "lunch": "the meal in the middle of the day", "dinner": "the main meal in the evening",
    "breakfast": "the first meal of the day", "ball": "a round thing you throw, kick or hit in games",
    "toy": "a thing children play with", "car": "a road vehicle for a few people", "bus": "a big road vehicle for many people",
    "train": "a long vehicle that runs on a railway", "boat": "a small vehicle that travels on water",
    "plane": "a vehicle with wings that flies", "bike": "a bicycle: two wheels you ride by pedalling",
    "kite": "a light toy that flies in the wind on a string", "game": "something you play, with rules",
    "big": "large", "small": "not large; little", "hot": "very warm", "cold": "not warm", "happy": "feeling good",
    "sad": "feeling unhappy", "good": "nice, right or well done", "bad": "not good", "new": "just made or just bought",
    "old": "having lived or been used for a long time", "long": "measuring a lot from one end to the other",
    "short": "not long or not tall", "tall": "higher than most people or things", "fast": "moving quickly",
    "slow": "not fast", "clean": "not dirty", "dirty": "not clean", "hungry": "wanting food", "thirsty": "wanting a drink",
    "tired": "needing rest or sleep", "go": "to move to another place", "come": "to move towards here",
    "eat": "to put food in your mouth and swallow it", "drink": "to take water, milk or juice into your mouth and swallow it",
    "sleep": "to rest with your eyes closed, at night", "play": "to have fun with games or toys",
    "run": "to move very fast on your feet", "walk": "to move on your feet, not fast", "jump": "to push yourself up into the air",
    "sit": "to rest on a chair or the floor", "stand": "to be on your feet", "look": "to turn your eyes to see something",
    "see": "to notice with your eyes", "hear": "to notice sounds with your ears", "say": "to speak words",
    "read": "to look at words and understand them", "write": "to put letters and words on paper",
    "draw": "to make a picture with a pen or pencil", "sing": "to make music with your voice",
    "dance": "to move your body to music", "wash": "to clean with water", "open": "to make something not closed",
    "close": "to shut", "give": "to let someone have something", "take": "to get and hold something",
    "like": "to enjoy or think something is nice", "love": "to like someone or something very much",
    "want": "to wish to have or do something", "help": "to make something easier for someone",
    "know": "to have something in your mind", "make": "to build or produce something", "put": "to place something somewhere",
    "stop": "to not move or not continue", "wait": "to stay until something happens", "thank": "to say you are pleased someone helped",
    "morning": "the early part of the day", "night": "the dark time when people sleep", "day": "the time when it is light; 24 hours",
    "week": "seven days", "time": "what a clock measures, in minutes and hours", "people": "men, women and children",
    "work": "a job; to do a job", "year": "twelve months", "friend": "a person you know and like",
}.items()}

BRIT = {"color": "colour", "colors": "colours", "colored": "coloured", "center": "centre", "centers": "centres",
        "liter": "litre", "liters": "litres", "meter": "metre", "meters": "metres", "theater": "theatre",
        "favorite": "favourite", "behavior": "behaviour", "neighbor": "neighbour", "honor": "honour",
        "labor": "labour", "humor": "humour", "flavor": "flavour", "gray": "grey", "organize": "organise",
        "organized": "organised", "realize": "realise", "recognize": "recognise", "defense": "defence",
        "license": "licence", "program": "programme", "traveling": "travelling", "traveled": "travelled",
        "fiber": "fibre", "jewelry": "jewellery", "mom": "mum", "airplane": "aeroplane", "apartment": "flat",
        "candy": "sweets", "cookie": "biscuit", "gasoline": "petrol", "vacation": "holiday", "truck": "lorry"}


def british(text):
    return re.sub(r"\b(" + "|".join(BRIT) + r")\b", lambda m: BRIT[m.group(1)], text)


def main(src):
    entries, synsets = {}, {}
    for f in glob.glob(f"{src}/entries-*.yaml"):
        entries.update(yaml.load(open(f, encoding="utf-8"), Loader=yaml.CLoader))
    for f in glob.glob(f"{src}/[nvar]*.yaml"):
        if "entries" in f or "frames" in f:
            continue
        synsets.update(yaml.load(open(f, encoding="utf-8"), Loader=yaml.CLoader))
    words, rows = [], {}
    for name in ("kids3000", "core7000"):
        with open(DATA / f"{name}.tsv", encoding="utf-8") as fh:
            words += [(r["word"], r["pos"]) for r in csv.DictReader(fh, delimiter="\t")]
    missing = 0
    for word, pos in words:
        if word in rows:
            continue
        if word in OWN or word.lower() in OWN:
            d, ex = OWN.get(word) or OWN[word.lower()]
            rows[word] = (d, ex)
            continue
        entry = entries.get(word) or entries.get(word.lower()) or {}
        if word.lower() in SIMPLE:
            rows[word] = SIMPLE[word.lower()]
            continue
        # choose the part of speech with the most senses (the word's main use), then its first sense
        ours = [c for p in pos.split(", ") for c in POS_CODE.get(p, [])]
        counts = {c: len(entry.get(c, {}).get("sense", [])) for c in ("n", "v", "a", "s", "r")}
        order = sorted(counts, key=lambda c: (-counts[c], ours.index(c) if c in ours else 9))
        found = None
        for code in order:
            for sense in entry.get(code, {}).get("sense", [])[:1]:
                syn = synsets.get(sense["synset"])
                if syn and syn.get("definition"):
                    found = syn
                    break
            if found:
                break
        if not found:
            missing += 1
            continue
        d = british(found["definition"][0]).strip()
        d = re.sub(r"\s*\([^)]*\)\s*", " ", d).strip(" ;,") or d     # drop notes in brackets
        ex = ""
        for e in found.get("example", []):
            text = e["text"] if isinstance(e, dict) else e
            if word.lower() in text.lower() and len(text) < 90:
                ex = british(text.strip().strip('"'))
                break
        rows[word] = (d[:200], ex[:200])
    with open(DATA / "en_definitions.tsv", "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, delimiter="\t")
        w.writerow(["word", "definition", "example"])
        for word, (d, ex) in rows.items():
            w.writerow([word, d, ex])
    print(f"{len(rows)} definitions, {missing} words without one")


if __name__ == "__main__":
    main(sys.argv[1])
