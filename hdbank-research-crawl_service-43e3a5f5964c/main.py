from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from middleware import logging_middleware
from starlette.middleware.base import BaseHTTPMiddleware
from domain.tv import controller as tv_controller

app = FastAPI(title="Crawl Service")
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(BaseHTTPMiddleware, dispatch=logging_middleware)
app.include_router(tv_controller.module, prefix="/tv")
