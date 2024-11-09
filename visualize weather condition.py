import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
file_path = './dataset/L1_Train.csv'  # 請確認檔案路徑正確
df = pd.read_csv(file_path)

# Convert DateTime to datetime format
df['DateTime'] = pd.to_datetime(df['DateTime'])

month = "01"
date = ['02', '05', '06', '18']

for day in date:

    # Filter data for date list
    df_day = df[df['DateTime'].dt.date == pd.Timestamp(f'2024-{month}-{day}').date()]

    # Set the X-axis limit from 6:00 AM to 6:00 PM
    start_time = pd.Timestamp(f'2024-{month}-{day} 06:00:00')
    end_time = pd.Timestamp(f'2024-{month}-{day} 18:00:00')

    # Create a figure with 1 row and 4 columns for subplots
    fig, axs = plt.subplots(4, 1, figsize=(15, 10))  # (4, 1) arrangement

    # Plot Pressure(hpa)
    axs[0].plot(df_day['DateTime'], df_day['Pressure(hpa)'], color='b')
    axs[0].set_title('Pressure (hpa)')
    axs[0].set_xlim(start_time, end_time)
    axs[0].set_xlabel('Time')
    axs[0].set_ylabel('Pressure (hpa)')
    axs[0].tick_params(axis='x', rotation=0)

    # Plot Humidity(%)
    axs[1].plot(df_day['DateTime'], df_day['Humidity(%)'], color='g')
    axs[1].set_title('Humidity (%)')
    axs[1].set_xlim(start_time, end_time)
    axs[1].set_xlabel('Time')
    axs[1].set_ylabel('Humidity (%)')
    axs[1].tick_params(axis='x', rotation=0)

    # Plot Temperature(°C)
    axs[2].plot(df_day['DateTime'], df_day['Temperature(°C)'], color='r')
    axs[2].set_title('Temperature (°C)')
    axs[2].set_xlim(start_time, end_time)
    axs[2].set_xlabel('Time')
    axs[2].set_ylabel('Temperature (°C)')
    axs[2].tick_params(axis='x', rotation=0)

    # Plot Sunlight(Lux)
    axs[3].plot(df_day['DateTime'], df_day['Sunlight(Lux)'], color='y')
    axs[3].set_title('Sunlight (Lux)')
    axs[3].set_xlim(start_time, end_time)
    axs[3].set_xlabel('Time')
    axs[3].set_ylabel('Sunlight (Lux)')
    axs[3].tick_params(axis='x', rotation=0)

    # Adjust layout to prevent overlapping of subplots
    plt.tight_layout()

    # Save the figure as a PNG image
    plt.savefig(f'./fig/Jan KMeans/weather/weather_{month}-{day}')
    plt.close()  # Close the plot to prevent it from displaying
