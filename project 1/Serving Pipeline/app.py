from fastapi import FastAPI
from pydantic import BaseModel, Field

from project1.Pipelines.serving_pipeline.predict import make_prediction


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

    result = make_prediction(data)

    return {
        "prediction": result
    }