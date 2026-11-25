"""Question types: used for weak spots and 'practice by question type'."""

QTYPES = {
    # listening
    "lis_detail": ("listening", "Specific details", "নির্দিষ্ট তথ্য শোনা"),
    "lis_number": ("listening", "Numbers, times and prices", "সংখ্যা, সময় ও দাম"),
    "lis_gist": ("listening", "Main idea", "মূল বক্তব্য"),
    "lis_dictation": ("listening", "Hear and write", "শুনে লেখা"),
    "lis_attitude": ("listening", "Opinions and feelings", "মতামত ও অনুভূতি"),
    # speaking
    "spk_sentence": ("speaking", "Full sentences", "পূর্ণ বাক্যে বলা"),
    "spk_sounds": ("speaking", "Sounds and pronunciation", "ধ্বনি ও উচ্চারণ"),
    "spk_polite": ("speaking", "Polite phrases", "ভদ্র বাক্যাংশ"),
    "spk_stress": ("speaking", "Stress and intonation", "জোর ও সুর"),
    "spk_fluency": ("speaking", "Speaking at length", "সাবলীলভাবে বলা"),
    # reading
    "rd_detail": ("reading", "Finding details", "তথ্য খুঁজে বের করা"),
    "rd_gist": ("reading", "Main idea", "মূল ভাবনা"),
    "rd_infer": ("reading", "Inference", "ইঙ্গিত বোঝা"),
    "rd_vocab": ("reading", "Word meaning", "শব্দের অর্থ"),
    # writing
    "wr_mechanics": ("writing", "Capitals and punctuation", "বড় হাতের অক্ষর ও যতিচিহ্ন"),
    "wr_spelling": ("writing", "Spelling", "বানান"),
    "wr_linking": ("writing", "Linking and paragraphs", "যোগশব্দ ও অনুচ্ছেদ"),
    "wr_order": ("writing", "Word order", "শব্দের ক্রম"),
    "wr_style": ("writing", "Formal and polite style", "আনুষ্ঠানিক ও ভদ্র লেখা"),
    "wr_free": ("writing", "Free writing", "নিজে লেখা"),
    # grammar
    "gr_articles": ("grammar", "a, an, the", "a, an, the"),
    "gr_be": ("grammar", "am, is, are", "am, is, are"),
    "gr_plural": ("grammar", "Plurals", "বহুবচন"),
    "gr_demonstr": ("grammar", "this, that, these, those", "this, that, these, those"),
    "gr_tense": ("grammar", "Verb tenses", "ক্রিয়ার কাল"),
    "gr_prep": ("grammar", "Prepositions", "preposition"),
    "gr_compare": ("grammar", "Comparing", "তুলনা"),
    "gr_quantity": ("grammar", "Quantities", "পরিমাণ (much/many)"),
    "gr_condition": ("grammar", "If sentences", "শর্তবাচক বাক্য"),
    "gr_passive": ("grammar", "Passive voice", "কর্মবাচ্য"),
    "gr_clause": ("grammar", "who / which / that", "relative clause"),
    "gr_reported": ("grammar", "Reported speech", "পরোক্ষ উক্তি"),
}


def label(code, lang="en"):
    skill, en, bn = QTYPES.get(code, ("", code.replace("_", " ").title(), code))
    return bn if lang == "bn" else en


def skill_of(code):
    return QTYPES.get(code, ("",))[0]
