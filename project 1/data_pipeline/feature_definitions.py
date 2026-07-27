from feast import FileSource, Entity, FeatureView, Field
from feast.value_type import ValueType
from feast.types import Float64, Int32, String

Fs = FileSource(
    path            = r"D:Final_Pollution_Data.parquet", # use the final file's path
    timestamp_field = "timestamp"
)

sensors = Entity(
    name      = "pol_sens",
    join_keys = ["city_id"],  # Here we attach each of fields mention FeatureView are attached to the city_id to uniquely identify
    value_type = ValueType.STRING
)

sensors_features = FeatureView(
    name     = "sensors_features",
    entities = [sensors],
    schema   = [
        Field(name="pm25 µg/m³",         dtype=Float64),
        Field(name="pm10 µg/m³",         dtype=Float64),
        Field(name="no2 ppb",            dtype=Float64),
        Field(name="so2 ppb",            dtype=Float64),
        Field(name="o3 µg/m³",          dtype=Float64),
        Field(name="co ppb",             dtype=Float64),
        Field(name="no ppb",             dtype=Float64),
        Field(name="nox ppb",            dtype=Float64),
        Field(name="relativehumidity %", dtype=Float64),
        Field(name="temperature c",      dtype=Float64),
        Field(name="wind_speed m/s",     dtype=Float64),
        Field(name="wind_direction deg", dtype=Float64),
        Field(name="AQI_Value",          dtype=Int32),
        Field(name="AQI_Class",          dtype=Int32),
    ],
    source = Fs,
)
