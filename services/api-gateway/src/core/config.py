import os
from dotenv import load_dotenv


load_dotenv()


class Settings:
    jwtSecretKey = os.getenv("JWT_SECRET_KEY", "change_me")
    jwtAlgorithm = os.getenv("JWT_ALGORITHM", "HS256")
    accessTokenExpireMinutes = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

    uploadInputServiceUrl = os.getenv(
        "UPLOAD_INPUT_SERVICE_URL",
        "http://localhost:8101",
    )

    emailInputServiceUrl = os.getenv(
        "EMAIL_INPUT_SERVICE_URL",
        "http://localhost:8102",
    )
    
    scanInputServiceUrl = os.getenv(
    "SCAN_INPUT_SERVICE_URL",
    "http://localhost:8103",
)


settings = Settings()