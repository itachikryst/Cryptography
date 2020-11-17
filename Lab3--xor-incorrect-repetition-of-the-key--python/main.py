import sys

def text_converter(text):
	converted_text = ""
	for i,_char in enumerate(text):
		zakazane = """~“”\,.!?:;*'%/|"‘+-=()[]{}’-0123456789<>@"""
		if (_char not in zakazane) and _char != "\n":
			if i > 0:
				if not (converted_text[-1] == " " and text[i] == " "):
					converted_text += _char.lower()
			else:
				converted_text += _char.lower()
		elif _char == "\n":
			if i > 0:
				if converted_text[-1] != " ":
					converted_text += " "
	new_converted = ""
	for i,_char in enumerate(converted_text):
		i += 1
		if i%60==0 and i != 0:
			new_converted += _char
			new_converted += "\n"
		else:
			new_converted += _char
	return new_converted

def xor(s1,s2):
		return ''.join(chr(ord(a) ^ ord(b)) for a,b in zip(s1,s2))

def encryption():
	text = open("plain.txt","r").readlines()
	for x in range(len(text)):
		if "\n" in text[x]:
			text[x] = text[x][:-1]
	encrypted = []
	key = open("key.txt","r").read()
	new_key = ""
	for x in range(60):
		new_key += key[x%len(key)]
	for linia in text:
		temp = []
		for i,_char in enumerate(linia):
			temp.append(xor(_char,new_key[i]))
		encrypted.append(temp)
	to_file = ""
	for line in encrypted:
		for _char in line:
			to_file += _char
	byte_to_file = to_file.encode("utf8")
	open("crypto.txt","wb").write(byte_to_file)

def cryptoanalysis():
	text = open("crypto.txt","rb").read()
	klucz = []
	for x in range(60):
		klucz.append("")
	for i,_char in enumerate(text):
		if format(_char,'08b').startswith("010"):
			if klucz[i%60] == "":
				klucz[i%60] = xor(" ", chr(_char))
	klucz_do_zwrotu = ""
	decrypted = ""
	for x in klucz:
		if x !="":
			klucz_do_zwrotu += x
		else:
			klucz_do_zwrotu += "a"
	for i,_char in enumerate(text.decode("utf8")):
		if i%60 ==0 and i!=0:
			decrypted += "\n"
		decrypted += xor(_char,klucz_do_zwrotu[i%len(klucz_do_zwrotu)])
	open("decrypt.txt","w").write(decrypted)
	
options = sys.argv[1:]
if "-p" in options:
	open("plain.txt","w").write(text_converter(open("orig.txt","r").read()))
if "-e" in options:
	encryption()
if "-k" in options:
	cryptoanalysis()