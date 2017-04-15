import mcrcon
import sys
import os
import ConfigParser


class server_ARK:
    def __init__ (self, hn, pt, pw):
        self.host = hn
		self.port = pt
		self.password = pw

	def connect(self):
		rcon = mcrcon.MCRcon()

		print("# connecting to "+self.host+":"+self.port+"...")
		rcon.connect(self.host, self.port)

		print("# logging in...")
		rcon.login(self.password)

		print("# ready")

		try:
			while True:
				response = rcon.command(input('> '))
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
	"""
    parser = ConfigParser.RawConfigParser()
    if os.path.isfile(os.path.join('server_ARK.conf')):
        parser.read(os.path.join('server_ARK.conf'))
        server_config = parser._sections
    else:
        print("El fichero server_ARK.conf no existe.")

    server1 = server_ARK("127.0.0.1", str(server_config.get('ARK','rcon_port')), str(server_config.get('ARK','ServerAdminPassword')))
    server1.connect()
	"""
	host = '127.0.0.1'
	port = int('32330')
	password = '54321'

	server1 = server_ARK("127.0.0.1", str(server_config.get('ARK','rcon_port')), str(server_config.get('ARK','ServerAdminPassword')))
	server1.connect()
