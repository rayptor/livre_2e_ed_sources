import numpy as np
import matplotlib.pyplot as plt

def vdc(base: np.uint, n: np.uint) -> np.ndarray:
    sequence = np.empty(n)

    for i in range(n):
        i = np.arange(n, dtype=np.uint)
        denom = np.ones(n)
        v = 0
        while np.any(i > 0):
            reste = np.fabs(np.mod(i, base))
            i = np.floor_divide(i, base)
            denom *= 1. / base
            v += reste * denom

        sequence[i] = v

    return sequence

def halton(taille: np.uint) -> np.ndarray:
    bases = np.array([2, 3])
    l = bases.shape[0]
    sequence = np.empty((taille, l))

    for dim in range(l):
        b = bases[dim]
        i = np.arange(taille, dtype=np.uint)
        vecteur = np.zeros(taille)
        denom = np.ones(taille)

        while np.any(i > 0):
            reste = np.fabs(np.mod(i, b))
            i = np.floor_divide(i, b)
            denom *= 1. / b
            vecteur += reste * denom

        sequence[:, dim] = vecteur

    return sequence

taille = 10000
suiteHalton = halton(taille)
# suiteVDC = vdc(3, taille)
print(suiteHalton)
# print(suiteVDC)

seed = np.random.SeedSequence()
rng = np.random.default_rng(seed)
suiteNumpy = rng.random((taille, taille))
pas = 0.05
fig, ax = plt.subplots(2, 1, figsize=(8,16))

ax[0].scatter(suiteHalton[:, 0], suiteHalton[:, 1], s=1, color="k", alpha=1)
ax[0].set_title(f"Nombres QUASI-aléatoires en bases (2,3) avec la méthode de Halton")
ax[0].set_xlabel("Base 2")
ax[0].set_ylabel("Base 3")
ax[0].set_xlim(0, 1)
ax[0].set_ylim(0, 1)
ax[0].set_xticks(np.arange(0, 1+pas, pas))
ax[0].set_yticks(np.arange(0, 1+pas, pas))
ax[0].grid(True, ls="-", lw=1, alpha=1)

ax[1].scatter(suiteNumpy[:, 0], suiteNumpy[:, 1], s=1, color="k", alpha=1)
ax[1].set_title(f"Nombres PSEUDO-aléatoires avec la fonction random({rng})")
ax[1].set_xlabel("Numpy X")
ax[1].set_ylabel("Numpy Y")
ax[1].set_xlim(0, 1)
ax[1].set_ylim(0, 1)
ax[1].set_xticks(np.arange(0, 1+pas, pas))
ax[1].set_yticks(np.arange(0, 1+pas, pas))
ax[1].grid(True, ls="-", lw=1, alpha=1)

plt.tight_layout()
plt.show()
fig.savefig("halton.png")
