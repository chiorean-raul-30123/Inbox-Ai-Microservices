from sqlalchemy.orm import Session

from inbox_shared.exceptions import ValidationException
from inbox_shared.repositories import SystemSettingsRepository


AI_CONFIDENCE_THRESHOLD_KEY = "aiConfidenceThreshold"


class SettingsService:
    def __init__(self, systemSettingsRepository: SystemSettingsRepository) -> None:
        self.systemSettingsRepository = systemSettingsRepository

    def getAiThreshold(self, db: Session) -> float:
        setting = self.systemSettingsRepository.getByKey(
            db,
            AI_CONFIDENCE_THRESHOLD_KEY,
        )

        if setting is None:
            setting = self.systemSettingsRepository.createSettings(
                db,
                key=AI_CONFIDENCE_THRESHOLD_KEY,
                value="0.85",
                description="Minimum confidence required for automatic routing.",
            )

        return float(setting.value)

    def updateAiThresholdValue(
        self,
        db: Session,
        *,
        threshold: float,
    ) -> float:
        if threshold < 0 or threshold > 1:
            raise ValidationException("Threshold must be between 0 and 1.")

        setting = self.systemSettingsRepository.getByKey(
            db,
            AI_CONFIDENCE_THRESHOLD_KEY,
        )

        if setting is None:
            self.systemSettingsRepository.createSettings(
                db,
                key=AI_CONFIDENCE_THRESHOLD_KEY,
                value=str(threshold),
                description="Minimum confidence required for automatic AI routing.",
            )
        else:
            self.systemSettingsRepository.updateSettings(
                db,
                settings=setting,
                value=str(threshold),
            )

        return threshold
