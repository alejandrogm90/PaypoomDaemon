
import os
import sys
import json
import hashlib

from .MCRcon import MCRcon
try:
    import urllib.request as ur
except:
    import urllib as ur

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

class Comandos:

    def __init__ (self, datos, server_config):
        self.server_config = server_config
        json_data = open(os.path.join(datos))
        datos = json.load(json_data)
        json_data.close()
        self.listObjetos = list()
        for l1 in datos:
            comados2 = list()
            for l2 in datos[str(l1)]['comando']:
                comados2.append(str(datos[str(l1)]['comando'][l2]))
            obj1 = Objeto(str(l1), str(datos[str(l1)]['precio']), str(datos[str(l1)]['blueprint']), comados2)
            self.listObjetos.append(obj1)

        self.listaComandos = list()
        self.listaComandos.append('/pooms')
        self.listaComandos.append('/add')

    def mostrarObjetos(self):
        for l1 in self.listObjetos:
            print(l1)

    def mostrarMensageAJugador(self, idPlayer, mensage1):
        rcon = MCRcon()
        rcon.connect(self.server_config['ip'], int(self.server_config['rcon_port']))
        rcon.login(self.server_config['ServerAdminPassword'])
        response = rcon.command('ServerChatToPlayer "'+ idPlayer +'" ' + mensage1 )
        rcon.disconnect()

    def esComandoCorrecto(self, cadena):
        for cmd1 in self.listaComandos:
            if cadena.startswith(cmd1):
                return True
        return False

    ##=========================================================
    ##                    COMANDOS
    ##=========================================================

    def ejecutarComando(self, idPlayer, cadena):
        if cadena.split(' ')[0] == self.listaComandos[0]:
            #self.mostrarMensageAJugador("Bro", "Hola")
            self.mostrarPuntos(idPlayer)
        elif cadena.split(' ')[0] == self.listaComandos[1]:
            print('add')
        else:
            print('No es un comando')

    def mostrarPuntos(self, idPlayer):
        puntos = 0
        token = hashlib.md5()
        token.update((idPlayer+self.server_config['token']).encode('utf-8'))
        pass1 = token.hexdigest()
        cadena = self.server_config['web_Datos'] + '?act=pooms&idp=76561198004070725&ser=' + self.server_config['idServer'] + '&pas=' + pass1 + '&format=json'
        respuesta = ur.urlopen(cadena)
        datos = json.loads(respuesta.read().decode('utf-8'))
        puntos = datos['pooms']
        self.mostrarMensageAJugador(idPlayer, "Tus puntos acumulados son: "+str(puntos))
