import pandas as pd
catagory = 'SO2'
df = pd.read_csv('D:/DeepLearning/KDD/dataset/beijing_17_18_aq.csv')
# print(df)
select_df = pd.DataFrame(df)
# drop_value = select_df.dropna() # 有遺失值的觀測值都刪除
# print(drop_value)
# filled_value = select_df.fillna(0) # 有遺失值的觀測值填補 0
# print(filled_value)
filled_value_column = select_df.fillna("NULL")  # 依欄位填補遺失值
counter = 0
for _ in range(len(filled_value_column[catagory])):
    if filled_value_column[catagory][_] == "NULL":
        counter += 1
print(counter)
print(len(filled_value_column[catagory]))
# print(filled_value_column)
print("ok")