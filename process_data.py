import pandas as pd
import os
import glob
import logging
from datetime import datetime
import numpy as np

def setup_logging():
    os.makedirs('logs', exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file = f'logs/process_data_{timestamp}.log'
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    
    logging.info('Starting data processing')

def read_csv_with_dtypes(file_path):
    """Read CSV file with specified data types"""
    # First try reading without dtypes to check structure
    df = pd.read_csv(file_path)
    
    # Clean numeric columns - force conversion to float
    numeric_cols = ['Load (N)', 'Time (s)', 'Displacement (mm)', 'Stress (MPa)', 'Strain (%)']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Clean up any potential missing values
    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.dropna()
    
    return df

def calculate_flexural_modulus(stress, strain, region_size=0.02):
    """
    Calculate flexural modulus from the initial linear region of the stress-strain curve
    
    Parameters:
    - stress: Series of stress values (MPa)
    - strain: Series of strain values (%)
    - region_size: Size of strain region to use (default 2%)
    
    Returns:
    - modulus: Flexural modulus in MPa
    """
    # Convert strain to decimal form
    strain_decimal = strain / 100
    
    # Find data points in initial region (e.g., up to 2% strain)
    mask = strain_decimal <= region_size
    
    if mask.sum() < 2:  # Need at least 2 points for linear fit
        return None
    
    # Get points in the region
    stress_region = stress[mask]
    strain_region = strain_decimal[mask]
    
    # Calculate slope using linear regression
    coefficients = np.polyfit(strain_region, stress_region, 1)
    modulus = coefficients[0]  # Slope is the modulus
    
    return modulus

def process_csv_files():
    csv_files = glob.glob('raw_data/*.csv')
    logging.info('Found {} CSV files to process'.format(len(csv_files)))
    
    summary_data = []
    
    for file_path in csv_files:
        try:
            filename = os.path.basename(file_path)
            df = read_csv_with_dtypes(file_path)
            
            # Calculate flexural strength
            flex_strength = df['Stress (MPa)'].max()
            
            # Calculate flexural modulus
            flex_modulus = calculate_flexural_modulus(
                df['Stress (MPa)'],
                df['Strain (%)']
            )
            
            summary_data.append({
                'Filename': filename,
                'Flexural Strength (MPa)': flex_strength,
                'Flexural Modulus (MPa)': flex_modulus
            })
            
            logging.info('Successfully processed {}. Strength: {:.2f} MPa, Modulus: {:.2f} MPa'.format(
                filename, flex_strength, flex_modulus))
            
        except Exception as e:
            logging.error('Error processing {}: {}'.format(file_path, str(e)))
    
    # Create summary dataframe with explicit dtypes
    summary_df = pd.DataFrame(summary_data).astype({
        'Filename': 'string',
        'Flexural Strength (MPa)': 'float64',
        'Flexural Modulus (MPa)': 'float64'
    })
    
    # Create output directory if it doesn't exist
    os.makedirs('processed_data', exist_ok=True)
    
    # Export summary to CSV
    output_path = 'processed_data/flexural_strength_summary.csv'
    summary_df.to_csv(output_path, index=False)
    
    logging.info('Summary exported to {}'.format(output_path))
    logging.info('Total files processed: {}'.format(len(csv_files)))
    
    return summary_df

if __name__ == "__main__":
    setup_logging()
    summary_df = process_csv_files()