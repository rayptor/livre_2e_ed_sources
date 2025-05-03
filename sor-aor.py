import numpy as np
import time as t

def gauss_seidel(
    A: np.ndarray,
    b: np.ndarray,
    k: int,
    ) -> tuple[np.ndarray, int]:

    err1: str = "A n'est pas en 2D !"
    err2: str = "A est vide !"
    err3: str = "A est rectangulaire !"
    err4: str = "Ordre de A != ordre de b."

    if a.ndim != 2:
        raise np.linalg.LinAlgError(err1)

    if a.size == 0:
        raise np.linalg.LinAlgError(err2)

    n, m = a.shape
    if n != m:
        raise np.linalg.LinAlgError(err3)

    if n != b.shape[0]:
        raise np.linalg.LinAlgError(err4)

    x0 = x1 = np.zeros_like(b)
 
    D = np.diag(np.diag(A))
    L = np.tril(A, -1)
    U = np.triu(A, 1)

    DLI = np.linalg.inv(D + L)
    MN = np.dot(DLI, U)
    v = np.dot(DLI, b)

    it: int = 0
    while it < k:
        x1 = -(np.dot(MN, x0) + v)
        norme2 = np.linalg.norm((x1 - x0) / x1)
        if np.less(norme2, np.finfo(np.float32).eps):
            break
        x0 = x1
        it += 1

    return -x1, it


def sor(
    A: np.ndarray,
    b: np.ndarray,
    omega: float,
    k: int,
    ) -> tuple[np.ndarray, int]:

    err1: str = "A n'est pas en 2D !"
    err2: str = "A est vide !"
    err3: str = "A est rectangulaire !"
    err4: str = "Ordre de A != ordre de b !"
    err5: str = "Valeur de Omega incorrecte !"

    if a.ndim != 2:
        raise np.linalg.LinAlgError(err1)

    if a.size == 0:
        raise np.linalg.LinAlgError(err2)

    n, m = a.shape
    if n != m:
        raise np.linalg.LinAlgError(err3)

    if n != b.shape[0]:
        raise np.linalg.LinAlgError(err4)

    if 1 <= np.abs(omega) >= 2:
        raise np.linalg.LinAlgError(err5)

    x0 = x1 = np.zeros_like(b)

    D = np.diag(np.diag(A))
    L = -np.tril(A, -1)
    U = -np.triu(A, 1)

    M = np.linalg.inv(D - omega * L)
    N = (1 - omega) * D + omega * U
    MN = np.dot(M, N)
    Mb = omega * np.dot(M,b)

    it: int = 0
    while it < k:
        x1 = np.dot(MN, x0) + Mb
        norme2 = np.linalg.norm((x1 - x0) / x1)
        if np.less(norme2, np.finfo(np.float32).eps):
            break
        x0 = x1
        it += 1

    return x1, it

# https://www.joezhouman.com/2021/11/21/NumericalAnalysisIteration.html

def aor(
    A: np.ndarray,
    b: np.ndarray,
    omega: float,
    rho: float,
    k: int,
    ) -> tuple[np.ndarray, int]:

    err1: str = "A n'est pas en 2D !"
    err2: str = "A est vide !"
    err3: str = "A est rectangulaire !"
    err4: str = "Ordre de A != ordre de b !"
    err5: str = "Valeur de Omega incorrecte !"
    err6: str = "Valeur de Rho incorrecte !"

    if a.ndim != 2:
        raise np.linalg.LinAlgError(err1)

    if a.size == 0:
        raise np.linalg.LinAlgError(err2)

    n, m = a.shape
    if n != m:
        raise np.linalg.LinAlgError(err3)

    if n != b.shape[0]:
        raise np.linalg.LinAlgError(err4)

    if 1 <= np.abs(omega) >= 2:
        raise np.linalg.LinAlgError(err5)
    
    if rho >= omega or rho < 0:
        raise np.linalg.LinAlgError(err6)

    x0 = x1 = np.zeros_like(b)

    D = np.diag(np.diag(A))
    L = -np.tril(A, -1)
    U = -np.triu(A, 1)

    M = np.linalg.inv(D - rho * L)
    N = (1 - omega) * D + (omega - rho) * L + omega * U
    MN = np.dot(M, N)
    Mb = omega * np.dot(M, b)

    it: int = 0
    while it < k:
        x1 = np.dot(MN, x0) + Mb
        norme2 = np.linalg.norm((x1 - x0) / x1)
        if np.less(norme2, np.finfo(np.float32).eps):
            break
        x0 = x1
        it += 1

    return x1, it


def creation_systeme_tridiagonal(
        n: int
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:

    A = np.zeros((n, n))
    x = np.random.uniform(size=n)

    for i in range(n):
        if i > 0:
            val = np.random.uniform(0.1, 0.5)
            A[i, i-1] = val
            A[i-1, i] = val
        A[i, i] = np.random.uniform(2, 3.0)

    b = np.dot(A, x)

    return A, b, x

def test_gs(
        a: np.ndarray,
        b: np.ndarray,
        x2: np.ndarray,
        iter: int
    ) -> None:

    start1 = t.perf_counter()
    x1, it = gauss_seidel(a, b, iter)
    print(f"Temps GS : {t.perf_counter()-start1} s en {it} itérations")
    print("Vérification : ", end="")
    v = np.allclose(x1, x2, atol = np.finfo(np.float32).eps)
    if v:
        print("OK")
    else:
        print("KO")


def test_sor(
        a: np.ndarray,
        b: np.ndarray,
        x2: np.ndarray,
        omega: float,
        iter: int
    ) -> None:

    start1 = t.perf_counter()
    x1, it = sor(a, b, omega, iter)
    print(f"Temps SOR : {t.perf_counter()-start1} s en {it} itérations")
    print("Vérification : ", end="")
    v = np.allclose(x1, x2, atol = np.finfo(np.float32).eps)
    if v:
        print("OK")
    else:
        print("KO")


def test_aor(
        a: np.ndarray,
        b: np.ndarray,
        x2: np.ndarray,
        omega: float,
        rho: float,
        iter: int
    ) -> None:

    start1 = t.perf_counter()
    x1, it = aor(a, b, omega, rho, iter)
    print(f"Temps AOR : {t.perf_counter()-start1} s en {it} itérations")
    print("Vérification : ", end="")
    v = np.allclose(x1, x2, atol = np.finfo(np.float32).eps)
    if v:
        print("OK")
    else:
        print("KO")


if __name__ == "__main__":
    n = 1000
    itermax = n
    a, b, x = creation_systeme_tridiagonal(n)
    print("\n--------------------------------------")
    test_gs(a, b, x, itermax)
    print("--------------------------------------")
    lomega = np.arange(1.5,1.95,0.025)
    for omega in lomega:
        test_sor(a, b, x, omega, itermax)
    print("--------------------------------------")
    lomega = np.arange(1,1.95,0.025)
    lrho = np.arange(0.1,0.95,0.025)
    for omega in lomega:
        for rho in lrho:
            print(f"{omega=}, {rho=}")
            test_aor(a, b, x, omega, rho, itermax)
    print("--------------------------------------\n")
