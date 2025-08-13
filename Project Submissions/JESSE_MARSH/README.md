## Sensitive Information Scanner - Jesse Marsh 2025

A simple python tool to scan files for sensitive information like Social Security Numbers (SSNs) and credit card numbers.

## Current Features

* Supports `.xlsx`, `.xls`, `.csv`, and `.txt` files
* Uses regular expressions to detect sensitive data patterns
* Saves results to a specified output file

## How It Works

The scanner loads each file using a file-specific class like ExcelScanner or TxtScanner, then checks every cell, line, or word for sensitive information pattern matches.

## Folders

* `data/` - sample data files for scanning
* `scanners/` - contains `BaseScanner` class and scanner subclasses for each file type
* `utils/` - contains 'sensitive_patterns.py' for defining patterns of sensitive information

## Usage

1. Update `file_path;` in `main.py` to you input file
2. Update `outputTxtFile` in `base_scanner.py` for where results will be saved
3. Run the program

```bash
python main.py
