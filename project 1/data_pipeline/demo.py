
import pandas as pd

rangefile = pd.DataFrame({
    'Sensor': [
        'no ppb', 'so2 ppb', 'pm25 µg/m³', 'o3 µg/m³', 'relativehumidity %',
        'no2 ppb', 'co ppb', 'pm10 µg/m³', 'temperature c', 'wind_direction deg',
        'nox ppb', 'wind_speed m/s'
    ],
    'lower_bound': [
         0, # no ppb
         0, # so2 ppb
         0, # pm25 µg/m³
         0, # o3 µg/m³
         0, # relativehumidity %
         0, # no2 ppb
         0, # co ppb
         0, # pm10 µg/m³
       -10, # temperature c
         0, # wind_direction deg
         0, # nox ppb
         0  # wind_speed m/s
    ],
    'upper_bound': [
       500, # no ppb
       500, # so2 ppb
       999, # pm25 µg/m³
       500, # o3 µg/m³
       100, # relativehumidity %
       500, # no2 ppb
     10000, # co ppb (10 ppm, standard heavy traffic limit)
      1500, # pm10 µg/m³
        60, # temperature c (Delhi summer extreme)
       360, # wind_direction deg (0 to 360 circle)
      1000, # nox ppb
        50  # wind_speed m/s
    ]
})
c=0
df=pd.read_csv(r'D:\Arise\python\Mlops\project 1\data_pipeline\1common_sensors_long.csv')
sen_list=rangefile['Sensor'].values
for i in sen_list:
    df1= df[df['sensor_name'] == i]['value']
    lb= rangefile[rangefile['Sensor'] == i]['lower_bound'].iloc[0]
    ub= rangefile[rangefile['Sensor'] == i]['upper_bound'].iloc[0]
    valid=df1.between(lb,ub)
    invalid_values = df1[~valid]
    fal = valid[valid == False]
    print('fal',fal)

    print('dui',invalid_values)
    c=c+valid.sum()+(~valid).sum()
    print(f"{i}")
    print(f"  Total   : {len(df1)}")
    print(f"  Valid   : {valid.sum()}")
    print(f"  Invalid : {(~valid).sum()}")

print(c)



