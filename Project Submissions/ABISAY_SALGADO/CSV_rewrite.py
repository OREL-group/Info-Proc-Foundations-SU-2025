import pandas as pd

# Load the CSV file
df = pd.read_csv('Lottery_Mega_Millions_Winning_Numbers__Beginning_2002.csv')

# Split the 'Wining Numbers' column into separate columns
winning_numbers = df['Winning Numbers'].str.split(' ', expand=True)

# Rename the new columns
winning_numbers.columns = [f'winning_number_{i+1}' for i in range(winning_numbers.shape[1])]

# Drop the original 'Wining Numbers' column and concatenate the new columns
df = df.drop(columns=['Winning Numbers']).join(winning_numbers)

# Save the modified DataFrame to a new CSV file
df.to_csv('modified_file.csv', index=False)
