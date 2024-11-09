import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

# 定義圖片資料夾路徑
image_folder = './simular date plot/'

# 讀取圖片檔名並解析出缺失和相似日期
image_files = [f for f in os.listdir(image_folder) if f.endswith('.png')]
fill_instructions = []

for filename in image_files:
    parts = filename.split('_')
    file_num = parts[0].split('-')[0][1:]  # 擷取L{file_num}中的file_num
    missing_date = parts[1]
    similar_date = parts[3].replace('.png', '')

    fill_instructions.append((file_num, missing_date, similar_date))

# 開始填補缺失資料
for file_num, missing_date, similar_date in fill_instructions:
    # 讀取資料
    data_path = f'./single blank filled/L{file_num}_aggregated_fill1.csv'
    data = pd.read_csv(data_path, parse_dates=['DateTime'])

    # 將 DateTime 欄位設置為索引
    data.set_index('DateTime', inplace=True)

    # 獲取要填補的日期
    missing_date = pd.to_datetime(missing_date)
    similar_date = pd.to_datetime(similar_date)

    # 檢查缺值區間
    missing_times = pd.date_range(start=missing_date + timedelta(hours=7), 
                                  end=missing_date + timedelta(hours=17), 
                                  freq='10T')
    
    existing_missing_day_data = data[data.index.date == missing_date.date()]

    # 如果缺值時間段從上午9點到下午5點，跳過補值
    if (not existing_missing_day_data.empty and 
        existing_missing_day_data.index.min().time() == datetime.strptime("09:00", "%H:%M").time() and
        existing_missing_day_data.index.max().time() == datetime.strptime("17:00", "%H:%M").time()):
        print(f"日期 {missing_date.date()} 缺失時間為 09:00 至 17:00，跳過補值。")
        continue

    # 取得相似日期的資料
    similar_day_data = data[data.index.date == similar_date.date()]

    # 確認相似日期資料是否足夠
    if similar_day_data.empty:
        print(f"相似日期 {similar_date.date()} 沒有可用資料，無法補值日期 {missing_date.date()}。")
        continue

    # 填補缺失資料
    for missing_time in missing_times:
        if missing_time not in data.index:
            # 取得相似日期中對應時間的資料
            similar_time_data = similar_day_data[similar_day_data.index.time == missing_time.time()]
            
            if not similar_time_data.empty:
                # 取得相似日期對應時間的數據並加入到缺失日期中
                fill_values = similar_time_data.iloc[0].copy()
                fill_values.name = missing_time  # 設置為缺失時間
                data = pd.concat([data, fill_values.to_frame().T])  # 使用concat避免append的警告
                
            else:
                print(f"日期 {similar_date.date()} 缺少時間 {missing_time.time()} 的資料，無法補值。")

    # 排序資料，確保補值後的資料按照時間順序排列
    # data = data.sort_index()

    # 一開始將DateTime設為索引，出檔案會使標題消失，加回來
    data.index.name = "DateTime"

    # 四捨五入所有數值到小數點後兩位
    data = data.round(2)

    # 將補值後的資料儲存回原始檔案
    output_path = f'./fill by simu date/L{file_num}_filled.csv'
    data.to_csv(output_path)

    print(f"已完成日期 {missing_date.date()} 的缺值補值，結果儲存於 {output_path}")
