# Word lists

* `kids3000.tsv` — the 3000 most frequent English words, early-years words first (children, parents, grandparents).
* `core7000.tsv` — the 7000 most frequent English words (school students, IELTS).
* `bn_meanings.txt` — Bangla meanings for the first 1000 children's words, written by FamilyEnglish.

Built by `tools/build_wordlists.py` from open data. These are FamilyEnglish's own lists; no Oxford or
Cambridge list was copied (the Oxford 3000/5000 are copyrighted by Oxford University Press).

Attribution and licences
* Word frequencies: wordfreq by Robyn Speer, data licensed CC BY-SA 4.0 — https://github.com/rspeer/wordfreq.
  The word lists in this folder are shared under CC BY-SA 4.0 too.
* British pronunciations (IPA): Britfone, © 2017 Jose Llarena, MIT licence — https://github.com/JoseLlarena/Britfone
* Lemmas: lemminflect (MIT).
* English definitions and examples (`en_definitions.tsv`, built by `tools/build_definitions.py`): Open English
  WordNet (CC BY 4.0), derived from Princeton WordNet (WordNet 3.0 © 2006 Princeton University). Definitions
  for small grammar words and for children's first words were written by FamilyEnglish.
