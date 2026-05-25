import os
from dotenv import load_dotenv


load_dotenv()


class Settings:
    rabbitHost = os.getenv("RABBIT_HOST", "localhost")
    rabbitPort = int(os.getenv("RABBIT_PORT", "5672"))
    rabbitUser = os.getenv("RABBIT_USER", "inbox")
    rabbitPassword = os.getenv("RABBIT_PASSWORD", "inbox")


settings = Settings()