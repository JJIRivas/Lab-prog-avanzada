from pathlib import Path

from fileHandlers import csvParser, jsonParser


def getParser(filepath: Path):
    suffix = filepath.suffix.lower()

    if suffix == ".csv":
        return csvParser.csvParser()
    elif suffix == ".json":
        return jsonParser.jsonParser()

    raise ValueError(f"Extensión no soportada: {suffix}")
