import mlflow
from mlflow import register_model


def register_trained_model(run_id, model_name):
    model_uri = f"runs:/{run_id}/model"

    registered_model = register_model(
        model_uri=model_uri,
        name=model_name
    )

    print(f"Model '{model_name}' registered successfully.")
    print(f"Version: {registered_model.version}")

    print('## Model Registry is Completed ##')

    return registered_model.version