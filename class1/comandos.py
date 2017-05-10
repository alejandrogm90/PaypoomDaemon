#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import urllib
from .objeto import Objeto

class Comandos:

    def mostrarObjetos(self):
        for l1 in self.listObjetos:
            print(l1)

    def esComandoCorrecto(self, cadena):
        for cmd1 in self.listaComandos:
            if cadenacadena.startswith(cmd1):
                return True
        return False

    def __init__ (self, datos, server_config):
        #self.webDatos = 'http://www.paypoom.com/datos.php';
        self.server_config = server_config
        self.webDatos = 'http://localhost/arkunamatata/datos.php';
        json_data = open(os.path.join(datos))
        datos = json.load(json_data)
        json_data.close()
        self.listObjetos = list()
        for l1 in datos:
            comados2 = list()
            for l2 in datos[str(l1)]['comando']:
                #print(datos[str(l1)]['comando'][l2])
                comados2.append(str(datos[str(l1)]['comando'][l2]))
            obj1 = Objeto(str(l1), str(datos[str(l1)]['precio']), str(datos[str(l1)]['blueprint']), comados2)
            self.listObjetos.append(obj1)

        self.listaComandos = list()
        self.listaComandos.append('/pooms')
        self.listaComandos.append('/add')

    ##=========================================================
    ##                    COMANDOS
    ##=========================================================

    def ejecutarComando(self, cadena):
        for cmd1 in self.listaComandos:
            if cadena.startswith(cmd1):
                if cmd1 == self.listaComandos[0]:
                    self.mostrarPuntos(1)
                elif cmd1 == self.listaComandos[1]:
                    print('add')
                else:
                    print('Error')

    def mostrarPuntos(self, idPlayer):
        puntos = 0
        print(self.webDatos + '?act=pooms&idp=' + str(idPlayer) + '&ser=' + self.server_config['group'] + '&format=json')
        respuesta = urllib.request.urlopen(self.webDatos + '?act=pooms&idp=' + str(idPlayer) + '&ser=' + self.server_config['group'] + '&format=json')
        pagina = respuesta.read()
        encoding = respuesta.info().get_content_charset('utf-8')
        datos = json.load(pagina.decode(encoding))

        #puntos = datos['coins']
        print(str(puntos))
        return puntos
