
import os
import sys
import json
import hashlib

from .MCRcon import MCRcon
try:
    import urllib.request as ur
except:
    import urllib as ur

class Item_Paypoom:

    def __init__ (self, id1="",nombre="", precio="", blueprint="", comandos=list()):
        self.id1 = id1
        self.nombre = nombre
        self.blueprint = blueprint
        self.precio = precio
        self.comandos = comandos

    def getId(self):
        return self.id1

    def getName(self):
        return self.nombre

    def getPrice(self):
        return self.precio

    def getBlueprint(self):
        return self.blueprint

    def getCommand(self):
        return self.comandos

    def getCompleteCommand(self, idJugador):
        cad1 = ""
        numComandos = len(self.comandos)
        if numComandos > 1:
            for parte in range(0, numComandos):
                if parte < (numComandos - 1):
                    cad1 += self.comandos[parte] + ' ' + idJugador + ' '
                else:
                    cad1 += self.comandos[parte]
        else:
            cad1 += self.comandos[0] + ' ' + idJugador
        if self.blueprint != "0":
            cad1 += ' '+self.blueprint
        return cad1


    def getString(self):
        res = self.nombre + ' - ' + self.precio + ' - ' + self.blueprint
        for ln1 in self.comandos:
            res += ' - ' + ln1
        return res

class Commands_Paypoom:

    def __init__ (self, server_config):
        self.server_config = server_config
        self.lista_Item_Paypoom = list()
        self.listaComandos = list()
        self.listaComandos.append('/pooms')
        self.listaComandos.append('/add')
        # Cargo los datos
        self.chargeFromURL(self.server_config['web_Datos']+'?act=items&ser='+self.server_config['idServer'])

    def chargeFromURL(self, datos):
        respuesta = ur.urlopen(datos)
        datos = json.loads(respuesta.read().decode('utf-8'))
        for l1 in datos:
            comados2 = list()
            for l2 in datos[str(l1)]['comando']:
                comados2.append(str(datos[str(l1)]['comando'][l2]))
            obj1 = Item_Paypoom(str(datos[str(l1)]['id']), str(l1), str(datos[str(l1)]['precio']), str(datos[str(l1)]['blueprint']), comados2)
            print(obj1.getString())
            print(obj1.getCompleteCommand('235345245'))
            self.lista_Item_Paypoom.append(obj1)

    def chargeFromFile(self, datos):
        print("Cargando la lista de ITEMS ......")
        json_data = open(os.path.join(datos))
        datos = json.load(json_data)
        json_data.close()
        for l1 in datos:
            comados2 = list()
            for l2 in datos[str(l1)]['comando']:
                comados2.append(str(datos[str(l1)]['comando'][l2]))
            obj1 = Item_Paypoom(str(datos[str(l1)]['id']), str(l1), str(datos[str(l1)]['precio']), str(datos[str(l1)]['blueprint']), comados2)
            self.lista_Item_Paypoom.append(obj1)
        print("Lista de ITEMS cargada.")

    def getPosItem(self, id1):
        res = -1
        for pos1 in range(len(self.lista_Item_Paypoom)):
            if self.lista_Item_Paypoom[pos1].getId() == id1:
                res = pos1
        return res

    def interactDirectly(self):
        rcon = MCRcon()
        try:
            mcrcon1.connect(self.server_config['ip'], int(self.server_config['rcon_port']))
            mcrcon1.login(self.server_config['ServerAdminPassword'])
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

    def showMenssageToPlayer(self, idPlayer, mensage1):
        self.executeCommand('ServerChatTo "'+ idPlayer +'" ' + mensage1)

    def executeCommand(self, comando1):
        rcon = MCRcon()
        rcon.connect(self.server_config['ip'], int(self.server_config['rcon_port']))
        rcon.login(self.server_config['ServerAdminPassword'])
        response = rcon.command(comando1)
        rcon.disconnect()
        return response

    def getPlayerIDForSteamID(self, idSteam):
        return self.executeCommand('GetPlayerIDForSteamID '+ idSteam)

    def getSteamIDForPlayerID(self, idPlayer):
        return self.executeCommand('GetSteamIDForPlayerID '+ idPlayer)

    def isRigthCommand(self, cadena):
        for cmd1 in self.listaComandos:
            if cadena.startswith(cmd1):
                return True
        return False

    ##=========================================================
    ##                    COMMANDS
    ##=========================================================

    def interpreteACommand(self, cadena):
        if cadena.split(' ')[0] == self.listaComandos[0]:
            print('pooms')
        elif cadena.split(' ')[0] == self.listaComandos[1]:
            p1, r1, i1 = self.spendPoints(cadena.split(' ')[1])
            if p1 != "0":
                if r1 == "yes":
                    posItem = self.getPosItem(i1)
                    if posItem >= 0:
                        self.showMenssageToPlayer(p1, self.server_config['lang']['string_13'])
                        self.executeCommand(self.lista_Item_Paypoom[posItem].getCompleteCommand(p1))
                    else:
                        self.showMenssageToPlayer(p1, self.server_config['lang']['string_11'])
                else:
                    self.showMenssageToPlayer(p1, self.server_config['lang']['string_12'])
        else:
            print('No es un comando')

    def spendPoints(self, cadena):
        token = hashlib.md5()
        token.update((cadena+self.server_config['token']).encode('utf-8'))
        pass1 = token.hexdigest()
        cadena = self.server_config['web_Datos'] + '?act=spend&ser=' + self.server_config['idServer'] + '&tok=' + cadena + '&cla=' + pass1 + '&format=json'
        print(cadena)
        respuesta = ur.urlopen(cadena)
        datos = json.loads(respuesta.read().decode('utf-8'))
        try:
            p1 = datos['player']
            r1 = datos['res']
            i1 = datos['item']
        except:
            # En caso enviar algo que no tenga sentido.
            p1 = "0"
            r1 = datos['error']
            i1 = datos['numError']
        return p1, r1, i1

    def getPoints(self, idPlayer):
        token = hashlib.md5()
        token.update((idPlayer+self.server_config['token']).encode('utf-8'))
        pass1 = token.hexdigest()
        cadena = self.server_config['web_Datos'] + '?act=pooms&idp='+idPlayer+'&ser=' + self.server_config['idServer'] + '&pas=' + pass1 + '&format=json'
        respuesta = ur.urlopen(cadena)
        datos = json.loads(respuesta.read().decode('utf-8'))
        puntos = datos['pooms']
        self.showMenssageToPlayer(idPlayer, "Tus puntos acumulados son: "+str(puntos))
