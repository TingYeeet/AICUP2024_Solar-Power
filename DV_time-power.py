import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
file_path = './dataset/L1_Train.csv'  # Ensure the file is in the correct directory
df = pd.read_csv(file_path)

# Convert DateTime to datetime format
df['DateTime'] = pd.to_datetime(df['DateTime'])

# Filter the data for January 1st only
df_january_1 = df[df['DateTime'].dt.date == pd.Timestamp('2024-01-01').date()]

# Plot the scatter plot for DateTime vs Power (January 1st only)
plt.figure(figsize=(10,6))
plt.scatter(df_january_1['DateTime'], df_january_1['Power(mW)'], color='b')
plt.xlabel('DateTime')
plt.ylabel('Power (mW)')
plt.title('Solar Power Generation on January 1st (Scatter Plot)')
plt.xticks(rotation=45, ha='right')  # Rotate the X-axis labels for readability
plt.tight_layout()  # Adjust layout to prevent clipping

# Save the scatter plot as a PNG image
plt.savefig('solar_power_january_1_scatter_plot.png')  # Saves to the current working directory
plt.close()  # Close the plot to prevent it from displaying
