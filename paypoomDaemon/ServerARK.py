#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class ServerArk:
    def __init__ (self, hn, pt, pw):
        self.host = hn
        self.port = pt
        self.password = pw

    def connect(self):
        rcon = mcrcon.MCRcon()

        print("# connecting to "+self.host+":"+str(self.port)+"...")
        rcon.connect(self.host, self.port)

        print("# logging in...")
        rcon.login(self.password)

        print("# ready")

        try:
            while True:
                response = rcon.command(raw_input('> '))
                if response:
                    print(response)

        except KeyboardInterrupt:
            print("\n# disconnecting...")
            rcon.disconnect()

    def getHostname(self):
        return self.host

    def getPort(self):
        return self.port

    def getPassword(self):
        return self.password
