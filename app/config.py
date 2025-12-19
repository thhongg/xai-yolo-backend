import os

# ---------- S3-compatible (Cloudflare R2) ----------
S3_ENDPOINT = os.getenv("S3_ENDPOINT")        # https://<account>.r2.cloudflarestorage.com
S3_ACCESS_KEY = os.getenv("S3_ACCESS_KEY")
S3_SECRET_KEY = os.getenv("S3_SECRET_KEY")
S3_BUCKET = os.getenv("S3_BUCKET")
S3_REGION = os.getenv("S3_REGION", "auto")
S3_PUBLIC_ENDPOINT = os.getenv("S3_PUBLIC_ENDPOINT")  # để generate public URL
