from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello from Render FastAPI"}

@app.post("/predict")
def predict(data: dict):
    return {
        "prediction": "setosa",
        "received_data": data
    }
