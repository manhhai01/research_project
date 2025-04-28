from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from domain.train import controller as train_controller
from database.database import Base, engine
# from sqlalchemy_utils import database_exists, drop_database, create_database
# from config import DATABASE_URL
from middleware import logging_middleware
from starlette.middleware.base import BaseHTTPMiddleware

Base.metadata.create_all(engine)
app = FastAPI(title="Model Service")
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(BaseHTTPMiddleware, dispatch=logging_middleware)
app.include_router(train_controller.module, prefix="/train")

