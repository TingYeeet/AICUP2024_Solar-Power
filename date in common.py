import pandas as pd

# 讀取兩個資料集
df1 = pd.read_csv('./dataset/L1_Train.csv')
df2 = pd.read_csv('./dataset/L2_Train.csv')

# 將 DateTime 欄位轉換為 datetime 格式
df1['DateTime'] = pd.to_datetime(df1['DateTime'])
df2['DateTime'] = pd.to_datetime(df2['DateTime'])

# 去掉年份和秒數，只保留 月-日 時:分
df1['DateTime_mod'] = df1['DateTime'].dt.strftime('%m-%d %H:%M')
df2['DateTime_mod'] = df2['DateTime'].dt.strftime('%m-%d %H:%M')

# 合併兩個資料集，只保留相同的日期時間
common_dates = pd.merge(df1[['DateTime_mod']], df2[['DateTime_mod']], on='DateTime_mod')

# 列出「兩者都有資料的日期」
print("兩者都有資料的日期時間 (無年份和秒數):")
print(common_dates['DateTime_mod'])
