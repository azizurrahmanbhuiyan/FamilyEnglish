from django.urls import path

from . import views, words

app_name = "practice"

urlpatterns = [
    path("checks/", views.checks, name="checks"),
    path("checks/<str:skill>/", views.level_check, name="level_check"),
    path("checks/result/<int:pk>/", views.check_result, name="check_result"),
    path("skill/<str:skill>/", views.skill_practice, name="skill_practice"),
    path("dictation/", views.dictation, name="dictation"),
    path("dictation/save/", views.dictation_save, name="dictation_save"),
    path("speaking/", views.speaking, name="speaking"),
    path("speaking/save/", views.speaking_save, name="speaking_save"),
    path("writing/", views.writing, name="writing"),
    path("tutor/", views.tutor, name="tutor"),
    path("tutor/history/<int:learner_pk>/", views.tutor_history, name="tutor_history"),
    path("words/", words.words_home, name="words"),
    path("words/<slug:slug>/", words.word_week, name="word_week"),
    path("words/<slug:slug>/write/", words.word_write, name="word_write"),
    path("words/<slug:slug>/done/", words.word_done, name="word_done"),
    path("vocabulary/", views.vocab, name="vocab"),
    path("vocabulary/review/", views.vocab_study, name="vocab_review"),
    path("vocabulary/rate/", views.vocab_rate, name="vocab_rate"),
    path("vocabulary/<slug:slug>/", views.vocab_study, name="vocab_deck"),
    path("reports/", views.reports, name="reports"),
    path("refer/", views.refer, name="refer"),
    path("how-to-use/", views.tutorials, name="tutorials"),
    path("support/", views.support, name="support"),
    path("support/file/<int:pk>/", views.support_file, name="support_file"),
    path("typing/", views.typing, name="typing"),
    path("typing/save/", views.typing_save, name="typing_save"),
]
