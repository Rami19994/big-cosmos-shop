from botocore.exceptions import ClientError
from storages.backends.s3boto3 import S3Boto3Storage


class ResilientS3Storage(S3Boto3Storage):
    """Treat deleted Supabase objects as absent instead of failing admin edits."""

    @staticmethod
    def _is_missing_object(error):
        code = str(error.response.get("Error", {}).get("Code", ""))
        status = str(error.response.get("ResponseMetadata", {}).get("HTTPStatusCode", ""))
        return code in {"404", "410", "NoSuchKey", "Gone"} or status in {"404", "410"}

    def exists(self, name):
        try:
            return super().exists(name)
        except ClientError as error:
            if self._is_missing_object(error):
                return False
            raise

    def size(self, name):
        try:
            return super().size(name)
        except ClientError as error:
            if self._is_missing_object(error):
                return 0
            raise
