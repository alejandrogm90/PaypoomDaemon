
import os
import sys
import json
import hashlib

from .MCRcon import MCRcon
try:
    import urllib.request as ur
except:
    import urllib as ur

class Item_dino:

    def __init__ (self, id1="",nombre="", precio="", blueprint="", comandos=list()):
        self.id1 = id1
        self.nombre = nombre
        self.blueprint = blueprint
        self.precio = precio
        self.comandos = comandos

    def getId(self):
        return self.id1

    def getNombre(self):
        return self.nombre

    def getPrecio(self):
        return self.precio

    def getBlueprint(self):
        return self.blueprint

    def getComandos(self):
        return self.comandos

    def mostrarItem_dino(self):
        res = self.nombre + ' - ' + self.precio + ' - ' + self.blueprint
        for ln1 in self.comandos:
            res += ' - ' + ln1
        return res

    def getCadena(idJugador):
        cad1 = ""
        for parte in range(len(self.comandos)):
            if parte < (len(self.comandos) - 1):
                cad1 += self.comandos[parte] + idJugador
            else:
                cad1 += self.comandos[parte]

class Comandos:

    def __init__ (self, datos, server_config):
        self.server_config = server_config
        json_data = open(os.path.join(datos))
        datos = json.load(json_data)
        json_data.close()
        self.lista_Item_dino = list()
        for l1 in datos:
            comados2 = list()
            for l2 in datos[str(l1)]['comando']:
                comados2.append(str(datos[str(l1)]['comando'][l2]))
            obj1 = Item_dino(str(datos[str(l1)]['id']), str(l1), str(datos[str(l1)]['precio']), str(datos[str(l1)]['blueprint']), comados2)
            self.lista_Item_dino.append(obj1)

        self.listaComandos = list()
        self.listaComandos.append('/pooms')
        self.listaComandos.append('/add')

    def getPosItemDino(id1):
        res = -1
        for pos1 in range(len(self.lista_Item_dino)):
            if self.lista_Item_dino[pos1].getId() == id1:
                res = pos1
        return res

    def interactuarDirectamente():
        rcon = MCRcon()
        try:
            mcrcon1.connect(server_config['ip'], int(server_config['rcon_port']))
            mcrcon1.login(server_config['ServerAdminPassword'])
        except:
            print("\nError al conectar con el serbidor, compruebe que los datos del fichero server.conf son correctos.")
        try:
            while True:
                response = rcon.command(input('> '))
                if response:
                    print("  %s" % response)
        except KeyboardInterrupt:
            print("\n# disconnecting...")
        rcon.disconnect()

    def mostrarObjetos(self):
        for l1 in self.lista_Item_dino:
            print(l1)

    def mostrarMensageAJugador(self, idSteam, mensage1):
        rcon = MCRcon()
        rcon.connect(self.server_config['ip'], int(self.server_config['rcon_port']))
        rcon.login(self.server_config['ServerAdminPassword'])
        response = rcon.command('ServerChatTo "'+ idPlayer +'" ' + mensage1 )
        rcon.disconnect()

    def ejecutarUnComando(self, comando1):
        rcon = MCRcon()
        rcon.connect(self.server_config['ip'], int(self.server_config['rcon_port']))
        rcon.login(self.server_config['ServerAdminPassword'])
        response = rcon.command(comando1)
        rcon.disconnect()
        return response

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
            #self.mostrarMensageAJugador("543098457304530", "Hola")
        elif cadena.split(' ')[0] == self.listaComandos[1]:
            p1, r1, i1 = self.gastarPuntos(cadena.split(' ')[1])
            if r1 == "yes":
                self.mostrarMensageAJugador(p1,"Correcto.")
                posItem = self.getPosItemDino(i1)
                if posItem >= 0:
                    self.ejecutarComando(self.lista_Item_dino[posItem].getCadena(p1))
                else:
                    self.mostrarMensageAJugador(p1,"Error: el ID del Item no existe, contacta con el ADMIN.")
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
        i1 = datos['item']
        return p1, r1, i1

    def getPuntos(self, idPlayer):
        token = hashlib.md5()
        token.update((idPlayer+self.server_config['token']).encode('utf-8'))
        pass1 = token.hexdigest()
        cadena = self.server_config['web_Datos'] + '?act=pooms&idp='+idPlayer+'&ser=' + self.server_config['idServer'] + '&pas=' + pass1 + '&format=json'
        respuesta = ur.urlopen(cadena)
        datos = json.loads(respuesta.read().decode('utf-8'))
        puntos = datos['pooms']
        self.mostrarMensageAJugador(idPlayer, "Tus puntos acumulados son: "+str(puntos))
