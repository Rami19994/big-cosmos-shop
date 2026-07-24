from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase


class EnsureSuperuserCommandTests(TestCase):
    def test_command_creates_a_staff_superuser_from_environment(self):
        with patch.dict("os.environ", {
            "DJANGO_SUPERUSER_USERNAME": "deployment-admin",
            "DJANGO_SUPERUSER_PASSWORD": "secure-test-password",
            "DJANGO_SUPERUSER_EMAIL": "admin@example.com",
        }, clear=False):
            call_command("ensure_superuser")

        user = get_user_model().objects.get(username="deployment-admin")
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.check_password("secure-test-password"))
