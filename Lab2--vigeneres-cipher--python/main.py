import sys


def plain_cleanup():
    try:
        plain = open("plain.txt", "r").read()
        open("orig.txt", "w").write(plain)
        plain = convertText(plain)
        open("plain.txt", "w").write(plain)
    except:
        open("plain.txt", "w")
        open("orig.txt", "w")


def convertText(text):
    text_clear = ""
    for x in text:
        if x.isalnum():
            text_clear += x.lower()
    ready_text = ''.join([i for i in text_clear if not i.isdigit()])
    return ready_text


def encrypt_vigenere():
    plain = open("plain.txt", "r").read()
    password = open("key.txt", "r").read()
    if len(plain) > len(password):
        len_diff = len(plain) - len(password)
        for x in range(len_diff):
            password += password[x]
    else:
        password = password[:len(plain)]
    cipher = ""
    for x in range(len(plain)):
        cipher += find_in_alphabet_table(plain[x], password[x])
    open("crypto.txt", "w").write(cipher)


def generate_alphabet_table():
    alphabet_table = []
    starter = "a"
    for x in range(26):
        temp_iterator = starter
        table = []
        for y in range(26):
            table.append(temp_iterator)
            temp_iterator = chr((ord(temp_iterator) - ord("a") + 1) % 26 +
                                ord("a"))
        alphabet_table.append(table)
        starter = chr(ord(starter) + 1)
    return alphabet_table


def find_in_alphabet_table(tekst, haslo):
    tekst = (ord(tekst) - ord("a")) % 26
    haslo = (ord(haslo) - ord("a")) % 26
    return generate_alphabet_table()[haslo][tekst]


def decrypt_vigenere():
    crypto = open("crypto.txt", "r").read()
    password = open("key.txt", "r").read()
    decrypted = ""
    alphabet_table = generate_alphabet_table()
    for x in range(len(crypto)):
        test = alphabet_table[ord(password[x % len(password)]) -
                              ord("a")].index(crypto[x])
        decrypted += chr(test + ord("a"))
    open("decrypt.txt", "w").write(decrypted)


def cryptoanalysis():
    key_length = find_key_len()
    crypto = open("crypto.txt", "r").read()
    key = ""
    for y in range(key_length):
        temp = []
        for i, x in enumerate(crypto):
            if i % key_length == y:
                temp.append(x)
        key += freq_analysis(temp)
    open("key-crypto.txt", "w").write(key)


def closest(list, Number):
    aux = []
    for valor in list:
        aux.append(abs(Number - valor))

    return aux.index(min(aux))


def find_key_len():
    crypto = open("crypto.txt", "r").read()
    crypto_table = []
    for x in range(1, len(crypto)):
        crypto_table.append(crypto[:-x])
    table_of_coincidences = []
    for x in range(len(crypto_table)):
        temp = crypto[x + 1:]
        coincidences = 0
        for y in range(len(crypto_table[x])):
            if temp[y] == crypto_table[x][y]:
                coincidences += 1
        table_of_coincidences.append(coincidences)
    table_of_coincidence_index = []
    for x in table_of_coincidences:
        table_of_coincidence_index.append(x / len(crypto))
    ideal = table_of_coincidences[closest(table_of_coincidence_index, 0.067)]
    iterator = 1
    key_values = []
    for x in table_of_coincidences:
        if x > ideal:
            key_values.append(iterator)
            iterator = 1
        else:
            iterator += 1
    return min(key_values)


def freq_analysis(sequence):
    english_frequences = (0.082, 0.015, 0.028, 0.043, 0.127, 0.022, 0.020,
                          0.061, 0.070, 0.002, 0.008, 0.040, 0.024, 0.067,
                          0.075, 0.029, 0.001, 0.060, 0.063, 0.091, 0.028,
                          0.010, 0.023, 0.001, 0.020, 0.001)
    powers_of_moves = [0] * 26

    for i in range(26):

        power_of_moves = 0.0

        sequence_offset = [
            chr(((ord(sequence[j]) - 97 - i) % 26) + 97)
            for j in range(len(sequence))
        ]
        v = [0] * 26
        for l in sequence_offset:
            v[ord(l) - ord('a')] += 1
        for j in range(26):
            v[j] *= (1.0 / float(len(sequence)))

        for j in range(26):
            power_of_moves += ((v[j] - float(english_frequences[j]))**
                               2) / float(english_frequences[j])

        powers_of_moves[i] = power_of_moves

    shift = powers_of_moves.index(min(powers_of_moves))

    return chr(shift + 97)


options = sys.argv[1:]
if "-p" in options:
    plain_cleanup()
if "-e" in options:
    encrypt_vigenere()
if "-d" in options:
    decrypt_vigenere()
if "-k" in options:
    cryptoanalysis()
