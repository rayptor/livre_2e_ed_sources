import numpy as np
    
# Computing Simple Roots by an Optimal Sixteenth-Order Class
def SalimiNikLongSharifiPansera(
    f: callable,
    df: callable,
    x0: np.float128,
    k: int = 10,
    tol = np.finfo(np.float128).eps
    ) -> np.float128:

    dec = np.finfo(np.float128).precision
    xo = x0
    xn = xo

    beta = 1

    for _ in range(k):
        fxn = f(xn)
        if np.isclose(fxn, 0.0, atol=tol) == True:
            break
        dfxn = df(xn)
        yn = xo - fxn/dfxn
        fyn = f(yn)
        zn1 = yn - (2.0*fyn) / dfxn
        zn2 = fyn * (fxn+(beta-2.0) * fyn) / (dfxn * (fxn + beta*fyn))
        zn3 = ((dfxn*fyn) / (fxn * (fxn+beta * fyn))) * (fyn / dfxn)**2
        zn = zn1 + zn2 - zn3
        fzn = f(zn)
        tn = fyn/fxn
        un = fzn/fxn
        eta = (1.0+tn-4.0*beta*tn**3) / (1.0+tn+8.0*tn**3)
        varphi = 3.0 - 2.0/(1.0+un)
        fzy = (fyn-fzn) / (yn-zn)
        fzx = (fxn-fzn) / (xn-zn)
        fzxx = (fzx-dfxn) / (zn-xn)
        xn = zn - (fzn*eta*varphi) / (fzy + (zn-yn)*fzxx)

        if np.less(np.fabs(xn - xo), tol) == True:
            break
        else:
            xo = xn

    return np.format_float_positional(np.float128(xn), unique=False, precision=dec)

if __name__ == "__main__":
    f = lambda x: (x-2)**5 - np.log(x + 4.0) - np.sin((x*np.pi) / 4.0) + 100.0*x + 10.0
    df = lambda x: 5.0*(x-2.0)**4 - 1.0 / (x+4.0) - (1.0/4.0) * np.pi * np.cos((np.pi*x) / 4.0) + 100.0
    print("x =", SalimiNikLongSharifiPansera(f, df, 0.11))
