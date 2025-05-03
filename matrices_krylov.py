import numpy as np
import time as t

def cgs(
    a: np.ndarray,
    b: np.ndarray,
    k: int,
    tol:np.float64 = np.finfo(np.float64).eps
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

    nb = np.linalg.norm(b)
    x = np.zeros(n)
    r = b - a@x
    r0 = rn = r.copy()
    p = q = u = r.copy()
    alpha = beta = rho = 0
    
    for _ in range(k):
        rho = np.dot(r0,r)
        ap = a @ p
        alpha = rho / np.dot(ap,r)
        q = u - alpha * ap
        upq = u + q
        x += alpha * upq
        auq = a @ upq
        rn -= alpha * auq
        beta = np.dot(rn,r) / rho
        u = rn + beta * q
        p = u + beta * (q + beta * p)
        err = np.linalg.norm(rn)
        if np.isclose(err, 0.0, atol=tol * nb) == True:
            break
        else:
            r0 = rn

    return x


def tfqmr(
    A: np.ndarray,
    b: np.ndarray,
    k: int,
    tol = np.finfo(np.float32).eps
) -> np.ndarray:

    if A.ndim != 2:
        raise np.linalg.LinAlgError("a n'est pas en 2D !")
    if A.size == 0:
        raise np.linalg.LinAlgError("a est vide !")
    if A.shape[0] != A.shape[1]:
        raise np.linalg.LinAlgError("a est rectangulaire !")
    if A.shape[0] != b.shape[0]:
        raise np.linalg.LinAlgError("Ordre de a != ordre de b.")

    x = np.zeros_like(b)
    r = b - A @ x
    w = r.copy()
    y0 = y1 = r.copy()
    d = np.zeros_like(b)

    v = A @ y0
    u0 = u0 = v.copy()

    theta = eta = 0.0
    tau = np.linalg.norm(r)
    rho0 = rho1 = tau**2

    it = 0
    while it < k:
        it += 1
        sigma = (np.dot(r, v))
        if np.isclose(sigma, 0):
            raise ValueError("Breakdown: sigma ≈ 0")

        alpha = rho0 / sigma

        for j in range(2):
            if j == 1:
                y1 = y0 - alpha * v
                u1 = A @ y1

            yj = y0 if j == 0 else y1
            uj = u0 if j == 0 else u1
            w -= alpha * uj
            d = yj + ((theta**2 * eta) / alpha) * d if it > 1 or j > 0 else yj
            theta = np.linalg.norm(w) / tau
            c = 1.0 / np.sqrt(1.0 + theta**2)
            tau *= theta * c
            eta = c**2 * alpha
            x += eta * d

            if tau * np.sqrt(2 * it - 1 + j) <= tol:
                return x

        if np.isclose(rho0, 0):
            raise ValueError("Breakdown: rho0 ≈ 0")

        rho1 = np.dot(r, w)
        beta = rho1 / rho0
        y0 = w + beta * y1
        u0 = A @ y0
        v = u0 + beta * (u1 + beta * v)
        rho0 = rho1

    return x


def bicr(
    a: np.ndarray,
    b: np.ndarray,
    k: int,
    tol:np.float64 = np.finfo(np.float64).eps
    ) -> np.ndarray:

    err1:str = "a n'est pas en 2D !"
    err2:str = "a est vide !"
    err3:str = "a est rectangulaire !"
    err4:str = "Ordre de a != ordre de b."

    if a.ndim != 2:
        raise np.linalg.LinalgError(err1)

    if a.size == 0:
        raise np.linalg.LinalgError(err2)

    n, m = a.shape
    if n != m:
        raise np.linalg.LinalgError(err3)

    if n != b.shape[0]:
        raise np.linalg.LinalgError(err4)

    x0 = x1 = np.ones(n)
    r0 = r0Star = b - a@x0
    r1 = r1Star = r0.copy()
    p0 = p0Star = np.zeros(n)
    p1 = p1Star = np.zeros(n)
    alpha = beta = 0
    bNormTol = tol * np.linalg.norm(b)
    
    for _ in range(k):
        p1 = r1 + beta * p0
        p1Star = r1Star + beta * p0Star
        ar1 = np.dot(a, r1)
        ap = ar1 + beta * (a @ p0)
        atps = a.T @ p1Star
        alpha_num = np.dot(r1Star, ar1)
        alpha_den = atps @ ap
        alpha = alpha_num / alpha_den
        x1 = x0 + alpha * p1
        r1 = r0 - alpha * ap
        r1Star = r0Star - alpha * atps
        beta_num = np.inner(r1Star, np.dot(a, r1))
        beta_den = np.inner(r0Star, np.dot(a, r0))
        beta = beta_num / beta_den
        if np.linalg.norm(r1) <= bNormTol:
            break
        else:
            x0 = x1
            r0 = r1
            r0Star = r1Star
            p0 = p1
            p0Star = p1Star

    return x1


# def gpbicg(
#     a: np.ndarray,
#     b: np.ndarray,
#     k: int,
#     tol: float = np.finfo(np.float64).eps
#     ) -> np.ndarray:

#     err1:str = "a n'est pas en 2D !"
#     err2:str = "a est vide !"
#     err3:str = "a est rectangulaire !"
#     err4:str = "Ordre de a != ordre de b."

#     if a.ndim != 2:
#         raise np.linalg.LinalgError(err1)

#     if a.size == 0:
#         raise np.linalg.LinalgError(err2)

#     n, m = a.shape
#     if n != m:
#         raise np.linalg.LinalgError(err3)

#     if n != b.shape[0]:
#         raise np.linalg.LinalgError(err4)

#     xn = np.zeros_like(b)
#     r0Star = ro = b - a @ xn
#     rn = np.zeros_like(b)
#     pn = to = tn = un = wn = yn = zn = np.copy(ro)
#     alpha = beta = eta = zeta = 0.0

#     for i in range(k):
#         pn = ro + beta * (pn - un)
#         apn = a @ pn
#         r0Star_rn = np.dot(r0Star, rn)
#         alpha = r0Star_rn / np.dot(r0Star,apn)
#         yn = to - rn - alpha * wn + alpha * apn
#         tn = ro - alpha * apn
#         atn = a @ tn
#         if i == 0:
#             zeta = np.dot(atn,tn) / np.dot(atn,atn)
#             eta = 0
#         else:
#             atn_atn = np.dot(atn,atn)
#             atn_tn = np.dot(atn,tn)
#             atn_yn = np.dot(atn,yn)
#             yn_atn = np.dot(yn,atn)
#             yn_tn = np.dot(yn,tn)
#             yn_yn = np.dot(yn,yn)
#             d1 = atn_atn * yn_yn
#             d2 = yn_atn**2
#             denom = d1 - d2
#             if np.fabs(denom) < tol:
#                 np.linalg.LinAlgError("Division par zéro !")
#             z1 = yn_yn * atn_tn
#             z2 = yn_tn * atn_yn
#             zeta = z1 - z2
#             zeta /= denom
#             e1 = atn_atn * yn_tn
#             e2 = yn_atn * atn_tn
#             eta = e1 - e2
#             eta /= denom
#         un = zeta * apn + eta * (to - ro + beta * un)
#         zn = zeta * ro + eta * zn - alpha * un
#         xn += alpha * pn + zn
#         rn = tn - eta * yn - zeta * atn
#         b1 = (alpha / zeta)
#         b2 = (np.dot(r0Star, rn) / r0Star_rn)
#         beta = b1 * b2
#         wn = atn + beta * apn
#         norme1 = np.linalg.norm(a @ xn)
#         norme2 = tol * np.linalg.norm(b)
#         if norme1 <= norme2:
#             break
#         ro = rn
#         to = tn

#     return xn


def qmrcgstab2(
    a: np.ndarray,
    b: np.ndarray,
    k: int,
    tol:np.float64 = np.finfo(np.float64).eps
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

    x = xn = np.ones(n)
    r0 = b - a @ x
    r = s = np.copy(r0)
    dn = pn = nu = np.zeros(n)
    alpha = beta = omega = 1
    rho1 = rho2 = 1
    eta = etaTilde = 0
    tau = tauTilde = np.fabs(np.linalg.norm(r0))
    theta = thetaTilde = np.linalg.norm(r) / tauTilde

    for _ in range(k):
        rho2 = np.dot(r0,r)
        beta = (rho2 * alpha) / (rho1 * omega)
        pn = r + beta * (pn - omega * nu)
        nu = a @ pn
        rho1 = np.dot(r0,nu)
        alpha = rho2 / rho1
        s = r - alpha * nu
        thetaTilde = np.linalg.norm(s) / tau
        c = np.reciprocal(np.sqrt(1 + thetaTilde**2))
        tauTilde = tau * thetaTilde * c
        etaTilde = c**2 * alpha
        dn = pn + ((theta**2 * eta) / alpha) * dn
        xn = x + etaTilde * dn
        t = a @ s
        omega = np.dot(s,s) / np.dot(s,t)
        r = s - omega * t
        theta = np.linalg.norm(r) / tauTilde
        c = np.reciprocal(np.sqrt(1 + theta**2))
        tau = tauTilde * theta * c
        eta = c**2 * omega
        dn = s + ((thetaTilde**2 * etaTilde) / omega) * dn
        x = xn + eta * dn
        err = np.linalg.norm(b - a @ x) * np.fabs(tau)

        if np.isclose(err, 0.0, atol=tol) == True:
           break
        else:
            rho1 = rho2
            
    return x


def bicgstabl(
        L: int,
        A: np.ndarray,
        b: np.ndarray,
        itmax: int
    ) -> np.ndarray:

    n = b.shape[0]
    x = np.zeros_like(b)
    rHat = np.zeros((L+1, n))
    uHat = np.zeros((L+1, n))
    gamma = np.zeros(L+1)
    gammaa = np.zeros(L+1)
    gammaaa = np.zeros(L+1)
    tau = np.zeros((L, L))
    sigma = np.zeros(L + 1)

    rHat[0] = b - np.dot(A, x)
    rTilde = np.random.uniform(size=n)

    rho0 = rho1 = 1
    alpha = 0
    omega = 1

    it = 0
    tolConv = np.finfo(np.float64).eps
    tolBrkdwn = tolConv
    bNrm = np.linalg.norm(b)
    while np.linalg.norm(rHat[0]) > tolConv * bNrm and it < itmax:
        rho0 *= -omega
        for j in range(L):
            rho1 = np.dot(rHat[j], rTilde)
            if np.fabs(rho0) < tolBrkdwn:
                raise np.linalg.LinAlgError("Breakdown !")
            beta = alpha * rho1 / rho0
            for i in range(j + 1):
                uHat[i] = rHat[i] - beta * uHat[i]
            uHat[j + 1] = np.dot(A, uHat[j])
            alpha = rho0 / np.dot(uHat[j+1], rTilde)
            for i in range(j + 1):
                rHat[i] -= alpha * uHat[i + 1]
            rHat[j + 1] = np.dot(A, rHat[j])
            x += alpha * uHat[0]

        for j in range(1, L+1):
            for i in range(1, j):
                tau[j-1, i-1] = np.dot(rHat[j], rHat[i]) / sigma[i]
                rHat[j] -= tau[j-1, i-1] * rHat[i]
            sigma[j] = np.dot(rHat[j], rHat[j])
            gammaa[j] = np.dot(rHat[0], rHat[j]) / sigma[j]

        omega = gamma[L] = gammaa[L]
        for j in range(L - 1, 0, -1):
            gamma[j] = gammaa[j]
            for i in range(j+1, L+1):
                gamma[j] -= tau[i-1, j-1] * gamma[i]

        for j in range(1, L):
            gammaaa[j] = gamma[j+1]
            for i in range(j+1, L):
                gammaaa[j] += tau[i-1, j-1] * gamma[i + 1]

        x += gamma[1] * rHat[0]
        rHat[0] -= gammaa[L] * rHat[L]
        uHat[0] -= gamma[L] * uHat[L]
        for j in range(1, L):
            x += gammaaa[j] * rHat[j]
            rHat[0] -= gammaa[j] * rHat[j]
            uHat[0] -= gamma[j] * uHat[j]

        rho0 = rho1
        it += 1
    else:
        return x


def systeme_lineaire_non_symetrique(
	    n: int
	) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
	
    A = np.random.uniform(-0.0999, -0.999, size=(n,n))
    x = np.random.uniform(size=n)

    for i in range(n):
        A[i,i] = np.random.uniform(1, 2.0) - np.sum(A[i,:])*2

    b = np.dot(A, x)
    
    return A, b, x


if __name__ == "__main__":
    ordre = 8000
    itermax = ordre
    tol = np.finfo(np.float64).eps
    dec = np.finfo(np.float32).precision
    a, b, x = systeme_lineaire_non_symetrique(ordre)

    solvers = (
        (cgs, "CGS"),
        (tfqmr, "TFQMR"),
        (bicr, "BICR"),
        (qmrcgstab2, "QMRCGSTAB2"),
        (bicgstabl, "BICGSTAB(L)")
    )

    for solver, name in solvers:
        debut = t.perf_counter()
        if solver != bicgstabl:
            xx = solver(a, b, itermax)
        else:
            xx = solver(4, a, b, itermax)
        fin = t.perf_counter()
        print(f"{name} -> {np.round(fin - debut, decimals=dec)} secondes.", end="")
        print(" Vérification... ", end="")
        ret = np.allclose(xx, x, tol)
        if ret:
            print("OK")
        else:
            print("KO")

    debut = t.perf_counter()
    xx = np.linalg.solve(a, b)
    fin = t.perf_counter()
    print(f"NUMPY -> {np.round(fin - debut, decimals=dec)} secondes.")
