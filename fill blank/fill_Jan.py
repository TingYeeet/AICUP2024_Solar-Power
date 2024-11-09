import pandas as pd

# 讀取資料
data = pd.read_csv('L1_aggregated_fill1.csv', parse_dates=['DateTime'])
data['Date'] = data['DateTime'].dt.date
data['Time'] = data['DateTime'].dt.time

# 產生一月的完整時間範圍（7:00 至 17:00，每10分鐘一次）
start_time = '07:00:00'
end_time = '17:00:00'
date_range = pd.date_range(start='2024-01-01', end='2024-01-31', freq='D')
time_range = pd.date_range(start=start_time, end=end_time, freq='10T').time

# 確保 full_datetime 中的 Date 列和 Time 列格式與 data 中一致
full_datetime = pd.DataFrame([(d, t) for d in date_range for t in time_range], columns=['Date', 'Time'])
full_datetime['Date'] = pd.to_datetime(full_datetime['Date']).dt.date  # 設定為日期格式
full_datetime['Time'] = full_datetime['Time']  # 保持時間格式

# 合併資料來偵測缺失的時間點
merged_data = pd.merge(full_datetime, data, on=['Date', 'Time'], how='left')

# 定義補值函數
def fill_missing_data(date_missing, date_source=None, use_neighbors=False):
    for time in merged_data[(merged_data['Date'] == date_missing) & (merged_data['Power(mW)'].isna())]['Time']:
        if date_source:  # 用另一日期同時段數據補值
            fill_values = merged_data[(merged_data['Date'] == date_source) & (merged_data['Time'] == time)].iloc[0]
            if not fill_values.empty:
                # 將發電量及其他欄位補值
                merged_data.loc[(merged_data['Date'] == date_missing) & (merged_data['Time'] == time), ['Power(mW)', 'WindSpeed(m/s)', 'Pressure(hpa)', 'Temperature(°C)', 'Humidity(%)', 'Sunlight(Lux)']] = fill_values[['Power(mW)', 'WindSpeed(m/s)', 'Pressure(hpa)', 'Temperature(°C)', 'Humidity(%)', 'Sunlight(Lux)']].values
        elif use_neighbors:  # 用前後十分鐘數據平均補值
            prev_time = (pd.to_datetime(f'{date_missing} {time}') - pd.Timedelta(minutes=10)).time()
            next_time = (pd.to_datetime(f'{date_missing} {time}') + pd.Timedelta(minutes=10)).time()
            prev_values = merged_data[(merged_data['Date'] == date_missing) & (merged_data['Time'] == prev_time)][['Power(mW)', 'WindSpeed(m/s)', 'Pressure(hpa)', 'Temperature(°C)', 'Humidity(%)', 'Sunlight(Lux)']].values
            next_values = merged_data[(merged_data['Date'] == date_missing) & (merged_data['Time'] == next_time)][['Power(mW)', 'WindSpeed(m/s)', 'Pressure(hpa)', 'Temperature(°C)', 'Humidity(%)', 'Sunlight(Lux)']].values
            
            if len(prev_values) > 0 and len(next_values) > 0:
                # 平均補值
                merged_data.loc[(merged_data['Date'] == date_missing) & (merged_data['Time'] == time), ['Power(mW)', 'WindSpeed(m/s)', 'Pressure(hpa)', 'Temperature(°C)', 'Humidity(%)', 'Sunlight(Lux)']] = (prev_values + next_values) / 2

# 1. 針對 1/15 缺值，以 1/25 同時段數據補足
fill_missing_data(date_missing=pd.to_datetime('2024-01-15').date(), date_source=pd.to_datetime('2024-01-25').date())

# 2. 針對 1/26 缺值，以前後十分鐘數據平均補足
fill_missing_data(date_missing=pd.to_datetime('2024-01-26').date(), use_neighbors=True)

# 3. 針對 1/14 缺值，以 1/09 同時段數據補足
fill_missing_data(date_missing=pd.to_datetime('2024-01-14').date(), date_source=pd.to_datetime('2024-01-09').date())

# 填補 NaN 值後四捨五入至小數點第二位
merged_data[['Power(mW)', 'WindSpeed(m/s)', 'Pressure(hpa)', 'Temperature(°C)', 'Humidity(%)', 'Sunlight(Lux)']] = merged_data[['Power(mW)', 'WindSpeed(m/s)', 'Pressure(hpa)', 'Temperature(°C)', 'Humidity(%)', 'Sunlight(Lux)']].round(2)

# 計算 DateTime 列
merged_data['DateTime'] = pd.to_datetime(merged_data['Date'].astype(str) + ' ' + merged_data['Time'].astype(str))

# 輸出結果
merged_data.to_csv('L1_fill_Jan.csv', index=False)
print("缺值補足完成，輸出為 L1_fill_Jan.csv。")
