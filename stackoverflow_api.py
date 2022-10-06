# https://github.com/netology-code/py-homeworks-basic/tree/master/9.http.requests - задание 3
# Отправьте, пожалуйста, на доработку, хочется сделать это задание.
from datetime import datetime, date, time
import requests

dt_now = datetime.now()
print(dt_now)
time = int(datetime.timestamp(dt_now)) - int(datetime.timestamp(dt_now)) % 86400
print(time)
url_time = time - 86400 * 2

url = 'https://api.stackexchange.com//2.3/questions'
headers = {}
params = {'order': 'desc',
          'min': url_time,
          'sort': 'activity',
          'site': 'stackoverflow'}
r = requests.get(url=url, params=params, headers=headers)
print(r)

jsoned = r.json()
print(jsoned)
