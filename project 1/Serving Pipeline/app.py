from fastapi import FastAPI
from pydantic import BaseModel, Field

from project1.Pipelines.serving_pipeline.predict import make_prediction
from project1.Pipelines.serving_pipeline.production_data import (
    save_production_data
)
from prometheus_client import generate_latest
from fastapi.responses import Response
import time

from project1.Pipelines.serving_pipeline.predict import make_prediction
from project1.Pipelines.serving_pipeline.Monitoring import (
    prediction_requests,
    prediction_errors,
    prediction_latency
)

app = FastAPI(
    title="Pollution Prediction API",
    description="API for predicting Air Quality using XGBoost model",
    version="1.0"
)


class PredictionInput(BaseModel):

    pm25: float = Field(alias="pm25 µg/m³")
    pm10: float = Field(alias="pm10 µg/m³")
    no2: float = Field(alias="no2 ppb")
    so2: float = Field(alias="so2 ppb")
    o3: float = Field(alias="o3 µg/m³")
    co: float = Field(alias="co ppb")
    no: float = Field(alias="no ppb")
    nox: float = Field(alias="nox ppb")
    humidity: float = Field(alias="relativehumidity %")
    temperature: float = Field(alias="temperature c")
    wind_speed: float = Field(alias="wind_speed m/s")
    wind_direction: float = Field(alias="wind_direction deg")


@app.get("/")
def home():

    return {
        "message": "Pollution Prediction API is running"
    }


@app.post("/predict")
def predict(data: PredictionInput):

    prediction_requests.inc()

    start_time = time.time()

    try:
        save_production_data(data) ## Here we will store the user's request's features values in the data_production.csv
        result = make_prediction(data)

        return {
            "prediction": result
        }

    except Exception:
        prediction_errors.inc()
        raise

    finally:
        prediction_latency.observe(time.time() - start_time)

@app.get("/metrics")
def metrics():

    return Response(
        content=generate_latest(),
        media_type="text/plain"
    )
