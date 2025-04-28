import pandas as pd
from neuralprophet import NeuralProphet

# import plotly.io as pio
from neuralprophet import NeuralProphet, set_log_level, set_random_seed
import pickle

set_random_seed(42)
set_log_level("ERROR")


class NeuralProphetModel:
    def data_processing(self):
        df = pd.read_excel(
            self.DATA_PATH, sheet_name=self.type, header=2 if self.type == "UV" else 3
        )
        if self.type == "10Y-VBMA":
            df = df.rename(columns={"Timestamp": "ds", "Mid Yield Close": "y"})
            df = df.dropna()
            df["y"] = df["y"] / 100
            df = df.iloc[::-1]
        elif self.type == "UV":
            df = df.iloc[:, 1:]
            df = df.iloc[:4674, :]
            df = df.iloc[:, :2]
            df.columns = ["ds", "y"]
            df["ds"] = pd.to_datetime(df["ds"])
            df = df.iloc[::-1]
            df = df.fillna(method="bfill")

        else:
            pass
        self.df = df

    def __init__(self, type, data_path=None, output_path=None):
        if type not in ["10Y-VBMA", "UV"]:
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
        self.model = None
        self.max_horizon = 280 if self.type == "10Y-VBMA" else 252

    def model_defined(self, horizon=None):
        if horizon is not None:
            self.max_horizon = horizon
        self.model = NeuralProphet(
            growth="discontinuous",
            n_changepoints=500 if self.type == "10Y-VBMA" else 320,
            changepoints_range=0.95 if self.type == "10Y-VBMA" else 0.8,
            trend_reg=0.001 if self.type == "10Y-VBMA" else 0.005,
            trend_reg_threshold=False,
            trend_global_local="global",
            yearly_seasonality=True,
            weekly_seasonality=False,
            daily_seasonality=False,
            seasonality_mode=(
                "additive" if self.type == "10Y-VBMA" else "multiplicative"
            ),
            seasonality_reg=10,
            season_global_local="global",
            n_lags=0 if self.type == "10Y-VBMA" else 252 * 2,
            ar_reg=0.001 if self.type == "10Y-VBMA" else 10,
            ar_layers=[256, 128] if self.type == "10Y-VBMA" else [256, 128, 128, 256],
            learning_rate=0.001 if self.type == "10Y-VBMA" else 0.003,
            epochs=100,
            batch_size=32,
            newer_samples_weight=1 if self.type == "10Y-VBMA" else 1.5,
            newer_samples_start=0,
            loss_func="MSE",
            drop_missing=True,
            accelerator="auto",
            n_forecasts=None if self.type == "10Y-VBMA" else 252,
        )

    def model_training(self):
        self.model.fit(self.df)
        with open(f"{self.OUTPUT_PATH}/{self.type}.pkl", "wb") as f:
            pickle.dump(self.model, f)

    def model_retrain(self):
        self.data_processing()
        self.model_training()
        self.model_forecasting()
        self.model_plotting()
        print("Finish")
        return True

    def model_forecasting(self):
        future = self.model.make_future_dataframe(
            self.df,
            periods=self.max_horizon,
            n_historic_predictions=True if self.type == "10Y-VBMA" else False,
        )
        self.pred = self.model.predict(future)
        self.pred.to_excel(f"{self.OUTPUT_PATH}/{self.type}.xlsx")
        return self.pred.to_dict()

    def model_plotting(self):
        self.model.set_plotting_backend("plotly")
        fig = self.model.plot(self.pred, figsize=(15, 12))
        fig.update_layout(width=1500, height=600)
        fig.write_image(f"{self.OUTPUT_PATH}/{self.type}.png")
        # pio.write_html(
        #     fig, file=f"{self.OUTPUT_PATH}/{self.type}.html", auto_open=False
        # )
