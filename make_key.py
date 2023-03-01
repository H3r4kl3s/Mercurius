from cryptography.fernet import Fernet

KEY = 'key.key'
PASS = 'pass.key'

#Generates Key
arq = open(KEY, 'wb')
key = Fernet.generate_key()
arq.write(key)
arq.close()

print("Key file generated:", KEY)
print("")

#Generates password
pasw = input('Pass:').encode()
with open(PASS, 'wb') as p_arq:
	p_arq.write(Fernet(key).encrypt(pasw))
	

print("Password file generated:", PASS)
