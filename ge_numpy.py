import numpy as np
import time as t

def pivotgauss_np(
    a: np.ndarray,
    b: np.ndarray,
    ) -> np.ndarray:

    err1:str = "A n'est pas en 2D !"
    err2:str = "A est vide !"
    err3:str = "A est rectangulaire !"
    err4:str = "Ordre de A != ordre de b."

    if a.ndim != 2:
        raise np.linalg.LinAlgError(err1)

    if a.size == 0:
        raise np.linalg.LinAlgError(err2)

    n, m = a.shape
    if n != m:
        raise np.linalg.LinAlgError(err3)

    if n != b.shape[0]:
        raise np.linalg.LinAlgError(err4)

    for i in range(n):
        pivot = a[i, i]
        if np.less_equal(np.fabs(pivot), np.finfo(np.float64).eps):
            max_row = i
            for j in range(i+1, n):
                if np.greater(a[j, i], a[max_row, i]):
                    max_row = j
            for k in range(i,n+1):
                tmp = a[i, k-1]
                a[i, k-1] = a[max_row,k-1]
                a[max_row, k-1] = tmp
        if i < n-1:
            frac = a[i+1:, i] / pivot
            a[i+1:, i:] -= frac[:, np.newaxis] * a[i, i:]
            b[i+1:] -= frac * b[i]
            a[i+1:, i] = 0.0

    x = np.empty_like(b)
    for i in range(n-1, -1, -1):
        x[i] = (b[i] - np.sum(a[i, i+1:] * x[i+1:])) / a[i, i]

    return x

# @np.vectorize
def systeme_lineaire_non_symetrique_np(
        n: np.uint16
        ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:

    rng = np.random.default_rng()
    a = rng.random((n,n), dtype = np.float64)
    x = rng.random(n, dtype = np.float64)
    b = a @ x
    
    return a, b, x


if __name__ == "__main__":
    a, b, x = systeme_lineaire_non_symetrique_np(1000)

    print("np.ndarray : résolution du système Ax = b... ", end="")
    debut = t.perf_counter()
    xge = pivotgauss_np(a,b)
    fin = t.perf_counter()
    temps = "{:.2f}".format(fin - debut)
    print(f"en {temps} secondes")

    print("NUMPY : résolution du système Ax = b avec np.linalg.solve... ", end="")
    debut = t.perf_counter()
    xnp = np.linalg.solve(a,b)
    fin = t.perf_counter()
    temps = "{:.2f}".format(fin - debut)
    print(f"en {temps} secondes")

    print("Comparaison avec le vecteur X calculé... ", end="")
    ret = np.allclose(xge, x, np.finfo(np.float64).eps)
    if ret:
        print("OK")
    else:
        print("KO")

# np.ndarray : résolution du système Ax = b... en 58.66 secondes
# NUMPY : résolution du système Ax = b avec np.linalg.solve... en 0.7187 secondes
# Comparaison avec le vecteur X calculé... OK
