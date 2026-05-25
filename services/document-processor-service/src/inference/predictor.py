import html
import json
import os
import re
from pathlib import Path

import fitz
import torch
import torch.nn.functional as F

from inbox_shared.exceptions import DocumentFileException, ModelArtifactException
from src.inference.cnnModel import TextCNN


projectRoot = Path(__file__).resolve().parents[4]

MODEL_PATH = Path(
    os.getenv("MODEL_PATH", projectRoot / "model-artifacts" / "cnn_model.pt")
)

VOCAB_PATH = Path(
    os.getenv("VOCAB_PATH", projectRoot / "model-artifacts" / "vocab.json")
)

SEQ_LEN = 900
PAD_TOKEN = "<PAD>"
UNK_TOKEN = "<UNK>"

ID_TO_LABEL = {
    0: "HR",
    1: "FINANCE",
    2: "LEGAL",
}


def tokenize(text: str):
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return text.split()


def cleanText(text: str) -> str:
    if not isinstance(text, str):
        return ""

    text = html.unescape(text)
    text = text.replace("\r", " ").replace("\n", " ")
    text = " ".join(text.split())
    return text.strip()


def extractTextFromPdf(pdfPath: Path) -> str:
    doc = fitz.open(pdfPath.as_posix())
    parts = []

    for page in doc:
        pageText = page.get_text("text")
        if pageText:
            parts.append(pageText)

    return cleanText("\n".join(parts))


def encodeText(text: str, vocab: dict, seqLen: int):
    tokens = tokenize(text)
    ids = [vocab.get(token, vocab[UNK_TOKEN]) for token in tokens]

    if len(ids) > seqLen:
        ids = ids[:seqLen]
    else:
        ids = ids + [vocab[PAD_TOKEN]] * (seqLen - len(ids))

    return ids


class DocumentClassifier:
    def __init__(self):
        self.device = torch.device("cpu")

        if not MODEL_PATH.exists():
            raise ModelArtifactException(f"Model file not found: {MODEL_PATH}")

        if not VOCAB_PATH.exists():
            raise ModelArtifactException(f"Vocab file not found: {VOCAB_PATH}")

        with open(VOCAB_PATH, "r", encoding="utf-8") as file:
            self.vocab = json.load(file)

        self.model = TextCNN(
            vocabSize=len(self.vocab),
            embedDim=128,
            numClasses=3,
        ).to(self.device)

        self.model.load_state_dict(
            torch.load(MODEL_PATH, map_location=self.device)
        )

        self.model.eval()

    def predictText(self, text: str):
        cleaned = cleanText(text)
        encoded = encodeText(cleaned, self.vocab, SEQ_LEN)

        x = torch.tensor([encoded], dtype=torch.long).to(self.device)

        with torch.no_grad():
            logits = self.model(x)
            probs = F.softmax(logits, dim=1)[0]

        predictedId = int(torch.argmax(probs).item())
        confidence = float(probs[predictedId].item())

        return {
            "label": ID_TO_LABEL[predictedId],
            "confidence": round(confidence, 4),
            "probabilities": {
                ID_TO_LABEL[index]: round(float(probs[index].item()), 4)
                for index in range(len(ID_TO_LABEL))
            },
        }

    def predictPdf(self, pdfPath: str):
        path = Path(pdfPath)

        if not path.exists():
            raise DocumentFileException(f"File not found: {pdfPath}")

        extractedText = extractTextFromPdf(path)
        result = self.predictText(extractedText)

        return {
            "file": str(path),
            "extractedTextLength": len(extractedText),
            **result,
        }