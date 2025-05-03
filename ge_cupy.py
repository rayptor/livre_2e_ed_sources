import cupy as cp
import time as t

def pivotgauss_cp(
    a: cp.ndarray,
    b: cp.ndarray,
    ) -> cp.ndarray:

    err1: str = "A n'est pas en 2D !"
    err2: str = "A est vide !"
    err3: str = "A est rectangulaire !"
    err4: str = "Ordre de A != ordre de b."

    if a.ndim != 2:
        raise cp.linalg.LinAlgError(err1)

    if a.size == 0:
        raise cp.linalg.LinAlgError(err2)

    n, m = a.shape
    if n != m:
        raise cp.linalg.LinAlgError(err3)

    if n != b.shape[0]:
        raise cp.linalg.LinAlgError(err4)

    for i in range(n):
        pivot = a[i, i]
        if cp.less_equal(cp.abs(pivot), cp.finfo(cp.float64).eps):
            max_row = i
            for j in range(i+1, n):
                if cp.greater(a[j, i], a[max_row, i]):
                    max_row = j
            for k in range(i, n+1):
                tmp = a[i, k-1]
                a[i, k-1] = a[max_row, k-1]
                a[max_row, k-1] = tmp
        if i < n-1:
            frac = a[i+1:, i] / pivot
            a[i+1:, i:] -= frac[:, cp.newaxis] * a[i, i:]
            b[i+1:] -= frac * b[i]
            a[i+1:, i] = 0.0

    x = cp.empty_like(b)
    for i in range(n-1, -1, -1):
        x[i] = (b[i] - cp.sum(a[i, i+1:] * x[i+1:])) / a[i, i]

    return x

def systeme_lineaire_non_symetrique_cp(
        n: int
        ) -> tuple[cp.ndarray, cp.ndarray, cp.ndarray]:

    rng = cp.random.default_rng()
    a = rng.random((n,n), dtype=cp.float64)
    x = rng.random(n, dtype=cp.float64)
    b = a @ x
    
    return a, b, x


if __name__ == "__main__":
    a, b, x = systeme_lineaire_non_symetrique_cp(4000)

    print("cp.ndarray : résolution du système Ax = b... ", end="")
    debut = t.perf_counter()
    xge = pivotgauss_cp(a, b)
    fin = t.perf_counter()
    temps = "{:.4f}".format(fin - debut)
    print(f"en {temps} secondes")

    print("CUPY : résolution du système Ax = b avec cp.linalg.solve... ", end="")
    debut = t.perf_counter()
    xcp = cp.linalg.solve(a, b)
    fin = t.perf_counter()
    temps = "{:.4f}".format(fin - debut)
    print(f"en {temps} secondes")

    print("Comparaison avec le vecteur X calculé... ", end="")
    ret = cp.allclose(xge, x, atol=cp.finfo(cp.float64).eps)
    if ret:
        print("OK")
    else:
        print("KO")

# cp.ndarray : résolution du système Ax = b... en 2.9884 secondes
# CUPY : résolution du système Ax = b avec cp.linalg.solve... en 0.2699 secondes
# Comparaison avec le vecteur X calculé... OK
