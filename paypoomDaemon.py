#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import json
import urllib
import time
import platform
import subprocess

from clases.Comandos import Comandos
from clases.MCRcon import MCRcon
from clases.ServerArk import ServerArk

def leerConsola(server_config, mcrcon1, cmd1):
    print("\n# connecting...")
    try:
        while True:
            time.sleep(2)
            mcrcon1.connect(server_config['ip'], int(server_config['rcon_port']))
            response = mcrcon1.command('getchat')
            mcrcon1.disconnect()
            if response != "Server received, But no response!!":
                for linea1 in response:
                    idPlayer = cadena.split(' ')[0].split('(')[0]
                    cadena1 = linea1.split(':')[1].lstrip(" ")
                    if cmo1.esComandoCorrecto(cadena1):
                        cmo1.ejecutarComando(cadena1)
                        print("El jugador "+idPlayer+" ha ejecutado un comando")

    except KeyboardInterrupt:
        print("\n# disconnecting...")

if __name__ == '__main__':
    mcrcon1 = MCRcon()
    # Carga la configuracion
    if os.path.isfile(os.path.join('server_ARK.json')):
        try:
            json_data = open(os.path.join('server_ARK.json'))
            server_config = json.load(json_data)
            json_data.close()
            server1 = ServerArk(server_config['ip'], int(server_config['rcon_port']), server_config['ServerAdminPassword'] )
        except:
            print("El fichero server_ARK.json no ha podido ser cargado.")
            exit(2)
    else:
        print("El fichero server_ARK.json no existe.")
        exit(1)

    # Carga de los Objetos
    if os.path.isfile(os.path.join('objetos.json')):
        try:
            cmd1 = Comandos("objetos.json", server_config)
        except:
            print("El fichero objetos.json no ha podido ser cargado.")
            exit(4)
    else:
        print("El fichero objetos.json no existe.")
        exit(3)

    leerConsola(server_config, mcrcon1, cmd1)
