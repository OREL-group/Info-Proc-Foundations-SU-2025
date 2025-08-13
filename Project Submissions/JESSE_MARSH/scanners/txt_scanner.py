import re

import pandas as pd

from scanners.base_scanner import BaseScanner


class TxtScanner(BaseScanner):
    def load_file(self):
        print("txt scan start")
        return pd.read_csv(self.file_path, sep=" ", header=None)

    # TODO: Additional refinement is needed reduce redundancy in defined scanner
    def process_lines(self, df):
        for index, row in df.iterrows():
            for cell in row:
                self.check_patterns(str(cell), index + 1)

    def check_patterns(self, text, line_number):
        for pattern_name, pattern in self.patterns.items():
            matches = re.findall(pattern, text)
            for match in matches:
                self.results.append((line_number, pattern_name, match))
