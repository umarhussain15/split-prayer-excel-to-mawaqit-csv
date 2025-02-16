import pandas as pd
from datetime import datetime, timedelta
import os
import argparse

# Parse input arguments
parser = argparse.ArgumentParser(description='Process an Excel file for prayer times.')
parser.add_argument('file_path', type=str, help='Path to the input Excel file')
args = parser.parse_args()

# Load the Excel file
file_path = args.file_path
sheet_name = 0  # Assuming the first sheet contains relevant data

# Read the Excel file with correct header row
df = pd.read_excel(file_path, sheet_name=sheet_name, header=2)

# Drop the Hijri date column if it exists
if 'Hijri date' in df.columns:
    df.drop(columns=['Hijri date'], inplace=True)

# Column mapping
column_mapping = {
    "Gregorian calendar": "Date",
    "morning prayer (beginning of fasting)": "Fajr",
    "sunrise": "Shuruk",
    "midday prayer": "Duhr",
    "afternoon prayer": "Asr",
    "evening prayer": "Maghrib",
    "night prayer": "Isha"
}
df = df.rename(columns=column_mapping)

# Convert Date column to datetime
df['Date'] = pd.to_datetime(df['Date'], format='%d.%m.%Y')

# Get the year from the first date entry
year = df['Date'].dt.year.iloc[0]
output_folder = f"mawaqit-{year}"

# Function to check if a date falls in daylight saving time (DST)
def is_dst(date):
    year = date.year
    last_sunday_march = max(week for week in [datetime(year, 3, day) for day in range(25, 32)] if week.weekday() == 6)
    last_sunday_october = max(week for week in [datetime(year, 10, day) for day in range(25, 32)] if week.weekday() == 6)
    return last_sunday_march <= date < last_sunday_october

# Adjust times to remove DST (subtract 1 hour when in DST period)
def adjust_time(time_str, date):
    if is_dst(date):
        return (datetime.strptime(time_str, "%H:%M") - timedelta(hours=1)).strftime("%H:%M")
    return time_str

# Process each month separately
os.makedirs(output_folder, exist_ok=True)
for month in range(1, 13):
    month_df = df[df['Date'].dt.month == month].copy()
    month_df['Day'] = month_df['Date'].dt.day
    month_df.drop(columns=['Date'], inplace=True)
    
    # Reorder columns to have 'Day' first
    cols = ['Day'] + [col for col in month_df.columns if col != 'Day']
    month_df = month_df[cols]
    
    # Adjust times for DST removal
    for col in month_df.columns:
        if col not in ['Day']:
            month_df[col] = month_df.apply(lambda row: adjust_time(row[col], df.loc[row.name, 'Date']), axis=1)
    
    # Save to CSV with zero-padded month number as filename
    output_path = f"{output_folder}/{month:02d}.csv"
    month_df.to_csv(output_path, index=False)

print(f"CSV files for each month have been generated in the '{output_folder}' folder.")
