from fastapi import FastAPI, HTTPException, WebSocket, Depends
from bcrypt import hashpw, gensalt
from datetime import datetime
import websockets
from database.database import get_db
from sqlalchemy.orm import Session
from config import (
    SHARED_FOLDER,
    APP_SECRET,
    MODEL_SERVICE_URL,
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    AWS_REGION,
    BUCKET_NAME,

)
from middleware import logging_middleware
from starlette.middleware.base import BaseHTTPMiddleware
from model.main import Service
from logger import logger

TOKEN = None
LOCK = False


def upload_file(file_path, s3_key):
    s3_client.upload_file(
        file_path,  # Local file path
        BUCKET_NAME,  # S3 bucket name
        s3_key,  # S3 object key
        ExtraArgs={"ACL": "public-read"},  # Make the file publicly accessible
    )
    public_url = f"https://{BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{s3_key}"
    return public_url


s3_client = None
def hash_password():
    data = {"Key": APP_SECRET, "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    data = str(data).encode()
    TOKEN = hashpw(APP_SECRET.encode(), gensalt()).decode()
    with open(f"{SHARED_FOLDER}/secret_core.txt", "w") as file:
        file.write(TOKEN)


def verify_password(password: str):
    with open(f"{SHARED_FOLDER}/secret_core.txt", "r") as file:
        key = file.read()
    return key == password


hash_password()
app = FastAPI()
app.add_middleware(BaseHTTPMiddleware, dispatch=logging_middleware)

async def websocket_client():
    with open(f"{SHARED_FOLDER}/secret_api.txt", "r") as file:
        key = file.read()
    uri = f"ws://{MODEL_SERVICE_URL}/train/ws?password={key}"
    async with websockets.connect(uri) as websocket:
        await websocket.send("Finish")
        await websocket.close()


@app.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket, password: str, type: str, db: Session = Depends(get_db)
):
    logger.info("This is test /ws")
    global LOCK
    global s3_client
    if not verify_password(password) or LOCK:
        await websocket.close()
        return
    await websocket.accept()
    LOCK = True
    service = Service(type, db)
    receive_text = await websocket.receive_text()
    receive_text = receive_text.split("|")
    await websocket.close()
    hash_password()
    try:
        service.model_training()
        service.save_forecast(db)
        # service.save_model(upload_file)
    except Exception as e:
        LOCK = False
        await websocket_client()
        raise HTTPException(status_code=500, detail=str(e))
    LOCK = False
    await websocket_client()
