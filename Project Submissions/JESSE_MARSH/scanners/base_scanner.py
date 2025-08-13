# BaseScanner class defining the skeleton for scanning and reporting
# Following Template Method pattern as described in https://refactoring.guru/design-patterns/template-method/python/example
# TODO: Additional refinement is needed reduce redundancy in defined scanner

from abc import ABC, abstractmethod

from utils.sensitive_patterns import patterns

# File which report will be printed to.
outputTxtFile = "output.txt"

class BaseScanner(ABC):
    def __init__(self, file_path):
        self.file_path = file_path
        self.results = []
        self.patterns = patterns

    def scan(self):
        print("scanning...")
        content = self.load_file()
        self.process_lines(content)
        self.report()

    @abstractmethod
    def load_file(self):
        pass

    @abstractmethod
    def process_lines(self,content):
        pass

# Output findings to outputTxtFile
    def report(self):
        print("report")
        with open(outputTxtFile, "a") as f:
            f.write(f"Scan Results for {self.file_path}:")
        for line, ptype, match in self.results:
            with open(outputTxtFile, "a") as f:
                f.write(f"\nLine {line}: Found {ptype} → {match}")
