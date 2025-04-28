from tvDatafeed import TvDatafeed, Interval
from config import (
    TRADING_VIEW_PASSWORD,
    TRADING_VIEW_USERNAME,
)
import pandas as pd

class Service:
    async def get_data(
        self, symbol: str, exchange: str, interval: Interval, n_bars: int
    ):
        tv = TvDatafeed()
        data = tv.get_hist(
            symbol=symbol,
            exchange=exchange,
            interval=interval,
            n_bars=n_bars,
        )
        if len(data) == 0:
            return None
        data.index = data.index.astype(str)
        data.reset_index(inplace=True)
        return data.to_json(orient="records")
