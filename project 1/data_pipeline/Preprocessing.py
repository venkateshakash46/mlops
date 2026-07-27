import pandas as pd
from collections import defaultdict

class Preprocessing:
    def __init__(self, sensor_data):

        self.sensor_data = pd.read_csv(sensor_data)

    def type_converter(self):

        self.sensor_data['utc_DateTimeFrom'] = pd.to_datetime(self.sensor_data['utc_DateTimeFrom'],
                                                              utc=True).dt.tz_convert(None)
        self.sensor_data['utc_DateTimeTo'] = pd.to_datetime(self.sensor_data['utc_DateTimeTo'], utc=True).dt.tz_convert(
            None)
        self.sensor_data['local_DateTimeFrom'] = pd.to_datetime(self.sensor_data['local_DateTimeFrom'],
                                                                utc=True).dt.tz_convert(None)
        self.sensor_data['local_DateTimeTo'] = pd.to_datetime(self.sensor_data['local_DateTimeTo'],
                                                              utc=True).dt.tz_convert(None)

        self.sensor_data['sensor_id'] = pd.to_numeric(self.sensor_data['sensor_id'], errors='coerce').astype('Int64')
        self.sensor_data['location_id'] = pd.to_numeric(self.sensor_data['location_id'], errors='coerce').astype('Int64')
        self.sensor_data['value'] = pd.to_numeric(self.sensor_data['value'], errors='coerce')
        self.sensor_data['page'] = pd.to_numeric(self.sensor_data['page'], errors='coerce').astype('Int64')

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

        agg_dict = {k: v for k, v in agg_dict.items() if k in self.df_wide.columns}

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
                (30, 60, 50, 100),
                (60, 90, 100, 200),
                (90, 120, 200, 300),
                (120, 250, 300, 400),
                (250, 9999, 400, 500)
            ],
            'pm10 µg/m³': [
                (0, 50, 0, 50),
                (50, 100, 50, 100),
                (100, 250, 100, 200),
                (250, 350, 200, 300),
                (350, 430, 300, 400),
                (430, 9999, 400, 500)
            ],
            'no2 ppb': [
                (0, 21, 0, 50),
                (21, 43, 50, 100),
                (43, 96, 100, 200),
                (96, 149, 200, 300),
                (149, 213, 300, 400),
                (213, 9999, 400, 500)
            ],
            'so2 ppb': [
                (0, 15, 0, 50),
                (15, 31, 50, 100),
                (31, 145, 100, 200),
                (145, 305, 200, 300),
                (305, 611, 300, 400),
                (611, 9999, 400, 500)
            ],
            'o3 µg/m³': [
                (0, 50, 0, 50),
                (50, 100, 50, 100),
                (100, 168, 100, 200),
                (168, 208, 200, 300),
                (208, 748, 300, 400),
                (748, 9999, 400, 500)
            ],
            'co ppb': [
                (0, 873, 0, 50),
                (873, 1746, 50, 100),
                (1746, 8732, 100, 200),
                (8732, 14845, 200, 300),
                (14845, 29690, 300, 400),
                (29690, 99999, 400, 500)
            ],
            'no ppb': [
                (0, 33, 0, 50),
                (33, 65, 50, 100),
                (65, 147, 100, 200),
                (147, 228, 200, 300),
                (228, 326, 300, 400),
                (326, 9999, 400, 500)
            ],
            'nox ppb': [
                (0, 21, 0, 50),
                (21, 43, 50, 100),
                (43, 96, 100, 200),
                (96, 149, 200, 300),
                (149, 213, 300, 400),
                (213, 9999, 400, 500)
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
                    (breakpoint_df["CH"] > j)
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





