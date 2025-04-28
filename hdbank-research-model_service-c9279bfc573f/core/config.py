import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env.development")

MODEL_SERVICE_URL = os.getenv("MODEL_SERVICE_URL")
CORE_SERVICE_URL = os.getenv("CORE_SERVICE_URL")
APP_SECRET = os.getenv("APP_SECRET")
SHARED_FOLDER = os.getenv("SHARED_FOLDER")
DATABASE_URL = os.getenv("DATABASE_URL")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
BUCKET_NAME = os.getenv("BUCKET_NAME")
ENV = os.getenv("ENV")
