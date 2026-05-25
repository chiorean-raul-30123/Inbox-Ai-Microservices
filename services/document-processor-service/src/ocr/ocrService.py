from pathlib import Path

import cv2
import pytesseract
from PIL import Image

from inbox_shared.exceptions import DocumentFileException, ValidationException


class OcrService:
    def extractTextFromImage(self, filePath: str) -> str:
        path = Path(filePath)

        if not path.exists():
            raise ValidationException("Image file does not exist.")

        image = cv2.imread(str(path))

        if image is None:
            raise DocumentFileException("Could not read image for OCR.")

        grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        resizedImage = cv2.resize(
            grayImage,
            None,
            fx=1.5,
            fy=1.5,
            interpolation=cv2.INTER_CUBIC,
        )

        processedImage = cv2.threshold(
            resizedImage,
            0,
            255,
            cv2.THRESH_BINARY + cv2.THRESH_OTSU,
        )[1]

        pilImage = Image.fromarray(processedImage)

        text = pytesseract.image_to_string(pilImage)

        return " ".join(text.split())