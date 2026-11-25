"""Coach: role-play partners for real situations, written by FamilyEnglish.

Every scenario works without AI as a scripted conversation (the coach says a line, the learner says
the model reply or their own answer). When AI is switched on, "Free talk" lets the coach answer
anything the learner says, staying in the role.

Tool coaches (pronunciation, grammar, vocabulary, speech analyzer, presentation) open their own pages.
"""

CATEGORIES = [("all", "All", "সব"), ("language", "Language", "ভাষা"), ("everyday", "Everyday", "দৈনন্দিন"),
              ("professional", "Professional", "পেশাগত"), ("kids", "Kids", "শিশু")]


def S(slug, title, title_bn, setting, persona, lines):
    return {"slug": slug, "title": title, "title_bn": title_bn, "setting": setting, "persona": persona, "lines": lines}


def C(slug, icon, category, title, title_bn, desc, desc_bn, tool=None, scenarios=(), tag=""):
    return {"slug": slug, "icon": icon, "category": category, "title": title, "title_bn": title_bn,
            "desc": desc, "desc_bn": desc_bn, "tool": tool, "scenarios": list(scenarios), "tag": tag}


COACHES = [
    C("pronunciation", "🗣️", "language", "Pronunciation coach", "উচ্চারণ কোচ",
      "Clear British pronunciation step by step: 22 lessons, sound drills and shadowing stories.",
      "ধাপে ধাপে পরিষ্কার ব্রিটিশ উচ্চারণ: ২২টি পাঠ, ধ্বনি-অনুশীলন ও শ্যাডোয়িং গল্প।", tool="studio:pronunciation", tag="popular"),
    C("grammar", "📚", "language", "Grammar coach", "ব্যাকরণ কোচ",
      "41 short chat lessons from A1 to C, explained in English and Bangla.", "A1 থেকে C — ৪১টি ছোট চ্যাট-পাঠ, ইংরেজি ও বাংলায়।", tool="studio:grammar"),
    C("speech", "🎙️", "language", "Speech analyzer", "স্পিচ অ্যানালাইজার",
      "Record yourself and find out how you sound: speed, fillers, range of words.", "নিজের কথা রেকর্ড করে দেখুন: গতি, অপ্রয়োজনীয় শব্দ, শব্দভান্ডার।", tool="studio:analyzer", tag="new"),
    C("vocabulary", "🃏", "language", "Vocabulary coach", "শব্দভান্ডার কোচ",
      "Practise your saved words and your weekly word list.", "সংরক্ষিত শব্দ ও সাপ্তাহিক শব্দ অনুশীলন।", tool="studio:my_words"),
    C("presentation", "📊", "professional", "Presentation coach", "প্রেজেন্টেশন কোচ",
      "Paste your speech or slides' notes and rehearse it line by line.", "আপনার বক্তৃতা বা নোট পেস্ট করে লাইন ধরে অনুশীলন করুন।", tool="studio:rehearse", tag="beta"),
    C("everyday", "🛟", "everyday", "Everyday English", "দৈনন্দিন ইংরেজি",
      "Simple English to ask, order and get help.", "জিজ্ঞেস করা, অর্ডার ও সাহায্য চাওয়ার সহজ ইংরেজি।", tag="new", scenarios=[
          S("lost", "Asking for help in a new place", "নতুন জায়গায় সাহায্য চাওয়া", "A busy shopping mall", "a friendly security guard",
            [("Hello, can I help you?", "Yes, please. I can't find the lift."), ("It's behind the food court, on the left.", "Thank you. Is there a prayer room too?"),
             ("Yes, on the third floor.", "Great. And where can I find a toilet?"), ("Next to the lift.", "Thanks a lot for your help.")]),
          S("delivery", "A delivery that didn't arrive", "পৌঁছায়নি এমন ডেলিভারি", "A phone call to a delivery company", "a polite customer-care agent",
            [("Good afternoon, how can I help you?", "My parcel hasn't arrived. It was due yesterday."), ("Can I have your order number, please?", "Yes, it's four five two eight one."),
             ("Thank you. It's at the local hub. It will arrive tomorrow.", "Could it come in the morning? I'm out in the afternoon."), ("Yes, I've noted that.", "Thank you very much.")]),
      ]),
    C("travel", "🧳", "everyday", "Travel coach", "ভ্রমণ কোচ",
      "Practise English for airports, hotels and trips.", "বিমানবন্দর, হোটেল ও ভ্রমণের ইংরেজি।", scenarios=[
          S("airport", "Checking in at the airport", "বিমানবন্দরে চেক-ইন", "Shahjalal International Airport check-in desk", "an airline check-in officer",
            [("Good evening. May I see your passport and ticket?", "Here you are."), ("Do you have any bags to check in?", "Yes, one suitcase."),
             ("Would you like a window or an aisle seat?", "A window seat, please."), ("Here's your boarding pass. Gate twelve.", "Thank you. What time does boarding start?")]),
          S("hotel", "Checking into a hotel", "হোটেলে চেক-ইন", "A hotel reception in Cox's Bazar", "a hotel receptionist",
            [("Welcome! Do you have a reservation?", "Yes, it's under the name Hasan."), ("For three nights, a double room?", "That's right. Does it have a sea view?"),
             ("Yes, it does. Breakfast is from seven to ten.", "Great. Is there Wi-Fi in the room?"), ("Yes, the password is on your key card.", "Thank you very much.")]),
      ]),
    C("doctor", "🩺", "everyday", "Doctor visit", "ডাক্তার দেখানো",
      "Explain symptoms clearly and understand advice.", "লক্ষণ পরিষ্কার বলা ও পরামর্শ বোঝা।", scenarios=[
          S("fever", "A child with a fever", "শিশুর জ্বর", "A doctor's chamber", "a kind children's doctor",
            [("Hello. What's the problem today?", "My son has had a fever for two days."), ("Is he eating and drinking?", "He drinks water but he isn't eating much."),
             ("Any cough or rash?", "A little cough, but no rash."), ("Give him this syrup as it says on the label.", "Thank you, doctor. When should we come back?")]),
          S("pharmacy", "At the pharmacy", "ফার্মেসিতে", "A pharmacy", "a pharmacist",
            [("Hello, what do you need?", "I need something for a headache."), ("Do you have any allergies?", "No, I don't."),
             ("Take one tablet every six hours.", "Can I take it before food?"), ("Better after food.", "OK, thank you. How much is it?")]),
      ]),
    C("school-meeting", "🏫", "everyday", "Parent–teacher meeting", "অভিভাবক-শিক্ষক সভা",
      "Talk with your child's teacher in English.", "সন্তানের শিক্ষকের সাথে ইংরেজিতে কথা বলুন।", scenarios=[
          S("progress", "Asking about progress", "অগ্রগতি জানতে চাওয়া", "An English-medium school classroom", "a friendly class teacher",
            [("Good morning. Thank you for coming.", "Good morning. How is my daughter doing?"), ("She's doing well in maths, but she's quiet in class.", "I see. How can we help her speak more at home?"),
             ("Read together and ask her questions in English.", "That's a good idea. Is her homework OK?"), ("Yes, it's always on time.", "Thank you. We'll practise every evening.")]),
          S("absent", "Explaining an absence", "অনুপস্থিতির কারণ বলা", "The school office", "a school office assistant",
            [("Hello, can I help you?", "Yes. My son was absent yesterday because he was ill."), ("Do you have a note?", "Yes, here is the doctor's note."),
             ("Thank you. Will he come tomorrow?", "Yes, he's feeling much better now."), ("Good. I'll tell his teacher.", "Thank you. Could he get yesterday's homework?")]),
      ]),
    C("interview", "🤝", "professional", "Interview coach", "ইন্টারভিউ কোচ",
      "Practise job and admission interviews with clear answers.", "চাকরি ও ভর্তির ইন্টারভিউ অনুশীলন।", scenarios=[
          S("job", "A job interview", "চাকরির ইন্টারভিউ", "An office interview room", "a professional HR manager",
            [("Please tell me about yourself.", "I'm a graduate in accounting with two years of experience at a bank."),
             ("Why do you want this job?", "I want to grow my career, and your company is known for training staff well."),
             ("What is your greatest strength?", "I'm careful with details and I always meet deadlines."),
             ("Do you have any questions for us?", "Yes. What does a typical day look like in this role?")]),
          S("admission", "A university admission interview", "বিশ্ববিদ্যালয় ভর্তির ইন্টারভিউ", "A university admissions office", "a university professor",
            [("Why did you choose this subject?", "I've loved computers since school, and I want to build useful apps."),
             ("What did you do outside class?", "I was in the science club and I taught English to younger children."),
             ("Where do you see yourself in five years?", "Working as a software engineer and helping my community."),
             ("Thank you. Any questions?", "Are there chances for students to do research?")]),
      ]),
    C("meeting", "📅", "professional", "Meeting coach", "মিটিং কোচ",
      "Practise speaking up in work meetings.", "অফিস মিটিংয়ে কথা বলার অনুশীলন।", tag="new", scenarios=[
          S("update", "Giving a project update", "প্রকল্পের হালনাগাদ", "A weekly team meeting", "a team manager",
            [("Let's start. Can you give us your update?", "Sure. We finished the first stage last week."), ("Any problems?", "One supplier is late, so we may need two more days."),
             ("What do you suggest?", "I suggest we contact a second supplier as a backup."), ("Good idea. Anything else?", "No, that's all from me. Thank you.")]),
          S("disagree", "Disagreeing politely", "ভদ্রভাবে দ্বিমত", "A planning meeting", "a senior colleague",
            [("I think we should launch next month.", "I see your point, but I'm worried we won't be ready."), ("Why not?", "Testing will take at least three weeks."),
             ("So what's your plan?", "Perhaps we could launch a small version first."), ("That could work.", "Great. I'll prepare a timeline by Thursday.")]),
      ]),
    C("public-speaking", "🎤", "professional", "Public speaking coach", "জনসমক্ষে বক্তৃতা",
      "Give short talks with confidence. Your speech is analysed.", "আত্মবিশ্বাসের সাথে ছোট বক্তৃতা। আপনার কথা বিশ্লেষণ হবে।", tool="studio:analyzer"),
    C("customer", "🏦", "professional", "Customer service coach", "গ্রাহকসেবা কোচ",
      "Serve customers politely in a bank, shop or office.", "ব্যাংক, দোকান বা অফিসে ভদ্রভাবে গ্রাহকসেবা।", scenarios=[
          S("complaint", "An unhappy customer", "অসন্তুষ্ট গ্রাহক", "A bank branch counter (you are the officer)", "an annoyed bank customer",
            [("I've been waiting for forty minutes!", "I'm very sorry for the wait. How can I help you today?"), ("My card isn't working at the ATM.", "I understand. Let me check your card for you."),
             ("Can you fix it now?", "Yes, it was blocked. I've unblocked it now."), ("Thank you, finally.", "You're welcome. Is there anything else I can help with?")]),
          S("explain", "Explaining a service", "সেবা বুঝিয়ে বলা", "A mobile phone shop (you are the seller)", "a curious customer",
            [("What's the difference between these two phones?", "This one has a better camera, and that one has a bigger battery."),
             ("Which is better for my mother?", "The second one — the screen is bigger and easy to read."), ("How much is it?", "It's fifteen thousand taka, with a one-year warranty."),
             ("Can I pay by bKash?", "Yes, of course.")]),
      ]),
    C("negotiation", "💬", "professional", "Negotiation coach", "দরকষাকষি কোচ",
      "Practise real negotiations — a job offer, a price, a deadline.", "চাকরির প্রস্তাব, দাম, সময়সীমা নিয়ে দরকষাকষি।", tag="new", scenarios=[
          S("salary", "Discussing a job offer", "চাকরির প্রস্তাব নিয়ে আলোচনা", "An HR office", "an HR manager",
            [("We'd like to offer you the job at thirty thousand taka.", "Thank you. I'm very happy about the offer."), ("Do you accept?", "I was hoping for thirty-five, based on my experience."),
             ("We could offer thirty-two.", "Could we agree on thirty-two with a review after six months?"), ("That sounds fair.", "Great. Thank you very much.")]),
          S("rent", "Talking to a landlord", "বাড়িওয়ালার সাথে কথা", "A flat viewing", "a landlord",
            [("The rent is twenty thousand a month.", "The flat is nice, but it's a bit above my budget."), ("What's your budget?", "Around eighteen thousand."),
             ("Nineteen is my best price.", "If I sign for two years, could you make it eighteen and a half?"), ("OK, agreed.", "Wonderful. When can I move in?")]),
      ]),
    C("conflict", "🕊️", "professional", "Conflict management coach", "দ্বন্দ্ব সামলানো",
      "Handle disagreements without damaging relationships.", "সম্পর্ক না ভেঙে দ্বিমত সামলান।", tag="new", scenarios=[
          S("noise", "A noisy neighbour", "শব্দ করা প্রতিবেশী", "Your neighbour's door", "a slightly defensive neighbour",
            [("Yes? What is it?", "Hello! Sorry to bother you. Could I ask you something?"), ("Go ahead.", "The music late at night makes it hard for my children to sleep."),
             ("Oh, I didn't know it was so loud.", "No problem. Could you turn it down after ten?"), ("Sure, I'll do that.", "Thank you so much. I really appreciate it.")]),
          S("teammate", "A teammate who misses deadlines", "সময়মতো কাজ না করা সহকর্মী", "A quiet office corner", "a stressed colleague",
            [("You wanted to talk?", "Yes. I've noticed the reports are often late. Is everything OK?"), ("I have too much work.", "I understand. How can I help?"),
             ("Maybe share the data earlier?", "Sure. I'll send it on Monday mornings."), ("That would help a lot.", "Great, let's try it this week.")]),
      ]),
    C("storytelling", "📖", "kids", "Storytelling coach", "গল্প বলার কোচ",
      "Children tell a story picture by picture.", "শিশুরা ছবি ধরে ধরে গল্প বলে।", scenarios=[
          S("tiger", "The tiger and the clever rabbit", "বাঘ আর চালাক খরগোশ", "A story circle", "a cheerful storyteller",
            [("Once upon a time, there was a big tiger. Who did he meet?", "He met a small, clever rabbit."), ("What did the tiger want?", "The tiger wanted to eat the rabbit."),
             ("What did the rabbit say?", "The rabbit said, 'There is a bigger tiger in the well!'"), ("And then?", "The tiger saw his own face in the water, got scared and ran far away. The rabbit was safe.")]),
          S("show", "Show and tell", "দেখাও আর বলো", "A classroom", "a kind teacher",
            [("What did you bring today?", "I brought my toy boat."), ("Who gave it to you?", "My grandfather made it for me."),
             ("What colour is it?", "It's red and blue."), ("Why do you like it?", "Because I play with it in the bath.")]),
      ]),
    C("leadership", "🧭", "professional", "Leadership coach", "নেতৃত্ব কোচ",
      "Practise giving clear instructions and feedback.", "পরিষ্কার নির্দেশনা ও ফিডব্যাক দেওয়ার অনুশীলন।", tag="beta", scenarios=[
          S("feedback", "Giving feedback", "ফিডব্যাক দেওয়া", "A one-to-one meeting (you are the manager)", "a junior team member",
            [("You wanted to see me?", "Yes. First, thank you for your hard work on the report."), ("Thank you!", "There were a few mistakes in the numbers, though."),
             ("Oh, I'm sorry.", "That's OK. Next time, could you check them twice before sending?"), ("Yes, I will.", "Great. I'm happy with your progress.")]),
      ]),
]

BY_SLUG = {c["slug"]: c for c in COACHES}


def scenario(coach_slug, scen_slug):
    coach = BY_SLUG.get(coach_slug)
    if not coach:
        return None, None
    for s in coach["scenarios"]:
        if s["slug"] == scen_slug:
            return coach, s
    return coach, None
