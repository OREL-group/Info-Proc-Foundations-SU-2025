import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
file_path = 'sorted_data.csv'  # Replace with your CSV file path
data = pd.read_csv(file_path)

# Initialize a dictionary to hold counts for each number
number_counts = {}

# Iterate through each column in the DataFrame
for column in data.columns:
    # Filter numeric values and count occurrences
    numeric_values = data[column].dropna().astype(float)
    for number in numeric_values:
        if number in number_counts:
            number_counts[number] += 1
        else:
            number_counts[number] = 1

# Prepare data for plotting
sorted_numbers = sorted(number_counts.keys())
frequencies = [number_counts[number] for number in sorted_numbers]

# Create the bar chart
plt.bar(sorted_numbers, frequencies)
plt.xlabel('Numbers')
plt.ylabel('Frequency')
plt.title('Frequency of Numbers in CSV Columns')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
