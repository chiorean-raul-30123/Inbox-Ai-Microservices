from pathlib import Path

from inbox_shared.enums import DocumentLabel
from inbox_shared.exceptions import ValidationException

from src.inference.predictor import DocumentClassifier
from src.ocr.ocrService import OcrService


class InferencePipeline:
    def __init__(self) -> None:
        self.classifier = DocumentClassifier()
        self.ocrService = OcrService()

    def runInference(self, filePath: str, requiresOcr: bool = False) -> dict:
        path = Path(filePath)

        if not path.exists():
            raise ValidationException("Document file does not exist.")

        if requiresOcr:
            extractedText = self.ocrService.extractTextFromImage(str(path))
            result = self.classifier.predictText(extractedText)
        else:
            result = self.classifier.predictPdf(str(path))

        rawLabel = result["label"]
        probabilities = result["probabilities"]
        confidenceScore = float(result["confidence"])

        predictedLabel = self.mapRawLabel(rawLabel)

        return {
            "predictedLabel": predictedLabel,
            "confidenceScore": confidenceScore,
            "probabilities": {
                "HR": float(probabilities["HR"]),
                "FINANCE": float(probabilities["FINANCE"]),
                "LEGAL": float(probabilities["LEGAL"]),
            },
            "modelVersion": "cnn_v1",
        }

    def mapRawLabel(self, rawLabel: str) -> DocumentLabel:
        normalized = rawLabel.strip().upper()

        if normalized == "HR":
            return DocumentLabel.HR

        if normalized == "FINANCE":
            return DocumentLabel.FINANCE

        if normalized == "LEGAL":
            return DocumentLabel.LEGAL

        raise ValidationException(f"Unsupported model label: {rawLabel}")