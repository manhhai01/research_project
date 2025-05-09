import os
import pandas as pd
from statsforecast import StatsForecast
from statsforecast.utils import ConformalIntervals
from statsforecast.models import AutoETS, AutoCES, AutoTBATS
import warnings

warnings.filterwarnings("ignore")
os.environ["NIXTLA_ID_AS_COL"] = "1"


class StatsForecastModel:
    def __init__(self, type, data, data_path=None, output_path=None):
        if type not in ["VN10Y", "USDVND", "VNINBR"]:
            raise ValueError("Invalid type. Choose from: 'VN10Y', 'USDVND', 'VNINBR'.")

        self.type = type
        self.model_name = "StatsForecast"
        self.data = data
        # self.DATA_PATH = data_path or "shared/data/TREASURY_MARKET_VARIABLES.xlsx"
        self.OUTPUT_PATH = output_path or "shared/output/StatsForecast"
        os.makedirs(self.OUTPUT_PATH, exist_ok=True)

        self.max_horizon = 252 if self.type == "VN10Y" else 400 if self.type == "USDVND" else 365
        self.level = [68]
        self.n_windows = 2
        self.models = None
        self.predictor = None
        self.pred = None
        self.df = None
        self.horizon = self.max_horizon

        self.data_processing()

    def data_processing(self):
        df = pd.DataFrame(self.data)
        df.columns = [col.lower() for col in df.columns]

        # Xác định timestamp
        if "timestamp" in df.columns or "time" in df.columns:
            df["timestamp"] = df.get("timestamp", df.get("time"))
        else:
            raise ValueError("Missing 'timestamp' or 'time' column in input data.")

        # Xác định giá trị close
        if "close" not in df.columns:
            raise ValueError("Missing 'close' column in input data.")
        
        df = df[["timestamp", "close"]].copy()
        df.columns = ["ds", "y"]  # chuẩn hóa tên cột

        # Chuyển timestamp thành datetime
        if pd.api.types.is_numeric_dtype(df["ds"]):
            df["ds"] = pd.to_datetime(df["ds"], unit="s")
        else:
            df["ds"] = pd.to_datetime(df["ds"])

        # Thêm unique_id theo type
        df["unique_id"] = self.type  # Thêm dòng này để đảm bảo unique_id luôn được set

        if self.type == "VN10Y":
            if df["y"].mean() > 1:
                df["y"] = df["y"] / 100
            df = df[df["ds"].dt.dayofweek < 5]
            df = df[df["ds"] >= "2016-01-01"]
            df["unique_id"] = "10y"
            
            # Enhanced data processing for VN10Y
            # 1. Use shorter window to preserve recent trends
            df["y"] = df["y"].rolling(window=5, min_periods=1, center=True).mean()
            
            # 2. Much stricter constraints to prevent extreme drops
            last_value = df["y"].iloc[-1]
            min_allowed = last_value * 0.995  # Only allow 0.5% deviation down
            max_allowed = last_value * 1.005  # Only allow 0.5% deviation up
            df["y"] = df["y"].clip(lower=min_allowed, upper=max_allowed)

        # Đảm bảo df không rỗng trước khi gán
        if df.empty:
            raise ValueError("Processed dataframe is empty!")
            
        self.df = df

    def models_defined(self, horizon=None, models=None, level=None):
        if horizon:
            self.horizon = horizon
        if level:
            self.level = level
    
        if not models:
            # Điều chỉnh season_length dựa trên loại dữ liệu
            if self.type == "VN10Y":
                season_length = 252  # Define season_length first
                models = [
                    AutoETS(
                        season_length=season_length,
                        model="ZZZ",  # Let model select best configuration
                        damped=True
                    ),
                    AutoTBATS(
                        season_length=season_length,
                        use_arma_errors=False,  # Disable ARMA to improve stability
                        use_trend=True,
                        use_damped_trend=True
                    )
                ]
            elif self.type == "USDVND":
                season_length = 252  # Define season_length for USDVND
                models = [
                    AutoETS(
                        season_length=season_length,
                        model="MMM",  # Multiplicative model for exchange rates
                        damped=True
                    ),
                    AutoTBATS(
                        season_length=season_length,
                        use_arma_errors=False,
                        use_trend=True,
                        use_damped_trend=True
                    )
                ]
            else:  # VNINBR
                season_length = 52  # Define season_length for VNINBR
                models = [
                    AutoTBATS(
                        season_length=season_length,
                        use_arma_errors=True,
                        use_trend=True,
                        use_damped_trend=True
                    ),
                    AutoCES(
                        season_length=season_length,
                        model="MMMN"
                    )
                ]
            self.models = models  # Assign models to self.models

    def model_training(self):
        if not self.models:
            raise RuntimeError("Model not defined. Call `.models_defined()` first.")

        horizon = self.horizon
        self.predictor = StatsForecast(
            models=self.models,
            freq="D",
            n_jobs=-1,
            fallback_model=AutoETS(
                season_length=252,
                model="AAA",  # Match with primary model
                damped=True
            )
        )

        try:
            # Tăng số cửa sổ dự đoán để cải thiệm độ chính xác
            interval = ConformalIntervals(n_windows=5, h=horizon)
            forecast_df = self.predictor.forecast(
                df=self.df,
                h=horizon,
                level=self.level,
                fitted=True,  # Bật fitted để có thêm thông tin về hiệu suất mô hình
                prediction_intervals=interval,
            )
        except Exception as e:
            print(f"[Warning] Forecast with ConformalIntervals failed: {e}")
            print("[Fallback] Re-running forecast without prediction_intervals...")
            forecast_df = self.predictor.forecast(
                df=self.df,
                h=horizon,
                level=self.level,
                fitted=True
            )

        try:
            interval = ConformalIntervals(n_windows=self.n_windows, h=horizon)
            forecast_df = self.predictor.forecast(
                df=self.df,
                h=horizon,
                level=self.level,
                fitted=False,
                prediction_intervals=interval,
            )
        except Exception as e:
            print(f"[Warning] Forecast with ConformalIntervals failed: {e}")
            print("[Fallback] Re-running forecast without prediction_intervals...")
            forecast_df = self.predictor.forecast(
                df=self.df,
                h=horizon,
                level=self.level,
                fitted=False
            )

        print("[DEBUG] Forecast output columns:", forecast_df.columns.tolist())
        print("[DEBUG] Forecast sample:\n", forecast_df.head())

        forecast_df = forecast_df[forecast_df["ds"].dt.dayofweek < 5]

        forecast_columns = [col for col in forecast_df.columns if col not in ["unique_id", "ds"]]
        if not forecast_columns:
            raise ValueError("No forecast columns found. Forecast output is invalid.")

        forecast_col = "mean" if "mean" in forecast_columns else forecast_columns[0]
        print(f"[INFO] Using forecast column: {forecast_col}")

        self.pred = forecast_df.copy()
        self.forecast = {
            self.model_name: pd.DataFrame({
                "Timestamp": forecast_df["ds"],
                "Value": forecast_df[forecast_col],
            })
        }

        return self.forecast


    def model_plotting(self):
        if self.pred is None:
            raise RuntimeError("No forecast data to plot. Run `.model_training()` first.")
        uid = self.df["unique_id"].iloc[0]
        fig = self.predictor.plot(self.df, self.pred, unique_ids=[uid], level=self.level, engine="plotly")
        fig.update_layout(width=1500, height=600)
        fig.write_image(os.path.join(self.OUTPUT_PATH, f"{self.type}.png"))
        # fig.write_html(...) nếu bạn muốn thêm HTML đầu ra

    def model_retrain(self):
        self.data_processing()
        self.models_defined()
        self.model_training()
        # self.model_plotting()
        print("Model retrain complete.")
        return True
