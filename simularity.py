import pandas as pd
from sklearn.metrics import mean_squared_error
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import csv

# 開啟結果文件
result = open('./simularity_with_weight.csv', mode='w', newline='')
writer = csv.writer(result)
writer.writerow(['data a', 'data b', 'pearson_corr', 'cosine_sim', 'rmse', 'data_len', 'weight'])

# 儲存每個資料集的基準長度
base_lengths = {}

# 先計算每個資料集自己的基準長度
for i in range(1, 18):
    df1 = pd.read_csv('./dataset/L' + str(i) + '_Train.csv')
    
    # 轉換 DateTime 格式，並將時間精確到分鐘，忽略秒數
    df1['DateTime'] = pd.to_datetime(df1['DateTime']).dt.floor('min')
    
    # 計算自己與自己的共通長度作為基準
    base_lengths[i] = len(df1)

# 進行兩兩資料集的比較
for i in range(1, 18):
    df1 = pd.read_csv('./dataset/L' + str(i) + '_Train.csv')

    for j in range(1, 18):

        # 讀取資料集
        df2 = pd.read_csv('./dataset/L' + str(j) + '_Train.csv')

        # 轉換 DateTime 格式，並將時間精確到分鐘，忽略秒數
        df1['DateTime'] = pd.to_datetime(df1['DateTime']).dt.floor('min')
        df2['DateTime'] = pd.to_datetime(df2['DateTime']).dt.floor('min')

        # 合併兩個資料集，僅保留共有的日期（忽略秒數）
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

        # 計算基準長度
        base_length = base_lengths[i]

        # 計算共通資料長度的權重
        weight = len(power_L1) / base_length if base_length > 0 else 0

        # 1. Pearson Correlation
        pearson_corr = power_L1.corr(power_L2, method='pearson')

        # 2. Root Mean Square Error (RMSE)
        rmse = np.sqrt(mean_squared_error(power_L1, power_L2))

        # 3. Cosine Similarity
        cosine_sim = cosine_similarity([power_L1], [power_L2])[0][0]

        # 寫入結果，包括權重
        writer.writerow([str(i), str(j), pearson_corr, cosine_sim, rmse, power_L1.shape[0], weight])
        print(f"Written comparison: L{i} vs L{j}, weight: {weight}")

# 關閉結果文件
result.close()
