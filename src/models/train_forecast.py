import pandas as pd
from prophet import Prophet
import os
import pickle

DATA_PATH = "data/processed"
MODEL_PATH = "models"

def load_data():
    df = pd.read_csv(f"{DATA_PATH}/transactions_clean.csv")

    # Convert date
    df["date"] = pd.to_datetime(df["date"])

    # Aggregate to daily sales
    daily_sales = df.groupby("date")["total_amount"].sum().reset_index()

    # Prophet requires columns: ds, y
    daily_sales = daily_sales.rename(columns={"date": "ds", "total_amount": "y"})

    return daily_sales


def train_forecast_model(daily_sales):
    model = Prophet(
        yearly_seasonality=True,
        weekly_seasonality=True,
        daily_seasonality=False,
        interval_width=0.95
    )

    model.fit(daily_sales)
    return model


def make_future_predictions(model, days=60):
    future = model.make_future_dataframe(periods=days)
    forecast = model.predict(future)
    return forecast


def save_model(model):
    os.makedirs(MODEL_PATH, exist_ok=True)
    with open(f"{MODEL_PATH}/prophet_forecast.pkl", "wb") as f:
        pickle.dump(model, f)
    print("✔ Model saved at models/prophet_forecast.pkl")


def save_forecast(forecast):
    forecast.to_csv("data/processed/forecast_output.csv", index=False)
    print("✔ Forecast results saved at data/processed/forecast_output.csv")


def main():
    print("Loading data...")
    daily_sales = load_data()

    print("Training Prophet model...")
    model = train_forecast_model(daily_sales)

    print("Generating future forecast...")
    forecast = make_future_predictions(model)

    print("Saving model & forecast output...")
    save_model(model)
    save_forecast(forecast)

    print("✔ Forecasting pipeline completed successfully!")


if __name__ == "__main__":
    main()
