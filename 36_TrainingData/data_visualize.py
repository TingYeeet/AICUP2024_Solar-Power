import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

for i in range(1,18):
    # Load the dataset
    file_path = 'L' +str(i)+ '_Train.csv'  # Ensure the file is in the correct directory
    df = pd.read_csv(file_path)

    # Drop LocationCode and DateTime columns for heatmap analysis
    df_for_heatmap = df.drop(columns=['LocationCode', 'DateTime'])

    # Calculate correlation matrix
    correlation_matrix = df_for_heatmap.corr()

    # Plot heatmap with X-axis labels rotated for better readability
    plt.figure(figsize=(10,8))
    heatmap = sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f")
    plt.xticks(rotation=20, ha='right')  # Rotate X-axis labels
    plt.title('Feature Correlation Heatmap-L' +str(i))

    # Save the heatmap as a PNG image
    plt.savefig('feature_correlation_heatmap-L' +str(i)+ '.png')  # Saves to the current working directory
    plt.close()  # Close the plot to prevent it from displaying
