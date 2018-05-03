import urllib.request as urllib2
import json
import re
import pandas as pd
df = pd.read_csv("D:/DeepLearning/KDD/AQ_get.csv")
print('ok')
data = {
        "Inputs": {
                "input1":
                [
                    {
                            'stationId': "aotizhongxin_aq",
                            'utc_time': "2018-04-25T14:00:00Z",
                            'PM2.5': "453",
                            'PM10': "467",
                            'NO2': "156",
                            'CO': "7.2",
                            'O3': "3",
                            'SO2': "9",
                    }
                ],
                "input2":
                [
                    {
                            'stationId': "aotizhongxin_aq",
                            'utc_time': "2018-04-26T14:00:00Z",
                            'PM2.5': "153",
                            'PM10': "417",
                            'NO2': "116",
                            'CO': "9.2",
                            'O3': "5",
                            'SO2': "19",
                    }
                ],
        },
    "GlobalParameters":  {
    }
}

body = str.encode(json.dumps(data))

url = 'https://ussouthcentral.services.azureml.net/workspaces/d168f05628f4412bb94c4918eabcc3ab/services/6b21f0098c234adca3cfb5905f80bcea/execute?api-version=2.0&format=swagger'
api_key = 'VfUAlwuRr3kyLizvMwyDjTtx+LmAP+nHwXXRxQpwaabWJ3+rt5N3G+nYEvle5KEVyPZvWjyi3v8sd/ZV2BiVTg==' # Replace this with the API key for the web service
headers = {'Content-Type': 'application/json', 'Authorization': ('Bearer ' + api_key)}

req = urllib2.Request(url, body, headers)

try:
    response = urllib2.urlopen(req)

    result = response.read()
    print(result)
except urllib2.HTTPError as error:
    print("The request failed with status code: " + str(error.code))

    # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
    print(error.info())
    print(json.loads(error.read()))