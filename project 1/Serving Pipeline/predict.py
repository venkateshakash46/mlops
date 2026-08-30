import mlflow
import pandas as pd

mlflow.set_tracking_uri(
    "sqlite:///D:/Arise/python/Mlops/mlflow.db"
)

MODEL_URI = "models:/xgboost/2"

model = mlflow.xgboost.load_model(MODEL_URI)


def make_prediction(data):

    input_data = {
        "pm25 µg/m³": data.pm25,
        "pm10 µg/m³": data.pm10,
        "no2 ppb": data.no2,
        "so2 ppb": data.so2,
        "o3 µg/m³": data.o3,
        "co ppb": data.co,
        "no ppb": data.no,
        "nox ppb": data.nox,
        "relativehumidity %": data.humidity,
        "temperature c": data.temperature,
        "wind_speed m/s": data.wind_speed,
        "wind_direction deg": data.wind_direction
    }

    df = pd.DataFrame([input_data])

    prediction = model.predict(df)

    return int(prediction[0])