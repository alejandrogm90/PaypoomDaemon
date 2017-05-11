import os
import json

class Objeto:

    def __init__ (self, nombre="", precio="", blueprint="", comandos=list()):
        self.nombre = nombre
        self.blueprint = blueprint
        self.precio = precio
        self.comandos = comandos

    def getNombre(self):
        return self.nombre

    def getPrecio(self):
        return self.precio

    def getBlueprint(self):
        return self.blueprint

    def getComandos(self):
        return self.comandos

    def mostrarObjeto(self):
        res = self.nombre + ' - ' + self.precio + ' - ' + self.blueprint
        for ln1 in self.comandos:
            res += ' - ' + ln1
        return res
