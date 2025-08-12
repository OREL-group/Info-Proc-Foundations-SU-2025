# Publication Date Sorter and Plotter

This Python program sorts Chicago-style bibliography entries by publication year and visualizes their distribution over time. It accepts input via a text file or standard input. It extracts publication years from the user input and generates two distinct outputs: a chronologically organized bibliography and a bar chart  displaying the number of entries per year.

## In order for the program to run correctly:

* Input must follow Chicago-style citation format. 

* Distinct bibliographic entries must be on their own line or separated by at least one blank line.

## Note: 

* If the program cannot find a publication year in a bibliographic entry, it will assign "2222" as the publication year. For example, the entry "John Doe, USA," which does not contain a year of publication, will be assigned "2222" as its year of publication.

# Program Background and Development

My initial idea for this project was to create a program that produces a visualization of the distribution of publication dates in a set of bibliographic data. The most basic way to do this was to input an existing set of pre-formatted, Python-friendly bibliographic data directly into the program code. The bibliographic data would already be organized into a list. The list would contain separate dictionaries for each bibliographic item. The program would extract publication dates from a particular key-value pair in each dictionary in the list. The program would then produce a visualization from a publication date list that plots these dates on a graph. 

I successfully got this first version of the program functioning. After this, I decided to try to make the program more practical for real world application. I wanted the program to be less reliant on a pre-formatted dataset and to be able to take a less Python-friendly input from the user. I wanted it to be able to parse actual published bibliographies and to extract relevant values from them that could then be worked on by the program. I wanted the program user to be able to copy and paste the text of a bibliography directly into the program as an input and to receive a visualization of publication dates as an output. 

For this second version of the program, the output would be identical to the first version, but the input would be more complex. However, deciding to work directly with real world examples of published bibliographies gave me another idea. The items listed in bibliographies are conventionally sorted by author’s last name. Items with the same author are grouped together. But I’ve often found myself wanting to see bibliographies organized chronologically, with items grouped according to publication date. 

If the program was now to be expanded to work not only with pre-formatted bibliographic data, but with actual published bibliographies, then I thought it should be relatively easy to produce code that could rearrange a published bibliography according to publication date. This would give the program user two distinct and complimentary outputs: the publication date visualization and the chronological bibliography. This was the final version of the program I settled on.

## Part 1: Sorting bibliography entries by date

For this program, I limited myself to bibliographies published according to Chicago-style citation. I considered two options to create my chronological bibliography output from a standard Chicago-style bibliography input. 

The first option was to create a program to accurately reconstruct a Chicago-style bibliography from a Python list containing bibliographic item dictionaries. 

The second option was to create a program to reliably identify publication date values from within the raw input (the copy and pasted text of a published bibliography) and to rearrange the bibliography according to these particular values. 

I decided that the first option would require a lot of unnecessary steps that wouldn’t be relevant to the immediate purpose of my program, which is to organize and visualize bibliographic data according to publication date. In the first option, I would not only need to parse the input for publication date, but also for author, editor, title, publisher, and any other kind of bibliographic information that might be included in each bibliographic entry. This would add a great deal of unnecessary complexity to my program. In the second option, I would focus only on the value that was relevant to my program (publication date) and use the relatively rigid formatting rules of Chicago-style citation to my advantage. 

I quickly learned that I could use regular expressions to extract data from my text input. In Chicago-style bibliographies, publication date always follows a period, a colon ("[City of publication]:"), and a comma ("[Publisher],”). By using this rule to structure my code, I was able to greatly simplify my program while achieving reliable results. 

One issue I ran into was that the program produced a bad output if the copy and pasted text didn’t conform perfectly to the Chicago-style citation format. If distinct bibliographic entries weren’t separated by a blank line, the program would sometimes lump them together. I decided to incorporate a block of code to ensure that the program accurately detected each distinct bibliographic entry. 

To solicit user input, I used sys.stdin.read() instead of a for loop with input() because a) I did not want the user to have to enter bibliographic entries line by line and b) there is not a reliable delimiter (e.g. periods, commas, semicolons) in bibliographies that would permit the use of split() and allow the user to enter all text on one line. As the program exists currently, the user can input their bibliography as a single block of text, which is an asset, but each bibliographic entry has to already be separated by a blank line. This is an obvious limitation to this program. One solution would be to write a program that can extract bibliographic text from OCRed and non-OCRed PDFs using pypdf. I experimented with this idea, but it proved to be beyond my skill level.

## Part 2: Plotting from sorted_bibliography

For the data visualization, I originally assumed I had to first identify the structure of the text input, extract key-value pairs to form dictionaries, populate a master list with these dictionaries, and feed this master list to matplotlib to generate a visualization. I ended up not needing to rely on a list of dictionaries. The final plotting function (plot_dates) takes the years from the extract_date function in Part 1 (which extracts the dates from a Chicago-style bibliography input), counts their frequency, and sorts them in a list called sorted_years for plotting. The list sorted_bibliography calls the plot_dates function to produce the visualization. 

In addition to coming up against my very limited knowledge of Python data visualization, one issue I had in this section was that a blank user input would generate a Value Error. I worked around this issue by inserting a conditional “if counts” on “plot.yticks(range(0, max(counts)+1)).”

## Program Limitations and Conclusion

This program is limited in several ways. Above all, the program’s function is limited; it is only designed to extract publication dates from a set of bibliographic data. In addition, it can only take an input that is formatted according to Chicago-style citation rules with appropriate spacing. If the input is formatted correctly, this program seems to yield consistently accurate results. However, the program will fail to accurately sort and plot if the correct regex sequence of punctuation and a year appears elsewhere in the bibliographic entry (e.g. in the title). 

Overall this was a great educational experience for me in identifying a problem and developing a basic Python program to solve the problem according to some of the programming principles discussed in IS 430. I am happy to say that I have successfully made a functioning (if by no means perfect) version of this program.