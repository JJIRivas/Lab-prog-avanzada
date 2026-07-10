import json
from pathlib import Path

import pandas as pd


# Clase que se dedica a verificar si el archivo es CSV o JSON, devuelve la informacion relevante.
class fileReader:
    @staticmethod
    def leer(filepath):
        filepath = Path(filepath)
        suffix = filepath.suffix.lower()

        # NOTA: Se ocupa dict aqui y cuando se trabaja con el archivo- pero esto se decidio porque la libreria JSON trabaja con estos, y pasar de un DataFrame de pandas
        # a un dict es facil- lo que bajo la complejidad del codigo para manejar archivos. Es de notar que dict NO es ocupado para manejar los incidentes una vez guardados,
        # sino que la tabla hash creada por mi cuenta, como se pide (igual, solo se menciona este requerimiento en esa parte, por lo que dict en otras partes no es mencionado si
        # es ok o no).
        if suffix == ".csv":
            return pd.read_csv(filepath).to_dict("records")
        elif suffix == ".json":
            with open(filepath, "r") as file:
                return json.load(file)
        else:
            # Igual que en fileBrowser, en teoria no se podria llegar aqui- pero se agrego por si acaso.
            raise ValueError(f"Extensión no soportada: {suffix}")
