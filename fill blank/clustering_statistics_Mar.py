import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from datetime import datetime, timedelta

# 讀取資料
agg_df = pd.read_csv('L1_aggregated_fill1.csv', parse_dates=['DateTime'])

# 篩選出三月份的資料，並新增日期欄位
agg_df['Date'] = agg_df['DateTime'].dt.date
march_data = agg_df[agg_df['DateTime'].dt.month <= 3]

# 定義三個時段的範圍
time_ranges = [
    ('morning', datetime.strptime('07:00', '%H:%M').time(), datetime.strptime('11:00', '%H:%M').time()),
    ('midday', datetime.strptime('11:00', '%H:%M').time(), datetime.strptime('14:00', '%H:%M').time()),
    ('afternoon', datetime.strptime('14:00', '%H:%M').time(), datetime.strptime('17:00', '%H:%M').time())
]

# 計算每日分時段的統計特徵，並加上整天的統計特徵
daily_stats = []
for date, group in march_data.groupby('Date'):
    stats = {'Date': date}
    
    # 計算每個時段的統計特徵
    for period_name, start_time, end_time in time_ranges:
        period_data = group[(group['DateTime'].dt.time >= start_time) & (group['DateTime'].dt.time < end_time)]
        stats[f'{period_name}_max'] = period_data['Power(mW)'].max() if not period_data.empty else 0
        stats[f'{period_name}_min'] = period_data['Power(mW)'].min() if not period_data.empty else 0
        stats[f'{period_name}_mean'] = period_data['Power(mW)'].mean() if not period_data.empty else 0
        stats[f'{period_name}_std'] = period_data['Power(mW)'].std() if not period_data.empty else 0
    
    # 計算整天的統計特徵
    stats['daily_max'] = group['Power(mW)'].max()
    stats['daily_min'] = group['Power(mW)'].min()
    stats['daily_mean'] = group['Power(mW)'].mean()
    stats['daily_std'] = group['Power(mW)'].std()
    
    daily_stats.append(stats)

# 將每日統計數據轉換為 DataFrame
daily_stats_df = pd.DataFrame(daily_stats).fillna(0).set_index('Date')

# 使用 KMeans 進行分群，K=6
kmeans = KMeans(n_clusters=10, random_state=42)
clusters = kmeans.fit_predict(daily_stats_df)

# 建立分群資料夾
base_dir = 'Mar k=6'
os.makedirs(base_dir, exist_ok=True)
for i in range(10):
    os.makedirs(os.path.join(base_dir, f'k={i}'), exist_ok=True)

# 繪製每一日的發電量散布圖並儲存至對應的資料夾
for idx, (date, row) in enumerate(daily_stats_df.iterrows()):
    cluster_label = clusters[idx]
    date_data = march_data[march_data['Date'] == date]

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

print("三月資料的分群完成並已儲存各日的發電量散布圖，包含缺失區間標記。")
