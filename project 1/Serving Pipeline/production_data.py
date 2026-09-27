import os
import pandas as pd


PRODUCTION_FILE = r"D:\Arise\python\Mlops\project1\Data\production_data.csv"


def save_production_data(data):

    row = {
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

    df = pd.DataFrame([row])

    os.makedirs(
        os.path.dirname(PRODUCTION_FILE),
        exist_ok=True
    )

    if os.path.exists(PRODUCTION_FILE):
        df.to_csv(
            PRODUCTION_FILE,
            mode="a",
            header=False,
            index=False
        )
    else:
        df.to_csv(
            PRODUCTION_FILE,
            index=False
        )