# -*- coding: utf-8 -*-
import requests
import json
import time
import datetime
import warnings
#忽略warning輸出
warnings.filterwarnings('ignore')

headers = {'Content-type': 'application/json'}

data_json = json.dumps({"table":"testtttt"})
print data_json
# response = requests.get("https://127.0.0.1:3687/", params=payload, verify=False)
#response = requests.post("https://127.0.0.1:3687/api/IOT/2.0/myps/Sensor/Rows/test_servoD", params=params, verify=False, data=data_json, headers=headers)
response = requests.post("https://127.0.0.1:3687/test.php", verify=False, data=data_json, headers=headers)
# time.sleep(1)
# response_dic = response.json()
print(response)