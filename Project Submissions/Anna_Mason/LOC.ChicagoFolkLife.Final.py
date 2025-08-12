"""
LOC.ChicagoFolkLife.Final.py

An interactive menu style tool that helps the user learn about the makeup of the 1977 Chicago Ethnic Folk Arts Project
This program should present the user with a menu when it is first run
In order to return to the original menu or other menu items, the program must be rerun again from the start.
If user chooses to see a pie chart, the program should generate an external pop-up window with the visualization

This is not a complete project -- this is discussed in the ReadMe file

Dependencies:
    -chicago_FolkLife.csv

"""

import pandas as pd
import matplotlib.pyplot as plt
##toolboxes for data analysis and visualization

df = pd.read_csv("chicago_FolkLife.csv")
##this reads in my dataset from the Library of Congress

##my goal for this project was to make this catalog navigable, so I am making a menu
def show_menu():
    print(
        "Welcome to the Library of Congress 1977 Chicago Folklife Survey Notes Catalog.\n\tWould you like to learn about the Irish or Italian communities?")
    print("\t1 - Irish")
    print("\t2 - Italian")
    print("\t3 - Exit")
##there are just Irish and Italian menu options right now, the goal is to eventually include all ethnic groups

    choice = input("Enter your selection: ")
    if choice == "1":
        Irish_menu()
    elif choice == "2":
        Italian_menu()
    elif choice == "3":
        print("Goodbye")
        return
    else:
        print("Invalid. Please enter 1,2 or 3")
        return

##defining my matplotlib function which creates a pie chart representation of the dataset
def show_ethnic_pie_chart():
  ethnic_groups = ["irish", "italian", "polish", "german", "african", "jewish", "scandanavian", "lithuanian","greek","russian", "slovenian", "croatian", "serbian", "macedonian"]
  group_counts = {}
  #this dictionary is where the counts for each ethnic group mention is stored

  for group in ethnic_groups:
      count = (
          df['Transcription'].str.contains(group, case=False, na=False) |
          df['Tags'].str.contains(group, case=False, na=False)
      ).sum()
      ##this is counting if any of the individual strings in my ethnic_group dictionary is present in the transcription OR the tags columns in my dataset
      group_counts[group.title()] = count
      ##this then adds the count from the previous lines to my group_counts dictionary

#All of these commands are about the physical appearance of the chart
  labels = list(group_counts.keys())
  ##this refers back to the group_counts dictionary I defined before
  sizes = list(group_counts.values())
  ##this determines the size of each of the pie chart slices
  plt.figure(figsize=(8, 8))
  ##this determines my figure, and that it will be an 8x8 inch square
  plt.pie(sizes, labels=labels,
          autopct='%1.1f%%')
          ##this generates a percent label up to the 10th percent of how much of the dataset is about that ethnic group
  plt.title("Ethnic Community Makeup of the 1977 Chicago Folklife Survey")
  plt.axis("equal")
  #Setting the aspect ratio to equal makes sure we get a round chart and not an oval!
  plt.tight_layout()
  ##this gives the chart more room so that text isn't overlapping
  plt.show()
  return

##this is the menu the user is presented with if they select option two aka to learn more about the irish representation in the dataset
def Irish_menu():
        print("\nIrish Community Data Exploration Options")
        print("\t1 - Show chart of Irish makeup compared to other ethnic makeup in the survey")
        print("\t2 - See how many notebook pages within the survey are about the Chicago Irish community")

        choice = input("Enter your selection: ")
        if choice == "1":
            show_ethnic_pie_chart()
            return
        if choice == "2":
            count = (df['Transcription'].str.contains('irish', case=False, na=False) | df['Tags'].str.contains('irish',
            case=False,na=False)).sum()
            ##this counts the number of times irish comes up in the transcription OR tags columns and adds them together
            ##I realize this means that it will double count a single row if the word shows up in both the transcription and tags columns
            print(fr'Of the 3657 pages in this catalog, {count} of them pertain to the Irish community.')
        else:
            print("Invalid selection. Please enter 1 or 2")

##this is the menu the user is faced with if they select 2 AKA to learn more about the italian presence in the dataset
def Italian_menu():
        print("\nItalian Community Data Exploration Options")
        print("\t1 - See a chart representation of what types of Italian cultural activities are detailed in the survey")
        print("\t2 - See how many notebook pages within the survey are about the Chicago Italian community")

        choice = input("Enter your selection: ")
        if choice == "1":
            show_ethnic_pie_chart()
            ##it is the same chart that comes up in the irish menu
            ##I talk more about in the README how I originally wanted these to be different
            return
        if choice == "2":
            count = (df['Transcription'].str.contains('italian', case=False, na=False) | df['Tags'].str.contains(
                'italian', case=False, na=False)).sum()
            print(fr'Of the 3657 pages in this catalog, {count} of them pertain to the Italian community.')
            ##this is the same function I used before, but it is looking for "italian" rather than "irish"
            ##it still has the same problem of double counting if italian is in both transcription and tags columns
        else:
            print("Invalid selection. Please enter 1 or 2")


show_menu()

