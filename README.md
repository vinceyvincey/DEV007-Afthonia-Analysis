# Flexural Modulus Analyzer

A Python application for analyzing flexural modulus from stress-strain data using a graphical interface.

## Prerequisites

- Python 3.8+ (comes pre-installed on macOS)
- macOS (M2 chip)
- pip (Python package installer)

## Installation Instructions for M2 MacBook Air

1. **Verify Python Installation**
   ```bash
   # Open Terminal and check Python version
   python3 --version
   
   # Check pip installation
   python3 -m pip --version
   ```
   If pip is not installed, install it with:
   ```bash
   curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
   python3 get-pip.py
   ```

2. **Clone the Repository**
   ```bash
   # Open Terminal and navigate to where you want to store the project
   cd ~/Documents
   git clone https://github.com/your-username/flexural-modulus-analyzer.git](https://github.com/vinceyvincey/DEV007-Afthonia-Analysis.git
   cd DEV007-Afthonia-Analysis
   ```

3. **Create and Activate Virtual Environment**
   ```bash
   # Create a new virtual environment
   python3 -m venv venv
   
   # Activate the environment
   source venv/bin/activate
   ```

4. **Install Dependencies**
   ```bash
   # Install required packages
   pip install -r requirements.txt
   ```

## Data Preparation

1. Create a `raw_data` folder in the project directory:
   ```bash
   mkdir raw_data
   ```

2. Place your CSV files in the `raw_data` folder. Files should have the following format:
   - Required columns: "Strain (%)" and "Stress (MPa)"
   - Values should be numeric
   - Use comma as delimiter

## Running the Program

1. **Ensure your virtual environment is activated**
   ```bash
   source venv/bin/activate
   ```

2. **Run the program**
   ```bash
   python3 analyze_modulus.py
   ```

## Using the Program

1. **Interface Overview**
   - The main window shows the stress-strain curve
   - Red dashed lines indicate the strain range for modulus calculation
   - Text boxes show the current strain values
   - The calculated modulus is displayed at the top

2. **Adjusting Strain Range**
   - Drag the red dashed lines to adjust the strain range
   - Or enter values directly in the text boxes
   - The modulus will update automatically

3. **Processing Multiple Files**
   - Use the file selector dropdown to switch between files
   - Click "Accept" or press Enter to save the current analysis
   - Results are automatically tracked for all processed files

4. **Exporting Results**
   - Click "Export Data" to save all results
   - Results will be saved as 'modulus_results.csv' in the project directory

## Troubleshooting

If you encounter TkAgg backend issues:
```bash
# Install tkinter
brew install python-tk@3.9
```

If you see matplotlib warnings:
```bash
# Reinstall matplotlib
pip install --upgrade matplotlib
```

## File Structure
```
flexural-modulus-analyzer/
├── analyze_modulus.py
├── requirements.txt
├── README.md
├── .gitignore
└── raw_data/
    └── (your .csv files)
```

## Support

For issues or questions:
1. Check the [Issues](https://github.com/your-username/flexural-modulus-analyzer/issues) page
2. Create a new issue with:
   - Your macOS version
   - Python version
   - Error message (if any)
   - Description of the problem

