import numpy as np

def SharmaBahl(
		f: callable,
		df: callable,
		x0: np.float128,
		k:int,
		tol = np.finfo(np.float128).eps
    ) -> np.float128:

    dec = np.finfo(np.float128).precision
    xo = x0
    xn = xo

    for _ in range(k):
        fxn = f(xn)
        if np.isclose(fxn, 0.0, atol=tol) == True:
            break
        dfxn = df(xn)
        wn = xo - fxn / dfxn
        fwn = f(wn)
        zn = wn - fxn / (fxn - 2 * fwn) * (fwn / dfxn)
        fzn = f(zn)
        fwz = np.float128((fzn - fwn) / (zn - wn))
        fxw = np.float128((fwn - fxn) / (wn - xn))
        fxz = np.float128((fzn - fxn) / (zn - xn))
        xn1 = fxn**3 / (fxn**3 + fwn**3) + fzn/fxn + fzn**2 / fxn**2
        xn2 = fzn / (fxz + fwz - fxw)
        xn = zn - xn1 * xn2
        if np.less(np.fabs(xn - xo), tol) == True:
            break
        xo = xn

    return np.format_float_positional(xn, unique=False, precision=dec)

if __name__ == "__main__":
    f = lambda x: x**9 - np.pi * x**3 - np.arctan(x) + 2 * x * np.log(x + 3) - 2
    df = lambda x: 9 * x**8 - 3 * np.pi * x**2 - (1 / (x**2 + 1)) + ((2 * x) / (x + 3)) + 2 * np.log(x + 3)
    print(f"x = {SharmaBahl(f, df, 1.3, 20)}")
