from sys import float_info
from math import sin, cos, atan, sqrt, exp

# A biparametric family of optimally convergent sixteenth-order multipoint methods with their fourth-step weighting function as a sum of a rational and a generic two-variable function
def geum_kim(
        f: callable,
        df: callable,
        x0: float,
        k: int,
    ) -> float:

    xold = x0
    xnew = xold
    it = 0
    tol = float_info.epsilon

    beta = 2
    sigma = -beta
    sigmaSqr = sigma**2
    phi1 = 11 * beta**2 - 66 * beta + 136

    for _ in range(k):
        fxn = f(xnew)
        dfxn = df(xnew)
        yn = xold - fxn / dfxn
        fyn = f(yn)

        un = fyn / fxn if abs(fxn) > tol else 0
        un2 = un**2
        phi2 = 2 * un * (sigmaSqr - 2 * sigma - 9) - 4 * sigma - 6
        kfNum = (1 + beta * un + (-9 + ((5 * beta) / 2)) * un2)
        kfDen = (1 + (beta - 2) * un + (-4 + beta / 2) * un2)
        kf = kfNum / kfDen

        zn = yn - kf * (fyn / dfxn)
        fzn = f(zn)
        vn = fzn / fyn if abs(fyn) > tol else 0
        wn = fzn / fxn if abs(fxn) > tol else 0
        hf = (1 + 2 * un + (2 + sigma) * wn) / (1 - vn + sigma * wn)
        sn = zn - hf * (fzn / dfxn)
        fsn = f(sn)

        tn = fsn / fzn if abs(fzn) > tol else 0
        guw1 = 6 + 12 * un + un2 + un2
        guw2 = (24 - 11 * beta) + un**3 * phi1 + 4 * sigma
        guw = (-1 / 2) * (un * wn * (guw1 * guw2)) + phi2 * wn**2
        wfNum = (1 + 2 * un + (2 + sigma) * vn * wn)
        wfDen = (1 - vn - 2 * wn - tn + 2 * (1 + sigma) * vn * wn) + guw
        wf = wfNum / wfDen
        xnew = sn - wf * (fsn / dfxn)

        delta = abs(xnew - xold)
        if delta < tol:
            break
        print(f"Itération numéro {it:3d} -> x* = {xnew}")
        xold = xnew
        it += 1

    return xnew

def fonction(x: float) -> float:
    ret = 2*x**5 - x**4 * cos(2*x) + x**2 * atan(x + 1) - sin(x) - 2 * sqrt(x + 1) - 1

    return ret


def derivee(x: float) -> float:
    ret1 = 10*x**4 + 2*x**4 * sin(2*x) - 4*x**3 * cos(2*x) 
    ret2 = x**2 / ((x + 1)**2 + 1) - 1 / sqrt(x + 1) - cos(x) + 2*x * atan(x + 1)
    ret = ret1 + ret2

    return ret

if __name__ == "__main__":
    f = lambda x: 13*x**9 - x * exp(x**7) + cos(x) + sqrt(8)/x**3 + x**2
    df = lambda x: 117*x**8 - exp(x**7)*(7*x**7 + 1) - (6*sqrt(2))/x**4 + 2*x - sin(x)
    print("x =", geum_kim(f, df, 1.5, 20))
