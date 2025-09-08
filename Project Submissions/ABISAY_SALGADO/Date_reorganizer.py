import pandas as pd

# Load the CSV file
df = pd.read_csv('modified_file.csv')

# Convert the date column to datetime format
df['Draw Date'] = pd.to_datetime(df['Draw Date'])

# Sort the DataFrame by the date column
df_sorted = df.sort_values(by='Draw Date')

# Write the sorted DataFrame to a new CSV file
df_sorted.to_csv('sorted_data.csv', index=False)

print('Dates sorted and saved to sorted_data.csv')
