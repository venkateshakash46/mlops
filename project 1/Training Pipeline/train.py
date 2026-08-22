from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier

from .data_loader import load_training_data


def train_xgboost(
    repo_path,
    data_path,
    start_date=None,
    end_date=None
):
    # Load data from Feast
    X, y = load_training_data(
        repo_path,
        data_path,
        start_date,
        end_date
    )

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    # Create model
    model = XGBClassifier(
        objective="multi:softprob",
        num_class=len(y.unique()),
        n_estimators=100,
        learning_rate=0.1,
        max_depth=6,
        random_state=42,
        eval_metric="mlogloss"
    )

    # Train model
    model.fit(X_train, y_train)
    print('## Training Process is Completed ##')

    return model, X_test, y_test