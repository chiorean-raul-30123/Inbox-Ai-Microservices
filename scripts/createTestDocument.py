from inbox_shared.database import createDbSession
from inbox_shared.enums import DocumentStatus
from inbox_shared.repositories import DocumentRepository


def main():
    db = createDbSession()

    try:
        documentRepository = DocumentRepository()

        document = documentRepository.create(
            db,
            originalFilename="test.pdf",
            storedFilename="test.pdf",
            filePath="documents/test.pdf",
            mimeType="application/pdf",
            fileSize=12345,
            uploadedBy=None,
            status=DocumentStatus.RECEIVED,
        )

        print(document.id)

    finally:
        db.close()


if __name__ == "__main__":
    main()