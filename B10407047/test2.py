import requests
from datetime import datetime
url = 'https://biendata.com/competition/airquality/ld/2018-03-31-0/2018-04-30-21/2k0d1d8'
# a = datetime.strptime('2014-01-01-00', '%Y-%m-%d-%H')
# params = {'city': 'bj','time': '2018-04-01-00'}
respones= requests.get(url)
with open('D:/DeepLearning/KDD/London_AQ_get_new.csv', 'w') as f:
    f.write(respones.text)
