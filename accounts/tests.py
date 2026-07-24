from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from accounts.models import Address


class AddressDeletionTests(TestCase):
    def test_address_deletion_requires_post(self):
        user = User.objects.create_user(username="customer", password="safe-password")
        address = Address.objects.create(user=user, full_name="Customer", phone="123", country="Iraq", city="Baghdad", address_line1="Test street")
        self.client.force_login(user)

        response = self.client.get(reverse("accounts:delete_address", args=[address.pk]))

        self.assertEqual(response.status_code, 405)
        self.assertTrue(Address.objects.filter(pk=address.pk).exists())
