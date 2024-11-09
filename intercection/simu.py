import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

for file_num in range(1, 18):
    plot_index = 1  # 起始編號
    for month in range(1, 8):

        # 讀取資料（LX_aggregated_fill1.csv）
        data = pd.read_csv('./single blank filled/L' +str(file_num)+ '_aggregated_fill1.csv', parse_dates=['DateTime'])

        # 篩選一月份的資料並新增日期欄位
        data['Date'] = data['DateTime'].dt.date
        january_data = data[data['DateTime'].dt.month == month]

        # 生成時間範圍（每天上午7:00至下午5:00的固定時間範圍）
        time_range = pd.date_range("07:00", "17:00", freq="10T").time

        # 找出缺失資料的日期（完全沒有該時間段資料的日期）
        missing_dates = []

        for date, group in january_data.groupby('Date'):
            existing_times = group['DateTime'].dt.time.tolist()
            missing_times = [time for time in time_range if time not in existing_times]
            
            # 如果有缺失時間段，記錄該日期
            if missing_times:
                missing_dates.append(date)

        # 計算相似度並繪圖
        for missing_date in missing_dates:
            # 取得該缺值日期的非缺值資料
            missing_day_data = january_data[(january_data['Date'] == missing_date) & (~january_data['Power(mW)'].isna())]

            # 如果該缺值日期的非缺值資料為空，跳過此日期
            if missing_day_data.empty:
                print(f"日期 {missing_date} 沒有非缺值資料，跳過此日期。")
                continue

            # 與其他日期計算相似度
            best_similarity = float('inf')
            most_similar_date = None
            
            for date, group in january_data.groupby('Date'):
                if date == missing_date:
                    continue

                # 取得該日期資料
                common_data = group[group['DateTime'].dt.date == date]
                
                # 計算該日期的缺值時段
                existing_times = common_data['DateTime'].dt.time.tolist()
                missing_times = [time for time in time_range if time not in existing_times]
                
                # 如果缺值時段總計超過五個小時，跳過此日期
                if len(missing_times) > (5 * 60) // 10:  # 5 hours in 10-minute intervals
                    continue
                
                # 計算發電量的歐式距離，這裡將比較兩天所有的發電量資料
                common_times = set(missing_day_data['DateTime'].dt.time).intersection(set(common_data['DateTime'].dt.time))
                
                # 取出共同時間段的發電量資料
                missing_day_power = missing_day_data[missing_day_data['DateTime'].dt.time.isin(common_times)]['Power(mW)']
                common_day_power = common_data[common_data['DateTime'].dt.time.isin(common_times)]['Power(mW)']
                
                # 如果共同時間段的發電量資料不夠，跳過此日期
                if len(missing_day_power) < 1 or len(common_day_power) < 1:
                    continue

                # 計算歐式距離作為相似度
                similarity = np.linalg.norm(missing_day_power.values - common_day_power.values)
                
                # 儲存最相似的日期
                if similarity < best_similarity:
                    best_similarity = similarity
                    most_similar_date = date

            # 如果找到最相似的日期，則繪圖
            if most_similar_date:
                print(f"日期 {missing_date} 的最相似日期為 {most_similar_date}，相似度為 {best_similarity:.4f}。")
                
                # 從原資料中提取出兩天的發電量資料，並只保留時間部分
                missing_day_data_full = january_data[january_data['Date'] == missing_date].copy()
                similar_day_data_full = january_data[january_data['Date'] == most_similar_date].copy()

                # 提取時間部分並轉換為小時數值
                missing_day_data_full['Time'] = missing_day_data_full['DateTime'].dt.hour + missing_day_data_full['DateTime'].dt.minute / 60
                similar_day_data_full['Time'] = similar_day_data_full['DateTime'].dt.hour + similar_day_data_full['DateTime'].dt.minute / 60

                # 繪製合併後的發電量散布圖
                plt.figure(figsize=(16, 9))

                # 缺值日發電量散布圖
                plt.scatter(missing_day_data_full['Time'], missing_day_data_full['Power(mW)'], color='blue', s=10, label=f'Missing Date: {missing_date}')

                # 最相似日發電量散布圖
                plt.scatter(similar_day_data_full['Time'], similar_day_data_full['Power(mW)'], color='orange', s=10, marker="x", label=f'Similar Date: {most_similar_date}')

                # 設定標籤和標題
                plt.xlabel('Time (Hours)')
                plt.ylabel('Power (mW)')
                plt.title(f'{missing_date} vs {most_similar_date} - Power Generation Comparison')
                plt.ylim(0, 2500)

                plt.legend()
                plt.grid(True)

                # 輸出為 PNG 檔案
                plt.savefig(f'./simular date plot/L{file_num}-{plot_index}_{missing_date}_vs_{most_similar_date}.png')
                plt.close()

                # 更新編號
                plot_index += 1
            else:
                print(f"日期 {missing_date} 沒有找到最相似的日期。")

        print(f"L{file_num}-{month}月 相似度計算及圖表輸出完成。")
