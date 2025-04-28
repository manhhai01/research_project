import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env.development")

TRADING_VIEW_USERNAME = os.getenv("TRADING_VIEW_USERNAME")
TRADING_VIEW_PASSWORD = os.getenv("TRADING_VIEW_PASSWORD")
