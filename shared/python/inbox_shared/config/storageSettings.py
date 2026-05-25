import os
from dataclasses import dataclass


@dataclass
class StorageSettings:
    storageProvider: str = os.getenv("STORAGE_PROVIDER", "minio")

    s3EndpointUrl: str = os.getenv("S3_ENDPOINT_URL", "http://localhost:9002")
    s3AccessKey: str = os.getenv("S3_ACCESS_KEY", "inboxminio")
    s3SecretKey: str = os.getenv("S3_SECRET_KEY", "inboxminio123")
    s3BucketName: str = os.getenv("S3_BUCKET_NAME", "inbox-ai-documents")
    s3Region: str = os.getenv("S3_REGION", "us-east-1")


storageSettings = StorageSettings()