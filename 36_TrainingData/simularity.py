import pandas as pd
from scipy.spatial.distance import euclidean
from sklearn.metrics import mean_squared_error
from sklearn.metrics.pairwise import cosine_similarity
from fastdtw import fastdtw
import numpy as np
import csv

# 開啟結果文件
result = open('./simularity.csv', mode='w', newline='')
writer = csv.writer(result)
writer.writerow(['', 'pearson_corr', 'el_dist', 'rmse', 'cosine_sim'])

for i in range(1, 18):
    df1 = pd.read_csv('L' + str(i) + '_Train.csv')

    for j in range(i+1, 18):

        # 讀取資料集
        df2 = pd.read_csv('L' + str(j) + '_Train.csv')

        # 轉換 DateTime 格式
        df1['DateTime'] = pd.to_datetime(df1['DateTime'])
        df2['DateTime'] = pd.to_datetime(df2['DateTime'])

        # 合併兩個資料集，僅保留共有的日期
        merged_df = pd.merge(df1[['DateTime', 'Power(mW)']], df2[['DateTime', 'Power(mW)']], on='DateTime', suffixes=('_L1', '_L2'))

        # 移除任何空值
        merged_df = merged_df.dropna()

        # 提取 Power 欄位
        power_L1 = merged_df['Power(mW)_L1']
        power_L2 = merged_df['Power(mW)_L2']

        # 如果樣本數量不足，跳過這一對比
        if len(power_L1) <= 1 or len(power_L2) <= 1:
            print(f"Not enough data for comparison between L{i} and L{j}, skipping...")
            continue

        # 1. Pearson Correlation
        pearson_corr = power_L1.corr(power_L2, method='pearson')

        # 2. Euclidean Distance
        euclidean_dist = euclidean(power_L1, power_L2)

        # 3. Root Mean Square Error (RMSE)
        rmse = np.sqrt(mean_squared_error(power_L1, power_L2))

        # 4. Cosine Similarity
        cosine_sim = cosine_similarity([power_L1], [power_L2])[0][0]

        # 寫入結果
        writer.writerow([f"{i} {j}", pearson_corr, euclidean_dist, rmse, cosine_sim])
        print(f"Written comparison: L{i} vs L{j}")

# 關閉結果文件
result.close()
