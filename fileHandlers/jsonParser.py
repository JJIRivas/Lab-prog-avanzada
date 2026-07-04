import json

from fileHandlers import baseParser


class jsonParser(baseParser.parser):
    def __init__(self):
        super().__init__()

    def parseFile(self, filepath):
        with open(filepath, "r") as file:
            return super().parseFile(json.load(file))
