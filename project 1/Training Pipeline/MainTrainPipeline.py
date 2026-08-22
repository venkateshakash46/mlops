from .data_loader import load_training_data
from .train import train_xgboost
from .evaluate import evaluate_model
from .experiment_tracker import log_experiment
from .model_registry import register_trained_model

from project1.Configurations import TrainConfi as tc
print("repoPath =", tc.repoPath)
print("filepath =", tc.filepath)
X, y = load_training_data(tc.repoPath,tc.filepath)

model,X_test,y_test = train_xgboost(tc.repoPath,tc.filepath)
metrics = evaluate_model(model,X_test,y_test)
run_id = log_experiment(model,metrics,tc.model_name)
rmv = register_trained_model(run_id,tc.model_name)