import re
import sys
import matplotlib.pyplot as plot

## PART ONE: SORTING BIBLIOGRAPHY ENTRIES BY DATE ##

# Date extraction function
# Function to extract the publication year from a Chicago-style bibliography entry
def extract_date(entry):
    # Prefer original date in brackets if available
    bracket_match = re.search(r'\[(\d{4})\]', entry)
    if bracket_match:
        return int(bracket_match.group(1))

    # Check for Chicago-style citation format of a colon and comma followed by a date
    # e.g. "Publication Location: Publisher, 2020"
    colon_pos = entry.find(':')
    if colon_pos != -1:
        after_colon = entry[colon_pos:]
        # This regex looks for a 4-digit year after the colon, possibly after any characters and optional comma/space
        date_match = re.search(r'[:,]?[^\d]*(\d{4})', after_colon)
        if date_match:
            return int(date_match.group(1))

    # Alternately, find the first 4-digit year in the entry
    # Note: This may not always yield the correct publication year if multiple years are present
    general_match = re.search(r'(\d{4})', entry)
    if general_match:
        return int(general_match.group(1))

    # If date still not found, assign a fallback
    return 2222

# Prompt user to paste Chicago-style bibliography text or provide a file
if len(sys.argv) > 1:
    # If filename provided as command-line argument, read from file
    with open(sys.argv[1], 'r', encoding='utf-8') as input_file:
        pasted_input = input_file.read()
else:
    print("Enter your Chicago-style bibliography below.")
    print("Press Ctrl+D when done:\n")
    pasted_input = sys.stdin.read()

# Split bibliographic entries
# Assumes each entry is on its own line or separated by at least one blank line
raw_entries = pasted_input.strip().split('\n')
bibliography = [entry.strip() for entry in raw_entries if entry.strip()]

# Sort bibliography by extracted date
sorted_bibliography = sorted(bibliography, key=extract_date)

# Output the sorted bibliography
print("\n\nSorted bibliography:\n")
for entry in sorted_bibliography:
    print(entry + "\n")

## END OF PART ONE ##

## PART 2: PLOTTING FROM sorted_bibliography ##

# Plotting function
# Function to plot the number of entries by year
def plot_dates(entries):
    # Extract years from the extract_date function
    years = [extract_date(entry) for entry in entries]
    
    # Count the frequency of each year
    year_counts = {}
    for year in years:
        year_counts[year] = year_counts.get(year, 0) + 1
    
    # Sort years for plotting
    sorted_years = sorted(year_counts.keys())
    counts = [year_counts[year] for year in sorted_years]

    # Plot 
    plot.figure(figsize=(10,5))
    plot.bar(sorted_years, counts, color='black')
    plot.xlabel('Year of Publication', fontsize=14)
    plot.ylabel('Number of Entries', fontsize=14)
    plot.title('Bibliographic Entries by Year of Publication', fontsize=18)
    plot.xticks(sorted_years, rotation=45)
    # Avoid value error if no entries present
    if counts:
        plot.yticks(range(0, max(counts)+1))
    plot.tight_layout()
    plot.show()

# Call the plotting function with the sorted bibliography
plot_dates(sorted_bibliography)

## END OF PART TWO ##