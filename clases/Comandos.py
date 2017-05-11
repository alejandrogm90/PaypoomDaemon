
import os
import json
import urllib

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

    def mostrarObjetos(self):
        for l1 in self.listObjetos:
            print(l1)

    def esComandoCorrecto(self, cadena):
        for cmd1 in self.listaComandos:
            if cadena.startswith(cmd1):
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
        datos = json.loads(respuesta.read().decode('utf-8'))
        puntos = datos['pooms']
        print(str(puntos))
        return puntos
