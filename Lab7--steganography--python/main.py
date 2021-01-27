import sys

def toBits():
		with open("mess.txt", "r") as file:
				fileRead = file.read()
				binString = ""
				scale = 16	## equals to hexadecimal
				num_of_bits = 4
				for charHex in fileRead:
						binString += bin(int(charHex, scale))[2:].zfill(num_of_bits)
		return binString


def toHex(message):
	hexMsg = ""
	import re
	msgList = re.findall('....',message)
	for x in msgList:
		hexMsg += str(hex(int(x, 2)))[2:]
	return hexMsg	


def encrypt(params="-1"):
		with open("cover.html", "rb") as file:
				fileRead = file.read()
		binString = toBits()
		fileWrite = ""
		if params == "-1":
				newlines = 0
				for i, element in enumerate(fileRead):
						if chr(element) == "\n":
								newlines += 1
				if newlines < len(binString):
						print("Za długa wiadomość")
						return 0
				for i, element in enumerate(fileRead):
						if chr(element) == "\n" and len(binString) > 0:
								if binString[0] == "0":
										fileWrite += " " + "\n"
										binString = binString[1:]
								elif binString[0] == "1":
										fileWrite += "  " + "\n"
										binString = binString[1:]
								else:
										break
						else:
								fileWrite += chr(element)

		elif params == "-2":
				spaces = 0
				for i, element in enumerate(fileRead):
						if chr(element) == " ":
								spaces += 1
				if spaces < len(binString):
						print("Za długa wiadomość")
						return 0
				for i, element in enumerate(fileRead):
						if chr(element) == " " and len(binString) > 0:
								if binString[0] == "0":
										fileWrite += "  "
										binString = binString[1:]
								elif binString[0] == "1":
										fileWrite += "   "
										binString = binString[1:]
								else:
										break
						else:
								fileWrite += chr(element)

		elif params == "-3":
				paragraphs = 0
				cancel = 0
				for i, element in enumerate(fileRead):
						if chr(element) == "<" and chr(fileRead[i + 1]) == "p" and chr(
										fileRead[i + 2]) == ">":
								paragraphs += 1
				if paragraphs < len(binString):
						print("Za długa wiadomość")
						return 0
				for i, element in enumerate(fileRead):
						if chr(element) == "<" and chr(fileRead[i + 1]) == "p" and chr(
										fileRead[i +
														 2]) == ">" and len(binString) > 0 and cancel == 0:
								cancel = 2
								if binString[0] == "0":
										fileWrite += '''<p style="marginbottom: 0cm; line-height: 100%">'''
										binString = binString[1:]
								elif binString[0] == "1":
										fileWrite += '''<p style="margin-bottom: 0cm; lineheight: 100%">'''
										binString = binString[1:]
								else:
										break
						elif cancel > 0:
								cancel -= 1
						else:
								fileWrite += chr(element)

		elif params == "-4":
				markers = 0
				for i, element in enumerate(fileRead):
						if chr(element) == "<" and chr(fileRead[i + 1]) == "a":
								markers += 1
				if markers < len(binString):
						print("Za długa wiadomość")
						return 0
				for i, element in enumerate(fileRead):
						if chr(element) == "<" and chr(
										fileRead[i + 1]) == "a" and chr(fileRead[i + 2]) == " " and len(binString) > 0:
								if binString[0] == "1":
										fileWrite += "<><"
										binString = binString[1:]
										continue
						if chr(element) == ">" and chr(fileRead[i - 1]) == "a" and chr(
										fileRead[i - 2]) == "/" and len(binString) > 0:
								if binString[0] == "0":
										fileWrite += "><>"
										binString = binString[1:]
										continue
								else:
									fileWrite += chr(element)
						else:
								fileWrite += chr(element)

		file2 = open("watermark.html", "w")
		file2.write(fileWrite)


def decrypt(params="-1"):
		with open("watermark.html", "rb") as file:
				fileRead = file.read()
		message = ""
		if params == "-1":
				for i, element in enumerate(fileRead):
						if chr(fileRead[i-1]) != " " and chr(element) == " " and chr(fileRead[i+1]) == "\n":
								message += "0"
						if chr(fileRead[i-1]) == " " and chr(element) == " " and chr(fileRead[i+1]) == "\n":
								message += "1"

		elif params == "-2":
				for i, element in enumerate(fileRead):
						if chr(fileRead[i-1]) != " " and chr(element) == " " and chr(fileRead[i+1]) == " " and chr(fileRead[i+2]) != " " :
									message += "0"
						if chr(fileRead[i-1]) == " " and chr(element) == " " and chr(fileRead[i+1]) == " ":
									message += "1"

		elif params == "-3":
				temp = ""
				found = False
				for i, element in enumerate(fileRead):
					if chr(element) == "<" and chr(fileRead[i+1]) == "p" and not found:
						found = True
					if found:
						temp += chr(element)
						if chr(element) == ">":
							found = False
							if temp == str('''<p style="marginbottom: 0cm; line-height: 100%">'''):
								message += "0"
							elif temp == str('''<p style="margin-bottom: 0cm; lineheight: 100%">'''):
								message += "1"
							temp = ""
					
		elif params == "-4":
			for i, element in enumerate(fileRead):
				if chr(fileRead[i-2]) == "<" and chr(fileRead[i-1]) == ">" and chr(element) == "<" and chr(fileRead[i+1]) == "a" and chr(fileRead[i+2]) == " ":
					message +="1"
				if chr(fileRead[i-2]) == "<" and chr(fileRead[i-1]) == "/" and chr(element) == "a" and chr(fileRead[i+1]) == ">" and chr(fileRead[i+2]) == "<" and chr(fileRead[i+3]) == ">":
					message += "0"


		file2 = open("detect.txt", "w")
		file2.write(toHex(message))


options = sys.argv[1:]
if "-e" in options:
		if "-1" in options:
				encrypt("-1")
		elif "-2" in options:
				encrypt("-2")
		elif "-3" in options:
				encrypt("-3")
		elif "-4" in options:
				encrypt("-4")
elif "-d" in options:
		if "-1" in options:
				decrypt("-1")
		elif "-2" in options:
				decrypt("-2")
		elif "-3" in options:
				decrypt("-3")
		elif "-4" in options:
				decrypt("-4")
