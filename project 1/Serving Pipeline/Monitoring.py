from prometheus_client import Counter, Histogram



prediction_requests = Counter(
    "prediction_requests_total",
    "Total number of prediction requests"

# Total number of prediction requests
)



prediction_errors = Counter(
    "prediction_errors_total",
    "Total number of prediction errors"

# Total number of failed prediction requests
)



prediction_latency = Histogram(
    "prediction_latency_seconds",
    "Time taken to generate prediction"

# Prediction response time
)