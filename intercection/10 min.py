import pandas as pd
from datetime import datetime, timedelta

for file_num in range(1, 18):

    # 讀取資料
    data = pd.read_csv('../dataset/L' +str(file_num)+ '_Train.csv')

    # 移除秒數，只保留分鐘
    data['DateTime'] = pd.to_datetime(data['DateTime']).dt.floor('min')

    # 將時間向下取至每 10 分鐘
    data['DateTime'] = data['DateTime'].dt.floor('10T')

    # 設定每日目標範圍的時間區間（上午 7:00 至下午 5:00）
    start_time = '07:00'
    end_time = '17:00'

    # 生成完整的每日時間範圍
    all_days = pd.date_range(start=data['DateTime'].dt.date.min(), end=data['DateTime'].dt.date.max(), freq='D')
    missing_intervals = []

    # 逐日檢查並記錄缺失的時間段
    for day in all_days:
        day_start = datetime.combine(day, datetime.strptime(start_time, '%H:%M').time())
        day_end = datetime.combine(day, datetime.strptime(end_time, '%H:%M').time())
        day_times = pd.date_range(start=day_start, end=day_end, freq='10T')
        
        # 找出當天缺少的時間
        day_data = data[(data['DateTime'] >= day_start) & (data['DateTime'] <= day_end)]
        missing_times = day_times.difference(day_data['DateTime'])
        
        # 將缺失時間分段，找出連續的缺失區間
        if len(missing_times) > 0:
            start_interval = missing_times[0]
            end_interval = missing_times[0]
            
            for i in range(1, len(missing_times)):
                current_time = missing_times[i]
                previous_time = missing_times[i - 1]
                
                # 如果當前時間與前一個時間不連續，則結束前一段並開始新的一段
                if current_time != previous_time + timedelta(minutes=10):
                    missing_intervals.append([day.date(), start_interval.time(), end_interval.time()])
                    start_interval = current_time
                
                end_interval = current_time
            
            # 記錄當天最後一個缺失區間
            missing_intervals.append([day.date(), start_interval.time(), end_interval.time()])

    # 如果有缺少的時間區間，將其輸出成CSV檔案
    if missing_intervals:
        missing_df = pd.DataFrame(missing_intervals, columns=['Date', 'Start Time', 'End Time'])
        missing_df.to_csv('L' +str(file_num)+ '_missing.csv', index=False)

    # 聚合資料，計算平均值
    agg_data = data.groupby('DateTime').agg({
        'WindSpeed(m/s)': 'mean',
        'Pressure(hpa)': 'mean',
        'Temperature(°C)': 'mean',
        'Humidity(%)': 'mean',
        'Sunlight(Lux)': 'mean',
        'Power(mW)': 'mean'
    }).reset_index()

    # 過濾掉下午 5:10 到隔日早上 6:50 的時間
    agg_data = agg_data[(agg_data['DateTime'].dt.time >= datetime.strptime(start_time, '%H:%M').time()) & 
                        (agg_data['DateTime'].dt.time <= datetime.strptime(end_time, '%H:%M').time())]

    # 將結果輸出為 CSV 檔案
    agg_data.to_csv('L' +str(file_num)+ '_aggregated.csv', index=False)
