import pandas as pd

# Load the CSV file
df = pd.read_csv('modified_file.csv')

# List of columns to average
columns_to_average = ['winning_number_1', 'winning_number_2', 'winning_number_3', 'winning_number_4', 'winning_number_5', 'Mega Ball']

# Calculate the average for each specified column
averages = {col: df[col].mean() for col in columns_to_average}

# Print the averages
for col, avg in averages.items():
    print(f'The average of {col} is: {avg}')