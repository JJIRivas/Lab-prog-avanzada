import pandas as pd

from fileHandlers import baseParser


class csvParser(baseParser.parser):
    def __init__(self):
        super().__init__()

    def parseFile(self, filepath):
        records = pd.read_csv(filepath).to_dict("records")
        return super().parseFile(records)
