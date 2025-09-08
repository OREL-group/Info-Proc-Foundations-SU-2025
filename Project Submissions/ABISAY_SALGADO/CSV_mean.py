import pandas as pd


def calculate_mean(csv_file):
    # Read the CSV file
    data = pd.read_csv(csv_file)

    # Calculate the mean for each numerical column
    mean_values = data.mean()

    # Print the mean values
    print("Mean values for each numerical column:")
    for column, mean in mean_values.items():
        print(f"{column}: {mean}")


# Example usage
csv_file_path = 'sorted_data.csv'  # Replace with your CSV file path
calculate_mean(csv_file_path)
