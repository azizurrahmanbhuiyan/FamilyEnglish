"""Give existing learners the XP they already earned from finished lessons (20 + 10 per star)."""

from django.db import migrations


def backfill(apps, schema_editor):
    Progress = apps.get_model("learning", "Progress")
    XPEvent = apps.get_model("growth", "XPEvent")
    rows = []
    for p in Progress.objects.all():
        rows.append(XPEvent(learner_id=p.learner_id, amount=20, reason="lesson",
                            key=f"lesson-{p.lesson_id}", created_at=p.completed_at))
        for n in range(1, p.stars + 1):
            rows.append(XPEvent(learner_id=p.learner_id, amount=10, reason="lesson stars",
                                key=f"lesson-{p.lesson_id}-s{n}", created_at=p.completed_at))
    XPEvent.objects.bulk_create(rows, ignore_conflicts=True)


class Migration(migrations.Migration):
    dependencies = [
        ("growth", "0001_initial"),
        ("learning", "0002_planday_course_lesson_studyplan_kind_and_more"),
    ]
    operations = [migrations.RunPython(backfill, migrations.RunPython.noop)]
