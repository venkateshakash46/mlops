from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def home():

    return """
    <html>
        <body>

            <h1>Flower Prediction</h1>

            <input type="text" id="flower" placeholder="Enter flower">

            <button onclick="predict()">
                Predict
            </button>

            <h2 id="result"></h2>

            <script>

                async function predict() {

                    let flower_name =
                        document.getElementById("flower").value;

                    const response = await fetch('/predict', {

                        method: 'POST',

                        headers: {
                            'Content-Type': 'application/json'
                        },

                        body: JSON.stringify({
                            flower: flower_name
                        })
                    });

                    const data = await response.json();

                    document.getElementById("result").innerText =
                        "Prediction: " + data.prediction;
                }

            </script>

        </body>
    </html>
    """

@app.post("/predict")
def predict(data: dict):

    flower = data["flower"]

    return {
        "prediction": flower.upper()
    }
