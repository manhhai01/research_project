from fastapi import APIRouter
from .service import Service
from tvDatafeed import Interval
module = APIRouter()
service = Service()
@module.get("/data")
async def get_data(symbol: str, exchange: str, interval: Interval, n_bars: int):
    return await service.get_data(symbol, exchange, interval, n_bars)