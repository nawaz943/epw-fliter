import pandas as pd
import csv
import os

def filter_epw(input_path, output_path, months=None, days=None, hours=None):
    """
    Filters an EPW file by months, days, and hours.
    
    :param input_path: Path to the original .epw file
    :param output_path: Path where the filtered file will be saved
    :param months: List of integers (1-12)
    :param days: List of integers (1-31)
    :param hours: List of integers (1-24)
    """
    # EPW Standard Column Indices
    MONTH_COL = 1
    DAY_COL = 2
    HOUR_COL = 3
    
    # 1. Read the header (First 8 lines of an EPW file)
    with open(input_path, 'r') as f:
        header = [next(f) for _ in range(8)]
    
    # 2. Read the weather data (Starts from line 9)
    df = pd.read_csv(input_path, skiprows=8, header=None)
    
    # 3. Apply Filters
    if months:
        df = df[df[MONTH_COL].isin(months)]
    if days:
        df = df[df[DAY_COL].isin(days)]
    if hours:
        df = df[df[HOUR_COL].isin(hours)]
    
    # 4. Write the new file
    with open(output_path, 'w', newline='') as f:
        # Write the original metadata headers back
        for line in header:
            f.write(line)
        
        # Write the filtered weather data. 
        # EPW files are strictly comma-separated and usually do not use quotes.
        df.to_csv(f, header=False, index=False, quoting=csv.QUOTE_NONE, lineterminator='\n')

    print(f"Filtered file saved to: {output_path}")

if __name__ == "__main__":
    # Define the folder names
    input_folder = 'epw-input-files'
    output_folder = 'epw-output-files'
    
    # Ensure the output directory exists
    os.makedirs(output_folder, exist_ok=True)
    
    # Define your filtering criteria (e.g., May to November)
    target_months = [5, 6, 7, 8, 9, 10, 11]
    
    # Check if the input folder exists before proceeding
    if os.path.exists(input_folder):
        # Iterate through all files in the input folder
        for filename in os.listdir(input_folder):
            if filename.lower().endswith('.epw'):
                input_path = os.path.join(input_folder, filename)
                # Add "filtered_" prefix to the output filename
                output_path = os.path.join(output_folder, "filtered_" + filename)
                
                print(f"Processing: {filename}...")
                filter_epw(input_path, output_path, months=target_months)
        print("\nAll files have been processed successfully.")
    else:
        print(f"Error: The folder '{input_folder}' was not found. Please ensure it exists in your directory.")