
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
    """ Manage main menu. """
    def __init__ (self, id1="", nombre="", cantidad="", blueprint="", comandos=list()):
        self.id1 = id1
        self.nombre = nombre
        self.blueprint = blueprint
        self.cantidad = cantidad
        self.comandos = comandos

    def getId(self):
        return self.id1

    def getCompleteCommand(self, idJugador):
        """ Returns complete command line with ID-PLAYER """
        cad1 = ""
        numComandos = len(self.comandos)
        if numComandos > 1:
            for parte in range(0, numComandos):
                cad_p =  self.comandos[parte]
                if parte == 1:
                    cad_p = '\"'+cad_p+'\"'
                if parte < (numComandos - 1):
                    cad1 += cad_p + ' ' + idJugador + ' '
                else:
                    cad1 += cad_p
        else:
            cad1 += self.comandos[0] + ' ' + idJugador + ' '

        if self.blueprint != "0":
            cad1 += ' \"'+self.blueprint+'\"'
        cad1 += ' '+self.cantidad+ ' 0 0' #EL PRIMER 0 SE DEBE CAMBIAR POR LA VARIABLE DE CALIDAD Y EL SEGUNDO 0 POR LA VARIABLE BLUEPRIN U OBJETO

        return cad1

    def getCadena(self):
        return str(self.id1) + ' ' + str(self.nombre) + ' ' + str(self.blueprint) + ' ' + str(self.cantidad) + ' ' + str(self.comandos)

class Commands_Paypoom:
    """ Commands to SEND using RCON """
    def __init__ (self, server_config):
        self.server_config = server_config
        self.lista_Item_Paypoom = list()
        self.listaComandos = list()
        self.listaComandos.append('/pooms')
        self.listaComandos.append('/add')
        print(self.server_config['lang']['string_14'])
        self.chargeFromURL(self.server_config['web_Datos']+'?act=items&ser='+self.server_config['idServer'])
        print(self.server_config['lang']['string_15'])

    def mostrarComandos2(self):
        for c1 in self.lista_Item_Paypoom:
            print(c1.getCadena())

    def chargeFromURL(self, datos):
        """ load items from a URL """
        respuesta = ur.urlopen(datos)
        datos = json.loads(respuesta.read().decode('utf-8'))
        for l1 in datos:
            comados2 = list()
            for l2 in datos[str(l1)]['comando']:
                comados2.append(str(datos[str(l1)]['comando'][l2]))
            obj1 = Item_Paypoom(str(datos[str(l1)]['id']), str(l1), str(datos[str(l1)]['precio']), str(datos[str(l1)]['blueprint']), comados2)
            #print(obj1.getCompleteCommand('IDPLAYER'))
            self.lista_Item_Paypoom.append(obj1)

    def chargeFromFile(self, datos):
        """ load items from a FILE """
        json_data = open(os.path.join(datos))
        datos = json.load(json_data)
        json_data.close()
        for l1 in datos:
            comados2 = list()
            for l2 in datos[str(l1)]['comando']:
                comados2.append(str(datos[str(l1)]['comando'][l2]))
            obj1 = Item_Paypoom(str(datos[str(l1)]['id']), str(l1), str(datos[str(l1)]['cantidad']), str(datos[str(l1)]['blueprint']), comados2)
            self.lista_Item_Paypoom.append(obj1)

    def getPosItem(self, id1):
        """ Returns the position of an Itmens """
        res_getPosItem = -1
        for pos1 in range(0, len(self.lista_Item_Paypoom)):
            if self.lista_Item_Paypoom[pos1].getId() == id1:
                res_getPosItem = pos1
        return res_getPosItem

    def interactDirectly(self):
        rcon = MCRcon()
        try:
            rcon.connect(self.server_config['ip'], int(self.server_config['rcon_port']))
            rcon.login(self.server_config['ServerAdminPassword'])
            try:
                while True:
                    response = rcon.command(input('> '))
                    if response:
                        print("  %s" % response)
            except KeyboardInterrupt:
                print("\n# disconnecting...")
            rcon.disconnect()
        except:
            print("\nError al conectar con el serbidor, compruebe que los datos del fichero server.conf son correctos.")

    def showMenssageToPlayer(self, idPlayer, mensage1):
        print('ServerChatTo "'+ idPlayer +'" ' + mensage1)
        self.executeCommand('ServerChatTo "'+ idPlayer +'" ' + mensage1)

    def executeCommand(self, comando1):
        print(comando1)
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
            print('add')
            serverPlayerID = cadena.split(' ')[2]
            print(serverPlayerID)
            p1, r1, i1 = self.spendPoints(cadena.split(' ')[1], serverPlayerID)
            print('p1='+p1+' r1='+r1+' i1='+i1)
            if p1 != "0":
                print('p1')
                if r1 == "yes":
                    print('r1')
                    print(self.lista_Item_Paypoom[int(i1)].getCompleteCommand(serverPlayerID))
                    self.executeCommand(self.lista_Item_Paypoom[int(i1)].getCompleteCommand(serverPlayerID))
                    #posItem = self.getPosItem(i1)
                    posItem = 1
                    print('Pos item = '+ srt(posItem))
                    if posItem >= 0:
                        print(self.server_config['lang']['string_13'])
                        print(self.lista_Item_Paypoom[posItem].getCompleteCommand(serverPlayerID))
                        #self.showMenssageToPlayer(p1, self.server_config['lang']['string_13'])
                        #self.executeCommand(self.lista_Item_Paypoom[posItem].getCompleteCommand(serverPlayerID))
                    else:
                        #self.showMenssageToPlayer(p1, self.server_config['lang']['string_11'])
                        print(self.server_config['lang']['string_11'])
                else:
                    #self.showMenssageToPlayer(p1, self.server_config['lang']['string_12'])
                    print(self.server_config['lang']['string_12'])
            else:
                #self.showMenssageToPlayer(p1, self.server_config['lang']['string_12'])
                print(self.server_config['lang']['string_12'])
        else:
            print('No es un comando')

    def spendPoints(self, cadena, serverPlayerID):
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
