from cryptography.fernet import Fernet

KEY = 'key.key'

def login(con, arq):
	f = open(KEY, 'rb').read()
	
	psw = con.recv(1024)
	psw = Fernet(f).decrypt(psw)
	psw = psw.decode()
	
	with open(arq, 'rb') as yy:
		pswc = yy.read()
		pswc = Fernet(f).decrypt(pswc)
		pswc = pswc.decode()
		
		if psw == pswc:
			return True
		else:
			return False
