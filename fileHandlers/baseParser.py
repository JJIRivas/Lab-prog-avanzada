from fileHandlers import fileReader


# Clase padre para los parsers, define comportamiento base para manejar el archivo, pero no el como parsear como tal.
class parser:
    # Funcion que retorna los datos del archivo. Es necesaria ya que no sabemos si el archivo es JSON o CSV, por eso esta funcion sirve para llamar a fileReader, el
    # cual devuelve la informacion de manera correcta.
    def parseFile(self, filepath):
        data = fileReader.fileReader.leer(filepath)
        return self.parse(data)

    def parse(self, data):
        raise NotImplementedError
