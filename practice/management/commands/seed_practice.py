from django.core.management.base import BaseCommand
from django.db import transaction

from practice.models import Tutorial, VocabDeck, VocabWord
from practice.seed_data import DECKS, TUTORIALS
from practice.word_info import WORD_INFO


class Command(BaseCommand):
    help = "Load vocabulary decks and the 'How to use FamilyEnglish' tutorials (safe to re-run)."

    @transaction.atomic
    def handle(self, *args, **opts):
        for d_order, (slug, title, title_bn, emoji, level, words) in enumerate(DECKS, 1):
            deck, _ = VocabDeck.objects.update_or_create(
                slug=slug, defaults=dict(title=title, title_bn=title_bn, emoji=emoji, level=level,
                                         order=d_order))
            keep = []
            for w_order, (word, wemoji, bn, example) in enumerate(words, 1):
                w, _ = VocabWord.objects.update_or_create(
                    deck=deck, word=word,
                    defaults=dict(emoji=wemoji, meaning_bn=bn, example=example, order=w_order,
                                  pos=WORD_INFO.get(word, ("", ""))[0], definition=WORD_INFO.get(word, ("", ""))[1]))
                keep.append(w.id)
            # Words removed from the seed file are removed here (and their reviews with them).
            deck.words.exclude(id__in=keep).delete()

        for order, title, title_bn, group, summary, steps, minutes, link in TUTORIALS:
            t, created = Tutorial.objects.get_or_create(order=order, defaults=dict(
                title=title, title_bn=title_bn, group=group, summary=summary, steps_bn=steps,
                minutes=minutes, link_name=link))
            if not created:  # keep any youtube_id added in the admin
                for k, v in dict(title=title, title_bn=title_bn, group=group, summary=summary,
                                 steps_bn=steps, minutes=minutes, link_name=link).items():
                    setattr(t, k, v)
                t.save()

        if opts.get("verbosity", 1) > 0:
            self.stdout.write(self.style.SUCCESS(
                f"Seeded {VocabDeck.objects.count()} vocabulary decks, {VocabWord.objects.count()} words "
                f"and {Tutorial.objects.count()} tutorials."))
