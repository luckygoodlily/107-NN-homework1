from sklearn.linear_model import LinearRegression
import pandas as pd
import numpy as np
import types
import matplotlib.pyplot as plt

divide_traindata = 0.7
csv_path = 'D:/DeepLearning/KDD/'
df = pd.read_csv(csv_path + 'beijing_17_18_aq.csv')
train_indices = np.random.permutation(len(df))  # generate random training-data index
# step = df['step']
stationId = df['stationId']
utc_time = df['utc_time']
PM25 = df['PM2.5'].fillna(-1)
PM10 = df['PM10'].fillna(-1)
NO2 = df['NO2'].fillna(-1)
CO = df['CO'].fillna(-1)
O3 = df['O3'].fillna(-1)
SO2 = df['SO2'].fillna(-1)

def decode_data(utc, start, length):
    year = []
    month = []
    date = []
    hour = []
    for _ in range(length):
        if str(utc[_+start])[8] == ' ':
            hour.append(int(str(utc[_+start])[9])*10 + int(str(utc[_+start])[10]))
        elif str(utc[_+start])[9] == ' ':
            hour.append(int(str(utc[_+start])[10]) * 10 + int(str(utc[_+start])[11]))
        elif str(utc[_+start])[10] == ' ':
            hour.append(int(str(utc[_+start])[11]) * 10 + int(str(utc[_+start])[12]))

        if str(utc[_+start])[6] == '/':
            month.append(int(str(utc[_+start])[5]))
            if str(utc[_+start])[8] == ' ':
                date.append(int(str(utc[_+start])[7]))
            elif str(utc[_+start])[9] == ' ':
                date.append(int(str(utc[_+start])[7])*10 + int(str(utc[_+start])[8]))
        elif str(utc[_+start])[7] == '/':
            month.append(int(str(utc[_+start])[5])*10 + int(str(utc[_+start])[6]))
            if str(utc[_+start])[9] == ' ':
                date.append(int(str(utc[_+start])[8]))
            elif str(utc[_+start])[10] == ' ':
                date.append(int(str(utc[_+start])[8])*10 + int(str(utc[_+start])[9]))

        year.append(int(str(utc[_+start])[0])*1000 + int(str(utc[_+start])[1]) * 100 + int(str(utc[_+start])[2]) * 10 + int(str(utc[_+start])[3]))
    year = np.array(year)
    month = np.array(month)
    date = np.array(date)
    hour = np.array(hour)
    return year, month, date, hour


def catch_data(hour, PM25, PM10, NO2, CO, O3, SO2, start):
    data_PM25 = []
    data_PM10 = []
    data_NO2 = []
    data_CO = []
    data_O3 = []
    data_SO2 = []
    hour_counter = 0
    new_hour = []
    i = 0
    for _ in range(9480):
        try:
            if hour_counter == hour[i + 10]:
                new_hour.append(hour[i + 10])
                data_PM25.append(PM25[i + 10 + start])
                data_PM10.append(PM10[i + 10 + start])
                data_NO2.append(NO2[i + 10 + start])
                data_CO.append(CO[i + 10 + start])
                data_O3.append(O3[i + 10 + start])
                data_SO2.append(SO2[i + 10 + start])
                hour_counter += 1
            else:
                i -= 1
                new_hour.append(hour_counter)
                data_PM25.append(-1)
                data_PM10.append(-1)
                data_NO2.append(-1)
                data_CO.append(-1)
                data_O3.append(-1)
                data_SO2.append(-1)
                hour_counter += 1
            if hour_counter == 24:
                hour_counter = 0
            i += 1
        except:
            new_hour.append(hour_counter)
            data_PM25.append(-1)
            data_PM10.append(-1)
            data_NO2.append(-1)
            data_CO.append(-1)
            data_O3.append(-1)
            data_SO2.append(-1)
            hour_counter += 1
            if hour_counter == 24:
                hour_counter = 0
    return new_hour, data_PM25, data_PM10, data_NO2, data_CO, data_O3, data_SO2


start = 2
final_range = 8888
year, month, date, hour = decode_data(utc_time[start-2:final_range-1], start=start-2, length=final_range-start+1)
new_hour, data_PM25, data_PM10, data_NO2, data_CO, data_O3, data_SO2 = catch_data(hour, PM25[start-2:final_range-1], PM10[start-2:final_range-1], NO2[start-2:final_range-1], CO[start-2:final_range-1], O3[start-2:final_range-1], SO2[start-2:final_range-1], start-2)
data_PM25 = np.array(data_PM25)
data_PM10 = np.array(data_PM10)
data_NO2 = np.array(data_NO2)
data_CO = np.array(data_CO)
data_O3 = np.array(data_O3)
data_SO2 = np.array(data_SO2)
# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#
def avg_data(PM25, PM10, NO2, CO, O3, SO2):
    # PM25 = np.array(PM25)
    # PM10 = np.array(PM10)
    # NO2 = np.array(NO2)
    # CO = np.array(CO)
    # O3 = np.array(O3)
    # SO2 = np.array(SO2)
    month_list = [30, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31, 31]
    new_month = []
    new_date = []
    index = 1
    tmp_date = 1
    tmp_index = month_list[0] * 24
    avg_PM25 = np.zeros(shape=(24, 1))
    avg_PM10 = np.zeros(shape=(24, 1))
    avg_NO2 = np.zeros(shape=(24, 1))
    avg_CO = np.zeros(shape=(24, 1))
    avg_O3 = np.zeros(shape=(24, 1))
    avg_SO2 = np.zeros(shape=(24, 1))
    count_PM25 = np.zeros(shape=(24, 1))
    count_PM10 = np.zeros(shape=(24, 1))
    count_NO2 = np.zeros(shape=(24, 1))
    count_CO = np.zeros(shape=(24, 1))
    count_O3 = np.zeros(shape=(24, 1))
    count_SO2 = np.zeros(shape=(24, 1))
    for _ in range(9480):
        if tmp_index == _:
            index += 1
            tmp_index += month_list[index - 1] * 24
        if index != 13:
            new_month.append(index)
        else:
            new_month.append(1)
        if index == 1:
            new_date.append(tmp_date + 1)
        else:
            new_date.append(tmp_date)
        tmp = _ % 24
        if tmp == 23:
            if tmp_date == month_list[index - 1]:
                tmp_date = 0
            tmp_date += 1
        if PM25[_] != -1:
            avg_PM25[tmp] += PM25[_]
            count_PM25[tmp] += 1
        if PM10[_] != -1:
            avg_PM10[tmp] += PM10[_]
            count_PM10[tmp] += 1
        if NO2[_] != -1:
            avg_NO2[tmp] += NO2[_]
            count_NO2[tmp] += 1
        if CO[_] != -1:
            avg_CO[tmp] += CO[_]
            count_CO[tmp] += 1
        if O3[_] != -1:
            avg_O3[tmp] += O3[_]
            count_O3[tmp] += 1
        if SO2[_] != -1:
            avg_SO2[tmp] += SO2[_]
            count_SO2[tmp] += 1

    for _ in range(24):
        avg_PM25[_] /= count_PM25[_]
        avg_PM10[_] /= count_PM10[_]
        avg_NO2[_] /= count_NO2[_]
        avg_CO[_] /= count_CO[_]
        avg_O3[_] /= count_O3[_]
        avg_SO2[_] /= count_SO2[_]

    for _ in range(9480):
        tmp = _ % 24
        if PM25[_] == -1:
            PM25[_] = avg_PM25[tmp]
        if PM10[_] == -1:
            PM10[_] = avg_PM10[tmp]
        if NO2[_] == -1:
            NO2[_] = avg_NO2[tmp]
        if CO[_] == -1:
            CO[_] = avg_CO[tmp]
        if O3[_] == -1:
            O3[_] = avg_O3[tmp]
        if SO2[_] == -1:
            SO2[_] = avg_SO2[tmp]
    new_month = np.array(new_month)
    new_date = np.array(new_date)
    return new_month, new_date, PM25, PM10, NO2, CO, O3, SO2


new_month, new_date, avg_PM25, avg_PM10, avg_NO2, avg_CO, avg_O3, avg_SO2 = avg_data(data_PM25, data_PM10, data_NO2, data_CO, data_O3, data_SO2)
print('ok')
df2 = pd.DataFrame(data={'SO2': avg_SO2, 'CO': avg_CO, 'NO2': avg_NO2, 'PM2.5': avg_PM25, 'O3': avg_O3, 'PM10': avg_PM10, 'month': new_month, 'date': new_date, 'hour': new_hour})
df2.to_csv(csv_path + 'tmp/aotizhongxin_aq.csv')
