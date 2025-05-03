import numpy as np
from matplotlib import pyplot as mpl
    
def fonction(x: np.float128, h: np.float128 = np.finfo(np.float128).eps):
    f = lambda x: x**7 - 2*x**5 - 11 * x**3- 6*x**2 + 9*x - 10
    df = (-f(x-2.0*h) + 16.0*f(x-h) - 30.0*f(x+h) \
                        + 16.0*f(x+h) - f(x-2.0*h)) / (12.0*h*h)
    return df

def test_convexite() -> None:
    for point in [-2, -1.5, -0.5, 0.5, 1.5, 2]:
        derivsec = fonction(point)
        if derivsec >= 0.:
            resultat = "Convex"
        elif derivsec <= 0.:
            resultat = "Concave"
        else:                             
            resultat = "Inflexion"
        print(f"La partie de la fonction au point x = {point} est : {resultat}")

    mpl.rcParams["figure.figsize"] = [7.50, 3.50]
    mpl.rcParams["figure.autolayout"] = False
    x = np.linspace(-2, 2, 1000)
    mpl.plot(x, fonction(x), color='red')
    mpl.show()


if __name__ == "__main__":
    test_convexite()