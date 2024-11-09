import pandas as pd
from datetime import timedelta

for file_num in range(2, 18):

    # 讀取資料
    missing_df = pd.read_csv('L' +str(file_num)+ '_missing.csv', parse_dates=['Date'])
    agg_df = pd.read_csv('L' +str(file_num)+ '_aggregated.csv', parse_dates=['DateTime'])

    # 對於缺值時間的處理
    for index, row in missing_df.iterrows():
        if row['Start Time'] == row['End Time']:
            # 確認缺失時間
            missing_time = pd.to_datetime(f"{row['Date']} {row['Start Time']}")
            
            # 找到缺失時間前後的資料
            prev_time = missing_time - timedelta(minutes=10)
            next_time = missing_time + timedelta(minutes=10)
            
            # 確認前後時間點在資料集中存在
            prev_data = agg_df[agg_df['DateTime'] == prev_time]
            next_data = agg_df[agg_df['DateTime'] == next_time]
            
            # 如果前後資料都存在，取平均值補上缺失值
            if not prev_data.empty and not next_data.empty:
                mean_values = prev_data.iloc[:, 1:].mean() + next_data.iloc[:, 1:].mean()
                mean_values /= 2
                
                # 建立補值資料
                new_row = pd.Series([missing_time] + list(mean_values), index=agg_df.columns)
                
                # 將補值資料加入聚合資料中
                agg_df = pd.concat([agg_df, pd.DataFrame([new_row])], ignore_index=True)
                
                # 從 missing_df 中移除已補值的紀錄
                missing_df.drop(index, inplace=True)

    # 按時間排序聚合資料，並輸出新的 CSV 檔案
    agg_df.sort_values(by='DateTime', inplace=True)
    agg_df.to_csv('./single blank filled/L' +str(file_num)+ '_aggregated_fill1.csv', index=False)
    missing_df.to_csv('L' +str(file_num)+ '_missing_fill1.csv', index=False)

    print("已成功匯出新的 L1_aggregated_fill1.csv 和 L1_missing_fill1.csv")
