import pandas as pd

def filter_epw(input_path, output_path, months=None, days=None, hours=None):
    """
    Filters an EPW file by months, days, and hours.
    
    :param input_path: Path to the original .epw file
    :param output_path: Path where the filtered file will be saved
    :param months: List of integers (1-12)
    :param days: List of integers (1-31)
    :param hours: List of integers (1-24)
    """
    
    
    # 1. Read the header (First 8 lines of an EPW file)
    with open(input_path, 'r') as f:
        header = [next(f) for _ in range(8)]
    
    # 2. Read the weather data (Starts from line 9)
    # EPW data columns: Year, Month, Day, Hour, Minute...
    df = pd.read_csv(input_path, skiprows=8, header=None)
    
    # 3. Apply Filters
    if months:
        df = df[df[1].isin(months)]
    if days:
        df = df[df[2].isin(days)]
    if hours:
        df = df[df[3].isin(hours)]
    
    # 4. Write the new file
    with open(output_path, 'w', newline='') as f:
        # Write the original metadata headers back
        for line in header:
            f.write(line)
        
        # Write the filtered weather data
        df.to_csv(f, header=False, index=False)

    print(f"Filtered file saved to: {output_path}")

# --- EXAMPLE USAGE ---
# This example filters for January and February, first 10 days, between 9 AM and 5 PM
filter_epw(
    input_path='Dubai_Intl_Airp_-hour-2025.epw', 
    output_path='dxb-airp-filtered-MayNov-2025.epw',
    months=[5, 6, 7, 8, 9, 10, 11], 
    days=[], 
    hours=[]
)