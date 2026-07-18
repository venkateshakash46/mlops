import pandas as pd
from collections import defaultdict

class Preprocessing:
    def __init__(self, sensor_data):

        self.sensor_data = pd.read_csv(sensor_data)

    def type_converter(self):

        self.sensor_data['sensor_id'] = pd.to_numeric(self.sensor_data['sensor_id'], errors='coerce').astype('Int64')
        self.sensor_data['location_id'] = pd.to_numeric(self.sensor_data['location_id'], errors='coerce').astype('Int64')
        self.sensor_data['value'] = pd.to_numeric(self.sensor_data['value'], errors='coerce')
        self.sensor_data['page'] = pd.to_numeric(self.sensor_data['page'], errors='coerce').astype('Int64')
        self.sensor_data['utc_DateTimeFrom'] = pd.to_datetime(self.sensor_data['utc_DateTimeFrom']).dt.tz_localize(None)
        self.sensor_data['utc_DateTimeTo'] = pd.to_datetime(self.sensor_data['utc_DateTimeTo']).dt.tz_localize(None)
        self.sensor_data['local_DateTimeFrom'] = pd.to_datetime(self.sensor_data['local_DateTimeFrom']).dt.tz_localize(None)
        self.sensor_data['local_DateTimeTo'] = pd.to_datetime(self.sensor_data['local_DateTimeTo']).dt.tz_localize(None)
        self.sensor_data['sensor_name'] = self.sensor_data['sensor_name'].astype(str)

        print("****** type_converter done *******")


    def NullFiller(self):
        self.sensor_data['value'] = self.sensor_data.groupby('sensor_id')['value'].ffill()

    def Clipper(self):
        rangefile = pd.DataFrame({
            'Sensor': [
                'no ppb', 'so2 ppb', 'pm25 µg/m³', 'o3 µg/m³', 'relativehumidity %',
                'no2 ppb', 'co ppb', 'pm10 µg/m³', 'temperature c', 'wind_direction deg',
                'nox ppb', 'wind_speed m/s'
            ],
            'lower_bound': [
                0,  # no ppb
                0,  # so2 ppb
                0,  # pm25 µg/m³
                0,  # o3 µg/m³
                0,  # relativehumidity %
                0,  # no2 ppb
                0,  # co ppb
                0,  # pm10 µg/m³
                -10,  # temperature c
                0,  # wind_direction deg
                0,  # nox ppb
                0  # wind_speed m/s
            ],
            'upper_bound': [
                500,  # no ppb
                500,  # so2 ppb
                999,  # pm25 µg/m³
                500,  # o3 µg/m³
                100,  # relativehumidity %
                500,  # no2 ppb
                10000,  # co ppb (10 ppm, standard heavy traffic limit)
                1500,  # pm10 µg/m³
                60,  # temperature c (Delhi summer extreme)
                360,  # wind_direction deg (0 to 360 circle)
                1000,  # nox ppb
                50  # wind_speed m/s
            ]
        })

        sen_list = rangefile['Sensor'].values

        for i in sen_list:
            lb = rangefile[rangefile['Sensor'] == i]['lower_bound'].iloc[0]
            ub = rangefile[rangefile['Sensor'] == i]['upper_bound'].iloc[0]

            mask = self.sensor_data["sensor_name"] == i
            self.sensor_data.loc[mask, "value"] = (
                self.sensor_data.loc[mask, "value"].clip(lower=lb, upper=ub)
            )
            print(f"  {i} → clipped to [{lb}, {ub}]")

        print('## Clipping Completed ##')



    def pivot_wide(self):
        self.df_wide = self.sensor_data.pivot_table(
            index=['location_id', 'utc_DateTimeFrom', 'utc_DateTimeTo'],
            columns='sensor_name',
            values='value',
            aggfunc='mean'
        ).reset_index()
        self.df_wide.columns.name = None
        print('## pivot wide completed ##')
        print(f"## pivot_wide's shape: {self.df_wide.shape} ##")

    def aggregate_city_level(self):

        agg_dict = {
            'pm25 µg/m³': 'mean',
            'pm10 µg/m³': 'mean',
            'no2 ppb': 'mean',
            'so2 ppb': 'mean',
            'o3 µg/m³': 'mean',
            'co ppb': 'max',
            'no ppb': 'mean',
            'nox ppb': 'mean',
            'relativehumidity %': 'mean',
            'temperature c': 'mean',
            'wind_speed m/s': 'mean',
            'wind_direction deg': 'mean'
        }

        self.df_city = (
            self.df_wide
            .groupby("utc_DateTimeFrom", as_index=False)
            .agg(agg_dict)
        ).round(2)

        self.df_city.to_excel('ultimate data.xlsx', index=False)

    def AQI_Class_Labeler(self):

        BREAKPOINTS = {
            'pm25 µg/m³': [
                (0, 30, 0, 50),
                (31, 60, 51, 100),
                (61, 90, 101, 200),
                (91, 120, 201, 300),
                (121, 250, 301, 400),
                (251, 9999, 401, 500)
            ],
            'pm10 µg/m³': [
                (0, 50, 0, 50),
                (51, 100, 51, 100),
                (101, 250, 101, 200),
                (251, 350, 201, 300),
                (351, 430, 301, 400),
                (431, 9999, 401, 500)
            ],
            'no2 ppb': [
                (0, 21, 0, 50),
                (22, 43, 51, 100),
                (44, 96, 101, 200),
                (97, 149, 201, 300),
                (150, 213, 301, 400),
                (214, 9999, 401, 500)
            ],
            'so2 ppb': [
                (0, 15, 0, 50),
                (16, 31, 51, 100),
                (32, 145, 101, 200),
                (146, 305, 201, 300),
                (306, 611, 301, 400),
                (612, 9999, 401, 500)
            ],
            'o3 µg/m³': [
                (0, 50, 0, 50),
                (51, 100, 51, 100),
                (101, 168, 101, 200),
                (169, 208, 201, 300),
                (209, 748, 301, 400),
                (749, 9999, 401, 500)
            ],
            'co ppb': [
                (0, 873, 0, 50),
                (874, 1746, 51, 100),
                (1747, 8732, 101, 200),
                (8733, 14845, 201, 300),
                (14846, 29690, 301, 400),
                (29691, 99999, 401, 500)
            ],
            'no ppb': [
                (0, 33, 0, 50),
                (34, 65, 51, 100),
                (66, 147, 101, 200),
                (148, 228, 201, 300),
                (229, 326, 301, 400),
                (327, 9999, 401, 500)
            ],
            'nox ppb': [
                (0, 21, 0, 50),
                (22, 43, 51, 100),
                (44, 96, 101, 200),
                (97, 149, 201, 300),
                (150, 213, 301, 400),
                (214, 9999, 401, 500)
            ]
        }

        rows = []

        for sensor_name, breakpoints in BREAKPOINTS.items():
            for CL, CH, IL, IH in breakpoints:
                rows.append({
                    "sensor_name": sensor_name,
                    "CL": CL,
                    "CH": CH,
                    "IL": IL,
                    "IH": IH
                })

        breakpoint_df = pd.DataFrame(rows)

        print(breakpoint_df)

        df1 = self.df_city.drop(columns=['relativehumidity %', 'temperature c', 'wind_speed m/s', 'wind_direction deg'])

        AQI = defaultdict(list)
        cols = df1.columns.values
        for i in df1.values:
            timestamp = i[0]
            sensor_values = i[1:]
            sensor_cols = cols[1:]

            sub_index = []
            for k, j in enumerate(sensor_values):
                result = breakpoint_df[
                    (breakpoint_df["sensor_name"] == sensor_cols[k]) &
                    (breakpoint_df["CL"] <= j) &
                    (breakpoint_df["CH"] >= j)
                    ]

                if result.empty:
                    sub_index.append(500)
                    continue

                cl = result['CL'].values[0]
                ch = result['CH'].values[0]
                il = result['IL'].values[0]
                ih = result['IH'].values[0]

                si = round(((ih - il) / (ch - cl)) * (j - cl) + il)
                sub_index.append(si)

            maxx = max(sub_index)
            AQI['timestamp'].append(timestamp)
            AQI['AQI_Value'].append(maxx)

        aqi_df = pd.DataFrame(AQI)

        def aqi_to_class(aqi):
            if pd.isna(aqi):
                return None
            elif aqi <= 50:
                return 0
            elif aqi <= 100:
                return 1
            elif aqi <= 200:
                return 2
            elif aqi <= 300:
                return 3
            elif aqi <= 400:
                return 4
            else:
                return 5

        aqi_df['AQI_Class'] = aqi_df['AQI_Value'].apply(aqi_to_class)

        final_df = self.df_city.merge(aqi_df, left_on='utc_DateTimeFrom', right_on='timestamp', how='left')

        final_df.to_excel('Final_Preprocessed_Data.xlsx', index=False)
        print('Your Final Preprocessed Data has been saved to Final_Preprocessed_Data.xlsx')


    def run(self):
        self.type_converter()
        self.NullFiller()
        self.Clipper()
        self.pivot_wide()
        self.aggregate_city_level()
        self.AQI_Class_Labeler()


p = Preprocessing(r'D:\Arise\python\Mlops\project 1\data_pipeline\1common_sensors_long.csv')
p.run()





