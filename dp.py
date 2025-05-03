import numpy as np
import time as t

def dormand_prince(
          f:callable,
          y0:np.float64,
          h0:np.float64,
          a:np.float64,
          b:np.float64,
          tol = np.finfo(np.float64).eps
    ) -> np.float64:

    dopri5 = np.array([
        [0, 0, 0, 0, 0, 0, 0],
        [1/5, 0, 0, 0, 0, 0, 0],
        [3/40, 9/40, 0, 0, 0, 0, 0],
        [44/45, -56/15, 32/9, 0, 0, 0, 0],
        [19372/6561, -25360/2187, 64448/6561, -212/729, 0, 0, 0],
        [9017/3168, -355/33, 46732/5247, 49/176, -5103/18656, 0, 0],
        [35/384, 0, 500/1113, 125/192, -2187/6784, 11/84, 0] # dopri5[-1,:] et "bhat"
    ])
    
    bi = np.array([5179/57600, 0, 7571/16695, 393/640, -92097/339200, \
                   187/2100, 1/40])
    ci = np.array([0, 1/5, 3/10, 4/5, 8/9, 1, 1])
    
    y = t = np.zeros(1)
    t[0] = a
    y[0] = y0
    h = h0
    n = dopri5.shape[0]
    k = np.zeros(n)
    safetyfactor: np.float64 = np.exp(-0.1)
    p = 4.

    while t[-1] < b:
        for i in range(n):
            yi = y[-1] + h * np.sum(dopri5[i,:i] @ k[:i])
            ti = t[-1] + ci[i] * h
            k[i] = f(ti, yi)

        yk = y[-1]
        yn = yk + h * np.sum(dopri5[-1] @ k)
        yhat = yk + h * np.sum(bi @ k)
        delta = np.fabs(yn - yhat)
        
        e = safetyfactor * np.emath.power(tol / delta, np.reciprocal(p + 1))

        h *= np.clip(e, 0.5, 2.)

        if np.less(delta, tol):
            t = np.append(t, t[-1] + h)
            y = np.append(y, yn)

    return yn


def f(t, y):
    return -4 * y + np.exp(-t) * np.cos(t) + 1


if __name__ == "__main__":
    t0 = 0.0
    t1 = 20.0
    y0 = 0.1
    h0 = 0.05
    debut = t.perf_counter()
    res = dormand_prince(f, y0, h0, t0, t1)
    fin = t.perf_counter()
    np.set_printoptions(precision=np.finfo(np.float32).precision, suppress = True)
    temps = np.format_float_positional(np.float16(fin - debut))
    print(f"y = {res} en {temps} s")
	# np.test(label="full", verbose=2)

# y'(t) = -4 * y + exp(-t) * cos(t) + 1
# https://www.emathhelp.net/calculators/differential-equations/fourth-order-runge-kutta-method-calculator/?f=-4+*+y+%2B+exp%28-t%29+*+cos%28t2%29+%2B+1&type=h&h=0.05&t0=0&y0=0.1&t1=10
