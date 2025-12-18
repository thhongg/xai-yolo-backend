from minio import Minio
from app.config import (
    MINIO_ENDPOINT,
    MINIO_ACCESS_KEY,
    MINIO_SECRET_KEY,
    MINIO_BUCKET,
    MINIO_SECURE,
)

_client = None


def get_client():
    global _client
    if _client is None:
        _client = Minio(
            MINIO_ENDPOINT,
            access_key=MINIO_ACCESS_KEY,
            secret_key=MINIO_SECRET_KEY,
            secure=MINIO_SECURE,
        )
        if not _client.bucket_exists(MINIO_BUCKET):
            _client.make_bucket(MINIO_BUCKET)
    return _client


def upload_image(local_path: str, object_name: str) -> str:
    client = get_client()
    client.fput_object(
        MINIO_BUCKET,
        object_name,
        local_path,
        content_type="image/jpeg",
    )
    return f"http://localhost:9000/{MINIO_BUCKET}/{object_name}"
