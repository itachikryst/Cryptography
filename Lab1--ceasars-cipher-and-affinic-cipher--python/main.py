import sys
from math import gcd

def modular_multiplicative_inverse(multiplier):
	for x in range (0,26):
		if (multiplier*x)%26 == 1:
			return x
			
def get_key():
	file = open("key.txt", "r")
	text = file.read()
	text = text.split()
	file.close()
	return text

def get_plain_text():
	file = open("plain.txt", "r")
	text = file.read()
	file.close()
	return text

def get_crypto():
	file = open("crypto.txt", "r")
	text = file.read()
	file.close()
	return text

def get_extra():
	file = open("extra.txt", "r")
	text = file.read()
	file.close()
	return text

def encrypt_ceasar():
	plain_text = get_plain_text()
	encrypted = ""
	key = int(get_key()[0])
	for x in plain_text:
		if (x.isupper()):
			encrypted += chr((ord(x) + key-ord("A")) % 26 + ord("A"))
		else:
			encrypted += chr((ord(x) + key -ord("a")) % 26 + ord("a"))
	open("crypto.txt", "w").write(encrypted)

def decrypt_ceasar(key = None):
	encrypted = get_crypto()
	decrypted = ""
	if key == None:
		key = int(get_key()[0])%26
		file = "plain.txt"
	else:
		file = "decrypt.txt"
	for x in encrypted:
		if (x.isupper()):
				decrypted += chr((ord(x)-ord("A")- key)  % 26 + ord("A"))
		else:
				decrypted += chr((ord(x)-ord("a")- key)  % 26 + ord("a"))
	open(file, "a").write(decrypted+"\n")

def encrypt_affine():
	encrypted = ""
	move, multiplier = get_key()
	move = int(move)
	multiplier = int(multiplier)
	if gcd(multiplier, 26) == 1:
		plain_text = get_plain_text()
		for x in plain_text:
			if (x.isupper()):
				encrypted += chr((multiplier*(ord(x)-ord("A")) + move) % 26 + ord("A"))
			else:
				encrypted += chr((multiplier*(ord(x)-ord("a")) + move) % 26 + ord("a"))
		open("crypto.txt", "w").write(encrypted)
	else:
		print("Bad key, greatest common divider is not 1")

def decrypt_affine(key = None):
	decrypted = ""
	if key == None:
		move, multiplier = get_key()
		file = "plain.txt"
	else:
		file = "decrypt.txt"
		move, multiplier = key
	move = int(move)
	multiplier = modular_multiplicative_inverse(int(multiplier))
	if gcd(multiplier, 26) == 1:
		encrypted = get_crypto()
		for x in encrypted:
			if (x.isupper()):
				decrypted += chr((multiplier*(ord(x)-ord("A")- move) ) % 26 + ord("A"))
			else:
				decrypted += chr((multiplier*(ord(x)-ord("a")- move) ) % 26 + ord("a"))
		open(file, "a").write(decrypted+"\n")
	else:
		print("Bad key, greatest common divider is not 1")

def bruteforce_ceasar():
	for key in range(1,26):
		decrypt_ceasar(key)

def bruteforce_affine():
	for move in range(0,26):
		for multiplier in range(1,26):
			if gcd(multiplier, 26) == 1:
				decrypt_affine([move,multiplier])

def ceasar_with_extra():
	extra = get_extra()
	print(extra)
	encrypted = get_crypto()
	diff = []
	for x in range(0,len(extra)):
			diff.append(ord(encrypted[x]) -ord(extra[x]))
	for x in range(0,len(extra)):
		if diff[0] != diff[x]:
			print("Cannot find the key")
			return 0
	open("key-new.txt", "w").write(str(diff[0]))
	decrypt_ceasar(diff[0])

def affine_with_extra():
	extra = get_extra()
	crypto = get_crypto()
	if ord(extra[1]) > ord(extra[0]):
		diff_extra = ord(extra[1]) - ord(extra[0])
		diff_crypto = ord(crypto[1]) - ord(crypto[0])
		if diff_crypto < 0:
			diff_crypto = diff_crypto%26
		multiplier = int(diff_crypto/diff_extra)
	else:
		diff_extra = ord(extra[0]) - ord(extra[1])
		diff_crypto = ord(crypto[0]) - ord(crypto[1])
		if diff_crypto < 0:
			diff_crypto = diff_crypto%26
		multiplier = int(diff_crypto/diff_extra)
	move = ord(crypto[1]) - ord(extra[1])*multiplier
	move = modular_multiplicative_inverse(move%26)
	open("key-new.txt", "w").write(str(move)+" "+str(multiplier))
	try:
		decrypt_affine([move, multiplier])
	except:
		print("Couldn't find the key")

options = sys.argv[1:]
if "-c" in options:
	if "-e" in options:
		encrypt_ceasar()
	if "-d" in options:
		decrypt_ceasar()
	if "-k" in options:
		bruteforce_ceasar()
	if "-j" in options:
		ceasar_with_extra()
if "-a" in options:
	if "-e" in options:
		encrypt_affine()
	if "-d" in options:
		decrypt_affine()
	if "-k" in options:
		bruteforce_affine()
	if "-j" in options:
		affine_with_extra()