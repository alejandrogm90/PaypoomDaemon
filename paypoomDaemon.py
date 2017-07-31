#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import json
import urllib
import time
import platform
import subprocess

from clases.Commands_Paypoom import Commands_Paypoom
from clases.MCRcon import MCRcon

if __name__ == '__main__':
    mcrcon1 = MCRcon()

    # Carga la configuracion
    if os.path.isfile(os.path.join('server.json')):
        try:
            json_data = open(os.path.join('server.json'))
            server_config = json.load(json_data)
            json_data.close()
        except:
            print("The file 'server.json' can not be loaded.")
            exit(2)
    else:
        print("The file 'server.json' can not be find.")
        exit(1)

    # Carga la configuracion
    if os.path.isfile(os.path.join(server_config['default_language_file'])):
        try:
            json_data = open(os.path.join(server_config['default_language_file']))
            server_config['lang'] = json.load(json_data)
            json_data.close()
            print(server_config['lang']['string_4'])
        except:
            print("The file '"+server_config['default_language_file']+"' can not be loaded.")
            exit(3)
    else:
        print("The file '"+server_config['default_language_file']+"' can not be find.")
        exit(4)

    # Carga de los Items_Dinos
    """
    try:
        cmd1 = Commands_Paypoom(server_config)
    except:
        print("Items can not be loaded.")
        exit(5)
    """
    cmd1 = Commands_Paypoom(server_config)

    if len(sys.argv) > 1:
        if len(sys.argv) > 3 or sys.argv[1] != "-d" and sys.argv[1] != "--debug-mode" and sys.argv[1] != "-cl" and sys.argv[1] != "--command-line" :
            print(server_config['lang']['string_7'])
            print(server_config['lang']['string_8'])
            print(server_config['lang']['string_9'])
        else:
            if sys.argv[1] != "-d":
                cmd1.interactDirectly()
            if sys.argv[1] != "-c":
                response = cmd1.executeCommand(sys.argv[2])
                if response:
                    print("  %s" % response)
                else:
                    print(server_config['lang']['string_10'])
    else:
        print(server_config['lang']['string_1'])
        print(server_config['lang']['string_2'])
        lapse_request_time = int(server_config['lapse_request_time'])
        try:
            try:
                mcrcon1.connect(server_config['ip'], int(server_config['rcon_port']))
                mcrcon1.login(server_config['ServerAdminPassword'])
            except:
                print(server_config['lang']['string_6'])
                exit(6)
            while True:
                time.sleep(lapse_request_time)
                response = mcrcon1.command('getchat')
                if "Server received, But no response!!" not in response:
                    for linea1 in response.split("\n"):
                        print(linea1)
                        try:
                            #idPlayer = response.split(' ')[0]
                            cadena1 = linea1.split(':')[1].lstrip(" ")
                            if cmd1.isRigthCommand(cadena1):
                                cmd1.interpreteACommand(cadena1)
                        except :
                            pass
                else:
                    print(server_config['lang']['string_5'])
        except KeyboardInterrupt:
            mcrcon1.disconnect()
            print(server_config['lang']['string_3'])
