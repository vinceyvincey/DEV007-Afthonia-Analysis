import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plot_flexural_strength():
    """
    Reads flexural strength data from a CSV file, creates a bar plot, 
    and saves the plot as an image file.
    """
    # Define file paths
    input_file = 'processed_data/flexural_strength_summary.csv'
    output_file = 'processed_data/flexural_strength_plot.png'
    
    try:
        # Load data into a pandas DataFrame
        df = pd.read_csv(input_file)
    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found.")
        return
    except pd.errors.EmptyDataError:
        print(f"Error: The file '{input_file}' is empty or corrupted.")
        return
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return

    # Validate the required columns
    if 'Filename' not in df.columns or 'Flexural Strength (MPa)' not in df.columns:
        print("Error: The input file does not contain the required columns ('Filename', 'Flexural Strength (MPa)').")
        return

    # Set the visual style
    sns.set_theme(style="whitegrid")

    # Create a figure with specified size
    plt.figure(figsize=(12, 6))

    # Generate the bar plot
    sns.barplot(data=df, x='Filename', y='Flexural Strength (MPa)', palette='viridis')

    # Customize plot aesthetics
    plt.xticks(rotation=45, ha='right', fontsize=10)  # Rotate x-axis labels for readability
    plt.xlabel('Sample', fontsize=12)                 # X-axis label
    plt.ylabel('Flexural Strength (MPa)', fontsize=12) # Y-axis label
    plt.title('Flexural Strength by Sample', fontsize=14, fontweight='bold') # Plot title

    # Adjust layout to prevent label cutoff
    plt.tight_layout()

    try:
        # Save the plot as a file
        plt.savefig(output_file, dpi=300)
        print(f"Plot successfully saved as '{output_file}'")
    except Exception as e:
        print(f"Error saving the plot: {e}")

    # Show the plot (optional)
    # plt.show()

if __name__ == "__main__":
    plot_flexural_strength()