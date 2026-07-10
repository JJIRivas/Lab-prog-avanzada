from pathlib import Path
from tkinter import filedialog, messagebox


# Clase "interlazada" con la UI. Se dedica a abrir la ventana para seleccionar un archivo como tal, y verificar si es el formato adecuado.
# no esta en el archivo de UI porque maneja mas cercanamente con archivos, por lo que creo que es mas relevante dejarla en fileHandlers.
def browseFile() -> Path | None:
    rawPath = filedialog.askopenfilename(
        initialdir="/home/gyga/Downloads",  # Se coloco root, aunque idealmente deberia cambiarse a /home/$USER/... no estoy seguro como si. Ademas, si se corre en Windows o Mac puede ser diferente. Es cosa de cambiar la ruta de inicio simplemente.
        title="Selecciona un archivo",
        filetypes=(("CSV document", "*.csv"), ("JSON document", "*.json")),
    )

    if not rawPath:
        print("Cancelado por usuario.")
        return None

    filepath = Path(rawPath)
    suffix = filepath.suffix.lower()

    # En teoria, por como TKinter maneja la seleccion de archivos con filetypes="", no se deberia poder seleccionar un archivo de un formato incorrecto- pero
    # se agrego eso de todas maneras por algun edge case. Por si acaso.
    if suffix not in [".csv", ".json"]:
        messagebox.showerror(
            "Error de archivo",
            f"Err: Archivo esperado era CSV o JSON, pero se recibió {suffix}.",
        )
        return None

    return filepath
