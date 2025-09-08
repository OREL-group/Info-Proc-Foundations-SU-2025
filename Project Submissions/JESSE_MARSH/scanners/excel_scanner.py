import re

import pandas as pd

from scanners.base_scanner import BaseScanner


class ExcelScanner(BaseScanner):
    def load_file(self):
        print("excel scan start")
        return pd.read_excel(self.file_path)

    # TODO: Additional refinement is needed reduce redundancy in defined scanner
    def process_lines(self, df):        # Will iterate through pand
        for index, row in df.iterrows():
            for cell in row:
                self.check_patterns(str(cell), index + 1)

    def check_patterns(self, text, line_number):
        for pattern_name, pattern in self.patterns.items():
            matches = re.findall(pattern, text)
            for match in matches:
                self.results.append((line_number, pattern_name, match))
