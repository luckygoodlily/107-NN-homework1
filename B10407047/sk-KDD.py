from sklearn import svm
from sklearn.linear_model import SGDRegressor
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

divide_traindata = 0.7
csv_path = 'D:/DeepLearning/KDD/tmp/AirQuality/'
df = pd.read_csv(csv_path + 'aotizhongxin_aq.csv')
train_indices = np.random.permutation(len(df))  # generate random training-data index
# step = df['step']
# stationId = df['stationId']
hour = df['hour']
date = df['date']
month = df['month']
PM25 = df['PM2.5']
PM10 = df['PM10']
NO2 = df['NO2']
CO = df['CO']
O3 = df['O3']
SO2 = df['SO2']
clf = svm.NuSVR(C=1000)
new_hour = np.array(hour)
new_date = np.array(date)
new_month = np.array(month)
new_time = new_month*100 + new_date + new_hour / 24
norm_pm25 = np.linalg.norm(PM25)  # sqrt(x1**2 + x2**2 + ... + xn**2)
new_PM25 = np.array(PM25) / norm_pm25
new_time = new_time.reshape(-1, 1)
avg_PM25 = new_PM25.reshape(-1)

train_lower = 0
train_upper = 9480
test_lower = 2640
test_upper = 2640+24
train_xdata_hour = new_time[train_lower:train_upper]
train_ydata_PM25 = avg_PM25[train_lower:train_upper]
clf.fit(train_xdata_hour, train_ydata_PM25)
plt.figure(1)
y = clf.predict(new_time[test_lower:test_upper])
predict = y * norm_pm25
label = avg_PM25[test_lower:test_upper] * norm_pm25
plt.figure(1)
plt.plot(new_time[test_lower:test_upper], predict)

cost = 0
for _ in range(len(y)):
    cost += ((predict[_] - label[_])**2)
cost /= len(y)
cost = np.sqrt(cost)
print("cost= %f" % cost)
plt.plot(new_time[test_lower:test_upper], label)
plt.show()
print('ok')
