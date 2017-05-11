#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import json
import urllib
import time
import platform
#import signal
import subprocess
#import psutil

from class1.mcrcon import MCRcon
from class1.serverARK import serverArk
from class1.comandos import Comandos
from class1.objeto import Objeto

def leerConsola(server_config, mcrcon1, cmd1):
    print("\n# connecting...")
    try:
        while True:
            time.sleep(5)
            mcrcon1.connect(server_config['SessionName'], int(server_config['rcon_port']))
            response = mcrcon1.command('getchat')
            mcrcon1.disconnect()
            if response != "Server received, But no response!!":
                for linea1 in response:
                    cadena1 = linea1.split(':')[1].lstrip(" ")
                    if cmo1.esComandoCorrecto(cadena1):
                        print(cadena1)

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
            server1 = serverArk(server_config['ip'], int(server_config['rcon_port']), server_config['ServerAdminPassword'] )
        except:
            print("El fichero server_ARK.json no ha podido ser cargado.")
            exit(2)
    else:
        print("El fichero server_ARK.json no existe.")
        exit(1)

    # Carga de los Objetos
    if os.path.isfile(os.path.join('objetos.json')):
        try:
            cmo1 = Comandos("objetos.json", server_config)
        except:
            print("El fichero objetos.json no ha podido ser cargado.")
            exit(4)
    else:
        print("El fichero objetos.json no existe.")
        exit(3)

    cadena = "/add 5pooms"
    """
    if platform.system() == "Windows":
        print('w')
        pid1 = subprocess.Popen('dir', shell=False)
    else:
        print('l')
        pid1 = subprocess.Popen('ls', shell=False)
    """

    mcrcon1.connect(server_config['SessionName'], int(server_config['rcon_port']))
    response = mcrcon1.command('getchat')
    mcrcon1.disconnect()
    #response = {"Falcon90 (Mr-Trauma): /pooms","Falcon90 (Mr-Trauma): hola a todos","Falcon90 (Mr-Trauma): /add 5pooms"}
    if response != "Server received, But no response!!":
        for linea1 in response:
            cadena1 = linea1.split(':')[1].lstrip(" ")
            if cmo1.esComandoCorrecto(cadena1):
                print(cadena1)
