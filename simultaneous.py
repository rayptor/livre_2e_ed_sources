import numpy as np
import sys

def initiales(coefs: np.ndarray) -> np.ndarray:
	n = coefs.shape[0] - 1
	# Formule de Henrici
	d: np.float128 = np.max(np.power(np.abs(coefs), 1 / n))
	R: np.float128 = 2 * d
	# Formule de Aberth
	f = n + np.pi / (2 * n)
	e = np.exp((2j * np.pi \
			 * np.arange(n, dtype=np.complex256)) / f)
	x = -coefs[1] / n + R * e
	return x

def WeierstrassDurandKerner(
	coefs: np.ndarray,
	itmax: int = 100,
	eps = np.finfo(np.float128).eps
	) -> np.ndarray:

	n = coefs.shape[0] - 1

	if coefs[0] != 1.0:
		coefs /= coefs[0]
		
	if n < 3 or coefs[-1] == 0.0:
		raise ValueError("Polynôme incorrect !")

	x1 = initiales(coefs)
	x0 = x1.copy()
	k: int = 0

	while k <= itmax:
		for i in range(n):
			delta = x1[i] - np.delete(x1, i)
			denom = np.multiply.reduce(delta) \
			    if np.multiply.reduce(delta) != 0 else eps
			try:
				num = np.polyval(coefs, x1)
				x1[i] -= num[i] / denom
			except ZeroDivisionError:
				sys.exit(1)

		if np.all(np.linalg.vector_norm(x1 - x0) < eps) \
				or np.isnan(x1.all().real) \
				or np.isnan(x1.all().imag):
			break
		else:
			x0 = np.copy(x1)
			k += 1

	return np.real_if_close(np.sort(x1).astype(np.complex256), tol=eps)


def AberthErlich(
	coefs: np.ndarray,
	itmax: int = 100,
	eps = np.finfo(np.float128).eps
	) -> np.ndarray:

    n = coefs.shape[0] - 1

    if coefs[0] != 1.0:
        coefs /= coefs[0]
		
    if n < 3 or coefs[-1] == 0.0:
        raise ValueError("Polynôme incorrect !")

    x1 = initiales(coefs)
    x0 = x1.copy()
    d = np.polyder(coefs)
    v = np.zeros(n, dtype=np.complex256)
    k: int = 0
    
    while k <= itmax:
        for i in range(n):
            try:
                s1 = np.sum(1.0 / (x1[i] - x1[:i]))
                s2 = np.sum(1.0 / (x1[i] - x1[i + 1:]))
                v[i] = s1 + s2
                w = np.polyval(coefs, x1[i]) / np.polyval(d, x1[i])
                x1[i] -= w / (1 - w * v[i])
            except ZeroDivisionError:
                sys.exit(1)

        if np.all(np.linalg.vector_norm(x1 - x0) < eps) \
                or np.isnan(x1.all().real) \
                or np.isnan(x1.all().imag):
            break
        else:
            x0 = np.copy(x1)
            k += 1

    return np.real_if_close(np.sort(x1).astype(np.complex256), tol=eps)


def Nourein(
	coefs: np.ndarray,
	itmax: int = 100,
	eps = np.finfo(np.float128).eps
	) -> np.ndarray:

	n = coefs.shape[0] - 1
	if coefs[0] != 1.0:
		coefs /= coefs[0]
		
	if n < 3 or coefs[-1] == 0.0:
		raise ValueError("Polynôme incorrect !")

	x0 = initiales(coefs)
	x1 = x0.copy()
	k: int = 0
    
	while k < itmax:
		denom = 1
		for i in range(n):
			for j in range(n):
				if i != j:
					delta = x1[i] - np.delete(x1, i)
					denom = np.multiply.reduce(delta) \
			    		if np.multiply.reduce(delta) != 0 else eps
			x = x1[i]
			Wi = np.polyval(coefs, x) / denom
			s = 0
			for j in range(n):
				if i != j:
					delta = x1[i] - np.delete(x1, i)
					denom = np.multiply.reduce(delta) \
			    		if np.multiply.reduce(delta) != 0 else eps
					x = x1[j]
					Wj = np.polyval(coefs, x) / denom
					# s += Wj / (x1[i] - Wi - x1[j])
					s += Wj / (x1[i] - Wi)
			x1[i] -= Wi / (1 + s)
        
		if np.all(np.linalg.vector_norm(x1 - x0) < eps) \
				or np.isnan(x1.all().real) \
				or np.isnan(x1.all().imag):
			break
		else:
			x0 = np.copy(x1)
			k += 1
    
	return np.real_if_close(np.sort(x1).astype(np.complex256), tol=eps)


if __name__ == "__main__":
	test1 = "\n\n -> P(x) = x^6+(4+2i)x^5-(11-8i)x^4-(64-12i)x^3-(37-8i)x^2-(68-130i)x-1105"
    # (4-1i), (-4-1i), (1+2i), (1-2i), (-3+2i), (-3-2i)

	test2 = "\n\n -> P(x) = x^6+62x^5-14531x^4+356x^3+20003908x^2+35937824x-1198149120"
    # 80, 46, -9, -152, -34, 7

	test3 = "\n\n -> P(x) = x^9-5x^8+10x^7-50x^6+248x^5-600x^4+790x^3-750x^2+551x-195"
    # 1, 3, -2-3i, -2+3i, -i, i, 2-i, 2+i

	test4 = "\n\n -> P(x) = x^12+9x^11-3x^10+4x^9+6x^8-2x^7+5x^6-7x^5+2x^4-8x^3+4x^2-5x-1"
    # -9.35857, -1.19202, -0.168918, 0.951839
	# -0.62139-0.66938i, -0.62139+0.66938i
	# -0.09660-0.93364i, -0.09660+0.93364i
	# 0.49306-0.69278i, 0.49306+0.69278i
	# 0.60876-0.82377i, 0.60876+0.82377i

	coefs1 = np.array([np.complex256(1+0j), np.complex256(4+2j), -np.complex256(11-8j), -np.complex256(64-12j), -np.complex256(37-8j), -np.complex256(68-130j), -np.complex256(1105+0j)], dtype=np.complex256)
	coefs2 = np.array([1, 62, -14531, 356, 20003908, 35937824, -1198149120], dtype=np.float128)
	coefs3 = np.array([1, -5, 10, -50, 248, -600, 790, -750, 551, -195], dtype=np.float128)
	coefs4 = np.array([1, 9, -3, 4, 6, -2, 5, -7, 2, -8, 4, -5, -1], dtype=np.float128)
	rng = np.random.default_rng()
	coefs5 = rng.integers(low=-1000, high=1000, size=100, dtype=np.int16)

	# Calculs effectués en 128 bits, mais l'affichage
	# n'est fait qu'en 32 bits pour d'avantage de clarté.
	dec = np.finfo(np.float32).precision
	np.set_printoptions(precision=dec, suppress=True, formatter=None)
	for i, coefs in enumerate([coefs1, coefs2, coefs3, coefs4], start=1):
		match i:
			case 1:
				print(test1)
			case 2:
				print(test2)
			case 3:
				print(test3)
			case 4:
				print(test4)
		
		print(f"\nWEIERSTRASS-DURAND-KERNER :")
		print("---------------------------")
		roots = WeierstrassDurandKerner(coefs)
		print(f"{roots}")

		print(f"\nABERTH-ERLICH :")
		print("---------------")
		roots = AberthErlich(coefs)
		print(f"{roots}")

		print(f"\nNOUREIN :")
		print("---------")
		roots = Nourein(coefs)
		print(f"{roots}")

