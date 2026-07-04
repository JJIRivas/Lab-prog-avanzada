from pathlib import Path
from tkinter import filedialog, messagebox


def browseFile() -> Path | None:
    rawPath = filedialog.askopenfilename(
        initialdir="/",
        title="Select a file",
        filetypes=(("CSV document", "*.csv"), ("JSON document", "*.json")),
    )

    if not rawPath:
        print("Cancelado por usuario.")
        return None

    filepath = Path(rawPath)
    suffix = filepath.suffix.lower()

    if suffix not in [".csv", ".json"]:
        messagebox.showerror(
            "Error de archivo",
            f"Err: Archivo esperado era CSV o JSON, pero se recibió {suffix}.",
        )
        return None

    return filepath
