
import os
import sys
import json
import hashlib

from .MCRcon import MCRcon
try:
    import urllib.request as ur
except:
    import urllib as ur

class Items_Dinos:

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

    def mostrarItems_Dinos(self):
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
        self.lista_Items_Dinos = list()
        for l1 in datos:
            comados2 = list()
            for l2 in datos[str(l1)]['comando']:
                comados2.append(str(datos[str(l1)]['comando'][l2]))
            obj1 = Items_Dinos(str(l1), str(datos[str(l1)]['precio']), str(datos[str(l1)]['blueprint']), comados2)
            self.lista_Items_Dinos.append(obj1)

        self.listaComandos = list()
        self.listaComandos.append('/pooms')
        self.listaComandos.append('/add')

    def mostrarObjetos(self):
        for l1 in self.lista_Items_Dinos:
            print(l1)

    def mostrarMensageAJugador(self, idSteam, mensage1):
        rcon = MCRcon()
        rcon.connect(self.server_config['ip'], int(self.server_config['rcon_port']))
        rcon.login(self.server_config['ServerAdminPassword'])
        response = rcon.command('ServerChatTo "'+ idPlayer +'" ' + mensage1 )
        rcon.disconnect()

    def getPlayerIDForSteamID(self, idSteam):
        rcon = MCRcon()
        rcon.connect(self.server_config['ip'], int(self.server_config['rcon_port']))
        rcon.login(self.server_config['ServerAdminPassword'])
        response = rcon.command('GetPlayerIDForSteamID '+ idSteam)
        rcon.disconnect()
        return response

    def getSteamIDForPlayerID(self, idPlayer):
        rcon = MCRcon()
        rcon.connect(self.server_config['ip'], int(self.server_config['rcon_port']))
        rcon.login(self.server_config['ServerAdminPassword'])
        response = rcon.command('GetSteamIDForPlayerID '+ idPlayer)
        rcon.disconnect()
        return response

    def esComandoCorrecto(self, cadena):
        for cmd1 in self.listaComandos:
            if cadena.startswith(cmd1):
                return True
        return False

    ##=========================================================
    ##                    COMANDOS
    ##=========================================================

    def ejecutarComando(self, cadena):
        if cadena.split(' ')[0] == self.listaComandos[0]:
            print('pooms')
            #self.mostrarPuntos(idPlayer)
            #self.mostrarMensageAJugador("Bro", "Hola")
        elif cadena.split(' ')[0] == self.listaComandos[1]:
            p1, r1 = self.gastarPuntos(cadena.split(' ')[1])
            if r1 == "yes":
                self.mostrarMensageAJugador(p1,"Correcto.")
            else:
                self.mostrarMensageAJugador(p1,"No tienes puntos.")
        else:
            print('No es un comando')

    def gastarPuntos(self, cadena):
        token = hashlib.md5()
        token.update((cadena+self.server_config['token']).encode('utf-8'))
        pass1 = token.hexdigest()
        cadena = self.server_config['web_Datos'] + '?act=spend&ser=' + self.server_config['idServer'] + '&tok=' + cadena + '&cla=' + pass1 + '&format=json'
        respuesta = ur.urlopen(cadena)
        datos = json.loads(respuesta.read().decode('utf-8'))
        p1 = datos['player']
        r1 = datos['res']
        return p1, r1

    def getPuntos(self, idPlayer):
        token = hashlib.md5()
        token.update((idPlayer+self.server_config['token']).encode('utf-8'))
        pass1 = token.hexdigest()
        cadena = self.server_config['web_Datos'] + '?act=pooms&idp='+idPlayer+'&ser=' + self.server_config['idServer'] + '&pas=' + pass1 + '&format=json'
        respuesta = ur.urlopen(cadena)
        datos = json.loads(respuesta.read().decode('utf-8'))
        puntos = datos['pooms']
        self.mostrarMensageAJugador(idPlayer, "Tus puntos acumulados son: "+str(puntos))
