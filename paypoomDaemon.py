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

def leerConsola(server_config, mcrcon1, cmd1):
    print("\n# Pulsa Ctrl+c para salir.")
    print("\n# connecting...")
    try:
        try:
            mcrcon1.connect(server_config['ip'], int(server_config['rcon_port']))
            mcrcon1.login(server_config['ServerAdminPassword'])
        except:
            print("\nError al conectar con el serbidor, compruebe que los datos del fichero server.conf son correctos.")
            exit(1)
        while True:
            time.sleep(5)
            response = mcrcon1.command('getchat')
            if "Server received, But no response!!" not in response:
                for linea1 in response.split("\n"):
                    print(linea1)
                    try:
                        #idPlayer = response.split(' ')[0]
                        cadena1 = linea1.split(':')[1].lstrip(" ")
                        if cmd1.esComandoCorrecto(cadena1):
                            cmd1.ejecutarComando(cadena1)
                    except :
                        pass
            else:
                print("\n vacio...")
    except KeyboardInterrupt:
        mcrcon1.disconnect()
        print("\n# disconnecting...")

if __name__ == '__main__':
    mcrcon1 = MCRcon()

    # Carga la configuracion
    if os.path.isfile(os.path.join('server.json')):
        try:
            json_data = open(os.path.join('server.json'))
            server_config = json.load(json_data)
            json_data.close()
        except:
            print("El fichero server.json no ha podido ser cargado.")
            exit(2)
    else:
        print("El fichero server.json no existe.")
        exit(1)
    # Carga de los Items_Dinos
    if os.path.isfile(os.path.join('objetos.json')):
        try:
            cmd1 = Comandos("objetos.json", server_config)
        except:
            print("El fichero objetos.json no ha podido ser cargado.")
            exit(4)
    else:
        print("El fichero objetos.json no existe.")
        exit(3)

    if len(sys.argv) > 1:
        if len(sys.argv) > 3 or sys.argv[1] != "-d" and sys.argv[1] != "--debug-mode" and sys.argv[1] != "-cl" and sys.argv[1] != "--command-line" :
            print("ERROR - parametros erroneos.")
            print("-d  \t--debug-mode   \t\tModo para depurar.")
            print("-cl \t--command-line \t\tConsulta el tercer parámetro del argumento en una sola línea.")
        else:
            if sys.argv[1] != "-d":
                cmd1.interactuarDirectamente()
            if sys.argv[1] != "-c":
                response = cmd1.ejecutarUnComando(sys.argv[2])
                if response:
                    print("  %s" % response)
                else:
                    print("Consulta erronea")
    else:
        leerConsola(server_config, mcrcon1, cmd1)
