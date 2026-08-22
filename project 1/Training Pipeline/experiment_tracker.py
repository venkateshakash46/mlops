import mlflow
from project1.Configurations import TrainConfi as tc
mlflow.set_tracking_uri(
    tc.mlflow_ui_dp_path
)

mlflow.set_experiment("Pollution Prediction")


def log_experiment(
    model,
    metrics,
    model_name
):
    with mlflow.start_run() as run:

        mlflow.log_param("model_name", model_name)

        mlflow.log_params(model.get_params())

        mlflow.log_metric("accuracy", metrics["accuracy"])
        mlflow.log_metric("precision", metrics["precision"])
        mlflow.log_metric("recall", metrics["recall"])
        mlflow.log_metric("f1_score", metrics["f1_score"])

        mlflow.log_artifact(metrics["confusion_matrix_path"])
        mlflow.log_artifact(metrics["feature_importance_path"])

        mlflow.xgboost.log_model(
            model,
            artifact_path="model"
        )

        print("## Experiment Tracking is Completed ##")

        return run.info.run_id