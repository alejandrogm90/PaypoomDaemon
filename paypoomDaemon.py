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

def interactuar(host, port, password):
    rcon = MCRcon()

    print("# connecting to %s:%i..." % (host, port))
    rcon.connect(host, port)

    print("# logging in...")
    rcon.login(password)
    try:
        while True:
            response = rcon.command(input('> '))
            if response:
                print("  %s" % response)
    except KeyboardInterrupt:
        print("\n# disconnecting...")
    rcon.disconnect()

def leerConsola(server_config, mcrcon1, cmd1):
    print("\n# connecting...")
    try:
        mcrcon1.connect(server_config['ip'], int(server_config['rcon_port']))
        mcrcon1.login(server_config['ServerAdminPassword'])
        while True:
            time.sleep(5)
            response = mcrcon1.command('getchat')
            if "Server received, But no response!!" not in response:
                for linea1 in response.split("\n"):
                    print(linea1)
                    try:
                        idPlayer = response.split(' ')[0]
                        cadena1 = linea1.split(':')[1].lstrip(" ")
                        cmd1.ejecutarComando(idPlayer,cadena1)
                        #if cmd1.esComandoCorrecto(cadena1):
                        #    cmd1.ejecutarComando(idPlayer,cadena1)
                    except :
                        pass
            else:
                print("\n vacio...")
    except KeyboardInterrupt:
        mcrcon1.disconnect()
        print("\n# disconnecting.mi..")

if __name__ == '__main__':
    mcrcon1 = MCRcon()
    # Carga la configuracion
    if os.path.isfile(os.path.join('server_ARK.json')):
        try:
            json_data = open(os.path.join('server_ARK.json'))
            server_config = json.load(json_data)
            json_data.close()
            server1 = ServerArk(server_config['ip'], int(server_config['rcon_port']), server_config['ServerAdminPassword'])
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
    #cmd1.mostrarMensageAJugador("Bro", "Hola")
    #cmd1.mostrarPuntos("Bro")
    leerConsola(server_config, mcrcon1, cmd1)
    #interactuar(server_config['ip'], int(server_config['rcon_port']), server_config['ServerAdminPassword'])
