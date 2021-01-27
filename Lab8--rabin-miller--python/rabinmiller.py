from math import gcd, log, ceil, sqrt
from random import randrange, choice
import sys


def step1(a, n):
	if gcd(a,n) > 1:
		return str(gcd(a,n))
	else:
		return None


def maxPrimeFactor(n):
	x = ceil(sqrt(n))
	y = x**2 - n
	while not sqrt(y).is_integer():
		x += 1
		y = x**2 - n
	return x + sqrt(y), x - sqrt(y)

def miller_rabin(n, k):

		if n == 2:
				return True
		if n % 2 == 0:
				return False
		r, s = 0, ruw
		while s % 2 == 0:
				r += 1
				s //= 2
		for _ in range(k):
				a = randrange(2, n - 1)
				x = pow(a, s, n)
				if x == 1 or x == n - 1:
						continue
				for _ in range(r - 1):
						x = pow(x, 2, n)
						if x == n - 1:
								break
				else:
						return str(int(choice(maxPrimeFactor(n))))
		return "Prawdopodobnie pierwsza"

with open("wejscie.txt", "r") as file:
	lines = [int(x.rstrip()) for x in file.readlines()]
	if len(lines) >= 1:
		n = lines[0]
		if len(lines) >= 2:
			ruw = lines[1]
			if len(lines) == 3:
				ruw = ruw * lines[2] - 1
		else:
			ruw = n - 1

options = sys.argv[1:]
if "-f" in options:
	a = randrange(2, n)
	b = pow(a, n-1, n)
	if b == 1:
		open("wyjscie.txt", "w").write("Prawdopodobnie pierwsza")
	else:
		open("wyjscie.txt", "w").write("Na pewno złożona")
else:
	probability = 1 - pow(2, -40)
	a = randrange(2, n)
	if step1(a, n) != None:
		open("wyjscie.txt", "w").write("Na pewno złożona")
	range_ = int(log(-probability+1, (1/4)))
	open("wyjscie.txt", "w").write(miller_rabin(n, range_))

