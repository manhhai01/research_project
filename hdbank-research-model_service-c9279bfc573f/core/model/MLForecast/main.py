import pandas as pd
from mlforecast import MLForecast
from mlforecast.target_transforms import Differences
from utilsforecast.plotting import plot_series
# from lightgbm import LGBMRegressor
import xgboost as xgb
from sklearn.ensemble import RandomForestRegressor, AdaBoostRegressor
from sklearn.linear_model import ElasticNet
import os


class MLForecastModel:

    def __init__(self, type, data):
        if type not in ["VN10Y", "USDVND", "VNINBR"]:
            raise ValueError(
                "Invalid type. Please select one of the following: 'VN10Y', 'USDVND', 'VNINBR'"
            )
        self.type = type
        self.model_name = "MLForecast"
        self.data = data
        self.data_processing()
        self.max_horizon = (
            252 if self.type == "VN10Y" else 400 if self.type == "USDVND" else 365
        )
        self.fcst = None
        self.forecast = {}
        self.OUTPUT_PATH = "shared/output/MLForecast"

    def data_processing(self):
        df = pd.DataFrame(self.data)
        df.drop(columns=["open", "high", "low"], inplace=True)
        df.columns = ["ds", "y"]
        df["ds"] = pd.to_datetime(df["ds"]).dt.normalize()
        #df["unique_id"] = ["VN10Y"]*len(df)
        df["unique_id"] = [self.type]*len(df)
        df = df.sort_values(['unique_id', 'ds']).reset_index(drop=True)
        self.df = df

    def models_defined(self, models, horizon=None):
        self.max_horizon = horizon if horizon is not None else self.max_horizon
        self.models = [
            # LGBMRegressor(random_state=0, verbose=0),
            xgb.XGBRegressor(),
            RandomForestRegressor(random_state=0, verbose=0),
            AdaBoostRegressor(random_state=0),
            ElasticNet(random_state=0),
        ]
        self.models = [m for m, b in zip(self.models, models) if b]
        self.fcst = MLForecast(
            models=self.models,
            freq="D",
            lags=[1, 5] if self.type == "VNINBR" else [1, 5, 240],
            target_transforms=[Differences([1])],
        )

    def model_training(self):
        print(f"Training data sample:\n{self.df.head()}")
        print(f"Data types:\n{self.df.dtypes}")
        print(f"Missing values:\n{self.df.isnull().sum()}")
        print(f"Data length: {len(self.df)}")
        
        if self.df.empty:
            raise ValueError("Preprocessed data is empty!")
        
        self.fcst.fit(self.df, max_horizon=self.max_horizon)
        print("Model fitted successfully.")
        
        os.makedirs(self.OUTPUT_PATH, exist_ok=True)
        self.fcst.save(f"{self.OUTPUT_PATH}/{self.type}.pkl")
        print("Model saved.")

    def model_retrain(self, model=[True, False, False, False], horizon=None):
        print(f'Model retrain for {self.model_name}: {self.type}')
        self.data_processing()
        self.models_defined(model, horizon)
        self.model_training()
        self.model_forecasting()
        
        # self.model_plotting()
        print("Finish")
        return True

    def model_forecasting(self):
        forecast = self.fcst.predict(self.max_horizon, level=[90])
        subModels = forecast.columns[2:]
        for subModel in subModels:
            self.forecast[subModel] = pd.DataFrame({
                "Timestamp": forecast["ds"],
                "Value": forecast[subModel].values,
            })

    def model_plotting(self):
        fig = plot_series(self.df, self.forecast, engine="plotly")
        fig.update_layout(width=1500, height=600)
        fig.write_image(f"{self.OUTPUT_PATH}/{self.type}.png")

    def save_model(self, upload_func):
        upload_func(
            f"{self.OUTPUT_PATH}/{self.type}.pkl",
            f"model/{self.OUTPUT_PATH}/{self.type}.pkl",
        )
        upload_func(
            f"{self.OUTPUT_PATH}/{self.type}.png",
            f"output/image/{self.OUTPUT_PATH}/{self.type}.png",
        )
