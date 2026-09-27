import pandas as pd

from evidently import Report
from evidently.presets import DataDriftPreset


REFERENCE_FILE = r"D:\Arise\python\Mlops\project1\Data\Final_Preprocessed_Data.xlsx"
CURRENT_FILE = r"D:\Arise\python\Mlops\project1\Data\production_data.csv"


FEATURES = [
    "pm25 µg/m³"
    "pm10 µg/m³",
    "no2 ppb",
    "so2 ppb",
    "o3 µg/m³",
    "co ppb",
    "no ppb",
    "nox ppb",
    "relativehumidity %",
    "temperature c",
    "wind_speed m/s",
    "wind_direction deg"
]


def run_drift_check():

    reference_data = pd.read_excel(
        REFERENCE_FILE
    )

    current_data = pd.read_csv(
        CURRENT_FILE
    )

    reference_data = reference_data[FEATURES]
    current_data = current_data[FEATURES]

    report = Report(
        metrics=[
            DataDriftPreset()
        ]
    )

    result = report.run(
        reference_data=reference_data,
        current_data=current_data
    )

    result.save_html(
        "project1/Data/drift_report.html"
    )

    print("Data drift report generated successfully.")

if __name__ == "__main__":
    run_drift_check()