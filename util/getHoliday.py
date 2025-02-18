from datetime import datetime
import requests
import json
import os
from pandas import json_normalize
import configparser

environment = os.getenv('ENVIRONMENT', 'development')
if environment == 'production':
    config_path = os.path.join(os.getcwd(), 'config.ini')
    print(config_path)
else:
    config_path = os.path.join(os.getcwd(), 'config_development.ini')
config = configparser.ConfigParser()
config.read(config_path, encoding="utf-8")
key = config['HOLIDAY']['KEY']
error = config['CODE']['error']


async def API_Holiday(year=datetime.today().year):
    today = datetime.today().strftime("%Y%m%d")
    param  = {
        "_type":"json",
        "numOfRows" : 100,
        "solYear" : datetime.today().year,
        "ServiceKey" :  key
    }
    url = "http://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService/getRestDeInfo"
    try: 
        response = requests.get(url,params=param)
        if response.status_code == 200:
            json_ob = json.loads(response.text)
            holidays_data = json_ob["response"]["body"]["items"]["item"]
            filtered_data = [{'dateName': d['dateName'], 'isHoliday': d['isHoliday'], 'locdate': d['locdate']} for d in holidays_data]
        return filtered_data
    except Exception as e:
        return [error]



