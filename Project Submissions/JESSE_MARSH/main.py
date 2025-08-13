#Sensitive information scanner that can be used to detect sensitive data like SSN, CC numbers, etc
#Regular expressions are used to detect different information types, see sensitive_patterns.py
#Scanner is currently single file, which must be hardcoded in below

from scanners.csv_scanner import CsvScanner
from scanners.excel_scanner import ExcelScanner
from scanners.txt_scanner import TxtScanner

# File that will be scanned
# TODO: allow for input of file or folder
file_path = "data/DLP-Test-State-Data/DLPTEST-State-S.xlsx"
#outputTxtFile = "output.txt"

# Logic to determine file type
# TODO: logic to traverse folders and files
def main():
    if file_path.endswith((".xlsx", ".xls")):
        scanner = ExcelScanner(file_path)
    elif file_path.endswith(".csv"):
        scanner = CsvScanner(file_path)
    else:
        scanner = TxtScanner(file_path)  # TxtScanner is the default scanner for all other file types
    scanner.scan()


if __name__ == "__main__":
    main()
