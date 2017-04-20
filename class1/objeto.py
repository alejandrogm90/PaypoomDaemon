import os
import json

class Objeto:

    def __init__ (self, nombre, precio, comando):
        self.nombre = nombre
        self.precio = precio
        self.comando = comando

    def getNombre(self):
        return self.nombre

    def getPrecio(self):
        return self.precio

    def getComando(self):
        return self.comando

    def mostrarObjeto(self):
        print(self.nombre + ' - ' + self.precio + ' - ' + self.comando)
