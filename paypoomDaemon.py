import mcrcon
import sys
import os
import json


class server_ARK:
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

if __name__ == '__main__':
    if os.path.isfile(os.path.join('server_ARK.json')):
        json_data = open(os.path.join('server_ARK.json'))
        server_config = json.load(json_data)
        json_data.close()

    else:
        print("El fichero server_ARK.json no existe.")

    for lin1 in server_config:
        print(lin1)

    host = '127.0.0.1'
    port = server_config['server_ARK']['rcon_port']
    password = server_config['server_ARK']['ServerAdminPassword']

    server1 = server_ARK(host, port, password)
    #server1 = server_ARK('127.0.0.1',int('32330'),password)
    server1.connect()
