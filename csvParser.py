from pathlib import Path
from tkinter import filedialog, messagebox

import pandas as pd


def browser():
    rawPath = filedialog.askopenfilename(
        initialdir="/",
        title="Select a CSV file",
        filetypes=(("CSV document", "*.csv"),),
    )

    if not rawPath:
        print("Cancelado por usuario.")
        return None

    filepath = Path(rawPath)

    if filepath.suffix.lower() != ".csv":
        messagebox.showerror(
            "Error de archivo",
            f"Err: Archivo esperado era CSV, pero se recibio un archivo {filepath.suffix}.",
        )
        return None

    return pd.read_csv(filepath)
