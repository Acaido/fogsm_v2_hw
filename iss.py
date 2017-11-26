from urllib.request import urlopen
import json
from datetime import datetime

url = 'http://api.open-notify.org/iss-now.json'
request = urlopen(url)
iss_info = request.read()
iss_info = iss_info.decode()
iss_info = json.loads(iss_info)
print('Station location is ({}, {}) by state on {}.'.format(
    iss_info['iss_position']['longitude'], iss_info['iss_position']['latitude'],
    datetime.fromtimestamp(iss_info['timestamp'])
))
