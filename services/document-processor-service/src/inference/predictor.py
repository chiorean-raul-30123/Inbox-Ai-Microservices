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

ARTIFACTS_DIR = projectRoot / "model-artifacts"

MODEL_PATH = Path(
    os.getenv("MODEL_PATH", ARTIFACTS_DIR / "cnn_model_v3.pt")
)

VOCAB_PATH = Path(
    os.getenv("VOCAB_PATH", ARTIFACTS_DIR / "vocab_v3.json")
)

CONFIG_PATH = Path(
    os.getenv("CONFIG_PATH", ARTIFACTS_DIR / "cnn_config_v3.json")
)

PAD_TOKEN = "<PAD>"
UNK_TOKEN = "<UNK>"


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
    try:
        doc = fitz.open(pdfPath.as_posix())
        parts = []

        for page in doc:
            pageText = page.get_text("text")
            if pageText:
                parts.append(pageText)

        return cleanText("\n".join(parts))

    except Exception as exception:
        raise DocumentFileException(
            f"Could not extract text from PDF: {pdfPath}"
        ) from exception


def encodeText(text: str, vocab: dict, seqLen: int):
    tokens = tokenize(text)

    if UNK_TOKEN not in vocab:
        raise ModelArtifactException("Vocabulary is missing <UNK> token.")

    if PAD_TOKEN not in vocab:
        raise ModelArtifactException("Vocabulary is missing <PAD> token.")

    ids = [vocab.get(token, vocab[UNK_TOKEN]) for token in tokens]

    if len(ids) > seqLen:
        ids = ids[:seqLen]
    else:
        ids = ids + [vocab[PAD_TOKEN]] * (seqLen - len(ids))

    return ids


class DocumentClassifier:
    def __init__(self):
        self.device = torch.device("cpu")

        self.validateArtifacts()

        self.config = self.loadConfig()
        self.vocab = self.loadVocab()

        self.seqLen = int(self.config["seq_len"])
        self.modelVersion = str(self.config.get("model_version", "unknown"))
        self.idToLabel = self.loadLabels()

        configuredVocabSize = int(self.config["vocab_size"])

        if configuredVocabSize != len(self.vocab):
            raise ModelArtifactException(
                f"Config vocab_size={configuredVocabSize}, "
                f"but loaded vocab has size={len(self.vocab)}."
            )

        self.model = TextCNN(
            vocabSize=configuredVocabSize,
            embedDim=int(self.config["embed_dim"]),
            numClasses=int(self.config["num_classes"]),
            dropout=float(self.config.get("dropout", 0.5)),
        ).to(self.device)

        try:
            self.model.load_state_dict(
                torch.load(MODEL_PATH, map_location=self.device)
            )
        except Exception as exception:
            raise ModelArtifactException(
                f"Could not load model weights from: {MODEL_PATH}"
            ) from exception

        self.model.eval()

    def validateArtifacts(self):
        missingArtifacts = [
            path
            for path in [MODEL_PATH, VOCAB_PATH, CONFIG_PATH]
            if not path.exists()
        ]

        if missingArtifacts:
            missingNames = ", ".join(str(path) for path in missingArtifacts)
            raise ModelArtifactException(
                f"Missing model artifacts: {missingNames}"
            )

    def loadConfig(self) -> dict:
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as file:
                config = json.load(file)

            requiredKeys = [
                "model_version",
                "vocab_size",
                "seq_len",
                "embed_dim",
                "num_classes",
                "labels",
            ]

            missingKeys = [key for key in requiredKeys if key not in config]

            if missingKeys:
                raise ModelArtifactException(
                    f"Model config is missing keys: {', '.join(missingKeys)}"
                )

            return config

        except ModelArtifactException:
            raise
        except Exception as exception:
            raise ModelArtifactException(
                f"Could not load model config: {CONFIG_PATH}"
            ) from exception

    def loadVocab(self) -> dict:
        try:
            with open(VOCAB_PATH, "r", encoding="utf-8") as file:
                return json.load(file)

        except Exception as exception:
            raise ModelArtifactException(
                f"Could not load vocabulary: {VOCAB_PATH}"
            ) from exception

    def loadLabels(self) -> dict[int, str]:
        labels = self.config["labels"]

        try:
            return {
                int(labelId): labelName
                for labelId, labelName in labels.items()
            }
        except Exception as exception:
            raise ModelArtifactException(
                "Invalid labels format in model config."
            ) from exception

    def predictText(self, text: str):
        cleaned = cleanText(text)

        if not cleaned:
            raise DocumentFileException(
                "No readable text was found in the document."
            )

        encoded = encodeText(cleaned, self.vocab, self.seqLen)
        x = torch.tensor([encoded], dtype=torch.long).to(self.device)

        try:
            with torch.no_grad():
                logits = self.model(x)
                probabilities = F.softmax(logits, dim=1)[0]
        except Exception as exception:
            raise DocumentFileException("Model inference failed.") from exception

        predictedId = int(torch.argmax(probabilities).item())
        confidence = float(probabilities[predictedId].item())

        predictedLabel = self.idToLabel[predictedId]

        return {
            "label": predictedLabel,
            "confidence": round(confidence, 4),
            "probabilities": {
                self.idToLabel[index]: round(float(probabilities[index].item()), 4)
                for index in range(len(self.idToLabel))
            },
            "modelVersion": self.modelVersion,
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