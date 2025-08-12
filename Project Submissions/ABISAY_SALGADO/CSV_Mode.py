import pandas as pd

def calculate_mode(csv_file):
    # Read the CSV file
    data = pd.read_csv(csv_file)

    # Calculate the mode for each column
    mode_values = data.mode().iloc[0]  # Get the first mode in case of multiple modes

    # Print the mode values
    print("Mode values for each column:")
    for column, mode in mode_values.items():
        print(f"{column}: {mode}")


# Example usage
csv_file_path = 'sorted_data.csv'  # Replace with your CSV file path
calculate_mode(csv_file_path)
