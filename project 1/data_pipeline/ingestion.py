import requests
import pandas as pd
from datetime import datetime
from collections import defaultdict
import time
from datetime import datetime, timedelta



class Ingestion:

    def __init__(self, url,locations_ids):
        self.locations_ids = locations_ids
        self.url     = url
        self.api_key = "87845088304907dbb3dd787b22ac7c420a216c75c898eb4e459a40e446a6abcd"
        self.headers = {"X-API-Key": self.api_key}


    def station_details(self):
        d=defaultdict(list)

        for loc_id in self.locations_ids:
            #Location Details
            loc_url = f"{self.url}/locations/{loc_id}"
            response = requests.get(loc_url, headers=self.headers)
            response_status = response.raise_for_status()
            result = response.json()["results"][0]
            sen_result=result['sensors']

            #Sensor Detailse
            sen_url = f"{self.url}/locations/{loc_id}/sensors"
            sen_resp = requests.get(sen_url, headers=self.headers)
            sen_url_res = sen_resp.json()['results']


            for sen_id in range(len(sen_result)):
                d['Location_ID'].append(loc_id)
                d['Location_Name'].append(result['name'])
                d['Sensor'].append(sen_url_res[sen_id]['name'])
                d['Sensor_ID'].append(sen_url_res[sen_id]['id'])
                d['Sensor_Name'].append(sen_url_res[sen_id]['parameter']['name'])
                d['Sensor_Unit'].append(sen_url_res[sen_id]['parameter']['units'])
                d['StartFromDate'].append(sen_url_res[sen_id]['datetimeFirst']['utc'])
                d['EndToDate'].append(sen_url_res[sen_id]['datetimeLast']['utc'])


        station_report = pd.DataFrame(d)
        station_report.to_excel('NEW STATION REPORT.xlsx', index=False)
        return station_report

    def Common_Sensors(self,station_report_file):
        df = pd.read_excel(station_report_file)
        df['StartFromDate'] = pd.to_datetime(df['StartFromDate'], utc=True).dt.tz_localize(None)
        df['EndToDate'] = pd.to_datetime(df['EndToDate'], utc=True).dt.tz_localize(None)
        sensor_lists = []

        for loc in self.locations_ids:
            sensors = list(df[df['Location_ID'] == loc]['Sensor'])
            sensor_lists.append(sensors)

        common = set(sensor_lists[0]).intersection(*sensor_lists[1:])



        df2 = df[df["Sensor"].isin(list(common)) & (df['StartFromDate'].dt.year >= 2025)]
        df2.to_excel('NEW COMMON SENSOR REPORT.xlsx', index=False)
        return df2

    def Common_Start_End_Date(self,Common_Sensor_file):
        df = pd.read_excel(Common_Sensor_file)
        df['StartFromDate'] = pd.to_datetime(df['StartFromDate'], utc=True).dt.tz_localize(None)
        df['EndToDate'] = pd.to_datetime(df['EndToDate'], utc=True).dt.tz_localize(None)

        Com_sta = max(df['StartFromDate'])
        Com_end = min(df['EndToDate'])

        if Com_end < Com_sta:
            print('Invalid — EndDate is before StartDate')
            print(f'  StartDate : {Com_sta}')
            print(f'  EndDate   : {Com_end}')
            return None, None

        days = abs(Com_end - Com_sta).days

        print(f'StartDate  : {Com_sta}')
        print(f'EndDate    : {Com_end}')
        print(f'Total days : {days}')

        return Com_sta,Com_end

    def Current_EndDate_to_expected_day(self,days):
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)

        a = start_date.strftime("%Y-%m-%dT%H:%M:%SZ")
        b = end_date.strftime("%Y-%m-%dT%H:%M:%SZ")

        return a,b


    def Fetch_Sensors_Data(self,Common_Sensors_file,StartDate,EndDate,limit=100,page_limit=None):
        df = pd.read_excel(Common_Sensors_file)
        col = df[['Location_ID', 'Sensor', 'Sensor_ID']]
        v = col.values


        d = defaultdict(list)
        headers = {"X-API-Key": '87845088304907dbb3dd787b22ac7c420a216c75c898eb4e459a40e446a6abcd'}

        for loc_id, sensor_name, sensor_id in v:
            page = 1
            sleeps = 0.3


            while True:
                params = {
                    "datetime_from": StartDate,
                    "datetime_to": EndDate,
                    "limit": limit,
                    "page": page
                }

                url = f"https://api.openaq.org/v3/sensors/{sensor_id}/measurements"
                response = requests.get(url, headers=self.headers, params=params)
                result = response.json()['results']

                if not result:
                    print('No data found')
                    break

                for r in result:
                    d['page'].append(page)
                    d['location_id'].append(loc_id)
                    d['sensor_name'].append(sensor_name)
                    d['sensor_id'].append(sensor_id)
                    d['value'].append(r['value'])
                    d['utc_DateTimeFrom'].append(r['period']['datetimeFrom']['utc'])
                    d['utc_DateTimeTo'].append(r['period']['datetimeTo']['utc'])
                    d['local_DateTimeFrom'].append(r['period']['datetimeFrom']['local'])
                    d['local_DateTimeTo'].append(r['period']['datetimeTo']['local'])
                    d['Interval'].append(r['period']['interval'])

                print(f" location ID {loc_id} Sensor {sensor_id} ({sensor_name}) → page {page} → {len(result)} readings")


                if page_limit is not None and page == page_limit:
                    print(f"  Reached page limit {page_limit} — stopping")
                    break

                if len(result) < limit:
                    print(f'The size of result {len(result)} is smaller than limit')


                page += 1
                sleeps+=0.1
                time.sleep(sleeps)

        df_long = pd.DataFrame(d)
        df_long.to_csv("1common_sensors_long.csv", index=False)


l1  = [10831, 8472, 10485, 8915, 235, 8235, 6938, 50, 8239, 10486, 6931, 10484]
ing=Ingestion('https://api.openaq.org/v3',l1)

a,b=ing.Current_EndDate_to_expected_day(30)
ing.Fetch_Sensors_Data(r'D:\Arise\python\Mlops\project 1\data_pipeline\NEW COMMON SENSOR REPORT.xlsx',a,b,100,None)





