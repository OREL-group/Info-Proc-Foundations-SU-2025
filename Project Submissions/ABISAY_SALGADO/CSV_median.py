import pandas as pd

def calculate_median(csv_file):
    # Read the CSV file
    data = pd.read_csv(csv_file)

    # Calculate the median for each numerical column
    median_values = data.median()

    # Print the median values
    print("Median values for each numerical column:")
    for column, median in median_values.items():
        print(f"{column}: {median}")


# Example usage
csv_file_path = 'sorted_data.csv'  # Replace with your CSV file path
calculate_median(csv_file_path)
