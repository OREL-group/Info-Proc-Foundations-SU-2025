## Database Crosswalk Project in SQL

This code is meant to take an aggregate of records belonging to Eastern Illinois University's herbarium collection currently available and hosted by IDigBio/SEInet and make them compatible for upload in the university library's "Keep" for expanding access to a wider audience. The main process being run automates the transfer of data to a Darwin Core compliant metadata scheme through the use of Microsoft Access Database. Two versions of the code are included in the directory, one with commenting included and another with only the raw query due to restrictions within Access for allowable commentary. A sample spreadsheet of records as a .csv file is also included for downloading & testing the code. The steps to do so are as follows:
* Download seinetraw.csv from the project directory
* Open a blank database in Microsoft Access
* Under the "External Data" tab, select New Data Source > From File > Excel and import seinetraw.csv as a new table
* Select "Show Worksheets" and press next
* Select "First Row Contains Column Headings" and press next
* Do not edit field data types and press next (this is something I have to edit for the actual records, but isn't needed for an example)
* Select "Choose my own primary key" and in the drop-down menu choose "sourcePrimaryKey-dbpk"
* Import to table as "seinetraw" and press Finish
* Open the new table, navigate to the "Create" tab and select SQL Query
* Delete the automatic "SELECT;" function and paste the code from raw_query in the directory
* Select run

## Purpose & Scope

Due to the two repositories using different metadata standards for their digital collections, the records downloaded from the current IDigBio host site are not formatted in a way compatible for upload with the EIU Keep. As the collection contains upwards of 80,000 records, individually uploading and editing each specimen is not realistic. In order to comply with the batch upload system in the Keep, the original record data must be entered under recognized field names.

The scope of the code is as follows:
* The bulk of this code's functions equate the original repository's fields with a recognizable counterpart
* Fields that did not exist in the original records are added to the spreadsheet with any necessary included data (i.e., "Botany" under the field "discipline" for all records)
* Unnecessary fields are removed
* Common collectors recognized in the original "recordedBy" field have their known associated data added to the "author 1" fields
* Cultivation status is changed from binary 0/1 language to "yes/no" natural language
* Records with a location security status = 1 have data removed from locality, latitude, and longitude fields

## Problems, Limitations, & Final Comments

The main issues I ran into with writing this query had to do with Microsoft Access Database's functionality. Access does not allow from commenting within the code, making it difficult to notate what certain functions are meant to accomplish. Additionally, the SQL allowances are limited - IF/THEN statements, for example, are written as IIF(expression, truepart, falsepart) and require excessive nesting if including any more than one conditional. This makes the code somewhat difficult to follow and limits the number of collectors whose data could be automated. Without the commentary it starts to look a bit spaghettified. There is, at least, the ability to hide nested code through the use of arrows on the starting line numbers found at the left side of the code, which makes it slightly less confusing. If there is a better solution to include conditionals without these limits in Access, I haven't been able to find it yet.

The nature of specifying each individual field also lends to the code looking less neat than I'd like, rather than easily recognizable functions in simple blocks. It is an improvement from the original code I was given, however, which was a single large block without any line breaks. 

As it is, the code so far has been functional and sped up a decent amount of the otherwise manual data cleanup required for this crosswalk project. Alongside a word document with commentary I've provided to my supervisor that acts as code commenting would, I hope that it can also be clear and easily updated as needed moving forward.
