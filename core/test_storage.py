from unittest.mock import Mock, patch

from botocore.exceptions import ClientError
from django.test import SimpleTestCase

from core.storage import ResilientS3Storage


class ResilientS3StorageTests(SimpleTestCase):
    def test_missing_object_errors_are_handled(self):
        error = ClientError({"Error": {"Code": "Gone"}, "ResponseMetadata": {"HTTPStatusCode": 410}}, "HeadObject")
        storage = ResilientS3Storage()

        with patch("storages.backends.s3boto3.S3Boto3Storage.exists", side_effect=error):
            self.assertFalse(storage.exists("products/missing.avif"))
        with patch("storages.backends.s3boto3.S3Boto3Storage.size", side_effect=error):
            self.assertEqual(storage.size("products/missing.avif"), 0)
