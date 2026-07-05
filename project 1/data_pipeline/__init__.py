import pandas as pd
import numpy as np
from collections import defaultdict
import time
'''
class Validation:

    def __init__(self,file1,file2):

        self.file1 = pd.read_excel(file1)
        self.file2 = pd.read_excel(file2)



        # remove TOTAL row
        self.file1 = self.file1[
            self.file1['sensor_id'] != 'TOTAL'
            ].reset_index(drop=True)




        self.errors = []
        self.warnings = []
        self.passed = []

        self.errors1 = []
        self.warnings1 = []
        self.passed1 = []

    def log_pass(self, check):
        self.passed.append(check)
        print(f"  ✅ PASS : {check}")

    def log_fail(self, check, detail):
        self.errors.append(f"{check} — {detail}")
        print(f"  ❌ FAIL : {check} — {detail}")

    def log_warn(self, check, detail):
        self.warnings.append(f"{check} — {detail}")
        print(f"  ⚠️  WARN : {check} — {detail}")

    def log_pass1(self, check):
        self.passed1.append(check)
        print(f"  ✅ PASS : {check}")

    def log_fail1(self, check, detail):
        self.errors1.append(f"{check} — {detail}")
        print(f"  ❌ FAIL : {check} — {detail}")

    def log_warn1(self, check, detail):
        self.warnings1.append(f"{check} — {detail}")
        print(f"  ⚠️  WARN : {check} — {detail}")


    def file1_validation(self):
        f1 = self.file1

        # ── sensor_id ─────────────────────────────────────────────
        # null check
        null_count = f1['sensor_id'].isnull().sum()
        if null_count > 0:
            self.log_fail("sensor_id null check", f"{null_count} nulls found")
        else:
            self.log_pass("sensor_id null check")

        # negative check
        if (f1['sensor_id'] < 0).any():
            neg_count = (f1['sensor_id'] < 0).sum()
            self.log_fail("sensor_id negative check", f"{neg_count} negative values found")
        else:
            self.log_pass("sensor_id negative check")

        # duplicate check
        dup_count = f1['sensor_id'].duplicated().sum()
        if dup_count > 0:
            self.log_fail("sensor_id duplicate check", f"{dup_count} duplicates found")
        else:
            self.log_pass("sensor_id duplicate check")

        # integer type check
        non_int = f1['sensor_id'].apply(
            lambda x: not isinstance(x, (int, np.integer))
        ).sum()
        if non_int > 0:
            self.log_fail("sensor_id type check", f"{non_int} non-integer values found")
        else:
            self.log_pass("sensor_id type check")

        # ── sensor_name ─────────────────────────────────────────────
        # null check
        null_count = f1['sensor_name'].isnull().sum()
        if null_count > 0:
            self.log_fail("sensor_name null check", f"{null_count} nulls found")
        else:
            self.log_pass("sensor_name null check")

        # ── Location_id ─────────────────────────────────────────────
        # null check
        null_count = f1['location_id'].isnull().sum()
        if null_count > 0:
            self.log_fail("location_id null check", f"{null_count} nulls found")
        else:
            self.log_pass("location_id null check")

        # Negative check
        if (f1['location_id'] < 0).any():
            neg_count = (f1['location_id'] < 0).sum()
            self.log_fail("location_id negative check", f"{neg_count} negative values found")
        else:
            self.log_pass("location_id negative check")

        # Integer type check
        non_int = f1['location_id'].apply(
            lambda x: not isinstance(x, (int, np.integer))
        ).sum()
        if non_int > 0:
            self.log_fail("location_id type check", f"{non_int} non-integer values found")
        else:
            self.log_pass("location_id type check")

        # ── station_name ──────────────────────────────────────────
        # null check
        null_count = f1['station_name'].isnull().sum()
        if null_count > 0:
            self.log_fail("station_name null check", f"{null_count} nulls found")
        else:
            self.log_pass("station_name null check")

        # ── total_pages ──────────────────────────────────────────
        # Negative check
        if (f1['total_pages'] < 0).any():
            neg_count = (f1['total_pages'] < 0).sum()
            self.log_fail("total_pages negative check", f"{neg_count} negative values found")
        else:
            self.log_pass("total_pages negative check")

        # zero check
        zero_count = (f1['total_pages'] == 0).sum()
        if zero_count > 0:
            self.log_fail("total_pages zero check",
                          f"{zero_count} sensors with 0 pages")
        else:
            self.log_pass("total_pages zero check")

        # ── total_readings ──────────────────────────────────────────
        # null check
        null_count = f1['total_readings'].isnull().sum()
        if null_count > 0:
            self.log_fail("total_readings null check", f"{null_count} nulls found")
        else:
            self.log_pass("total_readings null check")

        # Zero Count
        zero_count = (f1['total_readings'] == 0).sum()
        if zero_count > 0:
            self.log_fail("total_readings zero check",
                          f"{zero_count} sensors with 0 readings")
        else:
            self.log_pass("total_readings zero check")

        # ── status ────────────────────────────────────────────────
        # Null check
        null_count = f1['status'].isnull().sum()
        if null_count > 0:
            self.log_fail("status null check", f"{null_count} nulls found")
        else:
            self.log_pass("status null check")

        # valid values check
        valid_statuses = {'collected', 'no data'}
        unexpected = set(f1['status'].unique()) - valid_statuses
        if unexpected:
            self.log_fail("status valid values check",
                          f"unexpected values: {unexpected}")
        else:
            self.log_pass("status valid values check")

    def file2_validation(self):
        f2 = self.file2


        rangefile = pd.DataFrame({
            'sensor_name': ['pm25', 'pm10', 'no2', 'so2', 'o3', 'co',
                            'no', 'nox', 'bc', 'relativehumidity',
                            'temperature', 'wind_speed', 'wind_direction'],
            'lower_bound': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -10, 0, 0],
            'upper_bound': [999, 999, 2.0, 1.0, 0.5, 50, 2.0, 3.0, 50, 100, 50, 50, 360]
        })

        new_df = f2.merge(rangefile, on='sensor_name', how='left')

        # ✅ check for sensor_names that didn't match the range file
        unmatched = new_df[new_df['lower_bound'].isnull()]['sensor_name'].unique()
        if len(unmatched) > 0:
            self.log_fail1("sensor_name range coverage check", f"no range defined for: {list(unmatched)}")
        else:
            self.log_pass1("sensor_name range coverage check")

        # ✅ compute in_range — this was missing
        new_df["in_range"] = new_df["Value"].between(
            new_df["lower_bound"], new_df["upper_bound"]
        )

        # ── location_id ──────────────────────────────────────────
        null_count = f2['location_id'].isnull().sum()
        if null_count > 0:
            self.log_fail1("location_id null check", f"{null_count} nulls found")
        else:
            self.log_pass1("location_id null check")

        if (f2['location_id'] < 0).any():
            neg_count = (f2['location_id'] < 0).sum()
            self.log_fail1("location_id negative check", f"{neg_count} negative values found")
        else:
            self.log_pass1("location_id negative check")

        # ── station_name ─────────────────────────────────────────
        null_count = f2['station_name'].isnull().sum()
        if null_count > 0:
            self.log_fail1("station_name null check", f"{null_count} nulls found")
        else:
            self.log_pass1("station_name null check")

        # ── sensor_id ────────────────────────────────────────────
        null_count = f2['sensor_id'].isnull().sum()
        if null_count > 0:
            self.log_fail1("sensor_id null check", f"{null_count} nulls found")
        else:
            self.log_pass1("sensor_id null check")

        if (f2['sensor_id'] < 0).any():
            neg_count = (f2['sensor_id'] < 0).sum()
            self.log_fail1("sensor_id negative check", f"{neg_count} negative values found")
        else:
            self.log_pass1("sensor_id negative check")

        non_int = f2['sensor_id'].apply(
            lambda x: not isinstance(x, (int, np.integer))
        ).sum()
        if non_int > 0:
            self.log_fail1("sensor_id type check", f"{non_int} non-integer values found")
        else:
            self.log_pass1("sensor_id type check")

        # ── sensor_name ──────────────────────────────────────────
        null_count = f2['sensor_name'].isnull().sum()
        if null_count > 0:
            self.log_fail1("sensor_name null check", f"{null_count} nulls found")
        else:
            self.log_pass1("sensor_name null check")

        # ── Value ────────────────────────────────────────────────
        null_count = f2['Value'].isnull().sum()
        if null_count > 0:
            self.log_warn1("Value null check", f"{null_count} nulls found")
        else:
            self.log_pass1("Value null check")

        if (f2['Value'] < 0).any():
            neg_count = (f2['Value'] < 0).sum()
            self.log_fail1("Value negative check", f"{neg_count} negative values found")
        else:
            self.log_pass1("Value negative check")

        # ✅ fixed range check — only counts rows with a defined range and non-null Value
        checkable = new_df[new_df['lower_bound'].notnull() & new_df['Value'].notnull()]
        false_count = (checkable["in_range"] == False).sum()

        if false_count > 0:
            self.log_fail1("Value range check", f"{false_count} values out of range")
        else:
            self.log_pass1("Value range check")

        # ── TimeInterval ─────────────────────────────────────────
        null_count = f2['TimeInterval'].isnull().sum()
        if null_count > 0:
            self.log_fail1("TimeInterval null check", f"{null_count} nulls found")
        else:
            self.log_pass1("TimeInterval null check")

        # ✅ fixed consistency check — per sensor, not globally
        inconsistent_sensors = []
        for sensor_id, group in f2.groupby('sensor_id'):
            if group['TimeInterval'].nunique() > 1:
                inconsistent_sensors.append(sensor_id)

        if inconsistent_sensors:
            self.log_fail1("TimeInterval consistency check",
                           f"sensors with mixed intervals: {inconsistent_sensors}")
        else:
            self.log_pass1("TimeInterval consistency check")

        # ── DateTimeFrom / DateTimeTo ──────────────────────────────
        null_count1 = f2['DateTimeFrom'].isnull().sum()
        if null_count1 > 0:
            self.log_fail1("DateTimeFrom null check", f"{null_count1} nulls found")
        else:
            self.log_pass1("DateTimeFrom null check")

        null_count2 = f2['DateTimeTo'].isnull().sum()
        if null_count2 > 0:
            self.log_fail1("DateTimeTo null check", f"{null_count2} nulls found")
        else:
            self.log_pass1("DateTimeTo null check")

        # ✅ fixed duplicate check — (sensor_id, DateTimeFrom) not just timestamps
        dup_count = f2[['sensor_id', 'DateTimeFrom']].duplicated().sum()
        if dup_count > 0:
            self.log_fail1("sensor_id + DateTimeFrom duplicate check", f"{dup_count} duplicates found")
        else:
            self.log_pass1("sensor_id + DateTimeFrom duplicate check")

        # valid DateTimeFrom and DateTimeTo
        f2["DateTimeFrom"] = pd.to_datetime(f2["DateTimeFrom"], utc=True)
        f2["DateTimeTo"] = pd.to_datetime(f2["DateTimeTo"], utc=True)

        invalid_count = (f2["DateTimeTo"] <= f2["DateTimeFrom"]).sum()
        if invalid_count > 0:
            self.log_fail1("DateTimeTo > DateTimeFrom check", f"{invalid_count} rows where DateTimeTo <= DateTimeFrom")
        else:
            self.log_pass1("DateTimeTo > DateTimeFrom check")

    def summary(self):
        print("\n" + "=" * 50)
        print("VALIDATION SUMMARY")
        print("=" * 50)
        print(f"  ✅ PASS : {len(self.passed)}")
        print(f"  ❌ FAIL : {len(self.errors)}")
        print(f"  ⚠️  WARN : {len(self.warnings)}")

        print("\n")
        print("=" * 50)
        print(f"  ✅ PASS : {len(self.passed1)}")
        print(f"  ❌ FAIL : {len(self.errors1)}")
        print(f"  ⚠️  WARN : {len(self.warnings1)}")


        if self.errors:
            print("\n  Failed checks:")
            for e in self.errors:
                print(f"    ❌ {e}")

        if self.warnings:
            print("\n  Warnings:")
            for w in self.warnings:
                print(f"    ⚠️  {w}")

        if not self.errors:
            print("\n  ✅ ALL CRITICAL CHECKS PASSED")
        else:
            print("\n  ❌ FIX FAILURES BEFORE PROCEEDING TO PREPROCESSING")

        # save report
        report = pd.DataFrame({
            'status': (['PASS'] * len(self.passed) +
                       ['FAIL'] * len(self.errors) +
                       ['WARN'] * len(self.warnings)),
            'detail': self.passed + self.errors + self.warnings
        })
        report.to_csv("validation_report.csv", index=False)
        print("  Saved: validation_report.csv")

    def run(self):
        self.file1_validation()
        self.file2_validation()  # ✅ was never called before
        self.summary()




val = Validation(
    file1 = "D:\Arise\python\Mlops\project 1\serving_pipeline\ingestion_summary.xlsx",
    file2 = "D:\Arise\python\Mlops\project 1\serving_pipeline\common_sensors.xlsx"
)
val.run()

'''



import requests
import pandas as pd
import time
from collections import defaultdict

df  = pd.read_excel(r'D:\Arise\python\Mlops\project 1\data_pipeline\NEW COMMON SENSOR REPORT.xlsx')
col = df[['Location_ID', 'Sensor', 'Sensor_ID']]
v   = col.values[:2]   # remove [:2] once testing is done

d = defaultdict(list)
headers = {"X-API-Key": '87845088304907dbb3dd787b22ac7c420a216c75c898eb4e459a40e446a6abcd'}

for loc_id, sensor_name, sensor_id in v:
    page = 1

    while True:
        params = {
            "datetime_from": '2025-10-10T18:15:00Z',
            "datetime_to":   '2026-06-27T13:15:00Z',
            "limit":         100,
            "page":          page
        }

        url      = f"https://api.openaq.org/v3/sensors/{sensor_id}/measurements"
        response = requests.get(url, headers=headers, params=params)
        result   = response.json()['results']

        if not result:
            break

        for r in result:
            d['location_id'].append(loc_id)
            d['sensor_name'].append(sensor_name)
            d['sensor_id'].append(sensor_id)
            d['value'].append(r['value'])
            d['utc_DateTimeFrom'].append(r['period']['datetimeFrom']['utc'])
            d['utc_DateTimeTo'].append(r['period']['datetimeTo']['utc'])
            d['local_DateTimeFrom'].append(r['period']['datetimeFrom']['local'])
            d['local_DateTimeTo'].append(r['period']['datetimeTo']['local'])
            d['Interval'].append(r['period']['interval'])

        if page == 2:
            break

        page += 1
        time.sleep(0.3)

df_long = pd.DataFrame(d)
df_long.to_csv("VENKATcommon_sensors_long.csv", index=False)











































