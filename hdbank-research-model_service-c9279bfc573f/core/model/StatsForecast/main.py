import pandas as pd
from statsforecast import StatsForecast
from statsforecast.utils import ConformalIntervals
from statsforecast.models import AutoETS, AutoCES, AutoTBATS

# import plotly.io as pio
import os

os.environ["NIXTLA_ID_AS_COL"] = "1"


class StatsForecastModel:
    def data_processing(self):
        df = pd.read_excel(
            self.DATA_PATH, sheet_name=self.type, header=2 if self.type == "UV" else 3
        )
        if self.type == "10Y-VBMA":
            df.columns = ["ds", "y"]
            df = df.iloc[:, 0:2]
            df["unique_id"] = "10y"
            df["y"] = df["y"] / 100
            df = df[df["ds"].dt.dayofweek < 5]
            df = df[df["ds"] >= "2016-01-01"]
            df = df.dropna()
        elif self.type == "UV":
            df = df.iloc[:, 1:]
            df = df.iloc[:4674, :]
            df = df.iloc[:, :2]
            df.columns = ["ds", "y"]
            df["ds"] = pd.to_datetime(df["ds"])
            df = df.dropna()
            df["unique_id"] = "UV"
        else:
            df.columns = ["ds", "y"]
            df["ds"] = pd.to_datetime(df["ds"])
            df["unique_id"] = "1W"
            df.dropna(inplace=True)
        self.df = df

    def __init__(self, type, data_path=None, output_path=None):
        if type not in ["10Y-VBMA", "UV", "VNIBOR1W"]:
            raise ValueError(
                "Invalid type. Please select one of the following: '10Y-VBMA', 'UV', 'VNIBOR1W'"
            )
        self.type = type
        self.DATA_PATH = (
            data_path
            if data_path is not None
            else "shared/data/TREASURY_MARKET_VARIABLES.xlsx"
        )
        self.OUTPUT_PATH = (
            output_path if output_path is not None else "shared/output/MLForecast"
        )
        self.data_processing()
        self.fcst = None
        self.max_horizon = (
            252 if self.type == "10Y-VBMA" else 400 if self.type == "UV" else 365
        )

    def models_defined(self, models, horizon=None):
        season_length = 252
        self.horizon = horizon
        self.level = [68]
        self.n_windows = 2
        self.models = [
            AutoTBATS(seasonal_periods=[5, 20, 240, 480]),
            AutoCES(season_length=season_length),
            AutoETS(season_length=season_length),
        ]

    def model_training(self):
        self.predictor = StatsForecast(models=self.models, freq="D", n_jobs=-1)
        interval = ConformalIntervals(n_windows=self.n_windows, h=self.horizon)
        forecast_df = self.predictor.forecast(
            df=self.df,
            h=self.horizon,
            level=self.level,
            fitted=False,
            prediction_intervals=interval,
        )
        self.predictor.save(f"{self.OUTPUT_PATH}/{self.type}.pkl")
        self.pred = forecast_df[forecast_df["ds"].dt.dayofweek < 5]
        self.pred.to_excel(f"{self.OUTPUT_PATH}/{self.type}.xlsx")
        return self.pred.to_dict()

    def model_plotting(self):
        fig = self.predictor.plot(
            self.df, self.pred, unique_ids=["10y"], level=self.level, engine="plotly"
        )
        fig.update_layout(width=1500, height=600)
        fig.write_image(f"{self.OUTPUT_PATH}/{self.type}.png")
        # pio.write_html(
        #     fig, file=f"{self.OUTPUT_PATH}/{self.type}.html", auto_open=False
        # )
