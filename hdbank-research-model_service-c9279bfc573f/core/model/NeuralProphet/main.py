import pandas as pd
from neuralprophet import NeuralProphet, set_log_level, set_random_seed
import os
import torch
import gc
import numpy as np  # Add this import

set_random_seed(42)
set_log_level("ERROR")


class NeuralProphetModel:
    def __init__(self, type, data, output_path=None):
        if type not in ["VN10Y", "USDVND", "VNINBR"]:
            raise ValueError("Invalid type. Please select one of: 'VN10Y', 'USDVND', 'VNINBR'")
        
        self.type = type
        self.model_name = "NeuralProphet"
        self.data = data
        self.OUTPUT_PATH = output_path or "shared/output/NeuralProphet"
        os.makedirs(self.OUTPUT_PATH, exist_ok=True)

        self.horizon_lookup = {"VN10Y": 365, "USDVND": 365, "VNINBR": 365}  # Thay đổi horizon cho tất cả loại
        self.max_horizon = self.horizon_lookup[type]

        self.df = None
        self.model = None
        self.pred = None
        self.forecast = {}
        self.data_processing()

    def data_processing(self):
        df = pd.DataFrame(self.data)
        df.columns = [col.lower() for col in df.columns]
    
        if "timestamp" not in df.columns or "close" not in df.columns:
            raise ValueError("Input data must include 'timestamp' and 'close' columns.")
    
        # Parse timestamp
        if pd.api.types.is_numeric_dtype(df["timestamp"]):
            df["ds"] = pd.to_datetime(df["timestamp"], unit='s')
        else:
            df["ds"] = pd.to_datetime(df["timestamp"])
    
        df["y"] = df["close"].astype(float)
        
        # Xử lý giá trị NaN và infinite
        df = df.replace([np.inf, -np.inf], np.nan)
        
        # Tạo index theo ngày và reindex để điền các ngày thiếu
        df = df[["ds", "y"]].dropna()
        df.set_index('ds', inplace=True)
        df = df.reindex(pd.date_range(start=df.index.min(), end=df.index.max(), freq='D'))
        df.reset_index(inplace=True)
        df.columns = ['ds', 'y']
        
        # Interpolate missing values với phương pháp cubic spline
        df['y'] = df['y'].interpolate(method='cubic').ffill().bfill()
        
        # Sort và loại bỏ duplicates
        df = df.sort_values("ds", ascending=True)
        df = df.drop_duplicates(subset=['ds'])
        
        # Scale VN10Y nếu cần
        if self.type == "VN10Y":
            df["y"] = df["y"] / 100
        
        self.df = df

    def model_defined(self):
        horizon = self.max_horizon
    
        config_map = {
            "VN10Y": {
                "n_changepoints": 30,        # Tăng số điểm thay đổi
                "trend_reg": 0.3,           # Giảm regularization
                "ar_layers": [16, 8],       # Tăng độ phức tạp của mạng
                "seasonality_mode": "multiplicative",
                "n_lags": 14,              # Tăng số lags
                "ar_reg": 0.1,             # Giảm AR regularization
                "learning_rate": 0.001,     # Điều chỉnh learning rate
                "epochs": 30               # Tăng epochs
            },
            "USDVND": {
                "n_changepoints": 40,
                "trend_reg": 0.15,
                "ar_layers": [16],
                "seasonality_mode": "multiplicative",
                "n_lags": 14,
                "ar_reg": 0.6,
                "learning_rate": 0.001,
                "epochs": 25
            },
            "VNINBR": {
                "n_changepoints": 35,
                "trend_reg": 0.15,
                "ar_layers": [16],
                "seasonality_mode": "multiplicative",
                "n_lags": 10,
                "ar_reg": 0.5,
                "learning_rate": 0.001,
                "epochs": 30
            }
        }

        model_args = config_map[self.type]

        self.model = NeuralProphet(
            yearly_seasonality=True,       # Bật yearly seasonality cho dự đoán dài hạn
            weekly_seasonality=True,       
            daily_seasonality=False,
            n_forecasts=365,              # Đặt n_forecasts bằng số ngày cần dự đoán
            batch_size=64,                # Tăng batch size
            loss_func="Huber",           
            normalize="standardize",      
            impute_missing=True,
            drop_missing=True,
            impute_linear=7,             # Tăng số ngày interpolate
            growth="linear",             
            seasonality_reg=0.1,
            accelerator="auto",
            **model_args
        )

    def model_training(self):
        """Train the NeuralProphet model with the processed data."""
        print(f"[{self.model_name}] Training model for {self.type}...")
        try:
            metrics = self.model.fit(self.df, freq="D")
            print(f"[{self.model_name}] Training complete.")
            return metrics
        except Exception as e:
            print(f"Error during training: {str(e)}")
            raise

    def model_forecasting(self):
        print(f"[{self.model_name}] Forecasting {self.max_horizon} days ahead...")
    
        try:
            # Tạo future dataframe
            future = self.model.make_future_dataframe(
                df=self.df,
                periods=self.max_horizon,
                n_historic_predictions=False
            )
            
            # Thực hiện dự đoán
            self.pred = self.model.predict(future)
            
            if self.pred.empty:
                raise RuntimeError("Forecast prediction is empty.")
    
            # Xử lý kết quả dự đoán
            forecast_cols = [col for col in self.pred.columns if col.startswith("yhat")]
            if not forecast_cols:
                raise RuntimeError("No forecast columns found in prediction output.")
    
            # Lấy giá trị dự đoán và xử lý
            values = self.pred[forecast_cols[0]]  # Lấy cột yhat đầu tiên
            
            # Chuyển đổi giá trị về thang gốc nếu cần
            if self.type == "VN10Y":
                values = values * 100
    
            # Tạo DataFrame kết quả
            df_forecast = pd.DataFrame({
                "Timestamp": self.pred["ds"],
                "Value": values
            }).dropna()
    
            # Lọc chỉ lấy các giá trị dự đoán tương lai
            last_historical_date = self.df["ds"].max()
            df_forecast = df_forecast[df_forecast["Timestamp"] > last_historical_date]
    
            self.forecast[self.model_name] = df_forecast
    
        except Exception as e:
            print(f"Error during forecasting: {str(e)}")
            raise


    def model_plotting(self):
        self.model.set_plotting_backend("plotly")
        try:
            fig = self.model.plot(self.pred, figsize=(15, 12))
            fig.update_layout(width=1500, height=600)
            fig.write_image(f"{self.OUTPUT_PATH}/{self.type}.png")
        except Exception as e:
            print(f"Plotting failed: {e}")

    def model_retrain(self):
        print(f"[{self.model_name}] Retraining model for {self.type}...")
        self.data_processing()
        self.model_defined()
        self.model_training()
        self.model_forecasting()
        print(f"[{self.model_name}] Retrain complete.")
        return True
