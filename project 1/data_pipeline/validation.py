from collections import defaultdict

import pandas as pd
import numpy as np

class Validation:

    def __init__(self,Common_Sensor_Report,Sensor_Data):

        self.file1 = pd.read_excel(Common_Sensor_Report)
        self.file2 = pd.read_csv(Sensor_Data)

        self.report1 = defaultdict(list)
        self.report2= defaultdict(list)


    def log_pass1(self,attribute_name, check_name , detail):
        self.report1['File'].append(1)
        self.report1['attribute_name'].append(attribute_name)
        self.report1['check_name'].append(check_name)
        self.report1['detail'].append(detail)

    def log_fail1(self,attribute_name, check_name , detail):
        self.report2['File'].append(1)
        self.report2['attribute_name'].append(attribute_name)
        self.report2['check_name'].append(check_name)
        self.report2['detail'].append(detail)

    def log_pass2(self,attribute_name, check_name , detail):
        self.report1['File'].append(2)
        self.report1['attribute_name'].append(attribute_name)
        self.report1['check_name'].append(check_name)
        self.report1['detail'].append(detail)

    def log_fail2(self,attribute_name, check_name , detail):
        self.report2['File'].append(2)
        self.report2['attribute_name'].append(attribute_name)
        self.report2['check_name'].append(check_name)
        self.report2['detail'].append(detail)




    def File1_Validation(self):
        f1 = self.file1

        # ── Location_ID ─────────────────────────────────────────────
        # null check
        null_count = f1['Location_ID'].isnull().sum()
        if null_count > 0:
            self.log_fail1('Location_ID',"null check", f"{null_count} nulls found")
        else:
            self.log_pass1('Location_ID',"null check","Passed")

        # negative check
        neg_count = (f1['Location_ID'] < 0).sum()
        if neg_count > 0:
            self.log_fail1('Location_ID',"negative check", f"{neg_count} negative values found")
        else:
            self.log_pass1('Location_ID',"negative check",'Passed')


        # integer type check #####
        non_int = f1['Location_ID'].apply(
            lambda x: not isinstance(x, (int, np.integer))
        ).sum()
        if non_int > 0:
            self.log_fail1('Location_ID',"type check", f"{non_int} non-integer values found")
        else:
            self.log_pass1('Location_ID',"type check",'Passed')

        # ── Location_Name ─────────────────────────────────────────────
        # null check
        null_count = f1['Location_Name'].isnull().sum()
        if null_count > 0:
            self.log_fail1('sensor_name',"null check", f"{null_count} nulls found")
        else:
            self.log_pass1('sensor_name',"null check",'Passed')

        # ── Sensor ─────────────────────────────────────────────
        # null check
        null_count = f1['Sensor'].isnull().sum()
        if null_count > 0:
            self.log_fail1('Sensor',"null check", f"{null_count} nulls found")
        else:
            self.log_pass1('Sensor',"null check",'Passed')

        # ── Sensor_ID ──────────────────────────────────────────
        null_count = f1['Sensor_ID'].isnull().sum()
        if null_count > 0:
            self.log_fail1('Sensor_ID', "null check", f"{null_count} nulls found")
        else:
            self.log_pass1('Sensor_ID', "null check", "Passed")

        # negative check
        neg_count = (f1['Sensor_ID'] < 0).sum()
        if neg_count > 0:
            self.log_fail1('Sensor_ID', "negative check", f"{neg_count} negative values found")
        else:
            self.log_pass1('Sensor_ID', "negative check", 'Passed')

        # duplicate check
        dup_count = f1['Sensor_ID'].duplicated().sum()
        if dup_count > 0:
            self.log_fail1('Sensor_ID', "duplicate check", f"{dup_count} duplicates found")
        else:
            self.log_pass1('Sensor_ID', "duplicate check", 'Passed')

        # integer type check
        non_int = f1['Sensor_ID'].apply(
            lambda x: not isinstance(x, (int, np.integer))
        ).sum()
        if non_int > 0:
            self.log_fail1('Sensor_ID', "type check", f"{non_int} non-integer values found")
        else:
            self.log_pass1('Sensor_ID', "type check", 'Passed')

        # ── Sensor_Name ─────────────────────────────────────────────
        # null check
        null_count = f1['Sensor_Name'].isnull().sum()
        if null_count > 0:
            self.log_fail1('Sensor_Name', "null check", f"{null_count} nulls found")
        else:
            self.log_pass1('Sensor_Name', "null check", 'Passed')

        # ── Sensor_Unit ─────────────────────────────────────────────
        # null check
        null_count = f1['Sensor_Unit'].isnull().sum()
        if null_count > 0:
            self.log_fail1('Sensor_Unit', "null check", f"{null_count} nulls found")
        else:
            self.log_pass1('Sensor_Unit', "null check", 'Passed')

        # Date Validation
        f1['StartFromDate'] = pd.to_datetime(f1['StartFromDate'], utc=True).dt.tz_localize(None)
        f1['EndToDate'] = pd.to_datetime(f1['EndToDate'], utc=True).dt.tz_localize(None)

        # ── StartFromDate ─────────────────────────────────────────────
        # null check
        null_count = f1['StartFromDate'].isnull().sum()
        if null_count > 0:
            self.log_fail1('StartFromDate', "null check", f"{null_count} nulls found")
        else:
            self.log_pass1('StartFromDate', "null check", "Passed")

        # Year check
        c = (f1['StartFromDate'].dt.year < 2025).sum()
        if c > 0:
            self.log_fail1('StartFromDate', "year check", f"{c} dates before 2025 found")
        else:
            self.log_pass1('StartFromDate', "year check", "Passed")

        # ── EndToDate ─────────────────────────────────────────────
        # Null Check
        null_count = f1['EndToDate'].isnull().sum()
        if null_count > 0:
            self.log_fail1('EndToDate', "null check", f"{null_count} nulls found")
        else:
            self.log_pass1('EndToDate', "null check", "Passed")

        # Year Check
        c = (f1['EndToDate'].dt.year < 2025).sum()
        if c > 0:
            self.log_fail1('EndToDate', "year check", f"{c} dates before 2025 found")
        else:
            self.log_pass1('EndToDate', "year check", "Passed")


    def File2_Validation(self):

        f2 = self.file2
        f2['utc_DateTimeFrom'] = pd.to_datetime(f2['utc_DateTimeFrom'])
        f2['utc_DateTimeTo'] = pd.to_datetime(f2['utc_DateTimeTo'])
        f2['local_DateTimeFrom'] = pd.to_datetime(f2['local_DateTimeFrom'])
        f2['local_DateTimeTo'] = pd.to_datetime(f2['local_DateTimeTo'])

        # ── page ─────────────────────────────────────────────
        # Null Check
        n=(f2['page'].isnull()).sum()
        if n > 0:
            self.log_fail2('page',"null check", f"{n} nulls found")
        else:
            self.log_pass2('page',"null check", 'Passed')

        # Negativity Check
        neg_count=(f2['page'] < 0).sum()
        if neg_count > 0:
            self.log_fail2('page', "negative check", f"{neg_count} negative values found")
        else:
            self.log_pass2('page', "negative check", 'Passed')

        # ── location_id ─────────────────────────────────────────────
        # null check
        null_count = f2['location_id'].isnull().sum()
        if null_count > 0:
            self.log_fail2('location_id', "null check", f"{null_count} nulls found")
        else:
            self.log_pass2('location_id', "null check", "Passed")

        # negative check
        neg_count = (f2['location_id'] < 0).sum()
        if neg_count > 0:
            self.log_fail2('location_id', "negative check", f"{neg_count} negative values found")
        else:
            self.log_pass2('location_id', "negative check", 'Passed')

        # integer type check #####
        non_int = f2['location_id'].apply(
            lambda x: not isinstance(x, (int, np.integer))
            ).sum()
        if non_int > 0:
            self.log_fail2('location_id', "type check", f"{non_int} non-integer values found")
        else:
            self.log_pass2('location_id', "type check", 'Passed')

        # ── sensor_name ─────────────────────────────────────────────
        # null check
        null_count = f2['sensor_name'].isnull().sum()
        if null_count > 0:
            self.log_fail2('sensor_name', "null check", f"{null_count} nulls found")
        else:
            self.log_pass2('sensor_name', "null check", 'Passed')

        # ── sensor_id ─────────────────────────────────────────────
        # null check
        null_count = f2['sensor_id'].isnull().sum()
        if null_count > 0:
            self.log_fail2('sensor_id', "null check", f"{null_count} nulls found")
        else:
            self.log_pass2('sensor_id', "null check", "Passed")

        # negative check
        neg_count = (f2['sensor_id'] < 0).sum()
        if neg_count > 0:
            self.log_fail2('sensor_id', "negative check", f"{neg_count} negative values found")
        else:
            self.log_pass2('sensor_id', "negative check", 'Passed')



        # integer type check #####
        non_int = f2['sensor_id'].apply(
            lambda x: not isinstance(x, (int, np.integer))
        ).sum()
        if non_int > 0:
            self.log_fail2('sensor_id', "type check", f"{non_int} non-integer values found")
        else:
            self.log_pass2('sensor_id', "type check", 'Passed')

        # ── Value ─────────────────────────────────────────────
        invalid_count=0
        # Null Check

        null_count = f2['value'].isnull().sum()
        if null_count > 0:
            self.log_fail2('value', "null check", f"{null_count} nulls found")
        else:
            self.log_pass2('value', "null check", 'Passed')

        # LB and UB Check
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
            df1 = f2[f2['sensor_name'] == i]['value']
            lb = rangefile[rangefile['Sensor'] == i]['lower_bound'].iloc[0]
            ub = rangefile[rangefile['Sensor'] == i]['upper_bound'].iloc[0]
            valid = df1.between(lb, ub)

            invalid= (~valid).sum()
            invalid_count +=invalid

            if invalid > 0:
                self.log_fail2('value', "Boundary Check", f" for {i} Total Values : {len(df1)} Valid  :{valid.sum()} Invalid : {invalid} ")
            else:
                self.log_pass2('value', "Boundary Check", f" for {i} Total Values : {len(df1)} Valid  :{valid.sum()} Invalid : {invalid} " )

        # Null and invalid value equality

        if invalid_count == null_count:
            print('Both null and Invalid Values may be same ')
        else:
            print('Both null and Invalid Values are not same ')


        # ── UTC DateFrom Validation ─────────────────────────────────────────────
        # Null Check
        null_count = f2['utc_DateTimeFrom'].isnull().sum()
        if null_count > 0:
            self.log_fail2('utc_DateTimeFrom', "null check", f"{null_count} nulls found")
        else:
            self.log_pass2('utc_DateTimeFrom', "null check", "Passed")

        # Year Check
        c = (f2['utc_DateTimeFrom'].dt.year < 2025).sum()
        if c > 0:
            self.log_fail2('utc_DateTimeFrom', "year check", f"{c} dates before 2025 found")
        else:
            self.log_pass2('utc_DateTimeFrom', "year check", "Passed")

        # ── UTC DateTo Validation ─────────────────────────────────────────────
        # Null Check
        null_count = f2['utc_DateTimeTo'].isnull().sum()
        if null_count > 0:
            self.log_fail2('utc_DateTimeTo', "null check", f"{null_count} nulls found")
        else:
            self.log_pass2('utc_DateTimeTo', "null check", "Passed")

        c = (f2['utc_DateTimeTo'].dt.year < 2025).sum()
        if c > 0:
            self.log_fail2('utc_DateTimeTo', "year check", f"{c} dates before 2025 found")
        else:
            self.log_pass2('utc_DateTimeTo', "year check", "Passed")

        # Valid Start and End Year Check
        # DateTimeTo must be after DateTimeFrom
        invalid_order = (f2['utc_DateTimeTo'] <= f2['utc_DateTimeFrom']).sum()
        if invalid_order > 0:
            self.log_fail2('utc_DateTimeTo', "utc_From_To order check",
                               f"{invalid_order} rows where DateTimeTo <= DateTimeFrom")
        else:
            self.log_pass2('utc_DateTimeTo', "utc_From_To order check", "Passed")

        # ── Local DateFrom Validation ─────────────────────────────────────────────
        # Null check
        null_count = f2['local_DateTimeFrom'].isnull().sum()
        if null_count > 0:
            self.log_fail2('local_DateTimeFrom', "null check", f"{null_count} nulls found")
        else:
            self.log_pass2('local_DateTimeFrom', "null check", "Passed")

        # Year Check
        c = (f2['local_DateTimeFrom'].dt.year < 2025).sum()
        if c > 0:
            self.log_fail2('local_DateTimeFrom', "year check", f"{c} dates before 2025 found")
        else:
            self.log_pass2('local_DateTimeFrom', "year check", "Passed")

        # ── Local DateTo Validation ─────────────────────────────────────────────
        # Null check
        null_count = f2['local_DateTimeTo'].isnull().sum()
        if null_count > 0:
            self.log_fail2('local_DateTimeTo', "null check", f"{null_count} nulls found")
        else:
            self.log_pass2('local_DateTimeTo', "null check", "Passed")

        # Year Check
        c = (f2['local_DateTimeTo'].dt.year < 2025).sum()
        if c > 0:
            self.log_fail2('local_DateTimeTo', "year check", f"{c} dates before 2025 found")
        else:
            self.log_pass2('local_DateTimeTo', "year check", "Passed")


        # ── Interval ─────────────────────────────────────────────
        # Null Check
        null_count = f2['Interval'].isnull().sum()
        if null_count > 0:
            self.log_fail2('Interval', "null check", f"{null_count} nulls found")
        else:
            self.log_pass2('Interval', "null check", "Passed")



    def Summary(self):

        print('## Error Summary ##')
        C_pas = len(self.report1['attribute_name'])
        C_Err = len(self.report2['attribute_name'])
        C_Tot = C_pas + C_Err
        print(f'The Count of Attributes : {C_Tot}')
        print(f'The Count of Pass : {C_pas}')
        print(f'The Count of Errors : {C_Err}')

        Validation_Report = pd.DataFrame({
            "File" : self.report1['File'] + self.report2['File'],
            "attribute_name" : self.report1['attribute_name'] + self.report2['attribute_name'],
            "check_name" : self.report1['check_name'] + self.report2['check_name'],
            "detail" : self.report1['detail'] + self.report2['detail'],
            "status": (['PASS'] * C_pas) + (['FAIL'] * C_Err)
        })
        Validation_Report.to_csv("Venkatesh_Validate.csv", index=False)
        print("\nSaved: validation_report.csv")




    def run(self):
        self.File1_Validation()
        self.File2_Validation()
        self.Summary()



val = Validation(r'D:\Arise\python\Mlops\project 1\data_pipeline\NEW COMMON SENSOR REPORT.xlsx',r'D:\Arise\python\Mlops\project 1\data_pipeline\1common_sensors_long.csv')
val.run()
















































