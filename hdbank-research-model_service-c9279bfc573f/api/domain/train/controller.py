from fastapi import APIRouter, UploadFile, WebSocket, Depends
from .service import Service
from utils.response.BaseResponse import BaseResponse
from bcrypt import hashpw, gensalt
from datetime import datetime
from config import SHARED_FOLDER, APP_SECRET
from database.database import get_db
from sqlalchemy.orm import Session


module = APIRouter()
service = Service()
SHARED_FOLDER = str(SHARED_FOLDER)
SECRET_KEY = str(APP_SECRET)
TOKEN = None
LOCK = False


def hash_password():
    data = {"Key": SECRET_KEY, "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    data = str(data).encode()
    TOKEN = hashpw(SECRET_KEY.encode(), gensalt()).decode()
    with open(f"{SHARED_FOLDER}/secret_api.txt", "w") as file:
        file.write(TOKEN)


def verify_password(password: str):
    with open(f"{SHARED_FOLDER}/secret_api.txt", "r") as file:
        key = file.read()
    return key == password


hash_password()


@module.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, password: str):
    if not verify_password(password):
        await websocket.close()
        return
    await websocket.accept()
    receive_text = await websocket.receive_text()
    if len(receive_text) > 0:
        service.set_LOCK(False)
    await websocket.close()


@module.post("/")
async def train(file: UploadFile | None = None, db: Session = Depends(get_db)):
    try:
        response = await service.train(file, db)
    except Exception as e:
        return BaseResponse(e.args[0]["message"]).error()
    return BaseResponse(response["message"]).success()
