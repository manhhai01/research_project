from sqlalchemy.orm import Session
from model.MLForecast.main import MLForecastModel
from database.model import (
    HistoryData,
    HistoryDataType,
    Symbol,
    ForecastData,
    SymbolSubModel,
    SubModel,
    Model,
)
import pandas as pd
from typing import List
from datetime import date


class Service:
    def __init__(self, type: str, db: Session):
        symbols = ["VN10Y", "VNINBR", "USDVND"]
        self.type = type
        self.data = self.load_data(db, symbols)
        self.models = []

    def load_data(self, db: Session, symbols: List[str]):
        dfs = {}
        for symbol in symbols:
            symbolId = db.query(Symbol).filter(Symbol.name == symbol).first()
            if symbolId is None:
                continue
            else:
                symbolId = symbolId.id
            data = (
                db.query(HistoryData)
                .filter(
                    (
                        HistoryData.type
                        == (
                            HistoryDataType.TRADINGVIEW
                            if self.type == "tv"
                            else HistoryDataType.BLOOMBERG
                        )
                    )
                    & (HistoryData.symbolId == symbolId)
                )
                .all()
            )
            df = pd.DataFrame(
                {
                    "Timestamp": list(map(lambda x: x.timestamp, data)),
                    "close": list(map(lambda x: x.close, data)),
                    "high": list(map(lambda x: x.high, data)),
                    "low": list(map(lambda x: x.low, data)),
                    "open": list(map(lambda x: x.open, data)),
                }
            )
            dfs[symbol] = df
        return dfs

    def model_training(self):
        # Declare model and import data for model
        self.models = [
            MLForecastModel("VN10Y", self.data["VN10Y"]),
            MLForecastModel("VNINBR", self.data["VNINBR"]),
            MLForecastModel("USDVND", self.data["USDVND"])
        ]
        # Training model
        for model in self.models:
            model.model_retrain()

    def save_forecast(self, db: Session):
        today = date.today()
        
        # Clear today's forecast data once
        db.query(ForecastData).filter(ForecastData.date == today).delete()
        db.commit()
        
        for model in self.models:
            # Get or create the Model
            model_obj = db.query(Model).filter(Model.name == model.model_name).first()
            if model_obj is None:
                model_obj = Model(name=model.model_name)
                db.add(model_obj)
                db.flush()  # Populates model_obj.id without committing

            for sub_model_name, data in model.forecast.items():
                # Get or create the SubModel
                sub_model_obj = (
                    db.query(SubModel).filter(SubModel.name == sub_model_name).first()
                )
                if sub_model_obj is None:
                    sub_model_obj = SubModel(name=sub_model_name, modelId=model_obj.id)
                    db.add(sub_model_obj)
                    db.flush()

                # Get the Symbol ID
                symbol = db.query(Symbol).filter(Symbol.name == model.type).first()
                if symbol is None:
                    raise ValueError(f"Symbol '{model.type}' not found.")

                # Get or create the SymbolSubModel
                symbol_sub_model = db.query(SymbolSubModel).filter_by(
                    symbolId=symbol.id,
                    subModelId=sub_model_obj.id
                ).first()
                if symbol_sub_model is None:
                    symbol_sub_model = SymbolSubModel(
                        symbolId=symbol.id,
                        subModelId=sub_model_obj.id
                    )
                    db.add(symbol_sub_model)
                    db.flush()

                # Add forecast data
                forecast_entries = [
                    ForecastData(
                        timestamp=row[0],
                        value=row[1],
                        symbolSubModelId=symbol_sub_model.id,
                        date=today,
                        type="TRADINGVIEW"
                    )
                    for row in data.itertuples(index=False)
                ]
                db.add_all(forecast_entries)

        db.commit()


    def save_model(self, upload_func):
        for model in self.models:
            model.save_model(upload_func)
