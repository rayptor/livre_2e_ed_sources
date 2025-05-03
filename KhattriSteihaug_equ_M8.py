import numpy as np

def KhattriSteihaug_equ_M8(
    f: callable,
    x0: np.float128,
    k:int = 10,
    tol = np.finfo(np.float128).eps
    ) -> np.float128:

	dec = np.finfo(np.float128).precision
	xo = x0
	xn = xo
	alpha = 1

	for _ in range(k):
		fxn = f(xn)
		yn = np.float128(xo - alpha * (fxn**2 / ((f(xn + alpha * fxn)) - fxn)))
		fyn = f(yn)
		zn1_1 = xn - yn + alpha * fxn
		zn1_2 = (xn - yn) * alpha
		zn1 = zn1_1 / zn1_2
		zn2_1 = xn - yn * f(xn + alpha * fxn)
		zn2_2 = (xn - yn + alpha * fxn) * alpha * fxn
		zn2 = zn2_1 / zn2_2
		zn3_1 = (2 * xn - 2 * yn + alpha * fxn) * fyn
		zn3_2 = (xn - yn) * (xn - yn + alpha * fxn)
		zn3 = zn3_1 / zn3_2
		zn = yn - fyn / (zn1 - zn2 - zn3)
		fzn = f(zn)
		h1_1 = (yn - zn) * (xn + alpha * fxn - zn)
		h1_2 = (xn - zn) * alpha * (xn - yn)
		h1 = (-1) * np.divide(h1_1, h1_2)
		h2_1 = (yn - zn) * (xn - zn) * f(xn + alpha * fxn)
		h2_2 = (xn + alpha * fxn - zn) \
			* (xn + alpha * fxn - yn) * alpha * fxn
		h2 = np.divide(h2_1, h2_2)
		h3_1 = (xn - zn) * (xn + alpha * fxn - zn) * fyn
		h3_2 = (yn - zn) * (xn - yn + alpha * fxn) * (xn - yn)
		h3 = np.divide(h3_1, h3_2)
		h4_1 = (xn * alpha - 2 * alpha * zn + alpha * yn) \
			* fxn + xn**2 + (-4 * zn + 2 * yn) * xn \
				+ 3 * zn**2 - 2 * yn * zn
		h4_2 = (yn - zn) * (xn - zn) * (xn - zn + alpha * fxn)
		h4 = np.divide(h4_1, h4_2) * fzn
		hn = h1 + h2 + h3 + h4
		xn = zn - fzn / hn

		if np.less(np.fabs(xn - xo), tol):
			break
		else:
			xo = xn

	return np.format_float_positional(np.float128(xn), unique=False, precision=dec)

	# x ≈ 0.275524497745287060301782478...
if __name__ == "__main__":
	f = lambda x: 13*x**9 - np.exp(x-1) + np.arctan(4*x)+ x - np.arccos(x) + 2/3
	print("x =", KhattriSteihaug_equ_M8(f, 0.2))
