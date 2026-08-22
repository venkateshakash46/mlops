from feast import FeatureStore
import pandas as pd

def load_training_data(repoPath,filepath,start_date=None,end_date=None):
    store = FeatureStore(
        repo_path=repoPath
    )

    df = pd.read_excel(filepath)

    df["timestamp"] = pd.to_datetime(df["timestamp"])

    if start_date and end_date:
        df = df[
            (df["timestamp"] >= start_date) &
            (df["timestamp"] <= end_date)
            ]

    entity_df = pd.DataFrame({
        "city_id": ["delhi"] * len(df),
        "timestamp": df["timestamp"]
    })


    FEATURES=[
            "sensors_features:pm25 µg/m³",
            "sensors_features:pm10 µg/m³",
            "sensors_features:no2 ppb",
            "sensors_features:so2 ppb",
            "sensors_features:o3 µg/m³",
            "sensors_features:co ppb",
            "sensors_features:no ppb",
            "sensors_features:nox ppb",
            "sensors_features:relativehumidity %",
            "sensors_features:temperature c",
            "sensors_features:wind_speed m/s",
            "sensors_features:wind_direction deg",
            "sensors_features:AQI_Value",
            "sensors_features:AQI_Class",
        ]

    training_df = store.get_historical_features(
        entity_df=entity_df,
        features= FEATURES
    ).to_df()

    print(f"Training data shape: {training_df.shape}")
    training_df = training_df.dropna()

    drop_features = ['city_id', 'timestamp','AQI_Value','AQI_Class']


    X = training_df.drop(columns=drop_features,errors="ignore")
    y = training_df["AQI_Class"]

    print('## Data Loading Process is Completed ##')

    return X, y


