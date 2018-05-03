import pandas as pd
import numpy as np
csv_path = 'D:/DeepLearning/KDD/ANS/0430/'
output_path = 'D:/DeepLearning/KDD/ANS/0430/'
df1 = pd.read_csv(csv_path + 'PM25_bj_0430.csv')
df2 = pd.read_csv(csv_path + 'PM10_bj_0430.csv')
df3 = pd.read_csv(csv_path + 'O3_bj_0430.csv')
df_out = pd.read_csv(output_path + 'sample_submission.csv')
time1 = np.array(df1['time'])
score1 = np.array(df1['Scored Labels'])
time2 = np.array(df2['time'])
score2 = np.array(df2['Scored Labels'])
time3 = np.array(df3['time'])
score3 = np.array(df3['Scored Labels'])
low = 4285
high = 4436
out_low = 1536
# out_high = 1775


def catch_data(temp_time, tmp_score):
    tmp_time = []
    for _ in range(len(temp_time)):
        if temp_time[_][8] == ' ':
            if len(temp_time[_][9:-1] + 'M') == 10:
                tmp_time.append(' ' + temp_time[_][9:-1] + 'M')
            else:
                tmp_time.append(temp_time[_][9:-1] + 'M')
        elif temp_time[_][9] == ' ':
            if len(temp_time[_][10:-1] + 'M') == 10:
                tmp_time.append(' ' + temp_time[_][10:-1] + 'M')
            else:
                tmp_time.append(temp_time[_][10:-1] + 'M')

    tmp_time = np.array(tmp_time)
    avg_score = np.zeros(shape=(24, 1))
    count_score = np.zeros(shape=(24, 1))
    flag = False
    for _ in range(len(tmp_time)):
        if str(tmp_time[_])[-2] == "A":
            flag = True
        elif str(tmp_time[_])[-2] == "P":
            flag = False

        if str(tmp_time[_])[0] == ' ':  # ex:  1:00:00 PM
            if flag == True:
                avg_score[int(str(tmp_time[_])[1])] += tmp_score[_]
                count_score[int(str(tmp_time[_])[1])] += 1
            else:
                avg_score[int(str(tmp_time[_])[1]) + 12] += tmp_score[_]
                count_score[int(str(tmp_time[_])[1]) + 12] += 1

        else:                           # ex: 12:00:00 PM
            if flag == True:
                tmp = int(str(tmp_time[_])[0]) * 10 + int(str(tmp_time[_])[1])
                if tmp == 12:
                    avg_score[0] += tmp_score[_]
                    count_score[0] += 1
                else:
                    avg_score[tmp] += tmp_score[_]
                    count_score[tmp] += 1
            else:
                tmp = int(str(tmp_time[_])[0]) * 10 + int(str(tmp_time[_])[1])
                if tmp == 12:
                    avg_score[12] += tmp_score[_]
                    count_score[12] += 1
                else:
                    avg_score[tmp + 12] += tmp_score[_]
                    count_score[tmp + 12] += 1
    for _ in range(len(avg_score)):
        avg_score[_] /= count_score[_]
    output_score = []
    output_score.append(avg_score)
    output_score.append(avg_score)
    output_score = np.array(output_score)
    output_score = np.reshape(output_score, [-1, 1])
    return output_score


small_time1 = time1[low:high+1]
small_score1 = score1[low:high+1]
output_score1 = catch_data(small_time1, small_score1)
small_time2 = time2[low:high+1]
small_score2 = score2[low:high+1]
output_score2 = catch_data(small_time2, small_score2)
small_time3 = time3[low:high+1]
small_score3 = score3[low:high+1]
output_score3 = catch_data(small_time3, small_score3)

out_pm25 = np.array(df_out['PM2.5'])
out_pm10 = np.array(df_out['PM10'])
out_o3 = np.array(df_out['O3'])
for _ in range(48):
    try:
        out_pm25[out_low + _] = output_score1[_]
        out_pm10[out_low + _] = output_score2[_]
        out_o3[out_low + _] = output_score3[_]
    except ValueError:
        print(_, "is Nan")
        out_pm25[out_low + _] = 60
        out_pm10[out_low + _] = 60
        out_o3[out_low + _] = 60
        continue
df_out['PM2.5'] = out_pm25
df_out['PM10'] = out_pm10
df_out['O3'] = out_o3
df_out.to_csv(output_path + 'sample_submission.csv')
print('ok')
