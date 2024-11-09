import pandas as pd
import matplotlib.pyplot as plt
import os

# Load the dataset
file_path = './dataset/L1_Train.csv'  # Ensure the file is in the correct directory
df = pd.read_csv(file_path)

# Convert DateTime to datetime format
df['DateTime'] = pd.to_datetime(df['DateTime'])

# Ensure output directory exists
output_dir = './fig/L1 Jan'
os.makedirs(output_dir, exist_ok=True)

# Loop through each day in January 2024
for day in range(1, 32):
    # Filter the data for the current day
    current_date = pd.Timestamp(f'2024-01-{day:02d}').date()
    df_current_day = df[df['DateTime'].dt.date == current_date]
    
    # If there's data for the current day, generate the scatter plot
    if not df_current_day.empty:
        plt.figure(figsize=(10,6))
        plt.scatter(df_current_day['DateTime'], df_current_day['Power(mW)'], color='b')
        plt.xlabel('DateTime')
        plt.ylabel('Power (mW)')
        plt.title(f'Solar Power Generation on {current_date} (Scatter Plot)')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()

        # Set the X-axis limit from 6:00 AM to 6:00 PM
        plt.xlim(pd.Timestamp(f'2024-01-{day:02d} 06:00:00'), pd.Timestamp(f'2024-01-{day:02d} 18:00:00'))
        plt.ylim(0, 2500)
        
        # Save the scatter plot as a PNG image
        plt.savefig(os.path.join(output_dir, f'solar_power_{current_date}_scatter_plot.png'))
        plt.close()  # Close the plot to prevent it from displaying
