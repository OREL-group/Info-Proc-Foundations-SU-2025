# Publication-Date-Sorter-and-Plotter

This Python program sorts Chicago-style bibliography entries by publication year and visualizes their distribution over time. It accepts input via a text file or standard input. It extracts publication years from the user input and generates two distinct outputs: a chronologically organized bibliography and a bar chart  displaying the number of entries per year.

In order for the program to run correctly:

* Input must follow Chicago-style citation format. 

* Distinct bibliographic entries must be on their own line or separated by at least one blank line.

Note: 

* If the program cannot find a publication year in a bibliographic entry, it will assign "2222" as the publication year. For example, the entry "John Doe, USA," which does not contain a year of publication, will be assigned "2222" as its year of publication.
