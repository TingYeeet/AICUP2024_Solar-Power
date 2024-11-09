import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from datetime import datetime, timedelta

# 讀取資料
agg_df = pd.read_csv('L1_aggregated_fill1.csv', parse_dates=['DateTime'])

# 篩選出一月份的資料，並新增日期欄位
agg_df['Date'] = agg_df['DateTime'].dt.date
january_data = agg_df[agg_df['DateTime'].dt.month == 2]

# 計算每日發電量的統計特徵：最大值、最小值、平均值和標準差
daily_stats = january_data.groupby('Date')['Power(mW)'].agg(['max', 'min', 'mean', 'std']).fillna(0)

# 使用 KMeans 進行分群，K=6
kmeans = KMeans(n_clusters=6, random_state=42)
clusters = kmeans.fit_predict(daily_stats)

# 建立分群資料夾
base_dir = 'Feb k=6'
os.makedirs(base_dir, exist_ok=True)
for i in range(6):
    os.makedirs(os.path.join(base_dir, f'k={i}'), exist_ok=True)

# 繪製每一日的發電量散布圖並儲存至對應的資料夾
for idx, (date, row) in enumerate(daily_stats.iterrows()):
    cluster_label = clusters[idx]
    date_data = january_data[january_data['Date'] == date]

    # 建立7:00到17:00的每十分鐘時間點
    time_intervals = pd.date_range(start=datetime(date.year, date.month, date.day, 7),
                                   end=datetime(date.year, date.month, date.day, 17), freq='10T')

    # 找出有資料的時間點並記錄缺失的時間點
    available_times = date_data['DateTime']
    missing_times = [time for time in time_intervals if time not in available_times.tolist()]

    # 繪製該日發電量的散布圖
    plt.figure(figsize=(10, 6))
    plt.scatter(date_data['DateTime'], date_data['Power(mW)'], color='blue', s=10, label='Available Data')
    
    # 標記缺失的十分鐘區間
    if missing_times:
        plt.scatter(missing_times, [0] * len(missing_times), color='red', s=10, label='Missing Data (Power=0)')

    plt.title(f'Date: {date} - Cluster: {cluster_label}')
    plt.xlabel('Time')
    plt.ylabel('Power (mW)')
    plt.xlim(datetime(date.year, date.month, date.day, 7), datetime(date.year, date.month, date.day, 17))
    plt.ylim(0, 2500)
    plt.legend()
    plt.grid(True)
    
    # 儲存圖表到對應的分群資料夾
    plt_path = os.path.join(base_dir, f'k={cluster_label}', f'{date}.png')
    plt.savefig(plt_path)
    plt.close()

print("分群完成並已儲存各日的發電量散布圖，包含缺失區間標記。")
