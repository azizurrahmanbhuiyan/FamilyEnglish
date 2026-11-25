"""Build the FamilyEnglish word lists (run once by the developer; the site only reads the TSV files).

Open sources (no Oxford or Cambridge material is copied):
  * word frequency: the `wordfreq` package (data CC BY-SA 4.0, Robyn Speer) — how often each word
    appears in English subtitles, books, news, web text;
  * British pronunciation: Britfone (MIT licence, Jose Llarena) — modern British IPA, no final r;
  * lemmas: the `lemminflect` package (MIT) — so 'went' counts as 'go' and 'children' as 'child'.

Output: practice/data/kids3000.tsv and practice/data/core7000.tsv with rank, word, part of speech, IPA.
Usage:  pip install wordfreq lemminflect;  git clone https://github.com/JoseLlarena/Britfone /tmp/britfone
        python tools/build_wordlists.py /tmp/britfone/britfone.main.3.0.1.csv
"""

import csv
import re
import sys
from pathlib import Path

from lemminflect import getAllLemmas
from wordfreq import top_n_list

OUT = Path(__file__).resolve().parent.parent / "practice" / "data"

# Function words and must-know names that the lemmatiser does not tag.
CLOSED = {
    "pron": "i me my mine myself you your yours yourself he him his himself she her hers herself it its itself we us our "
            "ours ourselves they them their theirs themselves this that these those who whom whose which what "
            "someone somebody something anyone anybody anything everyone everybody everything nobody nothing none "
            "each other another one",
    "det": "the a an some any no every all both either neither such much many more most few little less least several",
    "prep": "of in on at to for with from by about into over under after before between through during without "
            "against among around behind below above across along near off up down out since until till towards "
            "upon inside outside beside beyond within per via onto",
    "conj": "and but or so because if when while although though unless than as whether yet nor once",
    "aux": "be have do will would shall should can could may might must ought",
    "adv": "not very too also just only even still already yet again ever never always often sometimes usually here "
           "there now then today tomorrow yesterday tonight soon later ago away back please yes no okay perhaps maybe "
           "however therefore instead quite rather almost enough",
    "num": "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen "
           "seventeen eighteen nineteen twenty thirty forty fifty sixty seventy eighty ninety hundred thousand "
           "million billion first second third half twice",
    "noun": "monday tuesday wednesday thursday friday saturday sunday january february march april may june july "
            "august september october november december english britain british england london mr mrs ms dr",
    "excl": "hello hi bye goodbye thanks sorry oh wow",
}
CLOSED_POS = {w: pos for pos, words in CLOSED.items() for w in words.split()}
CAPITALS = {"i", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday", "january", "february",
            "march", "april", "june", "july", "august", "september", "october", "november", "december",
            "english", "britain", "british", "england", "london", "mr", "mrs", "ms", "dr"}
POS_NAME = {"NOUN": "noun", "VERB": "verb", "ADJ": "adjective", "ADV": "adverb", "AUX": "verb", "PROPN": "noun",
            "pron": "pronoun", "det": "determiner", "prep": "preposition", "conj": "conjunction",
            "aux": "verb", "adv": "adverb", "num": "number", "noun": "noun", "excl": "exclamation"}

# American → British spelling, kept only when the British form is in the pronunciation dictionary.
def british(word, ipa):
    for us, gb in (("or", "our"), ("er", "re"), ("ize", "ise"), ("izing", "ising"), ("ization", "isation"),
                   ("yze", "yse"), ("og", "ogue"), ("ense", "ence"), ("eled", "elled"), ("eling", "elling"),
                   ("eler", "eller"), ("am", "amme")):
        if word.endswith(us):
            cand = word[: -len(us)] + gb
            if cand in ipa:
                return cand
    for us, gb in (("ization", "isation"), ("ize", "ise"), ("or", "our")):
        if us in word and word.replace(us, gb) in ipa and len(word) > 5:
            return word.replace(us, gb)
    return word

PROFANE = set("fuck fucking shit bitch bastard damn dick cock pussy whore slut porn nigger nigga cunt crap piss arse "
              "asshole wanker bollocks fag faggot retard twat dyke tranny homo spastic paki slag tit tits boob boobs "
              "horny dildo ass".split())
NOT_FOR_KIDS = set("sex sexy sexual naked nude kill killer murder rape drug drugs cocaine heroin alcohol beer wine vodka "
                   "whisky drunk cigarette smoke gun guns weapon bomb terrorist terrorism suicide abuse prostitute "
                   "prison crime criminal violence violent blood dead death die dying war gambling bet casino "
                   "kiss lover affair divorce pregnant pregnancy hell devil bloody stupid".split())

# Early words for young children, taught first in the kids' list (and the talk-topic words).
EARLY = """mother father mum dad baby brother sister grandma grandpa family friend boy girl man woman child
teacher school book pen pencil bag desk chair table door window house home room bed kitchen bathroom garden
tree flower sun moon star sky rain water fire cloud wind sea river beach
cat dog cow goat hen duck fish bird horse elephant tiger lion monkey snake frog rabbit bee ant
red blue green yellow orange pink purple black white brown colour
one two three four five six seven eight nine ten number
head hair eye ear nose mouth tooth teeth face hand arm leg foot finger
apple banana mango rice bread egg milk tea juice cake sweet fruit vegetable food lunch dinner breakfast
ball toy car bus train boat plane bike kite game
big small hot cold happy sad good bad new old long short tall fast slow clean dirty hungry thirsty tired
go come eat drink sleep play run walk jump sit stand look see hear say read write draw sing dance wash
open close give take like love want help know make put stop wait
yes no please thank sorry hello goodbye morning night day today tomorrow week""".split()


def britfone(path):
    ipa = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            if "," not in line:
                continue
            word, pron = line.rstrip("\n").split(",", 1)
            word = re.sub(r"\(\d+\)$", "", word).lower()
            if word not in ipa and re.fullmatch(r"[a-z]+", word):
                ipa[word] = pretty(pron.strip())
    return ipa


ONSETS = {"pl", "pr", "bl", "br", "tr", "dr", "kl", "kr", "ɡl", "ɡr", "gl", "gr", "fl", "fr", "θr", "ʃr", "sp", "st",
          "sk", "sm", "sn", "sl", "sw", "tw", "kw", "dw", "spl", "spr", "str", "skr", "skw", "pj", "bj", "tj", "dj",
          "kj", "ɡj", "fj", "vj", "mj", "nj", "hj", "lj", "sj"}
VOWEL_START = set("ɪiɛeæaɑɒɔʊuʌɐəɜ")


def pretty(pron):
    """Britfone 'w ˈɔː t ə' → dictionary-style /ˈwɔːtə/ with the stress mark before the syllable."""
    sym = pron.replace("ɹ", "r").replace("ɐ", "ʌ").replace("ɛ", "e").replace("g", "ɡ").split()
    out = []
    for s in sym:
        stress = ""
        if s[0] in "ˈˌ":
            stress, s = s[0], s[1:]
        if stress:
            # move the stress mark back over the consonants that can start this syllable
            cons = []
            while out and out[-1][0] not in VOWEL_START and out[-1][0] not in "ˈˌ":
                cons.insert(0, out.pop())
            keep = cons
            for k in range(len(cons) + 1):
                tail = "".join(cons[k:]).replace("ɡ", "g")
                if k == len(cons) or tail in ONSETS or len(cons[k:]) == 1:
                    keep = cons[:k]
                    move = cons[k:]
                    break
            out.extend(keep)
            out.append(stress)
            out.extend(move)
        out.append(s)
    text = "".join(out)
    if sum(1 for s in sym if s.lstrip("ˈˌ")[:1] in VOWEL_START) <= 1:
        text = text.replace("ˈ", "")       # one-syllable words: no stress mark
    return "/" + text + "/"


def pos_label(lemma):
    """'noun, verb' — the parts of speech the word is used as (closed-class words first)."""
    if lemma in CLOSED_POS:
        return POS_NAME[CLOSED_POS[lemma]]
    lem = getAllLemmas(lemma)
    names = []
    for p in ("NOUN", "VERB", "ADJ", "ADV"):
        if p in lem and lemma in lem[p] and POS_NAME[p] not in names:
            names.append(POS_NAME[p])
    return ", ".join(names[:2]) or "noun"


ADJ_KEEP = set("""tired interested interesting bored boring excited exciting surprised surprising worried
amazing amazed married used annoyed annoying frightened frightening confused confusing pleased tiring relaxed
relaxing embarrassed embarrassing disappointed disappointing satisfied shocked shocking crowded wounded
united limited advanced experienced skilled detailed qualified complicated sophisticated dedicated talented
existing leading missing following living outstanding willing increasing""".split())
EXCLUDE = set("peter morgan medicare medicaid mickey marxist".split())

FORMS = {"am": "be", "is": "be", "are": "be", "was": "be", "were": "be", "been": "be", "being": "be",
         "has": "have", "had": "have", "having": "have", "does": "do", "did": "do", "doing": "do",
         "comes": "come", "means": "mean", "mom": "mum", "moms": "mum", "gonna": "go"}


def lemma_of(word):
    word = FORMS.get(word, word)
    if word in CLOSED_POS:
        return word, pos_label(word)
    lem = getAllLemmas(word)
    if not lem:
        return None, None
    if word in ADJ_KEEP:
        return word, pos_label(word)          # tired, interested, boring stay as they are
    if word.endswith(("ing", "ed")) and "VERB" in lem and lem["VERB"][0] != word:
        return lem["VERB"][0], pos_label(lem["VERB"][0])
    if word.endswith("s") and "NOUN" in lem and lem["NOUN"][0] != word:
        return lem["NOUN"][0], pos_label(lem["NOUN"][0])
    for p in ("NOUN", "VERB", "ADJ", "ADV", "AUX"):
        if p in lem and word in lem[p]:
            return word, pos_label(word)
    p = next(p for p in ("VERB", "NOUN", "ADJ", "ADV", "AUX") if p in lem) if any(
        p in lem for p in ("VERB", "NOUN", "ADJ", "ADV", "AUX")) else next(iter(lem))
    return lem[p][0], pos_label(lem[p][0])


def build(ipa, size, kids=False):
    seen, rows = set(), []

    def add(word, pos):
        word = british(word, ipa)
        if word in seen or word not in ipa or word in PROFANE or word in EXCLUDE or (kids and word in NOT_FOR_KIDS):
            return
        seen.add(word)
        rows.append([word.capitalize() if word in CAPITALS else word, pos, ipa[word]])

    if kids:
        for w in EARLY:
            lem, pos = lemma_of(w)
            add(lem or w, pos or "noun")
    for w in top_n_list("en", 60000):
        if len(rows) >= size:
            break
        if not re.fullmatch(r"[a-z]+", w) or (len(w) == 1 and w not in ("a", "i")):
            continue
        lem, pos = lemma_of(w)
        if lem:
            add(lem, pos)
    return rows


def main(path):
    ipa = britfone(path)
    OUT.mkdir(parents=True, exist_ok=True)
    for name, size, kids in (("kids3000", 3000, True), ("core7000", 7000, False)):
        rows = build(ipa, size, kids)
        with open(OUT / f"{name}.tsv", "w", encoding="utf-8", newline="") as f:
            w = csv.writer(f, delimiter="\t")
            w.writerow(["rank", "word", "pos", "ipa_gb"])
            for i, r in enumerate(rows, 1):
                w.writerow([i, *r])
        print(name, len(rows))


if __name__ == "__main__":
    main(sys.argv[1])
