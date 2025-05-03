import numpy as np
import time

def boole(f: callable, a: float, b: float, n: int) -> float:
	s: float = 0.0

	if n % 4 != 0:
		raise ValueError("n doit être un multiple de 4 !")
	
	h = abs(b - a) / (4.0 * n)

	for i in range(n):
		s += 7.0 * (f(a) + f(a + 4.0 * h))
		s += 12.0 * f((a + 2 * h))
		s += 32.0 * (f(a + h) + f(a + 3.0 * h))
		a += 4.0 * h

	return s * 2.0 * (h / 45.0)


def tests(a: float, b: float, n: int, p: bool):
	fonction1 = lambda x: 20 * np.sqrt(x**6) - 4 * x**3 + 18 * x**2 - 1
	fonction2 = lambda x: 4 * x**3 + 10 * x * np.exp(x) + 1
	fonction3 = lambda x: np.exp(x) - np.exp(x / 3)**3

	res1 = boole(fonction1, a, b, n)
	res2 = boole(fonction2, a, b, n)
	res3 = boole(fonction3, a, b, n)

	if p:
		print(f"20sqrt(x^6) - 4x^3 + 18x^2 - 1 = {res1}")
		print(f"4x^3 + 10x * exp(x) + 1 = {res2}")
		print(f"exp(x) - exp(x/3)^3 = {res3}")


if __name__ == "__main__":
	a, b, n = 0, 1, 1000
	ESSAIS = 10
	temps: float = 0
	for k in range(ESSAIS):
		debut = time.perf_counter()
		tests(a, b, n, False)
		temps += time.perf_counter() - debut

	print(f"Temps moyen écoulé pour un pas de {n = } \
	   et pour {ESSAIS} répétitions : {temps/ESSAIS} s")
