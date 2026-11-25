from pathlib import Path

from django.conf import settings
from django.test import TestCase
from django.urls import reverse

from .views import WORKSHEETS


class WorksheetTests(TestCase):
    def test_public_page_lists_five_downloads(self):
        r = self.client.get(reverse("core:worksheets"))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "familyenglish-phonics-", count=5)
        for slug, *_ in WORKSHEETS:
            pdf = Path(settings.BASE_DIR) / "static/downloads/phonics" / f"familyenglish-phonics-{slug}.pdf"
            self.assertTrue(pdf.exists(), pdf)

    def test_linked_from_public_footer(self):
        self.assertContains(self.client.get(reverse("core:pricing")), reverse("core:worksheets"))
