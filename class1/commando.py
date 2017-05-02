import os
import json
import urllib.request

class Commando:

    def __init__ (self, datos):
        json_data = open(os.path.join(datos))
        self.datos = json.load(json_data)
        json_data.close()
        self.listObjetos = list()
        print(self.datos)
        for l1 in self.datos:
            self.listObjetos.append(Objeto(srt(l1) ,l1['precio'], l1['comando']))
        #    print(Objeto(srt(l1) + ' - ' + self.datos[l1]['precio'] + ' - ' + self.datos[l1]['comando']))
        self.listaComandos = list()
        self.listaComandos.append('/puntos')
        self.listaComandos.append('/comprar')


    def mostrarObjetos(self):
        for l1 in self.listObjetos:
            print(l1)

    def esComandoCorrecto(self, cadena):
        for cmd1 in self.listaComandos:
            if cadenacadena.startswith(cmd1):
                return True
        return False
