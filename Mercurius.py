#Modulos
import socket
import threading
import sys
import random
from cryptography.fernet import Fernet
import loginTest

KEY = "key.key"
PASS = "pass.key"

#Args
args = sys.argv

class Chat:
	#Init
	def __init__(self, port):
		#PORT
		self.port = port
		#List of Clients
		self.sockets = []
		#Generic Socket
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		
		#If key file exists, read it. If it doesnt, create it and read it
		try:
			self.key = open(KEY, 'rb').read()
		except:
			
			if args[1] == 'server':
				with open(KEY, 'wb') as tt:
					tt.write(Fernet.generate_key())
					
				self.key = open(KEY, 'rb').read()
			else:
				print('Get the key file!')
				sys.exit()
	
	########Server############	
	def server_socket(self):
		
		#Socket Created
		self.s.bind(('127.0.0.1', self.port))
		self.s.listen(10)
		
	def broadcast(self, msg, color):
		
		#Sends message to all clients
		for conex in self.sockets:	
			#Style of Message
			data = color + msg + '\033[0m' 
				
			#Cryptography
			data = data.encode()						
			data = Fernet(self.key).encrypt(data)	
			
			try:
				#Sends Message
				conex[0].send(data)
			except:
				conex[0].close()
				self.sockets.remove((con, end))
						
	def recv_data(self, con, end, color):
		
		while True:
		
			#Client Data
			data = con.recv(1024)
			
			try:
				#Cryptography
				data = Fernet(self.key).decrypt(data)
				data = data.decode()
			except:
				con.close()
				self.sockets.remove((con, end))
				sys.exit()
			
			#Print on the server
			msg = '[' + str(end) + ']: ' + data
			print(color + msg + '\033[0m')
			
			#Sends to all the clients
			self.broadcast(msg, color)
			
	def accept_con(self):
		
		while True:
		
			#Accepts Connections
			con, end = self.s.accept()
			
			if not loginTest.login(con, PASS):
				con.close()
				continue
			
			self.sockets.append((con, end))
			
			#Chooses random color for each client
			color = random.choice(['\033[93m', '\033[91m', '\033[92m', '\033[94m', '\033[96m', '\033[95m'])
			
			#Prints new connection
			print(color +"[Connection]:" + str(end) + '\033[0m')
			
			#Sends new connection message to all clients
			self.broadcast("[Connection]:" + str(end), color)
			
			#Server starts receiving data from that client
			threading.Thread(target=self.recv_data, args=(con, end, color)).start()
			
	############CLIENT######################
	def client_socket(self, addres='127.0.0.1'):
		#Connects to Server
		self.s.connect((addres, self.port))
			
	def get_input(self):
		
		while True:
			#Receives input
			try:
				data = input("")
			except KeyboardInterrupt:
				sys.exit()
				
			#Cryptography
			data = data.encode()
			data = Fernet(self.key).encrypt(data)
			
			#Sends Data
			self.s.send(data)
			
	def get_response(self):
		
		while True:
			#Receives messages from Server
			data = self.s.recv(1024)
			
			#Cryptography
			data = Fernet(self.key).decrypt(data)
			data = data.decode()
			
			#Prints message
			print('\033[93m' + data + '\033[0m')
			

#Socket is created
s = Chat(int(args[2]))

#SERVER
if args[1] == "server":
	s.server_socket()
	s.accept_con()

#CLIENT
else:
	try:
		s.client_socket(args[3])
	except:
		s.client_socket()
	threading.Thread(target=s.get_input).start()
	threading.Thread(target=s.get_response).start()
	
