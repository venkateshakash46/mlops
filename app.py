from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello"}

@app.get("/predict-page", response_class=HTMLResponse)
def predict_page():

    return """
    <html>
        <body>
            <h1>Prediction Page</h1>

            <button onclick="sendRequest()">
                Predict
            </button>

            <p id="result"></p>

            <script>
                async function sendRequest() {

                    const response = await fetch('/predict', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            flower: 'iris'
                        })
                    });

                    const data = await response.json();

                    document.getElementById('result').innerText =
                        data.prediction;
                }
            </script>
        </body>
    </html>
    """

@app.post("/predict")
def predict(data: dict):

    return {
        "prediction": "venkatesh",
        "received_data": data
    }
