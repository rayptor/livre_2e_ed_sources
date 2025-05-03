import numpy as np

def racines(
	p: np.ndarray,
	) -> np.ndarray:

	n = p.shape[0]
	compagnon = np.eye(n, n, k = +1)
	p = p[::-1]
	for i in range(n):
		compagnon[-1,i] = (-1) * p[i]

	valp, _ = np.linalg.eig(compagnon)

	return np.sort(valp)

if __name__ == "__main__":
	print("Recherche des racines du polynôme :")
	print("x^7 - 22x^6 + 156x^5 - 254x^4 - 1393x^3 + 4836x^2 - 684x - 6480 = 0\n")
	p = np.array([-22, 156, -254, -1393, 4836, -684, -6480])
	print(f"Les {p.shape[0]} racines de P(x) sont", racines(p))
