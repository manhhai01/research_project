import logging
import sys
from config import ENV

logger = logging.getLogger()
formatter = logging.Formatter(
    fmt="%(asctime)s - %(levelname)s - %(message)s",
)
stream_handler = logging.StreamHandler(sys.stdout)
file_handler = logging.FileHandler("app.log")
stream_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.handlers = [stream_handler, file_handler]
# if ENV == "production":
#     logger.setLevel(logging.INFO)