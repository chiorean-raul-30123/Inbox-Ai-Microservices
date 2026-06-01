import uuid
from pathlib import Path

import boto3

from inbox_shared.config.storageSettings import storageSettings
from inbox_shared.exceptions import (
    MissingFileException,
    StorageDownloadException,
    StorageUploadException,
    UnsupportedFileTypeException,
    ValidationException,
)
import tempfile
import shutil
from inbox_shared.services.securityScanService import SecurityScanService


class StorageService:
    def __init__(self) -> None:
        self.bucketName = storageSettings.s3BucketName
        self.tempDir = Path("temp_uploads")
        self.tempDir.mkdir(parents=True, exist_ok=True)
        self.securityScanService = SecurityScanService()

        self.client = boto3.client(
            "s3",
            endpoint_url=storageSettings.s3EndpointUrl,
            aws_access_key_id=storageSettings.s3AccessKey,
            aws_secret_access_key=storageSettings.s3SecretKey,
            region_name=storageSettings.s3Region,
        )

    def uploadPdfFileObject(
        self,
        fileObject,
        *,
        filename: str,
        contentType: str,
    ) -> dict:
        if not filename:
            raise MissingFileException("No file was provided.")

        extension = Path(filename).suffix.lower()

        if extension != ".pdf":
            raise UnsupportedFileTypeException(
                "Unsupported file type. Please upload a PDF document."
            )

        if contentType != "application/pdf":
            raise UnsupportedFileTypeException(
                "Invalid content type. Only PDF documents are supported."
            )

        storedFilename = f"{uuid.uuid4()}{extension}"
        objectKey = f"documents/{storedFilename}"

        fileObject.seek(0, 2)
        fileSize = fileObject.tell()
        fileObject.seek(0)
        self.scanFileObjectBeforeUpload(
            fileObject,
            suffix=".pdf",
        )

        try:
            self.client.upload_fileobj(
                fileObject,
                self.bucketName,
                objectKey,
                ExtraArgs={
                    "ContentType": contentType,
                },
            )
        except Exception as exception:
            raise StorageUploadException(
                "Could not upload document to storage. Please try again."
            ) from exception

        return {
            "originalFilename": filename,
            "storedFilename": storedFilename,
            "objectKey": objectKey,
            "mimeType": contentType,
            "fileSize": fileSize,
        }

    def downloadToTempFile(self, objectKey: str) -> str:
        if not objectKey:
            raise ValidationException("Storage object key is missing.")

        extension = Path(objectKey).suffix.lower()

        if not extension:
            extension = ".bin"

        tempFilename = f"{uuid.uuid4()}{extension}"
        tempPath = self.tempDir / tempFilename

        try:
            self.client.download_file(
                self.bucketName,
                objectKey,
                str(tempPath),
            )
        except Exception as exception:
            raise StorageDownloadException(
                f"Could not download object from storage: {objectKey}"
            ) from exception

        return str(tempPath)

    def getDownloadUrl(self, objectKey: str, expiresInSeconds: int = 300) -> str:
        if not objectKey:
            raise ValidationException("Storage object key is missing.")

        return self.client.generate_presigned_url(
            "get_object",
            Params={
                "Bucket": self.bucketName,
                "Key": objectKey,
            },
            ExpiresIn=expiresInSeconds,
        )
    
    def uploadImageFileObject(
        self,
        fileObject,
        *,
        filename: str,
        contentType: str,
        ) -> dict:
        if not filename:
            raise MissingFileException("No file was provided.")
        
        allowedContentTypes = {
            "image/jpeg",
            "image/png",
            "image/webp",
        }

        if contentType not in allowedContentTypes:
            raise UnsupportedFileTypeException(
                "Unsupported scan file type. Please upload a JPEG, PNG, or WEBP image."
            )
        
        extension = Path(filename).suffix.lower()

        if extension not in [".jpg", ".jpeg", ".png", ".webp"]:
            raise UnsupportedFileTypeException(
                "Unsupported scan extension. Please upload .jpg, .jpeg, .png, or .webp."
            )

        storedFilename = f"{uuid.uuid4()}{extension}"
        objectKey = f"scans/{storedFilename}"

        fileObject.seek(0, 2)
        fileSize = fileObject.tell()
        fileObject.seek(0)
        self.scanFileObjectBeforeUpload(
            fileObject,
            suffix=extension,
        )

        try:
            self.client.upload_fileobj(
                fileObject,
                self.bucketName,
                objectKey,
                ExtraArgs={
                    "ContentType": contentType,
                },
            )
        except Exception as exception:
            raise StorageUploadException("Could not upload scanned image to storage. Please try again.") from exception

        return {
            "originalFilename": filename,
            "storedFilename": storedFilename,
            "objectKey": objectKey,
            "mimeType": contentType,
            "fileSize": fileSize,
        }
    
    def scanFileObjectBeforeUpload(
        self,
        fileObject,
        *,
        suffix: str,
    ) -> None:
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tempFile:
            tempPath = tempFile.name
            fileObject.seek(0)
            shutil.copyfileobj(fileObject, tempFile)
        print(f"Scanning file before upload: {tempPath}")

        try:
            self.securityScanService.scanFile(tempPath)
        finally:
            Path(tempPath).unlink(missing_ok=True)
            fileObject.seek(0)