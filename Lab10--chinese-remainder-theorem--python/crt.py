from math import gcd
from itertools import tee


def chineseReminder(mn,an, m):
		Mn = []
		yn = []
		for	k in range (0, len(mn)):
				Mk = m / mn[k]
				Mn.append(Mk)
				#TYLKO PYTHON 3.8
				yk = pow(int(Mn[k]), -1, int(mn[k]))
				yn.append(yk)
		x = 0
		for	k in range (0, len(yn)):
				x = x + an[k] * Mn[k] * yn[k]
		while x >= m:
				x = x - m
		return x


def pairwise(iterable):
		a, b = tee(iterable)
		next(b, None)
		return zip(a, b)


def main():
		userInput = [x.rstrip().split() for x in open("uklad.txt", "r")]
		a, m = [], []
		for pair in userInput:
			a.append(int(pair[0]))
			m.append(int(pair[1]))
		if any(flag <= 0 for flag in m):
			print("Liczby mi nie są dodatnie");
			return 0
		for v, w in pairwise(m):
			if gcd(v, w) != 1:
				print("Liczby mi nie są względnie pierwsze")
				return 0
		m0 = 1
		for _M in m:
			m0 *= _M
		a0 = int(chineseReminder(m, a, m0))
		open("crt.txt", "w").write(str(a0)+ " " + str(m0))

if __name__ == "__main__":
		main()