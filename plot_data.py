import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plot_flexural_strength():
    # Read the summary data
    df = pd.read_csv('processed_data/flexural_strength_summary.csv')
    
    # Create figure with larger size
    plt.figure(figsize=(12, 6))
    
    # Create bar plot
    sns.barplot(data=df, x='Filename', y='Flexural Strength (MPa)')
    
    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45, ha='right')
    
    # Add labels and title
    plt.xlabel('Sample')
    plt.ylabel('Flexural Strength (MPa)')
    plt.title('Flexural Strength by Sample')
    
    # Adjust layout to prevent label cutoff
    plt.tight_layout()
    
    # Save the plot
    plt.savefig('processed_data/flexural_strength_plot.png')
    print("Plot saved as 'processed_data/flexural_strength_plot.png'")

if __name__ == "__main__":
    plot_flexural_strength()