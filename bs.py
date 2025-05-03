import numpy as np

class BlackScholesFD:
    def __init__(self, T, S, K, sigma, r):
        self.T = T            # échéance
        self.S = S    # valeur initiale
        self.K = K            # strike
        self.sigma = sigma    # volatilité
        self.r = r            # taux d'intérêt

    def solve(self, sigma, pas, trajectoire):
        dt = self.T / trajectoire
        dS = self.S / pas

        i = np.arange(1, pas)
        S = i * dS

        sigma2_i2 = (sigma * i)**2
        a = 0.5 * dt * (sigma2_i2 - self.r * i)
        b = 1 - dt * (sigma2_i2 + self.r)
        c = 0.5 * dt * (sigma2_i2 + self.r * i)

        u = np.zeros((trajectoire+1, pas-1))

        u[0] = np.maximum(S - self.K, 0)

        for n in range(trajectoire):
            u[n+1, :] = (
                a * np.hstack(([0], u[n, :-1])) +
                b * u[n] +
                c * np.hstack((u[n, 1:], [0]))
            )
            t = n * dt
            p = 1/2 * dt * (pas-1) * (sigma**2 * (pas-1) + self.r) * (
                self.S - self.K * np.exp(-self.r * t)
            )
            u[n+1, -1] += p

        return u

if __name__ == "__main__":
    K, r = 5.0, 0.05
    sigma = 0.50
    T = 1.0
    pas = 11+1
    trajectoire = 29
    S = 10.0

    solver = BlackScholesFD(T, S, K, sigma, r)
    grid = solver.solve(sigma, pas, trajectoire)

    dS = S / pas
    S = np.arange(1, pas) * dS

    for Si, Ui in zip(S, grid[-1]):
        print(f"S = {Si:.2f}, option ≈ {Ui:.4f}")
