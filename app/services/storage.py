import os
import boto3
from datetime import timedelta
from botocore.client import Config
from botocore.exceptions import ClientError


# Load env
S3_ENDPOINT = os.getenv("S3_ENDPOINT")
S3_ACCESS_KEY = os.getenv("S3_ACCESS_KEY")
S3_SECRET_KEY = os.getenv("S3_SECRET_KEY")
S3_BUCKET = os.getenv("S3_BUCKET")
S3_REGION = os.getenv("S3_REGION", "auto")

_s3_client = None


def get_client():
    """
    Singleton S3 client (Cloudflare R2 compatible)
    """
    global _s3_client
    if _s3_client is None:
        _s3_client = boto3.client(
            "s3",
            endpoint_url=S3_ENDPOINT,
            aws_access_key_id=S3_ACCESS_KEY,
            aws_secret_access_key=S3_SECRET_KEY,
            region_name=None if S3_REGION == "auto" else S3_REGION,
            config=Config(signature_version="s3v4"),
        )

        # Ensure bucket exists
        try:
            _s3_client.head_bucket(Bucket=S3_BUCKET)
        except ClientError as e:
            if e.response["Error"]["Code"] != "404":
                raise

    return _s3_client


def upload_image(local_path: str, object_name: str) -> str:
    """
    Upload image to Cloudflare R2 and return presigned URL (1 hour)
    """
    client = get_client()

    client.upload_file(
        Filename=local_path,
        Bucket=S3_BUCKET,
        Key=object_name,
        ExtraArgs={"ContentType": "image/jpeg"},
    )

    # Presigned URL (1 hour)
    url = client.generate_presigned_url(
        ClientMethod="get_object",
        Params={
            "Bucket": S3_BUCKET,
            "Key": object_name,
        },
        ExpiresIn=3600,
    )

    return url