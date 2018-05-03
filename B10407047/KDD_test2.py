import pandas as pd
import numpy as np
from sklearn import svm

csv_path = 'D:/DeepLearning/KDD/ANS/practice/'
df = pd.read_csv(csv_path + 'AQ_get_practice.csv')
# step = df['step']
stationId = df['stationId']
utc_time = df['utc_time']
PM25 = df['PM2.5'].fillna(-1)
PM10 = df['PM10'].fillna(-1)
NO2 = df['NO2'].fillna(-1)
CO = df['CO'].fillna(-1)
O3 = df['O3'].fillna(-1)
SO2 = df['SO2'].fillna(-1)
day = 23
num_station = 35
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
    for _ in range(day*24):
        try:
            if hour_counter == hour[i]:
                new_hour.append(hour[i])
                data_PM25.append(PM25[i + start])
                data_PM10.append(PM10[i + start])
                data_NO2.append(NO2[i + start])
                data_CO.append(CO[i + start])
                data_O3.append(O3[i + start])
                data_SO2.append(SO2[i + start])
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


def avg_data(PM25, PM10, NO2, CO, O3, SO2):
    month_list = [1, 22]
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
    for _ in range(552):
        if tmp_index == _:
            index += 1
            tmp_index += month_list[index - 1] * 24
        if index == 1:
            new_month.append(3)
            new_date.append(tmp_date + 30)
        else:
            new_month.append(4)
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
        try:
            avg_PM25[_] /= count_PM25[_]
            avg_PM10[_] /= count_PM10[_]
            avg_NO2[_] /= count_NO2[_]
            avg_CO[_] /= count_CO[_]
            avg_O3[_] /= count_O3[_]
            avg_SO2[_] /= count_SO2[_]
        except:
            print('no count')
            avg_PM25[_] = 60
            avg_PM10[_] = 60
            avg_NO2[_] = 20
            avg_CO[_] = 1
            avg_O3[_] = 60
            avg_SO2[_] = 20

    for _ in range(552):
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


start = [2, 490, 978, 1466, 1954, 2442, 2930, 3418, 3906, 4394, 4882, 5370, 5858, 6346, 6834, 7322, 7810, 8298, 8786, 9274, 9762, 10250, 10738, 11226, 11714, 12202, 12690, 13178, 13666, 14154, 14642, 15130, 15618, 16106, 16594]
final_range = [489, 977, 1465, 1953, 2441, 2929, 3417, 3905, 4393, 4881, 5369, 5857, 6345, 6833, 7321, 7809, 8297, 8785, 9273, 9761, 10249, 10737, 11225, 11713, 12201, 12689, 13177, 13665, 14153, 14641, 15129, 15617, 16105, 16593, 17081]

all_month = []
all_date = []
all_hour = []
all_PM25 = []
all_PM10 = []
all_NO2 = []
all_CO = []
all_O3 = []
all_SO2 = []
for _ in range(num_station):
    year, month, date, hour = decode_data(utc_time[start[_]-2:final_range[_]-1], start=start[_]-2, length=final_range[_]-start[_]+1)
    new_hour, data_PM25, data_PM10, data_NO2, data_CO, data_O3, data_SO2 = catch_data(hour, PM25[start[_]-2:final_range[_]-1], PM10[start[_]-2:final_range[_]-1], NO2[start[_]-2:final_range[_]-1], CO[start[_]-2:final_range[_]-1], O3[start[_]-2:final_range[_]-1], SO2[start[_]-2:final_range[_]-1], start[_]-2)
    new_hour = np.array(new_hour)
    data_PM25 = np.array(data_PM25)
    data_PM10 = np.array(data_PM10)
    data_NO2 = np.array(data_NO2)
    data_CO = np.array(data_CO)
    data_O3 = np.array(data_O3)
    data_SO2 = np.array(data_SO2)

    new_month, new_date, avg_PM25, avg_PM10, avg_NO2, avg_CO, avg_O3, avg_SO2 = avg_data(data_PM25, data_PM10, data_NO2, data_CO, data_O3, data_SO2)
    all_month.append(new_month)
    all_date.append(new_date)
    all_hour.append(new_hour)
    all_PM25.append(avg_PM25)
    all_PM10.append(avg_PM10)
    all_NO2.append(avg_NO2)
    all_CO.append(avg_CO)
    all_O3.append(avg_O3)
    all_SO2.append(avg_SO2)

all_month = np.array(all_month)
all_date = np.array(all_date)
all_hour = np.array(all_hour)
all_PM25 = np.array(all_PM25)
all_PM10 = np.array(all_PM10)
all_NO2 = np.array(all_NO2)
all_CO = np.array(all_CO)
all_O3 = np.array(all_O3)
all_SO2 = np.array(all_SO2)

all_month = np.reshape(all_month, [-1])
all_date = np.reshape(all_date, [-1])
all_hour = np.reshape(all_hour, [-1])
all_PM25 = np.reshape(all_PM25, [-1])
all_PM10 = np.reshape(all_PM10, [-1])
all_NO2 = np.reshape(all_NO2, [-1])
all_CO = np.reshape(all_CO, [-1])
all_O3 = np.reshape(all_O3, [-1])
all_SO2 = np.reshape(all_SO2, [-1])
print('ok')
# new_time = new_month*100 + new_date + new_hour / 24
# norm_PM25 = np.linalg.norm(avg_PM25)    # sqrt(x1**2 + x2**2 + ... + xn**2)
# new_PM25 = avg_PM25 / norm_PM25
# norm_PM10 = np.linalg.norm(avg_PM10)    # sqrt(x1**2 + x2**2 + ... + xn**2)
# new_PM10 = avg_PM10 / norm_PM10
# norm_NO2 = np.linalg.norm(avg_NO2)      # sqrt(x1**2 + x2**2 + ... + xn**2)
# new_NO2 = avg_NO2 / norm_NO2
# norm_CO = np.linalg.norm(avg_CO)    # sqrt(x1**2 + x2**2 + ... + xn**2)
# new_CO = avg_CO / norm_CO
# norm_O3 = np.linalg.norm(avg_O3)    # sqrt(x1**2 + x2**2 + ... + xn**2)
# new_O3 = avg_O3 / norm_O3
# norm_SO2 = np.linalg.norm(avg_SO2)      # sqrt(x1**2 + x2**2 + ... + xn**2)
# new_SO2 = avg_SO2 / norm_SO2
#
# new_time = new_time.reshape(-1, 1)
# new_PM25 = new_PM25.reshape(-1)
# new_PM10 = new_PM10.reshape(-1)
# new_NO2 = new_NO2.reshape(-1)
# new_CO = new_CO.reshape(-1)
# new_O3 = new_O3.reshape(-1)
# new_SO2 = new_SO2.reshape(-1)
#
# clf_PM25 = svm.NuSVR()
# clf_PM10 = svm.NuSVR()
# clf_NO2 = svm.NuSVR()
# clf_CO = svm.NuSVR()
# clf_O3 = svm.NuSVR()
# clf_SO2 = svm.NuSVR()
# clf_PM25.fit(n)
new_stationId = []
count = 250
for _ in range(num_station):
    for _ in range(day * 24):
        new_stationId.append(stationId[count])
    count += 488
new_stationId = np.array(new_stationId)
df2 = pd.DataFrame(data={'station_id': new_stationId, 'month': all_month, 'date': all_date, 'PM2.5': all_PM25, 'PM10': all_PM10, 'NO2': all_NO2, 'CO': all_CO, 'O3': all_O3, 'SO2': all_SO2})
all_PM25 = df2['PM2.5'].fillna(60)
all_PM10 = df2['PM10'].fillna(60)
all_NO2 = df2['NO2'].fillna(20)
all_CO = df2['CO'].fillna(1)
all_O3 = df2['O3'].fillna(60)
all_SO2 = df2['SO2'].fillna(20)
df3 = pd.DataFrame(data={'station_id': new_stationId, 'month': all_month, 'date': all_date, 'PM2.5': all_PM25, 'PM10': all_PM10, 'NO2': all_NO2, 'CO': all_CO, 'O3': all_O3, 'SO2': all_SO2})
df3.to_csv('D:/DeepLearning/KDD/ANS/0503/AQ_get_0430_fillAVG.csv')
print('ok')

