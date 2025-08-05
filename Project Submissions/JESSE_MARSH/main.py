from scanners.csv_scanner import CsvScanner
from scanners.excel_scanner import ExcelScanner
from scanners.txt_scanner import TxtScanner

file_path = "data/Hello.xlsx"

def main():
    if file_path.endswith((".xlsx", ".xls")):
        scanner = ExcelScanner(file_path)
    elif file_path.endswith(".csv"):
        scanner = CsvScanner(file_path)
    else:
        scanner = TxtScanner(file_path)
    scanner.scan()


if __name__ == "__main__":
    main()
