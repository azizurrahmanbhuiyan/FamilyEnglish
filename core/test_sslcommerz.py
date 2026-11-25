from unittest import mock

from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import Family, PaymentRequest, Plan

GATEWAY = "https://sandbox.sslcommerz.com/EasyCheckOut/testcde"


@override_settings(SSLC_STORE_ID="testbox", SSLC_STORE_PASSWORD="qwerty", SSLC_SANDBOX=True)
class SslcommerzTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("p@example.com", "p@example.com", "very-safe-pass-9", first_name="Pia")
        self.client.force_login(self.user)

    def family(self, country):
        return Family.objects.create(owner=self.user, name="Pia family", country=country)

    def start(self, plan="monthly"):
        with mock.patch("core.sslcommerz._post", return_value={"status": "SUCCESS", "GatewayPageURL": GATEWAY}) as post:
            r = self.client.post(reverse("core:pay_online"), {"plan": plan})
        self.assertRedirects(r, GATEWAY, fetch_redirect_response=False)
        return PaymentRequest.objects.latest("created_at"), post.call_args[0][1]

    def valid(self, p, **over):
        data = {"status": "VALID", "tran_id": p.transaction_id, "val_id": "V1", "amount": "299.00",
                "currency": "BDT", "currency_type": p.currency, "currency_amount": f"{p.amount:.2f}",
                "bank_tran_id": "B1", "card_type": "BKASH-BKash", "risk_level": "0"}
        data.update(over)
        return data

    def test_bangladesh_family_pays_taka_and_plan_switches_on(self):
        fam = self.family("BD")
        p, sent = self.start()
        self.assertEqual((sent["currency"], sent["total_amount"], sent["tran_id"]), ("BDT", "299.00", p.transaction_id))
        self.assertTrue(sent["ipn_url"].endswith("/pay/sslcommerz/ipn/"))
        self.assertEqual(p.status, "pending")
        with mock.patch("core.sslcommerz._get", return_value=self.valid(p)):
            r = self.client.post(reverse("core:sslc_success"), {"tran_id": p.transaction_id, "val_id": "V1"})
        self.assertRedirects(r, reverse("core:pay_result") + "?t=" + p.transaction_id, fetch_redirect_response=False)
        p.refresh_from_db(); fam.refresh_from_db()
        self.assertEqual(p.status, "confirmed")
        self.assertEqual((p.bank_tran_id, p.card_type), ("B1", "BKASH-BKash"))
        self.assertEqual(fam.plan, Plan.MONTHLY)
        self.assertTrue(fam.is_paid_active)
        self.assertContains(self.client.get(r.url), "Payment done!")

    def test_family_abroad_pays_dollars(self):
        fam = self.family("GB")
        self.assertContains(self.client.get(reverse("core:pay")), "$25")
        p, sent = self.start("year")
        self.assertEqual((sent["currency"], sent["total_amount"], sent["cus_country"]), ("USD", "25.00", "United Kingdom"))
        with mock.patch("core.sslcommerz._get", return_value=self.valid(p, amount="3050.00", currency="BDT")):
            self.client.post(reverse("core:sslc_ipn"), {"status": "VALID", "tran_id": p.transaction_id, "val_id": "V1"})
        p.refresh_from_db(); fam.refresh_from_db()
        self.assertEqual((p.status, p.amount_bdt, p.display_amount), ("confirmed", 3050, "$25.00"))
        self.assertEqual(fam.plan, Plan.YEAR)

    def test_wrong_amount_is_refused(self):
        fam = self.family("BD")
        p, _ = self.start()
        with mock.patch("core.sslcommerz._get", return_value=self.valid(p, currency_amount="10.00")):
            self.client.post(reverse("core:sslc_success"), {"tran_id": p.transaction_id, "val_id": "V1"})
        p.refresh_from_db(); fam.refresh_from_db()
        self.assertEqual(p.status, "rejected")
        self.assertFalse(fam.is_paid_active)

    def test_invalid_or_fake_post_does_nothing(self):
        fam = self.family("BD")
        p, _ = self.start()
        with mock.patch("core.sslcommerz._get", return_value={"status": "INVALID_TRANSACTION"}):
            self.client.post(reverse("core:sslc_success"), {"tran_id": p.transaction_id, "val_id": "fake"})
        p.refresh_from_db()
        self.assertEqual(p.status, "pending")
        fam.refresh_from_db()
        self.assertFalse(fam.is_paid_active)

    def test_success_and_ipn_together_confirm_once(self):
        fam = self.family("BD")
        p, _ = self.start()
        with mock.patch("core.sslcommerz._get", return_value=self.valid(p)):
            self.client.post(reverse("core:sslc_success"), {"tran_id": p.transaction_id, "val_id": "V1"})
            first = Family.objects.get(pk=fam.pk).paid_until
            self.client.post(reverse("core:sslc_ipn"), {"status": "VALID", "tran_id": p.transaction_id, "val_id": "V1"})
        self.assertEqual(Family.objects.get(pk=fam.pk).paid_until, first)

    def test_high_risk_still_gets_access_with_a_note(self):
        fam = self.family("BD")
        p, _ = self.start()
        with mock.patch("core.sslcommerz._get", return_value=self.valid(p, risk_level="1", risk_title="Risky")):
            self.client.post(reverse("core:sslc_success"), {"tran_id": p.transaction_id, "val_id": "V1"})
        p.refresh_from_db(); fam.refresh_from_db()
        self.assertEqual(p.status, "confirmed")
        self.assertIn("High risk", p.note)
        self.assertTrue(fam.has_full_access)

    def test_slow_gateway_is_retried_on_the_result_page(self):
        fam = self.family("BD")
        p, _ = self.start()
        with mock.patch("core.sslcommerz._get", side_effect=TimeoutError):
            r = self.client.post(reverse("core:sslc_success"), {"tran_id": p.transaction_id, "val_id": "V1"})
        p.refresh_from_db()
        self.assertEqual((p.status, p.val_id), ("pending", "V1"))
        with mock.patch("core.sslcommerz._get", return_value=self.valid(p)):
            res = self.client.get(r.url)
        self.assertContains(res, "Payment done!")
        fam.refresh_from_db()
        self.assertTrue(fam.has_full_access)

    def test_access_is_immediate(self):
        fam = self.family("BD")
        self.assertFalse(fam.has_full_access)
        p, _ = self.start()
        with mock.patch("core.sslcommerz._get", return_value=self.valid(p)):
            self.client.post(reverse("core:sslc_success"), {"tran_id": p.transaction_id, "val_id": "V1"})
        fam.refresh_from_db()
        self.assertTrue(fam.has_full_access)

    def test_cancel_and_fail(self):
        self.family("BD")
        p, _ = self.start()
        r = self.client.post(reverse("core:sslc_cancel"), {"tran_id": p.transaction_id})
        p.refresh_from_db()
        self.assertEqual(p.status, "cancelled")
        self.assertContains(self.client.get(r.url), "did not go through")

    def test_gateway_down(self):
        self.family("BD")
        with mock.patch("core.sslcommerz._post", return_value={"status": "FAILED", "failedreason": "Store is inactive"}):
            r = self.client.post(reverse("core:pay_online"), {"plan": "monthly"})
        self.assertRedirects(r, reverse("core:pay"))
        self.assertEqual(PaymentRequest.objects.get().status, "failed")

    def test_abroad_cannot_use_bkash_form(self):
        self.family("US")
        self.client.post(reverse("core:pay"), {"plan": "monthly", "method": "bkash", "transaction_id": "X1"})
        self.assertFalse(PaymentRequest.objects.exists())

    @override_settings(SSLC_STORE_ID="")
    def test_hidden_without_store(self):
        self.family("BD")
        r = self.client.get(reverse("core:pay"))
        self.assertNotContains(r, "Pay now")
        self.assertContains(r, "01710503504")

    def test_pricing_in_dollars_abroad(self):
        self.client.logout()
        r = self.client.get(reverse("core:pricing"), HTTP_CF_IPCOUNTRY="US")
        self.assertContains(r, "$3")
        self.assertContains(r, "$2.08")
        r = self.client.get(reverse("core:pricing"), HTTP_CF_IPCOUNTRY="BD")
        self.assertContains(r, "৳299")
