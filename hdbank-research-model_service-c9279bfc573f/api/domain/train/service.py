from fastapi import UploadFile
import websockets
from config import SHARED_FOLDER, CORE_SERVICE_URL, MAX_RELOAD, CRAWL_SERVICE_URL
from sqlalchemy.orm import Session
from database.model import HistoryData, HistoryDataType, Symbol
from io import BytesIO
import requests
import json
import pandas as pd

LOCK = False

class Service:
    def __init__(self):
        self.MAX_RELOAD = MAX_RELOAD

    async def websocket_client(self, type: str):
        with open(f"{SHARED_FOLDER}/secret_core.txt", "r") as file:
            key = file.read()
        uri = f"ws://{CORE_SERVICE_URL}/ws?password={key}&type={type}"
        try:
            async with websockets.connect(uri) as websocket:
                await websocket.send("Train model")
                await websocket.close()
        except Exception as e:
            raise e

    def set_LOCK(self, value: bool):
        global LOCK
        LOCK = value

    async def fetch_tv_data(self):
        tickers = [["VN10Y", "TVC"], ["VNINBR", "ECONOMICS"], ["USDVND", "FX_IDC"]]
        dfs = []
        for ticker in tickers:
            count = 0
            df = []
            while (count < self.MAX_RELOAD) & (
                len(df) == 0 if type(df) == list else df is None
            ):
                df = json.loads(
                    requests.get(
                        f"http://{CRAWL_SERVICE_URL}/tv/data",
                        params={
                            "symbol": ticker[0],
                            "exchange": ticker[1],
                            "interval": "1D",
                            "n_bars": 100000,
                        },
                    ).json()
                )
                count += 1
            if df is None:
                raise Exception(
                    {
                        "message": f"Data {ticker[0]} is failed to be fetched! Please try again later!",
                        "status": 500,
                    }
                )
            df = pd.DataFrame(df)
            df.drop(
                columns=["symbol", "volume"],
                inplace=True,
            )
            df.rename(columns={"datetime": "Timestamp"}, inplace=True)
            df.dropna(subset=["close"], inplace=True)
            df["Timestamp"] = pd.to_datetime(df["Timestamp"])
            df["Timestamp"] = df["Timestamp"].dt.normalize()
            df.sort_values(by="Timestamp", ascending=False, inplace=True)
            df.reset_index(drop=True, inplace=True)
            df = df[["Timestamp", "close", "open", "high", "low"]]
            dfs.append([ticker[0], df])
        return dfs

    async def fetch_bloomberg_data(self, file):
        contents = await file.read()
        sheets = ["10Y-VBMA", "VNIBOR1W", "UV"]
        dfs = []
        for sheet in sheets:
            df = pd.read_excel(
                BytesIO(contents),
                sheet_name=sheet,
                header=3 if sheet != "UV" else 2,
                usecols=(
                    None
                    if sheet == "VNIBOR1W"
                    else "A:B" if sheet == "10Y-VBMA" else "B:G"
                ),
            )
            if sheet != "UV":
                df.columns = ["Timestamp", "close"]
                df["open"] = pd.NA
                df["high"] = pd.NA
                df["low"] = pd.NA
            else:
                df.drop(columns=["Trade Volume"], inplace=True)
                df.columns = ["Timestamp", "close", "high", "low", "open"]
                df = df[["Timestamp", "close", "open", "high", "low"]]
            ticker = (
                "USDVND"
                if sheet == "UV"
                else "VN10Y" if sheet == "10Y-VBMA" else "VNINBR"
            )
            df["Timestamp"] = pd.to_datetime(df["Timestamp"])
            df.dropna(subset=["close"], inplace=True)
            df.reset_index(drop=True, inplace=True)
            dfs.append([ticker, df])
        return dfs

    async def train(self, file: UploadFile | None, db: Session):
        global LOCK
        if LOCK:
            return {"message": "Model is training, please wait for a moment"}
        LOCK = True
        result = []
        try:
            if file is None:
                result = await self.fetch_tv_data()
            else:
                result = await self.fetch_bloomberg_data(file)
        except Exception as e:
            LOCK = False
            raise e
        for data in result:
            symbol = db.query(Symbol).filter(Symbol.name == data[0]).first()
            if symbol is None:
                db.add(Symbol(name=data[0]))
                db.commit()
                symbol = db.query(Symbol).filter(Symbol.name == data[0]).first()
            symbolId = symbol.id
            lastest_date = (
                db.query(HistoryData)
                .order_by(HistoryData.timestamp.desc())
                .filter(
                    (
                        HistoryData.type
                        == (
                            HistoryDataType.TRADINGVIEW
                            if file is None
                            else HistoryDataType.BLOOMBERG
                        )
                    )
                    & (HistoryData.symbolId == symbolId)
                )
                .first()
            )
            if lastest_date is not None:
                data[1] = data[1][
                    data[1]["Timestamp"] > pd.to_datetime(lastest_date.timestamp).normalize()
                ]
            if len(data[1]) != 0:
                db.add_all(
                    [
                        HistoryData(
                            type=(
                                HistoryDataType.TRADINGVIEW
                                if file is None
                                else HistoryDataType.BLOOMBERG
                            ),
                            timestamp=data[1].iloc[index, 0],
                            close=float(data[1].iloc[index, 1]),
                            open=(
                                float(data[1].iloc[index, 2])
                                if not pd.isna(data[1].iloc[index, 2])
                                else None
                            ),
                            high=(
                                float(data[1].iloc[index, 3])
                                if not pd.isna(data[1].iloc[index, 3])
                                else None
                            ),
                            low=(
                                float(data[1].iloc[index, 4])
                                if not pd.isna(data[1].iloc[index, 4])
                                else None
                            ),
                            symbolId=symbolId,
                        )
                        for index in range(len(data[1]))
                    ]
                )
                try:
                    db.commit()
                except Exception as e:
                    LOCK = False
                    raise Exception(
                        {
                            "message": f"Data {data[0]} is failed to be stored! Please try again later!",
                            "status": 500,
                        }
                    )
        try:
            await self.websocket_client("tv" if file is None else "bbg")
        except Exception as e:
            print(e.args[0])
            LOCK = False
            raise Exception(
                {
                    "message": "Cannot activate training model",
                }
            )
        return {
            "message": "Data is retrieved successfully! Model is training!",
        }
