#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import json
import urllib.request
import time

from class1.mcrcon import MCRcon
from class1.serverARK import serverArk
from class1.comandos import Comandos
from class1.objeto import Objeto

def leerConsola():
    comandos1 = Comandos("objetos.json")
    print("\n# connecting...")
    try:
        while True:
            time.sleep(5)
            response = rcon.command('getchat')
            if response:
                print(response)

    except KeyboardInterrupt:
        print("\n# disconnecting...")


if __name__ == '__main__':
    # Carga la configuracion
    if os.path.isfile(os.path.join('server_ARK.json')):
        json_data = open(os.path.join('server_ARK.json'))
        server_config = json.load(json_data)
        json_data.close()
        server1 = serverArk(server_config['ip'], int(server_config['rcon_port']), server_config['ServerAdminPassword'] )
    else:
        print("El fichero server_ARK.json no existe.")
        exit(1)

    #server1.connect()
    """
    pagina = urllib.request.urlopen("http://localhost/arkunamatata/datos.php?idplayer=1&format=json").read()
    datos = json.loads(pagina.decode('utf-8'))
    print(datos['puntos'])
    """

    cadena = "/comprar quitina"

    cmo1 = Comandos("objetos.json", server_config)

    cmo1.ejecutarComando('/pooms')
