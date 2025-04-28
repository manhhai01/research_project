import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env.development")

MODEL_SERVICE_URL = os.getenv("MODEL_SERVICE_URL")
CORE_SERVICE_URL = os.getenv("CORE_SERVICE_URL")
APP_SECRET = os.getenv("APP_SECRET")
SHARED_FOLDER = os.getenv("SHARED_FOLDER")
DATABASE_URL = os.getenv("DATABASE_URL")
MAX_RELOAD = int(os.getenv("MAX_RELOAD"))
CRAWL_SERVICE_URL = os.getenv("CRAWL_SERVICE_URL")
ENV = os.getenv("ENV")